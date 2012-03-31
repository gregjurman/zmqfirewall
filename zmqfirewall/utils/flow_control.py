__all__ = ['divert', 'interrupt']

# Similar to TG2's redirect method
def divert(new_action):
    from zmqfirewall.exceptions import DivertAction
    diversion = DivertAction(new_action)
    raise diversion

def interrupt(new_action):
    from zmqfirewall.exceptions import InterruptAction
    interruption = InterruptAction(new_action)
    raise interruption
