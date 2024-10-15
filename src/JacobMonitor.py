from .Udp import UDPReceiver

class JacobMonitor(UDPReceiver):
    
    def __init__(self, host: str = "127.0.0.1", port: int = 50001, print_msgs: bool = False, 
                 tempo: int = 120, time_signature: str = "4/4", tuning_mode: str = None):
        super().__init__(host=host, port=port, print_msgs=print_msgs)
        self.tempo = tempo
        self.time_signature = time_signature
        self.tuning_mode = tuning_mode
    
    def dispact_message(self, data):
        """Receiver Jacobian message types

        Args:
            data (dict): data can come in the following form: {tuning_mode: <"static", "dynamic", None>}
        """
        if isinstance(data, dict):
            if data.get("event") == "tempo_update":
                print("Updating tempo and time signature...")
                self.tempo = data.get("tempo")
                self.time_signature = data.get("time_signature")
            elif data.get(key="tuning_mode", default="none") != "none":
                tuning_mode = data.get("tuning_mode")
                self.tuning_mode = tuning_mode
