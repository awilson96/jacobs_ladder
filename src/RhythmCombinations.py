from .PolyRhythms import PolyRhythms
from .DataClasses import RhythemNoteEvent, NoteEvent
from .Dictionaries import beat_to_note_divisions
from .Enums import NoteDivisions
from .Utilities import division_to_dt
from itertools import product
from copy import deepcopy
import time

class RhythmCombinations(PolyRhythms):

    def __init__(self, tempo):
        super().__init__(tempo=tempo)

    def find_combinations(self, combinations: tuple[NoteDivisions], measure_duration: int) -> list[list[NoteDivisions]]:
        all_combinations = []

        def helper(remaining_duration: int, current_combo: list[NoteDivisions]):
            # If the remaining duration is exactly zero, we found a valid combination
            if remaining_duration == 0:
                all_combinations.append(current_combo[:])
                return
            # If remaining duration is negative, this path is invalid
            elif remaining_duration < 0:
                return

            # Try adding each note/rest to the current combination
            for note in combinations:
                current_combo.append(note)
                helper(remaining_duration - abs(note.value), current_combo)
                current_combo.pop()  # Backtrack to try the next note/rest

        # Start the recursive combination search
        helper(measure_duration, [])
        return all_combinations

    def display_combinations(self, combinations: list[list[NoteDivisions]]):
        # Displaying the combinations as formatted strings
        for combo in combinations:
            print("-".join(note.name for note in combo))

if __name__ == "__main__":
    rhythm_combinations = RhythmCombinations(tempo=120)
    measure_duration = NoteDivisions.WHOLE.value
    valid_combinations = rhythm_combinations.find_combinations(
        combinations=(
            NoteDivisions.HALF,
            NoteDivisions.HALF_REST,
            NoteDivisions.QUARTER,
            NoteDivisions.QUARTER_REST
        ),
        measure_duration=measure_duration
    )
    rhythm_combinations.display_combinations(valid_combinations)
