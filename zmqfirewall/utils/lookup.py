__all__ = ['get_action', 'get_filter']

def get_action(name):
    from zmqfirewall.actions.base import ActionMeta
    return ActionMeta.get_action_by_name(name)

def get_filter(name):
    from zmqfirewall.filters.base import FilterMeta
    return FilterMeta.get_filter_by_name(name)
