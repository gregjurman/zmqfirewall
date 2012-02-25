import zmqfirewall.actions

from nose.tools import eq_

def test_good_action():
    class TestAction(zmqfirewall.actions.Action):
        def action(self, message):
            return message

def test_missing_action():
    try:
        class MissingTestAction(zmqfirewall.actions.Action):
            pass

        assert(False)
    except AttributeError, e:
        eq_(str(e), 'MissingTestAction is missing an action callback')

def test_bad_action():
    try:
        class BadTestAction(zmqfirewall.actions.Action):
            action = "I am not callable"

        assert(False)
    except AttributeError, e:
        eq_(str(e), 'BadTestAction is missing an action callback')
