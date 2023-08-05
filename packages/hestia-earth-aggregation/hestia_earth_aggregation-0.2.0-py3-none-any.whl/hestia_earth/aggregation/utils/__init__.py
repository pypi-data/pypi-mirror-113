import math
from functools import reduce
from datetime import datetime
from hestia_earth.utils.tools import safe_parse_date

from ..log import logger
from ..version import VERSION
from .term import _group_by_term_id


def _aggregated_version(node: dict, *keys):
    node['aggregated'] = node.get('aggregated', [])
    node['aggregatedVersion'] = node.get('aggregatedVersion', [])
    all_keys = ['value'] if len(keys) == 0 else keys
    for key in all_keys:
        if key in node['aggregated']:
            node.get('aggregatedVersion')[node['aggregated'].index(key)] = VERSION
        else:
            node['aggregated'].append(key)
            node['aggregatedVersion'].append(VERSION)
    return node


def get_time_ranges(earliest_year: str, period_length: int = 10):
    """
    Get time ranges starting from the earliest Impact to today.

    Parameters
    ----------
    earliest_year : str
        The start date of the time range.
    period_length : int
        Optional - length of the period, 10 by default.
        Example: with 10 year period and the earliest impact in 2006 returns [[2001, 2010], [2011, 2020], [2021, 2030]]

    Returns
    -------
    list
        A list of time periods.
        Example: `[(1990, 1999), (2000, 2009)]`
    """
    current_year = datetime.now().year
    earliest_year = int(earliest_year[0:4])
    min_year = round(math.floor(earliest_year / 10) * 10)
    max_year = round((math.floor(current_year / 10) + 1) * 10)
    logger.debug('Time range between %s and %s', min_year, max_year)
    return [(i, i+period_length-1) for i in range(min_year, max_year, period_length)]


def _end_date_year(node: dict):
    date = safe_parse_date(node.get('endDate'))
    return date.year if date else None


def _group_by_product(nodes: list, props: list, include_matrix=True) -> dict:
    def group_by(group: dict, node: dict):
        end_date = _end_date_year(node)
        organic = node.get('organic', False)
        irrigated = node.get('irrigated', False)
        key = '-'.join([
            str(organic),
            str(irrigated),
            node.get('product').get('@id')
        ]) if include_matrix else node.get('product').get('@id')
        if key not in group:
            group[key] = {
                'product': node.get('product'),
                'nodes': [],
                'sites': [],
                **reduce(lambda prev, curr: {**prev, curr: {}}, props, {})
            }
        group[key]['nodes'].append(node)
        group[key]['sites'].append(node.get('site'))

        def group_by_prop(prop: str):
            # save ref to organic/irrigated for later grouping
            values = list(map(
                lambda v: {
                    **v,
                    'organic': organic,
                    'irrigated': irrigated,
                    'country': node.get('country'),
                    'year': end_date
                }, node.get(prop, [])))
            return reduce(_group_by_term_id, values, group[key][prop])

        group[key] = reduce(lambda prev, curr: {**prev, curr: group_by_prop(curr)}, props, group[key])
        return group

    return reduce(group_by, nodes, {})
