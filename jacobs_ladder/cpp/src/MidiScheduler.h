#ifndef MIDI_SCHEDULER_H
#define MIDI_SCHEDULER_H

// Project Includes
#include "Constants.h"
#include "MidiDefinitions.h"
#include "QpcUtils.h"
#include "rtmidi/RtMidi.h"

// System Includes
#include <random>
#include <queue>
#include <vector>
#include <memory>
#include <atomic>
#include <thread>
#include <mutex>
#include <condition_variable>

class MidiScheduler {
public:
    MidiScheduler(const std::string& outputPortName, bool startImmediately = true,  bool printMsgs = false);
    ~MidiScheduler();

    /**
     * @brief Add a singular MidiEvent to the schedule
     * 
     * @param event a MidiEvent struct to be scheduled
     */
    void addEvent(const Midi::MidiEvent &event);

    /**
     * @brief Add a singular MidiEvent to the schedule offset by some number of qpc ticks
     * 
     * @param event a MidiEvent struct to be scheduled
     * @param offsetTicks an offset in ticks to be added to event.qpcTime
     */
    void addEvent(Midi::MidiEvent &event, long long offsetTicks);

    /**
     * @brief Add a singular NoteEvent to the schedule which adds both the NOTE_ON and NOTE_OFF events separated by some duration
     * 
     * @param noteEvent a NoteEvent struct to be scheduled
     */
    void addEvent(Midi::NoteEvent &noteEvent);

    /**
     * @brief Add a singular NoteEvent to the schedule which adds both the NOTE_ON and NOTE_OFF events separated by some duration whose entire sequence can be separated by some offset in terms of beats (i.e quarter note, eigth note, etc.)
     * 
     * @param noteEvent a NoteEvent struct to be scheduled
     * @param offsetBeats an offset in terms of beats which gets converted to ticks and added to noteEvent.event.qpcTime
     */
    void addEvent(Midi::NoteEvent &noteEvent, Midi::NoteDuration offsetBeats);

    /**
     * @brief Add multiple MidiEvents to the schedule
     * 
     * @param events a vector of MidiEvents to be scheduled
     */
    void addEvents(const std::vector<Midi::MidiEvent> &events);

    /**
     * @brief Add multiple MidiEvents to the schedule offset by some number of qpc ticks
     * 
     * @param events a vector of MidiEvents to be scheduled
     * @param offsetTicks an offset in ticks to be added to each event's qpcTime member
     */
    void addEvents(std::vector<Midi::MidiEvent> &events, long long offsetTicks);

    /**
     * @brief Add multiple NoteEvents to the schedule which adds both the NOTE_ON and NOTE_OFF events for each NoteEvent separated by some duration
     * 
     * @param noteEvents a vector of NoteEvent structs to be scheduled
     */
    void addEvents(std::vector<Midi::NoteEvent> &noteEvents);

    /**
     * @brief Add multiple NoteEvents to the schedule which adds both the NOTE_ON and NOTE_OFF events for each NoteEvent separated by some duration whose entire sequence can be separated by some offset in terms of beats (i.e. quarter note, eighth note, etc.)
     * 
     * @param noteEvents a vector of NoteEvent structs to be scheduled
     * @param offsetBeats an offset in terms of beats which gets converted to ticks and added to noteEvent.event.qpcTime
     */
    void addEvents(std::vector<Midi::NoteEvent> &noteEvents, Midi::NoteDuration offsetBeats);

    /**
     * @brief A mechanism for sending the all notes off control change midi message which silences all currently played notes.
     */
    void allNotesOff();

    /**
     * @brief Get the tick time of the previously scheduled MidiEvent (usually NOTE_ON or NOTE_OFF). Often used as a future offset point for creating new sequences of MidiEvents or NoteEvents.
     * 
     * @return long long the qpc tick time of the previously scheduled note
     */
    long long getPreviouslyScheduledNoteQpcTimeTicks();

    /**
     * @brief Pause the player thread from playing and interrupt any currently played notes with allNotesOff() 
     * 
     */
    void pause();

    /**
     * @brief Resume the player thread without preserving notes which have already passed their scheduled time only playing previously scheduled notes which are still scheduled for the future
     */
    void resume();

    /**
     * @brief Used to start the player thread if it is not already running. Useful when using startImmediately=false in the constructor allowing the user to decide when they want to start the player thread.
     * 
     * @return true If the player thread was successfully started because it was not previously running
     * @return false If the player thread was unsuccessfully started because it was already running and does not need to be started again.
     */
    bool start();

    /**
     * @brief Stops the player thread and empties mQueue. Useful for conserving resources during times when the player thread is not needed for prolonged periods of time.
     */
    void stop();

private:
    std::atomic<bool> mRunning {false};
    std::atomic<bool> mPaused {false};
    std::atomic<bool> mPrintMsgs {false};

