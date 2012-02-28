from zmqfirewall.actions.bases import ActionMeta
from zmqfirewall.rules.bases import RuleMeta

def get_action(name):
    return ActionMeta.get_action_by_name(name)

def get_rule(name):
    return RuleMeta.get_rule_by_name(name)
