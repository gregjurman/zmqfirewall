
import zmqfirewall.actions.simple as zas
from zmqfirewall.message import Message

from nose.tools import eq_

test_msg = Message(message="I am the cheese", from_host="127.0.0.1")

def test_accept_action():
    out = zas.AcceptMessageAction.req(test_msg)

    eq_(test_msg, out)    
