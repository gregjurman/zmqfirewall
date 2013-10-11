from zmqfirewall.exceptions import DivertAction

from nose.tools import eq_


def bad_construct_test():
    try:
        DivertAction(123)
    except ValueError as e:
        eq_(str(e), "new_action must be a string or Action, got 123")
