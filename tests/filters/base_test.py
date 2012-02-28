import zmqfirewall.filters
from zmqfirewall.actions import AcceptMessageAction, FilterTopicAction

def test_basic_filter():
    class TestFilter(zmqfirewall.filters.FirewallFilter):
        chain = [FilterTopicAction(['test_topic'])]
