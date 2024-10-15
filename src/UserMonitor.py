from .Udp import UDPReceiver

class UserMonitor(UDPReceiver):
    def __init__(self, host: str = "127.0.0.1", port: int = 50001, print_msgs: bool = False):
        super().__init__(host=host, port=port, print_msgs=print_msgs)
        self.candidate_keys = []
        self.messages = []
        
    def dispact_message(self, data):
        """Handle user message types candidate_keys and general messages from the message heap

        Args:
            data (list): data can come in the form of list[str] or list[list[int]]
        """
        if isinstance(data, dict):
            if data.get('event') == "downbeat":
                # TODO Simplify this to simply be the beat instead of isolating the downbeat (i.e. 1, 2, 3, 4)
                # this is where calls to the rhythem generators schedule_events() will happen
                return
            elif data.get("event") == "beat":
                return
        elif data and any(isinstance(item, str) for item in data):
            self.candidate_keys = data
        elif data and any(isinstance(item, list) for item in data):
            self.messages = data
                    
