import struct

from .Utilities import build_udp_message
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
        elif message_type == 2:
            self._handle_get_midi_ports_message()
        else:
            print(f"Unknown message type: {message_type}")

    def _handle_recording_message(self, payload: bytes) -> None:
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
            
    def _handle_get_midi_ports_message(self) -> None:
        """Handle request for available MIDI input ports."""
        if not hasattr(self.manager, "get_midi_input_ports"):
            print("Manager does not implement get_midi_input_ports()")
            return

        ports = self.manager.get_midi_input_ports()
        
        if self.print_msgs:
            print(f"Recieved get_midi_input_ports request...\nSending ports:\n{ports}")

        if not ports:
            payload = b""
        else:
            # UTF-8, null-separated, trailing null is OK
            payload = b"\0".join(p.encode("utf-8") for p in ports) + b"\0"

        datagram = build_udp_message(
            message_type=2,
            payload_bytes=payload,
        )

        # Send back to frontend
        self.manager.udp_sender.send_bytes(datagram)
