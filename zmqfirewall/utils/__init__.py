from moksha.firewall.actions.base import ActionMeta
from moksha.firewall.rules.base import RuleMeta

def get_action(name):
    return ActionMeta.get_action_by_name(name)

def get_rule(name):
    return RuleMeta.get_rule_by_name(name)
