class MQInterface(object):
    """
        Defines a general interface for messages coming into the firewall
    """
    def send_message(self, message):
        """
            Form the message object into a proper binding specific message
            then call the base binding.
        """
        pass

    def handle_message(self, message):
        """
            Parse the message into a standard message object
        """
        pass
