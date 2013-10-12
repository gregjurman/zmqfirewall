import zmqfirewall.utils as zmu
from zmqfirewall.actions.simple import DropMessageAction as the_drop
from zmqfirewall.actions.base import ActionMeta

from nose.tools import assert_is_not_none
from unittest import TestCase


class UtilTest(TestCase):
    def setUp(self):
        ActionMeta.deregisterAll()

    def test_get_name(self):
        the_drop.register()
        assert_is_not_none(zmu.get_action('drop'), the_drop)
