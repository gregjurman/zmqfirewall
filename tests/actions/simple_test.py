
import zmqfirewall.actions.simple as zas
import zmqfirewall.actions.bases as zab
from zmqfirewall.message import Message

from nose.tools import eq_

test_msg = Message(message="I am the cheese", from_host="127.0.0.1")

def test_accept_action():
    out = zas.AcceptMessageAction.action(test_msg)

    eq_(test_msg, out)

def test_drop_action():
    out = zas.DropMessageAction.action(test_msg)

    eq_(out, None)

def test_custom_action():
    class MangleTestAction(zab.Action):
        def action(self, msg):
            msg.message = "Hello, " + msg.message
            return msg

    out = MangleTestAction.action(test_msg)
    eq_(str(out), "Hello, I am the cheese")
