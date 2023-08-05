from functools import reduce
from hestia_earth.schema import CycleStartDateDefinition, SchemaType
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import non_empty_list
from hestia_earth.utils.model import find_term_match, find_primary_product

from hestia_earth.aggregation.utils import _aggregated_version
from hestia_earth.aggregation.utils.queries import _download_node
from hestia_earth.aggregation.utils.term import _format_country_name
from hestia_earth.aggregation.site.utils import (
    _group_by_measurements, _format_results as format_site, _create_site, _update_site
)
from hestia_earth.aggregation.models.terms import aggregate as aggregate_by_term
from .input import _new_input
from .practice import _new_practice
from .product import _new_product

# TODO: add emissions
AGGREGATION_KEYS = ['inputs', 'products']


def _format_aggregate(new_func):
    def format(aggregate: dict):
        term = aggregate.get('term')
        value = aggregate.get('value')
        observations = aggregate.get('observations')
        node = new_func(term)
        node['value'] = [value]
        node['observations'] = [observations]
        return _aggregated_version(node, 'value', 'observations')
    return format


def _format_site(sites):
    groups = _group_by_measurements(sites)
    aggregates = aggregate_by_term('measurements', groups)
    return format_site(aggregates[0]) if len(aggregates) > 0 else None


def _format_terms_results(results: dict):
    inputs, data = results.get('inputs')
    products, _ = results.get('products')
    cycle = data.get('nodes', [])[0]
    # set the site if any measurements
    site = _format_site(data.get('sites', []))
    cycle['site'] = site or _create_site(cycle['site'], False)
    cycle = {
        **_create_cycle(cycle),
        'inputs': list(map(_format_aggregate(_new_input), inputs)),
        'products': list(map(_format_aggregate(_new_product), products))
    }
    # set the primary product
    primary_product = find_primary_product(cycle)
    product = find_term_match(cycle.get('products'), primary_product.get('term').get('@id'))
    product['primary'] = True
    return cycle


def _format_world_results(results: dict):
    # TODO: set practices for organic / irrigated
    return {
        **_format_terms_results(results)
    }


def _format_country_results(results: dict):
    _, data = results.get('inputs')
    cycle = data.get('nodes', [])[0]
    primary_product = find_primary_product(cycle)
    organic = _is_organic(cycle)
    irrigated = _is_irrigated(cycle)
    return {
        **_format_world_results(results),
        'name': _cycle_name(cycle, primary_product, organic, irrigated, False),
        'id': _cycle_id(cycle, primary_product, organic, irrigated, False)
    }


def _format_for_grouping(cycles: dict):
    def format(cycle: dict):
        product = find_primary_product(cycle)
        site = cycle.get('site')
        site = _download_node('recalculated')(site) if not site.get('siteType') else site
        # TODO: set organic / irrigated from practices
        return {
            **cycle,
            'site': site,
            'product': product.get('term'),
            'country': site.get('country'),
            'organic': _is_organic(cycle),
            'irrigated': _is_irrigated(cycle)
        } if product else None
    return non_empty_list([format(cycle) for cycle in cycles])


def _is_organic(cycle: dict):
    lookup = download_lookup('standardsLabels.csv', True)

    def term_organic(lookup, term_id: str):
        return get_table_value(lookup, 'termid', term_id, column_name('isOrganic')) == 'organic'

    practices = list(filter(lambda p: p.get('term') is not None, cycle.get('practices', [])))
    return any([term_organic(lookup, p.get('term', {}).get('@id')) for p in practices])


def _is_irrigated(cycle: dict):
    practices = cycle.get('practices', [])
    return next((p for p in practices if p.get('term', {}).get('@id') == 'irrigated'), None) is not None


def _cycle_id(n: dict, primary_product: dict, organic: bool, irrigated: bool, include_matrix=True):
    # TODO: handle cycles that dont have organic/irrigated version => only 1 final version
    return '-'.join(non_empty_list([
        primary_product.get('term', {}).get('@id'),
        _format_country_name(n.get('site', {}).get('country', {}).get('name')),
        ('organic' if organic else 'conventional') if include_matrix else '',
        ('irrigated' if irrigated else 'non-irrigated') if include_matrix else '',
        n.get('startDate'),
        n.get('endDate')
    ]))


def _cycle_name(n: dict, primary_product: dict, organic: bool, irrigated: bool, include_matrix=True):
    return ' - '.join(non_empty_list([
        primary_product.get('term', {}).get('name'),
        n.get('site', {}).get('country', {}).get('name'),
        ', '.join(non_empty_list([
            ('Organic' if organic else 'Conventional') if include_matrix else '',
            ('Irrigated' if irrigated else 'Non Irrigated') if include_matrix else ''
        ])),
        '-'.join([n.get('startDate'), n.get('endDate')])
    ]))


def _reset_completeness(dataCompleteness: dict):
    keys = [
        key for key in dataCompleteness.keys() if key not in [
            'updated', 'updatedVersion',
            'added', 'addedVersion'
        ]
    ]
    return {
        **reduce(lambda prev, curr: {**prev, curr: True}, keys, {}),
        '@type': SchemaType.COMPLETENESS.value
    }


def _create_cycle(data: dict):
    cycle = {'type': SchemaType.CYCLE.value}
    # copy properties from existing ImpactAssessment
    cycle['startDate'] = data.get('startDate')
    cycle['endDate'] = data.get('endDate')
    cycle['functionalUnitMeasure'] = data['functionalUnitMeasure']
    cycle['dataCompleteness'] = _reset_completeness(data['dataCompleteness'])
    cycle['startDateDefinition'] = CycleStartDateDefinition.START_OF_YEAR.value
    if _is_organic(data):
        cycle['practices'] = [_new_practice('organic')]
    if _is_irrigated(data):
        cycle['practices'] = [_new_practice('irrigated')]
    cycle['dataPrivate'] = False
    if data.get('site'):
        cycle['site'] = data['site']
    if data.get('defaultSource'):
        cycle['defaultSource'] = data['defaultSource']
    return cycle


def _update_cycle(country_name: str, start: int, end: int, source: dict = None, include_matrix=True):
    def update(cycle: dict):
        cycle['startDate'] = str(start)
        cycle['endDate'] = str(end)
        cycle['site'] = _update_site(country_name, source, False)(cycle['site'])
        primary_product = find_primary_product(cycle)
        organic = _is_organic(cycle)
        irrigated = _is_irrigated(cycle)
        cycle['name'] = _cycle_name(cycle, primary_product, organic, irrigated, include_matrix)
        cycle['site']['name'] = cycle['name']
        cycle['id'] = _cycle_id(cycle, primary_product, organic, irrigated, include_matrix)
        cycle['site']['id'] = cycle['id']
        return cycle if source is None else {**cycle, 'defaultSource': source}
    return update


def _remove_duplicated_cycles(cycles: list):
    def filter_cycle(cycle: dict):
        organic = _is_organic(cycle)
        irrigated = _is_irrigated(cycle)
        # removes non-organic + non-irrigated original cycles (they are recalculated by country average)
        return organic or irrigated or 'conventional-non-irrigated' not in cycle.get('id')

    return list(filter(filter_cycle, cycles))
