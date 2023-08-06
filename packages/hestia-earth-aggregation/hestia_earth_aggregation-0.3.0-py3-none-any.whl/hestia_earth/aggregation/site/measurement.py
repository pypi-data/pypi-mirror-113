from hestia_earth.schema import MeasurementJSONLD, MeasurementStatsDefinition
from hestia_earth.utils.model import linked_node

from hestia_earth.aggregation.utils import _aggregated_version


def _new_measurement(term: dict):
    measurement = MeasurementJSONLD().to_dict()
    measurement['term'] = linked_node(term)
    measurement['statsDefinition'] = MeasurementStatsDefinition.SITES.value
    return _aggregated_version(measurement, 'term', 'statsDefinition')
