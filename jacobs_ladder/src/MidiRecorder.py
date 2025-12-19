import logging
import threading
import mido
import os
import sys

is_posix = sys.platform.startswith("darwin") or sys.platform.startswith("linux")
try:
    from jacobs_ladder import qpc_utils
except ImportError:
    from .MockQpc import MockQpcUtils

class MidiRecorder:
    def __init__(self, logger: logging.Logger):
        if not is_posix:
            self.qpc = qpc_utils.QpcUtils()
        else:
            self.qpc = MockQpcUtils()
        self.logger = logger
        self.is_recording = False
        self.is_saving = False
        self.start_ticks = None
        self.last_ticks = None
        self.messages = []
        self._saving_thread = None
        self.tempo = 120

    def start(self, tempo: int):
        """Begin recording MIDI messages."""
        if self.is_recording:
            self.logger.warning("Warning: Recorder is already running.")
            return
        if self.is_saving:
            self.logger.warning("Cannot start recording: previous recording is still saving.")
            return

        self.tempo = tempo
        self.is_recording = True
        self.start_ticks = self.qpc.qpcGetTicks()
        self.last_ticks = self.start_ticks
        self.messages = []
        self.logger.info("Recording started...")

    def stop(self, filename="recording.mid"):
        """Stop recording and save in background. Safe against multiple calls."""
        if not self.is_recording:
            if self.is_saving:
                self.logger.warning("Stop called, but a save is already in progress. Ignoring.")
            else:
                self.logger.warning("No active recording to stop.")
            return

        if not self.messages:
            self.logger.warning("No MIDI messages recorded.")
            self.is_recording = False
            return

        # Transition to saving state
        self.is_recording = False
        self.is_saving = True

        # Spawn detached thread for saving
        self._saving_thread = threading.Thread(
            target=self._save_recording,
            args=(filename, self.start_ticks),
            daemon=True
        )
        self._saving_thread.start()
        self.logger.info(f"Recording stopped — saving in background to {filename}...")

    def _save_recording(self, filename, start_ticks):
        """Threaded save operation, clears messages after saving."""
        try:
            freq = self.qpc.qpcGetFrequency()
            mid = mido.MidiFile(ticks_per_beat=960)
            track = mido.MidiTrack()
            mid.tracks.append(track)

            last_ticks = start_ticks
            tempo = mido.bpm2tempo(self.tempo)

            for msg_data, ticks in self.messages:
                delta_s = (ticks - last_ticks) / freq
                last_ticks = ticks

                status, note_or_control, velocity_or_value = msg_data
                msg_type = None

                if 144 <= status < 160:
                    msg_type = 'note_on'
                elif 128 <= status < 144:
                    msg_type = 'note_off'
                elif 176 <= status < 192:
                    msg_type = 'control_change'

                self.logger.debug(msg_type, note_or_control, velocity_or_value, delta_s)

                if msg_type:
                    delta_ticks = int(mido.second2tick(delta_s, mid.ticks_per_beat, tempo))

                    if msg_type in ['note_on', 'note_off']:
                        msg = mido.Message(msg_type,
                                        note=note_or_control,
                                        velocity=velocity_or_value,
                                        time=delta_ticks)
                    elif msg_type == 'control_change':
                        msg = mido.Message(msg_type,
                                        control=note_or_control,
                                        value=velocity_or_value,
                                        time=delta_ticks)
                    track.append(msg)
                else:
                    self.logger.warning(f"Skipped unknown status byte: {status}")

            mid.save(filename)
            self.logger.info(f"Recording saved to: {os.path.abspath(filename)}")

        except Exception as e:
            self.logger.error(f"Error while saving MIDI file: {e}")

        finally:
            # Clear messages and reset flags
            self.messages = []
            self.is_saving = False


    def record_event(self, status: int, note: int, velocity: int):
        """Record an incoming MIDI message with high-resolution timestamp."""
        if not self.is_recording:
            return
        if self.is_saving:
            self.logger.warning("Recording blocked: previous recording is still saving.")
            return
        ticks = self.qpc.qpcGetTicks()
        self.messages.append(((status, note, velocity), ticks))
