from hestia_earth.schema import PracticeJSONLD, PracticeStatsDefinition
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import linked_node


def _new_practice(term: dict):
    practice = PracticeJSONLD().to_dict()
    term = term if isinstance(term, dict) else download_hestia(term)
    practice['term'] = linked_node(term)
    practice['statsDefinition'] = PracticeStatsDefinition.CYCLES.value
    return practice
