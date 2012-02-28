from moksha.firewall.actions.base import ActionMeta
from moksha.firewall.filters.base import FilterMeta

__all__ = ['get_action', 'get_filter']

def get_action(name):
    return ActionMeta.get_action_by_name(name)

def get_filter(name):
    return FilterMeta.get_filter_by_name(name)
