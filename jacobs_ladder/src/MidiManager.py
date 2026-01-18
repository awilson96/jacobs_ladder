import argparse
import sys
import heapq
import logging
import rtmidi
import subprocess
import warnings

from pathlib import Path
from copy import deepcopy

from .JacobMonitor import JacobMonitor
from .JustIntonation import JustIntonation
from .MidiRecorder import MidiRecorder
from .MockSender import MockSender
from .MusicTheory import MusicTheory
from .Pitch import PitchInfo
from .Udp import UDPSender

from .Logging import setup_logging
from .Utilities import build_udp_message, determine_octave, parse_midi_controller_config, pack_message, pack_message_heap

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "October 12th 2023 (creation)"

warnings.filterwarnings("ignore", message="RtMidiIn::getNextMessage.*user callback.*")


class MidiController:
    """This is a Midi Keyboard interface which allows for the manipulation of real time Midi data.
    MidiController maps 1 input port to 12 output ports used for single note manipulation.
    The MidiController does this to take advantage of the pitch wheel which globally alters the pitch of all 16 channels.
    By separating each note on to a unique rtmidi.MidiOut port, individual tuning of notes is possible.
    MidiController handles the mapping of a single port to 12 ports and all instance allocation and re-allocation.
    All tuning, chord display, and additional features are handled by other submodules.
    """

    def __init__(self, **kwargs):
        """Class Constructor creates a MidiController object.  MidiController handles MIDI port management, 
        output port instance management, and sustain pedal management.

        Args:
            input_port (str, optional): input port name. Defaults to "jacobs_ladder".
            output_ports (list, optional): output port name. Defaults to [f"jacobs_ladder_{i}" for i in range(12)].
            tuning (dict, optional): a dictionary giving the controller its tuning. Defaults to None.
            tuning_mode (str, optional): static, dynamic, or None for no tuning. Defaults to None.
        """
        allowed_keys = {
            'log_level', 'input_port', 'output_ports', 'scale_includes', 'tempo', 'time_signature', 'player', 
            'tuning', 'tuning_mode', 'tuning_ratios_all', 'tuning_ratios_pref', 'tuning_configuration'
        }

        for key in kwargs:
            if key not in allowed_keys:
                raise ValueError(f"Unknown argument: {key}")
        
        self.log_level = kwargs.get('log_level', 20)
        self.input_port = kwargs.get('input_port', None)
        self.output_ports = kwargs.get('output_ports', [f"jacobs_ladder_{i}" for i in range(12)])
        self.virtual_ports_initialized = False
        self.scale_includes = kwargs.get('scale_includes', [])
        tuning_cfg = kwargs.get('tuning_configuration', {})
        self.tuning = tuning_cfg.get('tuning', None)
        self.tuning_mode = tuning_cfg.get('tuning_mode', None)
        self.tuning_ratios_all = tuning_cfg.get('tuning_ratios_all', '5-limit-ratios')
        self.tuning_ratios_pref = tuning_cfg.get('tuning_ratios_pref', '5-limit-pref')
        self.tempo = kwargs.get('tempo', 120)
        self.time_signature = kwargs.get('time_signature', "4/4")

        self.logger = setup_logging(app_name="JacobsLadder", level=self.log_level)
        self.logger.info("[MM] Initializing MidiController...")
        
        # MIDI port management
        self.midi_in = rtmidi.MidiIn()
        self.midi_out_ports = [rtmidi.MidiOut() for _ in range(12)] if sys.platform.startswith("win") else []
        self.input_port = self.input_port
        self.output_ports = self.output_ports
        self.logger.info(f"[MM] Input port: {self.input_port}")
        self.logger.info(f"[MM] Output ports: {self.output_ports}")

        # TODO: On Windows call virtual port setup script here before initilization 
        
        # Create midi in and midi out virtual port objects
        self.initialize_ports()

        # Output port instance management
        self.instance_index = list(range(12))
        self.message_heap = [] 
        self.in_use_indices = {}

        # Sustain pedal management
        self.sustain = False
        self.sustained_notes = []
        
        # Music Theory
        self.music_theory = MusicTheory(logger=self.logger)
        self.logger.info(f"[MM] Initializing MusicTheory...")

        # Tuning management
        self.logger.info("[MM] Initializing JustIntonation...")
        if self.tuning and self.tuning_mode: 
            self.logger.info("[MM] Tuning is enabled")
            self.logger.info(f"[MM] Mode is set to \"{self.tuning_mode}\" tuning")
        else:
            self.logger.info("[MM] Tuning is disabled")
        self.just_intonation = JustIntonation(self.logger, **kwargs.get("tuning_configuration", None))
            
        # Transposition Management
        self.transpose = 0
        
        # Communication with Jacob
        if self.output_ports == [f"jacobs_ladder_{i}" for i in range(12)]:
            self.udp_sender = UDPSender(host='127.0.0.1', port=50005, logger=self.logger)
            
            self.udp_receiver = JacobMonitor(manager=self, host='127.0.0.1', port=50000, logger=self.logger)
            self.udp_receiver.start_listener()
            
            self.logger.info("[MM] Initializing connection to Jacob...")
        else:
            self.udp_receiver = JacobMonitor(manager=self, host='127.0.0.1', port=50002, logger=self.logger)
            self.udp_receiver.start_listener()
            self.udp_sender = MockSender(host='127.0.0.1', port=50003)
            self.logger.info("[MM] Initializing connection to User...")

        # Recorder
        self.should_record = False
        self.recorder = MidiRecorder(logger=self.logger)
        
        self.logger.info("[MM] Listening for Midi messages...")
        self.set_midi_callback()
        self.start_listening()
        
        self.logger.info("[MM] Exiting...")


    def initialize_ports(self):
        """Initialize input and output ports based on OS."""

        is_posix = sys.platform.startswith("darwin") or sys.platform.startswith("linux")

        if is_posix:
            input_port = None
            for i, name in enumerate(self.midi_in.get_ports()):
                if self.input_port in name:
                    input_port = i
                    print(f"Using input: {name}")
                    break

            if input_port is None:
                raise RuntimeError("MIDI input not found")

            self.midi_in.open_port(input_port)

            # ---- Create 12 virtual MIDI outputs ----
            NUM_PORTS = 12
            for i in range(NUM_PORTS):
                out = rtmidi.MidiOut()
                port_name = f"jacobs_ladder_{i}"
                out.open_virtual_port(port_name)
                self.midi_out_ports.append(out)
                print(f"Created virtual output: {port_name}")
            return

        # Non-POSIX (Windows)
        try:
            available_input_ports = self.midi_in.get_ports()
            self.logger.debug(f"[MM] available_input_ports (Windows) \n{available_input_ports}")

            # Match full port name or startswith self.input_port
            input_port_index = next(
                (i for i, p in enumerate(available_input_ports) if p.startswith(self.input_port)),
                None
            )

            if input_port_index is not None:
                self.midi_in.open_port(input_port_index)
                self.logger.info(f"[MM] Opened MIDI input port: {available_input_ports[input_port_index]}")
            else:
                raise ValueError(f"[MM] Input port '{self.input_port}' not found.")

        except (ValueError, rtmidi._rtmidi.SystemError) as e:
            raise RuntimeError(f"[MM] Failed to open input port '{self.input_port}': {e}")

        # Initialize MIDI output ports
        try:
            available_output_ports = self.midi_out_ports[0].get_ports()
            self.logger.debug(f"[MM] available_output_ports (Windows) \n{available_output_ports}")

            for midi_out_idx, port_name in enumerate(self.output_ports):
                # Match full port name or startswith
                output_port_index = next(
                    (i for i, p in enumerate(available_output_ports) if p.startswith(port_name)),
                    None
                )

                if output_port_index is not None:
                    self.midi_out_ports[midi_out_idx].open_port(output_port_index)
                    self.logger.info(f"[MM] Opened MIDI output port: {available_output_ports[output_port_index]}")
                else:
                    raise ValueError(f"[MM] Output port '{port_name}' not found.")

        except (ValueError, rtmidi._rtmidi.SystemError) as e:
            raise RuntimeError(f"[MM] Failed to open output port '{port_name}': {e}")


    def close_ports(self):
        """Closes all opened input and output ports."""
        # Close MIDI input port
        if self.midi_in.is_port_open():
            self.midi_in.close_port()

        # Close MIDI output ports
        for midi_out_port in self.midi_out_ports:
            if midi_out_port.is_port_open():
                midi_out_port.close_port()

    def set_input_port(self, port: str) -> None:
        """Set the input port to something new (used by the frontend to change the input midi port)

        Args:
            port (str): the Midi port you want to select
        """
        available_input_ports = self.midi_in.get_ports()
        input_port_index = next(
            (i for i, p in enumerate(available_input_ports) if p.startswith(port)),
            None
        )
        if input_port_index is not None:
            self.input_port = port
        else:
            raise RuntimeError(f"Failed to find port {port}")

    def delete_suspended_note(self, sus_note: list):
        """Delete notes which have been sustained when the associated NOTE_OFF message has already been played

        Args:
            sus_note (list): a list of suspended (or sustained) notes to be deleted
        """
        for index, sublist in enumerate(self.message_heap):
            if sublist[0] == sus_note[0]:
                del self.message_heap[index]
                return

    def filter(self, message: tuple, timestamp: float):
        """Filter used to set the MIDI callback.
        The MIDI callback filters out only the messages you want to process within the callback.
        The filter handles NOTE_ON, NOTE_OFF, CONTROL_CHANGE, and ALL_NOTES_OFF message types.
        The filter is called by start_listening() and can be thought of as the main control loop.

        Args:
            message (tuple): The raw MIDI message ([status, note, velocity], dt)
            timestamp (float): Empty variable, necessary for MIDI callback as the underlying C++ code 
            is expecting this function signiture
        """
        payload, dt  = message
        status, note, velocity = payload

        if self.should_record and self.tuning_mode in ("none", None):
            self.recorder.record_event(status, note, velocity)

        self.just_intonation.tuning_mode = self.tuning_mode

        if status in range(144, 160):
            instance_index = determine_octave(message_heap=self.message_heap, note=note)
            if instance_index is None:
                if note not in [msg_note[0] for msg_note in self.message_heap]:
                    instance_index = heapq.heappop(self.instance_index)
                else:
                    logging.warning(f"no instances are left! {instance_index}")
                        
            self.in_use_indices[note] = instance_index
            current_msg = [note + self.transpose, instance_index, status, velocity, PitchInfo()]
            heapq.heappush(self.message_heap, current_msg)

            self.logger.debug(f"[MM] {self.message_heap=}")
            
            chord = self.music_theory.determine_chord(self.message_heap)
            candidate_scales, bitmasks = self.music_theory.get_candidate_scales(message_heap=self.message_heap, scale_includes=self.scale_includes)
            key = self.music_theory.find_key()

            self.logger.debug(f"[MM] {chord=}")
            self.logger.debug(f"[MM] {candidate_scales=}")
            self.logger.debug(f"[MM] {bitmasks=}")
            self.logger.debug(f"[MM] {key=}")

            data_bytes = pack_message(message_heap=self.message_heap, candidate_scales=candidate_scales, bitmasks=bitmasks)
            datagram1 = build_udp_message(message_type=1, payload_bytes=data_bytes)
            self.udp_sender.send_bytes(datagram1)
            
            if self.tuning_mode == "static" or self.tuning_mode == "dynamic" or self.tuning_mode == "just-intonation":
                self.logger.debug(f"[MM] Tuning using {self.tuning_mode}")
                tuning_index, pitch_bend_message, message_heap = self.just_intonation.get_tuning_info(message_heap=self.message_heap, current_msg=current_msg, dt=dt, key=key)
                self.message_heap = message_heap
                self.midi_out_ports[tuning_index].send_message(pitch_bend_message)
            else:
                self.logger.debug(f"[MM] Applying no tuning to each MIDI instance...")
                self.midi_out_ports[instance_index].send_message([224, 0, 64])

            message_heap_bytes = pack_message_heap(self.message_heap)
            datagram2 = build_udp_message(message_type=2, payload_bytes=message_heap_bytes)
            self.udp_sender.send_bytes(datagram2)

            self.midi_out_ports[instance_index].send_message([status, note, velocity])

        elif status in range(128, 144):
            instance_index = self.in_use_indices[note]
            self.midi_out_ports[instance_index].send_message([status, note, velocity])
            if not self.sustain:
                # Delete only the first occurance of note in self.message_heap
                for index, sublist in enumerate(self.message_heap):
                    if sublist[0] == note:
                        del self.message_heap[index]
                        break
                heapq.heapify(self.message_heap)
                if instance_index not in self.instance_index:
                    heapq.heappush(self.instance_index, instance_index)
                del self.in_use_indices[note]

            else:
                heapq.heappush(self.sustained_notes, [note, instance_index, status, velocity])
            
            chord = self.music_theory.determine_chord(self.message_heap)
            candidate_scales, bitmasks = self.music_theory.get_candidate_scales(message_heap=self.message_heap, scale_includes=self.scale_includes)
            key = self.music_theory.find_key()
            self.logger.debug(f"[MM] {chord=}")
            self.logger.debug(f"[MM] {candidate_scales=}")
            self.logger.debug(f"[MM] {bitmasks=}")
            self.logger.debug(f"[MM] {key=}")

            data_bytes = pack_message(message_heap=self.message_heap, candidate_scales=candidate_scales, bitmasks=bitmasks)
            if data_bytes:
                datagram1 = build_udp_message(message_type=1, payload_bytes=data_bytes)
                self.udp_sender.send_bytes(datagram1)
            else:
                live_keys_payload = "Live keys"[:25].ljust(25).encode("ascii") + bytearray([0]*11)
                datagram1 = build_udp_message(message_type=1, payload_bytes=live_keys_payload)
                self.udp_sender.send_bytes(datagram1)
            
            message_heap_bytes = pack_message_heap(self.message_heap)
            datagram2 = build_udp_message(message_type=2, payload_bytes=message_heap_bytes)
            self.udp_sender.send_bytes(datagram2)

        elif status in range(176, 192) and note == 64:
            if velocity == 127:
                self.sustain = True
                for instance_index in range(12):
                    self.midi_out_ports[instance_index].send_message([status, 64, 127])
            elif velocity == 0:
                self.sustain = False
                for instance_index in range(12):
                    self.midi_out_ports[instance_index].send_message([status, 64, 0])
                
                sus_notes_copy = deepcopy(self.sustained_notes)
                multiple_played_notes = []
                for sus_note in sus_notes_copy:
                    instance_index = self.in_use_indices[sus_note[0]]
                    self.delete_suspended_note(sus_note=sus_note)
                    if instance_index or instance_index == 0:
                        if sus_note[1] not in [sublist[1] for sublist in self.message_heap]:
                            heapq.heappush(self.instance_index, instance_index)
                            del self.in_use_indices[sus_note[0]]
                        else:
                            multiple_played_notes.append(sus_note)

                if not self.message_heap:
                    self.in_use_indices = {}
                else:
                    counter = 0
                    length = len([note[0] for note in self.in_use_indices.items()])
                    while sorted([note[0] for note in self.in_use_indices.items()]) != sorted([note[0] for note in self.message_heap]):
                        if counter > 1000:
                            logging.warning("Loop is misbehaving or you just held the sustain pedal for a really long time!")
                            break
                        for duplicate_note in [note[0] for note in self.in_use_indices.items()]:
                            counter += 1
                            if duplicate_note not in [note[0] for note in self.message_heap]:
                                del self.in_use_indices[duplicate_note]
                                break
                
                heapq.heapify(self.message_heap)
                sus_notes_copy = []
                self.sustained_notes = []
        
        elif status in range(176, 192) and note == 1:
            # if velocity == 127:
            for midi_out in self.midi_out_ports:
                # No tuning message
                midi_out.send_message([status + 48, 0, 64])

        elif status == 169:
            self.turn_off_all_notes()

    def change_recording_mode(self, recording_mode: int, tempo: int) -> None:
        """Change the recording mode (start/stop)

        Args:
            recording_mode (str): start/stop
        """
        if recording_mode == 1:
            self.should_record = True
            self.recorder.start(tempo=tempo)
        elif recording_mode == 0:
            self.should_record = False
            self.recorder.stop()
        else:
            print("Error: Incorrect recording mode")
            
    def get_midi_input_ports(self) -> list[str]:
        """Get a list of the MIDI input ports

        Returns:
            list[str]: a list of MIDI input ports
        """
        return self.midi_in.get_ports()
    
    def transpose_by(self, amount: int) -> None:
        """Transpose by a given integer number of notes away from the root up or down

        Args:
            amount (int): a transposition amount in the range (-12, 12) inclusive
        """
        if -12 <= amount <= 12:
            self.transpose = amount

    def turn_off_all_notes(self):
        """ Utility function used in troubleshooting/debugging. It is useful when handling hanging MIDI messages, 
        and it's used to silence all output by sending ALL_NOTES_OFF message to all instances
        """
        all_notes_off_message = [176, 123, 0]
        retune_to_center_frequency = [224, 0, 64]
        for instance_index in range(12):
            self.midi_out_ports[instance_index].send_message(all_notes_off_message)
            self.midi_out_ports[instance_index].send_message(retune_to_center_frequency)

    def set_midi_callback(self):
        """This function filters the output to the console based on the filter function"""
        self.midi_in.set_callback(self.filter)

    def start_listening(self):
        """ This is the main control loop where execution takes place.
        The listener waits for Midi messages and acts according to the filter function
        """
        try:
            print("Listening for MIDI messages. Press Ctrl+C to exit.")
            while True:
                message = self.midi_in.get_message()
        except KeyboardInterrupt:
            print("Exiting...")
            self.turn_off_all_notes()
        finally:
            self.close_ports()
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load MidiController from YAML config.")
    parser.add_argument('config_path', type=str, help="Path to YAML config file.")
    args = parser.parse_args()

    kwargs = parse_midi_controller_config(args.config_path, print_config=True)
    midi_controller = MidiController(**kwargs)