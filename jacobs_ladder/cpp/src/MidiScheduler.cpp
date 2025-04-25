// Project includes
#include "MidiScheduler.h"
#include "MidiUtils.h"
#include "MathUtils.h"

// System includes
#include <cstdlib>
#include <stdexcept>

MidiScheduler::MidiScheduler(const std::string& outputPortName, bool startImmediately, bool printMsgs)
    : mGen(std::random_device{}()),
      mDist(-10000, 10000)
    {
    mTimer = std::make_unique<QpcUtils>();
    mFrequencyHz = mTimer->qpcGetFrequency();
    mPrintMsgs.store(printMsgs);
    if (mPrintMsgs.load()) {
        std::cout << "\n";
    }
    try {
        mMidiOut = std::make_unique<RtMidiOut>();

        unsigned int portCount = mMidiOut->getPortCount();
        bool portFound = false;

        for (unsigned int i = 0; i < portCount; ++i) {
            std::string rawName = mMidiOut->getPortName(i);
            std::string normalizedName = normalizePortName(rawName);
            if (mPrintMsgs.load())
                std::cout << "MIDI output port " << i << ": " << normalizedName << "\n";
            if (normalizedName == outputPortName) {
                mMidiOut->openPort(i);
                if (mPrintMsgs.load())
                    std::cout << "\nOpened MIDI output port: " << normalizedName << "\n";
                portFound = true;
                break;
            }
        }

        if (!portFound) {
            throw std::runtime_error("Could not find MIDI output port: " + outputPortName);
        }
        if (startImmediately) {
            mRunning.store(true);
            mPlayerThread = std::thread(&MidiScheduler::player, this);
        }

    } catch (const RtMidiError& error) {
        std::cerr << "Error opening MIDI output port: " << error.getMessage() << "\n";
        throw;
    } catch (const std::exception& e) {
        std::cerr << "Exception: " << e.what() << "\n";
        throw;
    }
}

MidiScheduler::~MidiScheduler() {
    // Stop the player() thread and wait for it to join
    stop();
    if (mPlayerThread.joinable())
        mPlayerThread.join();

    // Close all open Midi ports
    mMidiOut->closePort();
}

void MidiScheduler::addEvent(const Midi::MidiEvent &event) {
    std::lock_guard<std::mutex> lock(mBufferMutex);
    mBuffer.push(event);
}

void MidiScheduler::addEvent(Midi::MidiEvent &event, long long offsetTicks) {
    std::lock_guard<std::mutex> lock(mBufferMutex);
    event.qpcTime += offsetTicks;
    mBuffer.push(event);
}

void MidiScheduler::addEvent(Midi::NoteEvent &noteEvent) {
    long long beatTicks = getBeatTicks(noteEvent);
    Midi::MidiEvent noteOff = Midi::MidiEvent(noteEvent.event, beatTicks);

    addEvent(noteEvent.event);
    addEvent(noteOff);
}

void MidiScheduler::addEvent(Midi::NoteEvent &noteEvent, Midi::Beats offsetBeats) {
    long long adjustedOffsetQpcTicks = beatsToQpcTicks(noteEvent, offsetBeats);
    noteEvent.event.qpcTime += adjustedOffsetQpcTicks;
    long long beatTicksTicks = getBeatTicks(noteEvent);
    Midi::MidiEvent noteOff = Midi::MidiEvent(noteEvent.event, beatTicksTicks);

    addEvent(noteEvent.event);
    addEvent(noteOff);
}

void MidiScheduler::addEvents(const std::vector<Midi::MidiEvent> &events) {
    for (const auto &event : events) {
        std::lock_guard<std::mutex> lock(mBufferMutex);
        mBuffer.push(event);
    }
}

void MidiScheduler::addEvents(std::vector<Midi::MidiEvent> &events, long long offsetTicks) {
    for (auto &event : events) {
        std::lock_guard<std::mutex> lock(mBufferMutex);
        event.qpcTime += offsetTicks;
        mBuffer.push(event);
    }
}

void MidiScheduler::addEvents(std::vector<Midi::NoteEvent> &noteEvents) {
    for (auto &event : noteEvents) {
        addEvent(event);
    }
}

void MidiScheduler::addEvents(std::vector<Midi::NoteEvent> &noteEvents, Midi::Beats offsetBeats) {
    for (auto &noteEvent : noteEvents) {
        long long adjustedOffsetQpcTicks = beatsToQpcTicks(noteEvent, offsetBeats);
        noteEvent.event.qpcTime += adjustedOffsetQpcTicks;
        long long beatTicksTicks = getBeatTicks(noteEvent);
        Midi::MidiEvent noteOff = Midi::MidiEvent(noteEvent.event, beatTicksTicks);

        addEvent(noteEvent.event);
        addEvent(noteOff);
    }
}