    std::thread mPlayerThread;
    std::mutex mPauseMutex;
    std::mutex mBufferMutex;
    std::mutex mPreviouslyScheduledNoteQpcTimeMutex;
    std::condition_variable mPauseCv;

    std::priority_queue<Midi::MidiEvent> mQueue;
    std::priority_queue<Midi::MidiEvent> mBuffer;

    std::unique_ptr<QpcUtils> mTimer;
    std::unique_ptr<RtMidiOut> mMidiOut;
    long long mFrequencyHz {QPC_FREQUENCY};
    const long long mBudgetTicks {TEN_MILLISECOND_BUDGET_TICKS};
    long long mPreviouslyScheduledNoteQpcTime {0}; 

    std::mt19937 mGen;
    std::uniform_int_distribution<> mDist;

    /**
     * @brief Pause the player thread using a condition variable only if both mRunning and mPause are true, otherwise continue execution.
     */
    void conditionallyPause();

    /**
     * @brief Get the note duration in terms of future qpc ticks by extracting the tempo/division adjusted note duration.
     * 
     * To adjust the duration in terms of tempo the formula: tempo_adjusted_duration = ((duration * (60 / tempo)) / MS_TO_SEC_CONVERSION) * QPC_FREQUENCY ; is used.
     * To adjust the duration in terms of division the formula: division_adjusted_duration = tempo_adjusted_duration * division; where, (0 < division < 1) scales the duration by how staccato or legato the rhythem is played for within it's allotted time cell.
     * The scheduledTimeTicks are also conditionally set to mPreviouslyScheduledNoteQpcTime iff they have a negative value passed in (chaining). This is a feature where notes may optionally be scheduled in terms of the previous note for convenience.
     * 
     * @param noteEvent A noteEvent whose event member variables need to be adjusted in light of tempo, division, and scheduledTimeTicks
     * @return long long 
     */
    long long getNoteDurationTicks(Midi::NoteEvent &noteEvent);

    /**
     * @brief Get the a random tick offset between -1000 and 1000 ticks for separating out notes in time by a few hundred nanoseconds so the Midi processor is able to distinguish between simultaneously occurring NOTE_OFF events
     * 
     * Note that this decision was made based on the fact that the threshold for human hearing is around 10 ms latency. 
     * So long as the difference in timing is somewhere between plus or minus 10 ms, there will be an imperceptible difference in timing, where hundreds of nanoseconds is well below this threshold and still has good Midi processor performance.
     * 
     * @return long long a ticks offset between -1000 and 1000
     */
    long long getRandomOffset();

    /**
     * @brief The player thread, responsible for reacting to scheduled notes, and playing them in terms of min priority (i.e whichever note(s) is meant to be played soonest in the future)
     * 
     */
    void player();

    /**
     * @brief Sets the mPreviouslyScheduledNoteQpcTime to 0 which enforces that a runtime exception will be thrown if chaining is attempted before providing a fully time defined MidiEvent or NoteEvent as a reference point
     * 
     * This method is used by the player thread to reset to starting conditions whenever all of the scheduled notes have been either played or exhausted.
     * This ensures that chaining is never used on the first note which is scheduled.
     * 
     */
    void resetPreviouslyScheduledNoteQpcTime();

    /**
     * @brief Pushes notes to the queue when the player thread is smart sleeping, optimizing scheduling to when notes are not being played
     * 
     * This is different from addEvent which adds MidiEvents to mBuffer.
     * This method pops events off of mBuffer and adds them to mQueue (the actual queue used for playing notes).
     * Therefore it is safe to say that all actual scheduling takes place at the discretion of the player thread, and addEvents really only serves to 
     * inform the player thread of future notes it would like the player thread to play. This ensures that priority lies with playing over scheduling since scheduling is less time sensitive.
     * 
     * @param event a MidiEvent to be popped from the buffer and added to mQueue
     * @return true If the event to be added is in the future plus a ten millisecond budget (human perception range where it sounds no different than the originally scheduled time)
     * @return false If the event to be added is outside the scheduled time plus its ten millisecond budget and is therefore in the past. Results in the note getting dropped.
     */
    bool scheduleEvent(Midi::MidiEvent event);

    /**
     * @brief Continues to pop events from mBuffer adding them to mQueue until either the scheduled time minus mBudget (10 ms) has passed, or there are no more events in mBuffer to be added to mQueue.
     * 
     * The amount of time slept for is non-deterministic and is based on the number of MidiEvents in mBuffer.
     * This is by design as this is meant to be a kind of course sleep used to do useful work until we are within 10 ms the scheduled play time
     * The last 10 ms are handled with a kind of fine time wait until function which is outside the scope of this function's per view
     * If it exits early there is another mechanism for coarse sleeping in the fine time wait until function if needed
     * 
     * @param qpcTime The scheduled qpc time in ticks to sleep for 
     */
    void smartSleep(long long qpcTime);

};


#endif // MIDI_SCHEDULER_H
