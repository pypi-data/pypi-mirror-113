from hestia_earth.schema import ProductJSONLD, ProductStatsDefinition
from hestia_earth.utils.model import linked_node

from hestia_earth.aggregation.utils import _aggregated_version


def _new_product(term: dict):
    product = ProductJSONLD().to_dict()
    product['term'] = linked_node(term)
    product['statsDefinition'] = ProductStatsDefinition.CYCLES.value
    return _aggregated_version(product, 'term', 'statsDefinition')
