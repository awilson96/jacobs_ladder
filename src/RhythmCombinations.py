from .PolyRhythms import PolyRhythms
from .DataClasses import RhythmNoteEvent, NoteEvent
from .Dictionaries import beat_to_note_divisions
from .Enums import NoteDivisions
from .Utilities import division_to_dt
from itertools import product
from copy import deepcopy
import time

class RhythmCombinations(PolyRhythms):

    def __init__(self, tempo, tolerance: int = 82):
        super().__init__(tempo=tempo)
        self.tempo = tempo
        self.tolerance = tolerance

    def find_combinations(self, combinations: tuple[NoteDivisions], measure_duration: int) -> list[list[NoteDivisions]]:
        all_combinations = []

        def helper(remaining_duration: int, current_combo: list[NoteDivisions]):
            # If the remaining duration is within the tolerance, consider it a valid combination
            if abs(remaining_duration) <= self.tolerance:
                all_combinations.append(current_combo[:])
                return
            # If remaining duration is less than zero beyond the tolerance, this path is invalid
            elif remaining_duration < -self.tolerance:
                return

            # Try adding each note/rest to the current combination
            for note in combinations:
                current_combo.append(note)
                helper(remaining_duration - abs(note.value), current_combo)
                current_combo.pop()  # Backtrack to try the next note/rest

        # Start the recursive combination search
        helper(measure_duration, [])
        len_ms = measure_duration * len(all_combinations)
        return all_combinations, len_ms

    def display_combinations(self, combinations: list[list[NoteDivisions]]):
        # Displaying the combinations as formatted strings
        for combo in combinations:
            print("-".join(note.name for note in combo))

    def queue_combinations(self, combinations: list[list[NoteDivisions]], stash: bool = False):
        self.add_event(rhythem_note_event=RhythmNoteEvent(offset=0, division="ZERO", note="C7", status="NOTE_OFF", velocity=0, tempo=self.tempo), stash=stash)
        for combo in combinations:
            for division in combo: 
                status = "NOTE_ON" if "_REST" not in division.name else "NOTE_OFF"
                offset = self.get_offset(index=-1, stash=stash)
                self.add_events_with_duration(
                    rhythem_note_events=[RhythmNoteEvent(offset=offset, division="ZERO", note="E4", status=status, velocity=80, tempo=self.tempo),
                                         RhythmNoteEvent(offset=offset, division="ZERO", note="G4", status=status, velocity=80, tempo=self.tempo)],
                    duration_divisions=[division.name, division.name],
                    stash=stash)
                
        self.midi_scheduler.sort_events_by_dt(relative=False, stash=stash)

if __name__ == "__main__":
    rhythm_combinations = RhythmCombinations(tempo=120)
    measure_duration = NoteDivisions.QUARTER.value
    valid_combinations, len_ms = rhythm_combinations.find_combinations(
        combinations=(
            NoteDivisions.EIGHTH,
            NoteDivisions.SIXTEENTH,
            NoteDivisions.THIRTYSECOND
        ),
        measure_duration=measure_duration
    )

    rhythm_combinations.display_combinations(valid_combinations)
    rhythm_combinations.queue_combinations(combinations=valid_combinations, stash=False)
    rhythm_combinations.midi_scheduler.sort_events_by_dt(relative=True, stash=False)
    rhythm_combinations.midi_scheduler.schedule_events(initial_delay=0)


    rhythm_combinations.queue_combinations(combinations=valid_combinations, stash=True)
    rhythm_combinations.midi_scheduler.sort_events_by_dt(relative=True, stash=True)