void MidiScheduler::allNotesOff() {
    Midi::MidiEvent allNotesOff = 
        Midi::MidiEvent(
            Midi::MidiMessageType::CONTROL_CHANGE,
            ALL_NOTES_OFF,
            VALUE_OFF,
            VALUE_OFF
        );
    std::vector<unsigned char> message = { 
        static_cast<unsigned char>(allNotesOff.status),
        static_cast<unsigned char>(allNotesOff.note),
        static_cast<unsigned char>(allNotesOff.velocity) 
    };
    mTimer->qpcSleepMs(100);
    mMidiOut->sendMessage(&message);
}

long long MidiScheduler::getPreviouslyScheduledNoteQpcTimeTicks() {
    std::lock_guard<std::mutex> lock(mPreviouslyScheduledNoteQpcTimeMutex);
    return mPreviouslyScheduledNoteQpcTime;
}

void MidiScheduler::pause() {
    std::cout << "pausing..." << std::endl;
    mPaused.store(true);
    allNotesOff();
}

void MidiScheduler::resume() {
    std::cout << "resuming..." << std::endl; 
    {
        std::lock_guard<std::mutex> lock(mPauseMutex);
        mPaused.store(false);
    }
    mPauseCv.notify_one();
}

bool MidiScheduler::start() {
    if (mPlayerThread.joinable())
        return false;
    
    mRunning.store(true);
    mPlayerThread = std::thread(&MidiScheduler::player, this);
    return true;
}

void MidiScheduler::stop() {
    mRunning.store(false);
    mPauseCv.notify_all();
    std::priority_queue<Midi::MidiEvent> empty;
    mQueue.swap(empty);
}

long long MidiScheduler::beatsToQpcTicks(Midi::NoteEvent noteEvent, Midi::Beats offsetBeats) {
    long long adjustedOffsetMs = MathUtils::FpFloor<long long>(static_cast<long long>(offsetBeats) * (60.0 / noteEvent.tempo));
    long long adjustedOffsetQpcTicks = MathUtils::FpFloor<long long>((adjustedOffsetMs / MS_TO_SEC_CONVERSION_FACTOR) * mFrequencyHz);
    return adjustedOffsetQpcTicks;
}

void MidiScheduler::conditionallyPause() {
    std::unique_lock<std::mutex> lock(mPauseMutex);
    mPauseCv.wait(lock, [this]() { return !mPaused.load() || !mRunning.load(); });
    return;
}

long long MidiScheduler::getRandomOffset() {
    return static_cast<long long>(mDist(mGen));
}

void MidiScheduler::player() {
    while (mRunning.load()) {

        // If the user has invoked pause(), conditionally pause until they call resume(). Breaks out of pause if stop() is called or if mRunning becomes false.
        conditionallyPause();

        // If the queue is empty reset the previously scheduled note to 0 (i.e. impose the requirement that a qpcTime must be provided and chaining is not allowed)
        if (mQueue.empty()) {
            std::lock_guard<std::mutex> lock(mBufferMutex);
            // If the buffer is empty simply keep looping until the buffer has some notes to add to the queue
            if (mBuffer.empty()) {
                resetPreviouslyScheduledNoteQpcTime();
                continue;
            }
            
            // If the buffer is not empty and scheduling is successful then append the top item off the priority buffer and add it to mQueue
            // Otherwise pop items until there is an event that is actually scheduled for the future
            while(!mBuffer.empty()) {
                Midi::MidiEvent top = mBuffer.top();
                if (scheduleEvent(mBuffer.top())) {
                    mBuffer.pop();
                    break;
                } 
                else {
                    mBuffer.pop();
                }
            }

            // If the queue is still empty after attempting to schedule events just loop
            if (mQueue.empty()) {
                continue;
            }
        }

        // If we have neither been told to pause or stop and the queue is not empty then process the soonest MidiEvent 
        // and query the performance counter for the current time
        Midi::MidiEvent event = mQueue.top();
        mQueue.pop();
        long long currentTime = mTimer->qpcGetTicks();

        // If the currentTime is 10 ms or more behind schedule then just move on without playing it
        if (currentTime > event.qpcTime + mBudgetTicks) {
            continue;
        } 
        // If the currentTime is somewhere between the scheduled time and 10 ms behind then play it immediately
        else if (currentTime > event.qpcTime && currentTime <= event.qpcTime + mBudgetTicks) {
            std::vector<unsigned char> message = { static_cast<unsigned char>(event.status),
                static_cast<unsigned char>(event.note),
                static_cast<unsigned char>(event.velocity) };
            mMidiOut->sendMessage(&message);
        }
        
        // Helpful printout for debugging
        if (mPrintMsgs.load()) {
            std::cout << "Midi Event: \n"
                  << "Status: "   << static_cast<int>(event.status)   << "\n"
                  << "Note: "     << (int)event.note                  << "\n"
                  << "Velocity: " << (int)event.velocity              << "\n"
                  << "Time: "     << event.qpcTime                    << "\n\n";
        }
        
        // Smart sleep adds MidiEvents to the priority queue while it is still within mBudgetTicks of the scheduled event time
        // This budget was calculated as approximately 5 times the benchmarked time it takes to run the scheduleEvent() on average.
        // (i.e. 250 ns * 5 = 1250 ns) 
        smartSleep(event.qpcTime);

        // This is effectively a high resolution wait_until function for windows 
        LARGE_INTEGER now;
        do {
            QueryPerformanceCounter(&now);
        } while (now.QuadPart < event.qpcTime);

        // Prepare and send the MIDI message after waiting until the scheduled time
        std::vector<unsigned char> message = { static_cast<unsigned char>(event.status),
                                               static_cast<unsigned char>(event.note),
                                               static_cast<unsigned char>(event.velocity) };
        mMidiOut->sendMessage(&message);
    }
}

