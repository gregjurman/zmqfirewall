from zmqfirewall.actions.bases import ActionMeta

def get_action(name):
    return ActionMeta.get_action_by_name(name)
