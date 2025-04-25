#include "MidiScheduler.h"
#include "MidiDefinitions.h"
#include "QpcUtils.h"


using namespace Midi;

int main(int argc, const char *argv[]) {

    MidiScheduler midiScheduler("jacob", true, true);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();
    long long oneSecondFromNow = timer.qpcGetFutureTime(now, 1000);

    // Seed note
    double tempo = 120.0;
    MidiEvent firstEvent = 
        MidiEvent(
            MidiMessageType::NOTE_ON,
            60,
            100,
            oneSecondFromNow
        );

    NoteEvent note = 
        NoteEvent(
            0.5, 
            Beats::QUARTER, 
            firstEvent,
            tempo,
            oneSecondFromNow
        );
    
    midiScheduler.addEvent(note);

    long long previouslyScheduledNoteQpcTime = midiScheduler.getPreviouslyScheduledNoteQpcTimeTicks();

    NoteEvent nextNote = NoteEvent(note);
    nextNote.event.note = 64u;
    nextNote.scheduledTimeTicks += 1;
    midiScheduler.addEvent(nextNote);

    NoteEvent finalNote = NoteEvent(nextNote);
    finalNote.event.note = 67u;
    finalNote.scheduledTimeTicks += 1;
    midiScheduler.addEvent(finalNote);

    

    for (uint16_t i = 0; i < 3; i++) {
        note.scheduledTimeTicks = previouslyScheduledNoteQpcTime;
        nextNote.scheduledTimeTicks = previouslyScheduledNoteQpcTime;
        finalNote.scheduledTimeTicks = previouslyScheduledNoteQpcTime;
        midiScheduler.addEvent(note);
        previouslyScheduledNoteQpcTime = midiScheduler.getPreviouslyScheduledNoteQpcTimeTicks();
        midiScheduler.addEvent(nextNote);
        midiScheduler.addEvent(finalNote);
    }

    timer.qpcSleepMs(4000);

    // midiScheduler.allNotesOff();
    // timer.qpcSleepMs(2000);

}