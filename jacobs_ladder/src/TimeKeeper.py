import threading
from time import sleep

from .Udp import UDPSender
from .UserMonitor import UserMonitor

class TimeKeeper:
    def __init__(self, sender: UDPSender, tempo: int = 120, time_signature: str = "4/4"):
        """Initialize the TimeKeeper with a specified tempo and time signature.

        Args:
            tempo (int): The tempo in beats per minute.
            time_signature (str): The time signature (e.g., "4/4").
            host (str): The UDP host address.
            port (int): The UDP port number.
        """
        self.udp_sender = sender
        
        self.tempo = tempo
        self.time_signature = time_signature
        self.num_beats = int(time_signature.split("/")[0])
        self.is_running = False
        self.current_beat = 0
        
        self.quarter_note_duration_ms = (60 / self.tempo) * 1000
        self.timer = None
        

    def start_timekeeper(self):
        """Start the timekeeping process."""
        self.is_running = True
        self.schedule_next_event()

    def stop(self):
        """Stop the timekeeping process."""
        self.is_running = False
        if self.timer is not None:
            self.timer.cancel()  
        self.udp_sender.stop()

    def schedule_next_event(self):
        """Schedule the next quarter note event."""
        if self.is_running:
            self.timer = threading.Timer(self.quarter_note_duration_ms / 1000, self.send_event)
            if self.current_beat == 10000:
                self.current_beat = 0
            self.timer.start()

    def send_event(self):
        """Send a UDP message for the current event."""
        if self.is_running:
            self.send_beat_message()
            self.current_beat += 1
            self.schedule_next_event()

    def send_beat_message(self):
        """Send a UDP message indicating a downbeat."""
        if self.is_running:
            message = {"event": "beat", "beat": f"{self.current_beat % self.num_beats + 1}", "measure": self.current_beat // self.num_beats + 1}
            self.udp_sender.send(message)

    def set_timing(self, tempo: int, time_signature: str):
        """Update the tempo and notify subscribers.

        Args:
            new_tempo (int): The new tempo in beats per minute.
        """
        self.is_running = False
        self.tempo = tempo
        self.time_signature = time_signature
        self.num_beats = int(time_signature.split("/")[0])
        self.quarter_note_duration_ms = (60 / self.tempo) * 1000
        self.is_running = True

if __name__ == "__main__":
    udp_sender = UDPSender(host="127.0.0.1", port=50000, print_msgs=False)
    time_keeper = TimeKeeper(sender=udp_sender, tempo=120, time_signature="4/4")
    try:
        time_keeper.start_timekeeper()
        while True:
            sleep(10)
    except KeyboardInterrupt:
        print("Exiting...")
        time_keeper.stop()
