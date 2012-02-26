import zmqfirewall.actions

from nose.tools import eq_

def test_good_action():
    class GoodActionTestAction(zmqfirewall.actions.Action):
        def action(self, message):
            return message

def test_missing_action():
    try:
        class MissingActionTestAction(zmqfirewall.actions.Action):
            pass

        assert(False)
    except AttributeError, e:
        eq_(str(e), 'MissingActionTestAction is missing an action callback')

def test_bad_action():
    try:
        class BadActionTestAction(zmqfirewall.actions.Action):
            action = "I am not callable"

        assert(False)
    except AttributeError, e:
        eq_(str(e), 'BadActionTestAction is missing an action callback')


def test_duplicate_name_action():
    try:
        class WorkingActionTestAction(zmqfirewall.actions.Action):
            def action(self, message):
                return message

        class IdiotlyNamedAction(zmqfirewall.actions.Action):
            name = 'workingactiontest'

            def action(self, message):
                pass

        assert(False)
    except NameError as e:
        eq_(str(e),"An action named 'workingactiontest' is already registered!")

def test_duplicate_cls_name():
    try:
        class SameNameClassTestAction(zmqfirewall.actions.Action):
            def action(self, msg):
                pass

        import helper

        assert(False)
    except TypeError as e:
        eq_(str(e), 'SameNameClassTestAction is already registered!')
