from zmqfirewall.firewall.exceptions import DivertAction

__all__ = ['divert']

# Similar to TG2's redirect method
def divert(new_action):
    diversion = DivertAction(new_action)
    raise diversion
