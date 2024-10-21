from .RhythemGenerator import RhythmGenerator
from .DataClasses import RhythemNoteEvent, NoteEvent
from .Dictionaries import beat_to_note_divisions
from .Utilities import division_to_dt

class PolyRhythms(RhythmGenerator):

    def __init__(self, tempo):
        super().__init__(tempo=tempo)

    def create_polyrhythm(self, ratio: str, multiplicity: int):
        if ratio.split(":")[-1] == "1":
            [self.create_n_1_polyrhythm(n=int(ratio.split(":")[0])) for _ in range(multiplicity)]
        if ratio == "3:2":
            [self.create_3_2_polyrhythm(m=3, n=2) for _ in range(multiplicity)]

    def create_n_1_polyrhythm(self, n: int, rhythem_note_events: list[list[RhythemNoteEvent]], initial_offset: int, multiplicity: int):
        assert(n==len(rhythem_note_events)-1)
        for _ in range(multiplicity):
            division = beat_to_note_divisions[n]
            initial_offset = self.get_offset(index=-1)
            for i in range(len(rhythem_note_events[0])):
                rhythem_note_events[0][i] = RhythemNoteEvent(offset=initial_offset, division="ZERO", note=rhythem_note_events[0][i].note, 
                                                            status=rhythem_note_events[0][i].status, velocity=85, tempo=self.tempo)
            self.add_events_with_duration(rhythem_note_events=rhythem_note_events[0], duration_divisions=["WHOLE"]*len(rhythem_note_events[0]))

            for i in range(len(rhythem_note_events[1])):
                rhythem_note_events[1][i] = RhythemNoteEvent(offset=initial_offset, division="ZERO", note=rhythem_note_events[1][i].note, 
                                                            status=rhythem_note_events[1][i].status, velocity=85, tempo=self.tempo)
            self.add_events_with_duration(rhythem_note_events=rhythem_note_events[1], duration_divisions=[division]*len(rhythem_note_events[1]))

            for i in range(2, len(rhythem_note_events)):
                for j in range(len(rhythem_note_events[i])):
                    rhythem_note_events[i][j].absolute_time = self.midi_scheduler.events[-1].dt
                self.add_events_with_duration(rhythem_note_events=rhythem_note_events[i], duration_divisions=[division]*len(rhythem_note_events[i]))

    def create_3_2_polyrhythm(self, m: int, n: int):
        triplet_note_on = RhythemNoteEvent(division="ZERO", note="D\u266d6", status="NOTE_ON", velocity=85)
        quarter_note_on = RhythemNoteEvent(division="ZERO", note="A5", status="NOTE_ON", velocity=85)
        triplet_note_off = RhythemNoteEvent(division="TRIPLET_QUARTER", note="D\u266d6", status="NOTE_OFF", velocity=85)
        triplet_note2_off = RhythemNoteEvent(division="EIGHTH", note="D\u266d6", status="NOTE_OFF", velocity=85)
        quarter_note_off = RhythemNoteEvent(division="TRIPLET_SIXTEENTH", note="A5", status="NOTE_OFF", velocity=85)
        quarter_note2_off = RhythemNoteEvent(division="ZERO", note="A5", status="NOTE_OFF", velocity=85)


        note_list = [triplet_note_on, quarter_note_on, triplet_note_off, 
                     triplet_note_on, quarter_note_off]
        
        self.add_events(rhythem_note_events=note_list)

if __name__ == "__main__":
    tempo = 120
    polyrhythms = PolyRhythms(tempo=tempo)
    polyrhythms.add_event(rhythem_note_event=RhythemNoteEvent(offset=0, division="ZERO", note="C1", status="NOTE_OFF", velocity=85, tempo=polyrhythms.tempo))
    polyrhythms.add_events_with_duration(rhythem_note_events=
                                         [RhythemNoteEvent(offset=-1, division="ZERO", note="C4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]*56,
                                          duration_divisions=["QUARTER"]*56)
    
    polyrhythms.stage()

    for _ in range(2):
        polyrhythms.create_n_1_polyrhythm(n=2, 
            rhythem_note_events=[[RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythemNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
            initial_offset=0, 
            multiplicity=1)
        
        polyrhythms.create_n_1_polyrhythm(n=3, 
            rhythem_note_events=[[RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythemNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                    RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                    RhythemNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
            initial_offset=0, 
            multiplicity=1)
        polyrhythms.create_n_1_polyrhythm(n=4, 
            rhythem_note_events=[[RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                 RhythemNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
            initial_offset=0, 
            multiplicity=1)
        polyrhythms.create_n_1_polyrhythm(n=5, 
            rhythem_note_events=[[RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                 RhythemNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="A\u266d4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
            initial_offset=0, 
            multiplicity=1)
        polyrhythms.create_n_1_polyrhythm(n=6, 
            rhythem_note_events=[[RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                 RhythemNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="A5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="A\u266d4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
            initial_offset=0, 
            multiplicity=1)
        
        polyrhythms.create_n_1_polyrhythm(n=7, 
            rhythem_note_events=[[RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                 RhythemNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="A5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="A\u266d4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
            initial_offset=0, 
            multiplicity=1)
        polyrhythms.create_n_1_polyrhythm(n=8, 
            rhythem_note_events=[[RhythemNoteEvent(offset=0, division="ZERO", note="C6", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="D5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="A5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                 RhythemNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="A\u266d4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="D5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="F4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="D5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                                [RhythemNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="D4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                 RhythemNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
            initial_offset=0, 
            multiplicity=1)
        
    polyrhythms.stage()
    polyrhythms.pop_stash()   
    polyrhythms.midi_scheduler.sort_events_by_dt(relative=True)
    polyrhythms.midi_scheduler.schedule_events(initial_delay=1000)
