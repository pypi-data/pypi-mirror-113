from hestia_earth.schema import InputJSONLD, InputStatsDefinition
from hestia_earth.utils.model import linked_node

from hestia_earth.aggregation.utils import _aggregated_version


def _new_input(term: dict):
    input = InputJSONLD().to_dict()
    input['term'] = linked_node(term)
    input['statsDefinition'] = InputStatsDefinition.CYCLES.value
    return _aggregated_version(input, 'term', 'statsDefinition')
