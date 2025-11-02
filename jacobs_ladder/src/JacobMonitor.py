from .Udp import UDPReceiver
from .TimeKeeper import TimeKeeper

class JacobMonitor(UDPReceiver):
    
    def __init__(self, host: str = "127.0.0.1", port: int = 50001, print_msgs: bool = False, 
                 tuning_mode: str = None, timekeeper: TimeKeeper = None):
        super().__init__(host=host, port=port, print_msgs=print_msgs)
        self.tuning_mode = tuning_mode
        self.timekeeper = timekeeper
        if self.timekeeper:
            self.timekeeper.start_timekeeper()
    
    def dispatch_message(self, data):
        pass
