import threading
import mido
import os
from jacobs_ladder import qpc_utils

class MidiRecorder:
    def __init__(self):
        self.qpc = qpc_utils.QpcUtils()
        self.is_recording = False
        self.is_saving = False
        self.start_ticks = None
        self.last_ticks = None
        self.messages = []
        self._saving_thread = None

    def start(self):
        """Begin recording MIDI messages."""
        if self.is_recording:
            print("Warning: Recorder is already running.")
            return
        if self.is_saving:
            print("Cannot start recording: previous recording is still saving.")
            return

        self.is_recording = True
        self.start_ticks = self.qpc.qpcGetTicks()
        self.last_ticks = self.start_ticks
        self.messages = []
        print("Recording started...")

    def stop(self, filename="recording.mid"):
        """Stop recording and save in background. Safe against multiple calls."""
        if not self.is_recording:
            if self.is_saving:
                print("Stop called, but a save is already in progress. Ignoring.")
            else:
                print("No active recording to stop.")
            return

        if not self.messages:
            print("No MIDI messages recorded.")
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
        print(f"Recording stopped — saving in background to {filename}...")

    def _save_recording(self, filename, start_ticks):
        """Threaded save operation, clears messages after saving."""
        try:
            freq = self.qpc.qpcGetFrequency()
            mid = mido.MidiFile()
            track = mido.MidiTrack()
            mid.tracks.append(track)

            last_ticks = start_ticks

            for msg_data, ticks in self.messages:
                delta_s = (ticks - last_ticks) / freq
                last_ticks = ticks

                status, note, velocity = msg_data
                msg_type = None

                if 144 <= status < 160:
                    msg_type = 'note_on'
                elif 128 <= status < 144:
                    msg_type = 'note_off'
                elif 176 <= status < 192:
                    msg_type = 'control_change'

                if msg_type:
                    msg = mido.Message(msg_type, note=note, velocity=velocity, time=delta_s)
                    track.append(msg)
                else:
                    print(f"Skipped unknown status byte: {status}")

            mid.save(filename)
            print(f"Recording saved to: {os.path.abspath(filename)}")

        except Exception as e:
            print(f"Error while saving MIDI file: {e}")

        finally:
            # Clear messages and reset flags
            self.messages = []
            self.is_saving = False

    def record_event(self, status: int, note: int, velocity: int):
        """Record an incoming MIDI message with high-resolution timestamp."""
        if not self.is_recording:
            return
        if self.is_saving:
            print("Recording blocked: previous recording is still saving.")
            return
        ticks = self.qpc.qpcGetTicks()
        self.messages.append(((status, note, velocity), ticks))
