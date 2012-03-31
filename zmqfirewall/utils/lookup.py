__all__ = ['get_action', 'get_filter', 'get_interface']

def get_action(name):
    from zmqfirewall.actions.base import ActionMeta
    return ActionMeta.get_action_by_name(name)

def get_filter(name):
    from zmqfirewall.filters.base import FilterMeta
    return FilterMeta.get_filter_by_name(name)

def get_interface(name):
    from zmqfirewall.core.interface import InterfaceMeta
    return InterfaceMeta.get_interface_by_name(name)
