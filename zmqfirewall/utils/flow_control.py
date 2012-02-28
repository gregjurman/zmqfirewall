__all__ = ['divert']

# Similar to TG2's redirect method
def divert(new_action):
    from zmqfirewall.exceptions import DivertAction
    diversion = DivertAction(new_action)
    raise diversion
