import zmqfirewall.utils
from zmqfirewall.actions.simple import DropMessageAction as the_drop


def test_get_name():
    assert(isinstance(zmqfirewall.utils.get_action('drop'), the_drop))
