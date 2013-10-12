import zmqfirewall.actions as zma
from zmqfirewall.actions.base import ActionMeta

from nose.tools import eq_, raises, assert_is_not_none
from unittest import TestCase

class ActionTest(TestCase):
    def setUp(self):
        ActionMeta.deregisterAll()


    def test_good_action(self):
        class GoodActionTestAction(zma.Action):
            def action(self, message):
                return message


    @raises(AttributeError)
    def test_missing_action(self):
        class MissingActionTestAction(zma.Action):
            pass


    @raises(AttributeError)
    def test_bad_action(self):
        class BadActionTestAction(zma.Action):
            action = "I am not callable"


    @raises(NameError)
    def test_duplicate_name_action(self):
        class WorkingActionTestAction(zma.Action):
            def action(self, message):
                return message

        class IdiotlyNamedAction(zma.Action):
            name = 'workingactiontest'

            def action(self, message):
                pass


    def defineTestAction(self):
        class GoodActionTestAction(zma.Action):
            def action(self, msg):
                return msg


    @raises(TypeError)
    def test_duplicate_class_action(self):
        self.defineTestAction()
        self.defineTestAction()

    @raises(KeyError)
    def test_deregged_action(self):
        self.defineTestAction()
        assert_is_not_none(ActionMeta.get_action_by_name('goodactiontest'))
        ActionMeta.deregister('goodactiontest')
        ActionMeta.get_action_by_name('goodactiontest')

