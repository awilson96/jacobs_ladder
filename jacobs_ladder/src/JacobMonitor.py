import logging
import struct
import sys
import subprocess
from pathlib import Path
import yaml

from .Utilities import build_udp_message
from .Udp import UDPReceiver

class JacobMonitor(UDPReceiver):

    def __init__(self, manager, host: str = "127.0.0.1", port: int = 50001, logger: logging.Logger = None):
        super().__init__(host=host, port=port, logger=logger)

        self.manager = manager
        self.logger = logger

    def dispatch_message(self, data: bytes):
        """Decode and dispatch incoming UDP datagrams by message type."""
        if len(data) < 4:
            self.logger.warning("[JM] Received message too short")
            return

        # Unpack 32-bit message type (big-endian)
        message_type = struct.unpack_from(">I", data, 0)[0]
        payload = data[4:]

        self.logger.info(f"[JM] Received message type: {message_type}")


        if message_type == 1:
            self._handle_recording_message(payload)
        elif message_type == 2:
            self._handle_get_midi_ports_message()
        elif message_type == 3:
            self._handle_set_midi_input_port_message(payload)
        else:
            self.logger.warning(f"[JM] Unknown message type: {message_type}")

    def _handle_recording_message(self, payload: bytes) -> None:
        """Handle recording start/stop messages, with optional tempo BPM."""
        if len(payload) < 8:
            self.logger.warning(f"[JM] Recording message too short (got {len(payload)} bytes)")
            return

        # Unpack recording_state and tempo_bpm (both uint32, big-endian)
        recording_state, tempo_bpm = struct.unpack_from(">II", payload, 0)

        self.logger.info(f"[JM] Received recording_state={recording_state}, tempo_bpm={tempo_bpm}")

        if hasattr(self.manager, "change_recording_mode"):
            try:
                self.manager.change_recording_mode(int(recording_state), int(tempo_bpm))
            except TypeError:
                self.logger.error("[JM] Unable to change recording mode!")
        else:
            self.logger.error("[JM] Manager does not implement change_recording_mode()")
            
    def _handle_get_midi_ports_message(self) -> None:
        """Handle request for available MIDI input ports."""
        if not hasattr(self.manager, "get_midi_input_ports"):
            self.logger.error("[JM] Manager does not implement get_midi_input_ports()")
            return

        ports = self.manager.get_midi_input_ports()

        # Remove trailing indices if present
        cleaned_ports = []
        for port in ports:
            if "jacob" in port:
                continue
            elif " " in port and port.split()[-1].isdigit():
                cleaned_ports.append(" ".join(port.split()[:-1]))
            else:
                cleaned_ports.append(port)

        self.logger.info(f"[JM] Received get_midi_input_ports request...\nSending cleaned ports:\n{cleaned_ports}")

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
        """Switch MIDI input port (physical device selection) and update default_config.yaml."""

        required_methods = (
            "set_input_port",
            "initialize_ports",
            "set_midi_callback",
            "close_ports",
        )
        if not all(hasattr(self.manager, m) for m in required_methods):
            self.logger.error(
                "[JM] Manager does not implement one of the following:\n"
                "set_input_port()\ninitialize_ports()\nset_midi_callback()\nclose_ports()"
            )
            return
        
        try:
            new_port = payload.decode("utf-8").strip()
            if not new_port:
                return

            # Determine effective input port
            if sys.platform.startswith("win"):
                if not hasattr(self, "_map_ports_process"):
                    self._map_ports_process = None
                    self._mapped_input_port = None

                if new_port != getattr(self, "_mapped_input_port", None):
                    if self._map_ports_process is not None:
                        try:
                            self._map_ports_process.terminate()
                            self._map_ports_process.wait(timeout=2)
                        except Exception:
                            self._map_ports_process.kill()
                        finally:
                            self._map_ports_process = None

                    project_root = Path(__file__).resolve().parents[2]
                    map_ports_bin = project_root / "jacobs_ladder" / "cpp" / "bin" / "MapPorts"

                    self.logger.info(f"[JM] Launching MapPorts for input: {new_port}")
                    self._map_ports_process = subprocess.Popen(
                        [str(map_ports_bin), "--port", new_port],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    self._mapped_input_port = new_port

                effective_input_port = "jacobs_ladder"
            else:
                effective_input_port = new_port

            # Switch the port in the manager
            self.manager.close_ports()
            self.manager.set_input_port(effective_input_port)
            self.manager.initialize_ports()
            self.manager.set_midi_callback()

            self.logger.info(f"[JM] Input port switched successfully: {new_port}")

            # --- Update default_config.yaml ---
            project_root = Path(__file__).resolve().parents[2]
            config_path = project_root / "jacobs_ladder" / "configuration" / "yaml" / "default_config.yaml"

            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = yaml.safe_load(f) or {}

                # Update the input_port key
                config_data["input_port"] = new_port

                with open(config_path, "w", encoding="utf-8") as f:
                    yaml.safe_dump(config_data, f, default_flow_style=False, sort_keys=False)

                self.logger.info(f"[JM] default_config.yaml updated with input_port: {new_port}")
            else:
                self.logger.warning(f"[JM] default_config.yaml not found at {config_path}")

        except Exception as e:
            self.logger.error(f"[JM] Failed to switch input port: {e}")
