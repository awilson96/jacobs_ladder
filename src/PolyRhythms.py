from .RhythmGenerator import RhythmGenerator
from .DataClasses import RhythmNoteEvent, NoteEvent
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

    def create_n_1_polyrhythm(self, n: int, rhythem_note_events: list[list[RhythmNoteEvent]], initial_offset: int, multiplicity: int):
        assert(n==len(rhythem_note_events)-1)
        for _ in range(multiplicity):
            division = beat_to_note_divisions[n]
            for i in range(len(rhythem_note_events[0])):
                rhythem_note_events[0][i] = RhythmNoteEvent(offset=initial_offset, division="ZERO", note=rhythem_note_events[0][i].note, 
                                                            status=rhythem_note_events[0][i].status, velocity=85, tempo=self.tempo)
            self.add_events_with_duration(rhythem_note_events=rhythem_note_events[0], duration_divisions=["WHOLE"]*len(rhythem_note_events[0]))

            for i in range(len(rhythem_note_events[1])):
                rhythem_note_events[1][i] = RhythmNoteEvent(offset=initial_offset, division="ZERO", note=rhythem_note_events[1][i].note, 
                                                            status=rhythem_note_events[1][i].status, velocity=85, tempo=self.tempo)
            self.add_events_with_duration(rhythem_note_events=rhythem_note_events[1], duration_divisions=[division]*len(rhythem_note_events[1]))

            for i in range(2, len(rhythem_note_events)):
                for j in range(len(rhythem_note_events[i])):
                    rhythem_note_events[i][j].absolute_time = self.midi_scheduler.events[-1].dt
                self.add_events_with_duration(rhythem_note_events=rhythem_note_events[i], duration_divisions=[division]*len(rhythem_note_events[i]))

            initial_offset += division_to_dt(division="WHOLE", tempo=self.tempo)

    def create_m_n_polyrhythm(self, m: int, n: int, m_rhythem_note_events: list[list[RhythmNoteEvent]], n_rhythem_note_events: list[list[RhythmNoteEvent]], 
                              initial_offset: int, multiplicity: int):
        assert(m==len(m_rhythem_note_events)-1)
        assert(n==len(n_rhythem_note_events)-1)
        self.create_n_1_polyrhythm(n=m, rhythem_note_events=m_rhythem_note_events, initial_offset=initial_offset, multiplicity=multiplicity)
        self.create_n_1_polyrhythm(n=n, rhythem_note_events=n_rhythem_note_events, initial_offset=initial_offset, multiplicity=multiplicity)

if __name__ == "__main__":
    tempo = 120
    polyrhythms = PolyRhythms(tempo=tempo)
    polyrhythms.add_event(rhythem_note_event=RhythmNoteEvent(offset=0, division="ZERO", note="C1", status="NOTE_OFF", velocity=85, tempo=polyrhythms.tempo))
    polyrhythms.add_events_with_duration(rhythem_note_events=
                                         [RhythmNoteEvent(offset=-1, division="ZERO", note="C4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]*28,
                                          duration_divisions=["QUARTER"]*28)
    
    polyrhythms.stage_all()

    polyrhythms.create_n_1_polyrhythm(n=2, 
        rhythem_note_events=[[RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                            RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                            RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                            RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
        initial_offset=0, 
        multiplicity=1)
    
    offset = polyrhythms.get_offset(index=-1)
    polyrhythms.create_n_1_polyrhythm(n=3, 
        rhythem_note_events=[[RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                            RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                            RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                            RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
        initial_offset=offset, 
        multiplicity=1)
    
    offset = polyrhythms.get_offset(index=-1)
    polyrhythms.create_n_1_polyrhythm(n=4, 
        rhythem_note_events=[[RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
        initial_offset=offset, 
        multiplicity=1)
    
    offset = polyrhythms.get_offset(index=-1)
    polyrhythms.create_n_1_polyrhythm(n=5, 
        rhythem_note_events=[[RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="A\u266d4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
        initial_offset=offset, 
        multiplicity=1)
    
    offset = polyrhythms.get_offset(index=-1)
    polyrhythms.create_n_1_polyrhythm(n=6, 
        rhythem_note_events=[[RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="A5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="A\u266d4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
        initial_offset=offset, 
        multiplicity=1)
    
    offset = polyrhythms.get_offset(index=-1)
    polyrhythms.create_n_1_polyrhythm(n=7, 
        rhythem_note_events=[[RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="A5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="A\u266d4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
        initial_offset=offset, 
        multiplicity=1)
    
    offset = polyrhythms.get_offset(index=-1)
    polyrhythms.create_n_1_polyrhythm(n=8, 
        rhythem_note_events=[[RhythmNoteEvent(offset=0, division="ZERO", note="C6", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)], 
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="D5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="A5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="A\u266d4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="D5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="A4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="F4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="D5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                            [RhythmNoteEvent(offset=0, division="ZERO", note="G4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="D4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo), 
                                RhythmNoteEvent(offset=0, division="ZERO", note="B4", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
        initial_offset=offset, 
        multiplicity=1)
    
    offset = polyrhythms.get_offset(index=-1)
    polyrhythms.create_n_1_polyrhythm(n=7, rhythem_note_events=
        [[],
         [RhythmNoteEvent(offset=0, division="ZERO", note="C6", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
         [RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
         [RhythmNoteEvent(offset=0, division="ZERO", note="A5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
         [RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
         [RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
         [RhythmNoteEvent(offset=0, division="ZERO", note="D5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
         [RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
         initial_offset=offset,
         multiplicity=4)
    
    polyrhythms.create_n_1_polyrhythm(n=3, rhythem_note_events=
        [[],
         [RhythmNoteEvent(offset=0, division="ZERO", note="C3", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
         [RhythmNoteEvent(offset=0, division="ZERO", note="E3", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
         [RhythmNoteEvent(offset=0, division="ZERO", note="G3", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
         initial_offset=offset,
         multiplicity=4)
    
    offset = polyrhythms.get_offset(index=-1)
    polyrhythms.create_m_n_polyrhythm(m=5, n=2, 
        m_rhythem_note_events=[[],
                               [RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                               RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                               [RhythmNoteEvent(offset=0, division="ZERO", note="D5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                               RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                               [RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                               RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                               [RhythmNoteEvent(offset=0, division="ZERO", note="E5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                               RhythmNoteEvent(offset=0, division="ZERO", note="G5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                               [RhythmNoteEvent(offset=0, division="ZERO", note="D5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                               RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
        n_rhythem_note_events=[[],
                               [RhythmNoteEvent(offset=0, division="ZERO", note="C5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)],
                               [RhythmNoteEvent(offset=0, division="ZERO", note="F5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo),
                                RhythmNoteEvent(offset=0, division="ZERO", note="A5", status="NOTE_ON", velocity=85, tempo=polyrhythms.tempo)]],
        initial_offset=offset,
        multiplicity=2)
    
    polyrhythms.pop_stash()

    for event in polyrhythms.midi_scheduler.events:
        print(event)
      
    polyrhythms.midi_scheduler.sort_events_by_dt(relative=True, stash=False)
    polyrhythms.midi_scheduler.schedule_events(initial_delay=1000)
