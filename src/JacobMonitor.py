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
    
    def dispact_message(self, data):
        """Receiver Jacobian message types

        Args:
            data (dict): data can come in the following form: {tuning_mode: <"static", "dynamic", None>}
        """
        if isinstance(data, dict):
            if data.get("event") == "tempo_update":
                print("Updating tempo and time signature...")
                if self.timekeeper:
                    self.timekeeper.set_timing(tempo=data.get("tempo"), time_signature=data.get("time_signature"))
            elif data.get(key="tuning_mode", default="none") != "none":
                tuning_mode = data.get("tuning_mode")
                self.tuning_mode = tuning_mode
