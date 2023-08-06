from hestia_earth.schema import EmissionJSONLD, EmissionMethodTier, EmissionStatsDefinition, NodeType
from hestia_earth.utils.model import linked_node

from hestia_earth.aggregation.utils import _aggregated_version

MODEL = 'aggregatedModels'


def _new_emission(term: dict):
    emission = EmissionJSONLD().to_dict()
    emission['term'] = linked_node(term)
    emission['statsDefinition'] = EmissionStatsDefinition.CYCLES.value
    emission['methodModel'] = {'@type': NodeType.TERM.value, '@id': MODEL}
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    return _aggregated_version(emission, 'term', 'statsDefinition', 'methodModel', 'methodTier')
