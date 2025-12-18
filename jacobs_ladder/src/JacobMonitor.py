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
        elif message_type == 3:
            self._handle_set_midi_input_port_message(payload)
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

        # Remove trailing indices if present
        cleaned_ports = []
        for port in ports:
            if " " in port and port.split()[-1].isdigit():
                cleaned_ports.append(" ".join(port.split()[:-1]))
            else:
                cleaned_ports.append(port)

        if self.print_msgs:
            print(f"Received get_midi_input_ports request...\nSending cleaned ports:\n{cleaned_ports}")

        if not cleaned_ports:
            payload = b""
        else:
            # UTF-8, null-separated, trailing null is OK
            payload = b"\0".join(p.encode("utf-8") for p in cleaned_ports) + b"\0"

        datagram = build_udp_message(
            message_type=2,
            payload_bytes=payload,
        )

        # Send back to frontend
        self.manager.udp_sender.send_bytes(datagram)

    def _handle_set_midi_input_port_message(self, payload: bytes) -> None:
        """Switch MIDI input port without touching outputs."""
        if not hasattr(self.manager, "set_input_port") or not hasattr(self.manager, "initialize_ports") or not hasattr(self.manager, "set_midi_callback"):
            print("Manager does not implement one of the following:\nset_input_port()\ninitialize_ports()\nset_midi_callback")
            return
        
        self.manager.close_ports()
        try:
            new_port = payload.decode("utf-8").strip()
            if not new_port:
                return
            
            self.manager.set_input_port(new_port)

            # 2. Re-initialize input and output ports
            self.manager.initialize_ports()  # your full initialize_ports() method

            # 3. Rebind the MIDI callback
            self.manager.set_midi_callback()

            print(f"Input port switched successfully: {new_port}")
        except Exception as e:
            print(f"Failed to switch input port: {e}")