void MidiScheduler::resetPreviouslyScheduledNoteQpcTime() {
    std::lock_guard<std::mutex> lock(mPreviouslyScheduledNoteQpcTimeMutex);
    mPreviouslyScheduledNoteQpcTime = 0;
}

long long MidiScheduler::getBeatTicks(Midi::NoteEvent &noteEvent) {
    std::lock_guard<std::mutex> lock(mPreviouslyScheduledNoteQpcTimeMutex);
    // If the previously scheduled note is equal 0 (i.e. either the buffer has been depleted or this is the first event being added to the queue after instantiation)
    // then throw an invalid argument exception if chaining is attempted (i.e. scheduledTimeTicks is less than 0)
    if (mPreviouslyScheduledNoteQpcTime == 0 && noteEvent.scheduledTimeTicks < 0) {
        throw std::invalid_argument("When the queue is empty the schedule time must be specified. Chaining is only valid when the queue size is non-zero.");
    }
    // If the scheduled time is less than 0, then chaining is assumed (i.e. the scheduleTime for the current message is equal to the previously scheduled end time)
    else if (noteEvent.scheduledTimeTicks < 0) {
        if (mPrintMsgs.load()) {
            std::cout << "Chaining..." << "\n";
        }  
        noteEvent.scheduledTimeTicks = mPreviouslyScheduledNoteQpcTime;
    }
 
    // Set the MidiEvent Qpc time to the scheduled time in both the case where it has been adjusted and when it has not
    noteEvent.event.qpcTime = noteEvent.scheduledTimeTicks + getRandomOffset();

    // This converts the duration in from a beat representation (i.e. quarter note) to a ms and QPC ticks representation 
    long long adjustedDurationMs = MathUtils::FpFloor<long long>(static_cast<long long>(noteEvent.duration) * (60.0 / noteEvent.tempo));
    long long adjustedDurationQpcTicks = MathUtils::FpFloor<long long>((adjustedDurationMs / MS_TO_SEC_CONVERSION_FACTOR) * mFrequencyHz);

    // The qpc ticks time marker get's placed at the tail of the currently scheduled note, i.e. if a quarter note is played at the beat where it is released (NOTE_OFF)
    // Note though that this may not be the actual length that the note way played for (beatTicks), but rather the length of time the note was meant to occupy symbolically (adjustedDurationQpcTicks, or in our previous example: a quarter note)
    mPreviouslyScheduledNoteQpcTime = noteEvent.scheduledTimeTicks + adjustedDurationQpcTicks;

    // std::cout << "mPreviouslyScheduledNoteQpcTime: " << mPreviouslyScheduledNoteQpcTime << std::endl;

    // This is the actual length of time between the NOTE_ON and NOTE_OFF messages in terms of QPC tics. By contrast the adjusted duration in ms is the time the note 
    // is meant to occupy in space in therms of beats (i.e. quarter note). This gives the following note a clean time aligned place to start from (the end of the previous 
    // note's adjustedDurationQpcTicks)
    long long beatTicks = MathUtils::FpFloor<long long>(noteEvent.division * adjustedDurationQpcTicks);
    return beatTicks; 
}

bool MidiScheduler::scheduleEvent(Midi::MidiEvent event) {
    if (event.qpcTime >= mTimer->qpcGetTicks() + mBudgetTicks) {
        mQueue.push(event);
        return true;
    }
    std::cout << "Warning: exceeded budget for event: " << static_cast<int>(event.note) << std::endl;
    return false;
}

void MidiScheduler::smartSleep(long long qpcTime) {
    LARGE_INTEGER now;
    std::lock_guard<std::mutex> lock(mBufferMutex);
    // Query the performance counter each cycle to determine the moment our time budget has run out 
    // and loop on the condition that we are within mBudgetTicks of the scheduled event time
    do {
        // While the buffer is not exhausted add events from the buffer to the priority queue, otherwise break out of the loop to transition to fine time waiting
        if (!mBuffer.empty()) {
            scheduleEvent(mBuffer.top());
            mBuffer.pop();
        }
        else {
            break;
        }
        QueryPerformanceCounter(&now);
    } while (now.QuadPart < qpcTime - mBudgetTicks);
}

