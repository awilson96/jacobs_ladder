import struct

from .Udp import UDPReceiver

class JacobMonitor(UDPReceiver):

    def __init__(self, manager, host: str = "127.0.0.1", port: int = 50001, print_msgs: bool = False):
        super().__init__(host=host, port=port, print_msgs=print_msgs)

        self.manager = manager

    def dispatch_message(self, data: bytes):
        """Decode and dispatch incoming UDP datagrams by message type."""
        if len(data) < 4:
            print("Received message too short")
            return

        # Unpack 32-bit message type (big-endian)
        message_type = struct.unpack_from(">I", data, 0)[0]
        payload = data[4:]

        print(f"Received message type: {message_type}")


        if message_type == 1:
            self._handle_recording_message(payload)
        else:
            print(f"Unknown message type: {message_type}")

    def _handle_recording_message(self, payload: bytes):
        """Handle recording start/stop messages, with optional tempo BPM."""
        if len(payload) < 8:
            print(f"Recording message too short (got {len(payload)} bytes)")
            return

        # Unpack recording_state and tempo_bpm (both uint32, big-endian)
        recording_state, tempo_bpm = struct.unpack_from(">II", payload, 0)

        print(f"Received recording_state={recording_state}, tempo_bpm={tempo_bpm}")

        if hasattr(self.manager, "change_recording_mode"):
            try:
                self.manager.change_recording_mode(int(recording_state), int(tempo_bpm))
            except TypeError:
                print("Unable to change recording mode!")
        else:
            print("Manager does not implement change_recording_mode()")

