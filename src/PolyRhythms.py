from .RhythemGenerator import RhythmGenerator
from .DataClasses import RhythemNoteEvent

class PolyRhythms(RhythmGenerator):

    def __init__(self, tempo):
        super().__init__(tempo=tempo)

    def create_polyrhythm(self, ratio: str, multiplicity: int):
        if ratio.split(":")[-1] == "1":
            [self.create_n_1_polyrhythm(n=int(ratio.split(":")[0])) for _ in range(multiplicity)]

    def create_n_1_polyrhythm(self, n: int):
        long_note_on = RhythemNoteEvent(division="ZERO", note="D\u266d5", status="NOTE_ON", velocity=85)
        quarter_note_on = RhythemNoteEvent(division="ZERO", note="A5", status="NOTE_ON", velocity=85)
        quarter_note_off = RhythemNoteEvent(division="QUARTER", note="A5", status="NOTE_OFF", velocity=85)
        long_note_off = RhythemNoteEvent(division="ZERO", note="D\u266d5", status="NOTE_OFF", velocity=85)

        note_list = [long_note_on]
        for _ in range(n):
            note_list.append(quarter_note_on)
            note_list.append(quarter_note_off)
        note_list.append(long_note_off)
        self.add_events(rhythem_note_events=note_list)

if __name__ == "__main__":
    polyrhythms = PolyRhythms(tempo=120)
    polyrhythms.create_polyrhythm(ratio="2:1", multiplicity=1)
    polyrhythms.create_polyrhythm(ratio="3:1", multiplicity=1)
    polyrhythms.create_polyrhythm(ratio="4:1", multiplicity=1)
    polyrhythms.create_polyrhythm(ratio="5:1", multiplicity=1)
    polyrhythms.create_polyrhythm(ratio="6:1", multiplicity=1)
    polyrhythms.midi_scheduler.schedule_events(initial_delay=1000)
