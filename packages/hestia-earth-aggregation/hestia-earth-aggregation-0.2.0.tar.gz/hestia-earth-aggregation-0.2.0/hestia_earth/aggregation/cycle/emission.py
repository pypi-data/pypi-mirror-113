from hestia_earth.schema import EmissionJSONLD, EmissionStatsDefinition
from hestia_earth.utils.model import linked_node

from hestia_earth.aggregation.utils import _aggregated_version


def _new_emission(term: dict):
    emission = EmissionJSONLD().to_dict()
    emission['term'] = linked_node(term)
    emission['statsDefinition'] = EmissionStatsDefinition.CYCLES.value
    return _aggregated_version(emission, 'term', 'statsDefinition')
