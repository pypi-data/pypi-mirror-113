import json

from tests.utils import fixtures_path, start_year, end_year
from hestia_earth.aggregation.utils import _group_by_product
from hestia_earth.aggregation.models.countries import aggregate, _aggregate_weighted

class_path = 'hestia_earth.aggregation.models.countries'


def test_aggregate_cycle():
    from hestia_earth.aggregation.cycle.utils import (
        AGGREGATION_KEYS, _format_for_grouping, _update_cycle, _format_country_results
    )

    with open(f"{fixtures_path}/cycle/terms/aggregated.jsonld", encoding='utf-8') as f:
        cycles = json.load(f)
    with open(f"{fixtures_path}/cycle/countries/aggregated.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    cycles = _format_for_grouping(cycles)
    results = aggregate(AGGREGATION_KEYS, _group_by_product(cycles, AGGREGATION_KEYS, False))
    results = list(map(_format_country_results, results))
    results = list(map(_update_cycle(None, start_year, end_year, None, False), results))
    assert results == expected
    assert len(results) == 2


def test_aggregate_impact():
    from hestia_earth.aggregation.impact_assessment.utils import (
        AGGREGATION_KEY, _update_impact_assessment, _format_country_results
    )

    with open(f"{fixtures_path}/impact-assessment/terms/aggregated.jsonld", encoding='utf-8') as f:
        impacts = json.load(f)
    with open(f"{fixtures_path}/impact-assessment/countries/aggregated.jsonld", encoding='utf-8') as f:
        expected = json.load(f)
    results = aggregate(AGGREGATION_KEY, _group_by_product(impacts, [AGGREGATION_KEY], False))
    results = list(map(_format_country_results, results))
    results = list(map(_update_impact_assessment(None, start_year, end_year, None, False), results))
    assert results == expected
    assert len(results) == 6


def test_aggregate_weighted():
    country_id = 'GADM-AUS'
    year = 2000
    term = {'@id': 'term'}
    product = {'@id': 'product'}
    nodes = [{
        'organic': True,
        'irrigated': True,
        'value': 5
    }, {
        'organic': True,
        'irrigated': False,
        'value': 10
    }, {
        'organic': False,
        'irrigated': False,
        'value': 1
    }]
    result = _aggregate_weighted(country_id, year, term, nodes, product)
    assert result.get('value') == 1.0940374220686617
