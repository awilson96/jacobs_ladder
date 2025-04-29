// Project includes
#include "MidiScheduler.h"
#include "MidiUtils.h"
#include "MathUtils.h"

// System includes
#include <cstdlib>
#include <stdexcept>

MidiScheduler::MidiScheduler(const std::string& outputPortName, bool startImmediately, bool printMsgs, int beatsPerMeasure, int beatUnit, double tempoBpm)
    : mGen(std::random_device{}()),
      mDist(-10000, 10000),
      mBeatsPerMeasure(beatsPerMeasure),
      mBeatUnit(beatUnit),
      mTempoBpm(tempoBpm)
    {
    mTimer = std::make_unique<QpcUtils>();
    mFrequencyHz = mTimer->qpcGetFrequency();
    mPrintMsgs.store(printMsgs);
    if (mPrintMsgs.load()) {
        std::cout << "\n";
    }
    try {

        // Always start the pre-calculation of 5 minutes of future beats 1000 ms from now in the future
        long long now = mTimer->qpcGetTicks();
        preCalculateBeats(mTimer->qpcGetFutureTime(now, 1000));
        // long long later = mTimer->qpcGetTicks();
        // std::cout << "pre-calculate beats time: \n" << mTimer->qpcPrintTimeDiffUs(now, later) << " us" << std::endl;

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
            if (start())
                std::cout << "Successfully started player..." << std::endl;
            else
                throw std::runtime_error("Unable to start MidiScheduler...");
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
    // Turn off all currently playing notes
    allNotesOff();
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

    if (beatTicks <= 0) {
        noteEvent.event.velocity = 0;
    }

    addEvent(noteEvent.event);
    addEvent(noteOff);
}

void MidiScheduler::addEvent(Midi::NoteEvent &noteEvent, Midi::Beats offsetBeats) {
    long long adjustedOffsetQpcTicks = beatsToQpcTicks(noteEvent, offsetBeats);
    noteEvent.event.qpcTime += adjustedOffsetQpcTicks;
    long long beatTicks = getBeatTicks(noteEvent);
    Midi::MidiEvent noteOff = Midi::MidiEvent(noteEvent.event, beatTicks);

    if (beatTicks <= 0) {
        noteEvent.event.status = Midi::MidiMessageType::NOTE_OFF;
    }

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

long long MidiScheduler::beatsToTicks(double tempo, Midi::Beats beat) {
    if (tempo < 0) { tempo = mTempoBpm.load(); }
    long long adjustedOffsetMs = MathUtils::FpFloor<long long>(static_cast<long long>(beat) * (60.0 / tempo));
    long long adjustedOffsetQpcTicks = MathUtils::FpFloor<long long>((adjustedOffsetMs / MS_TO_SEC_CONVERSION_FACTOR) * mFrequencyHz);
    return adjustedOffsetQpcTicks;
}

long long MidiScheduler::beatsToTicks(double tempo, std::vector<Midi::Beats> beats) {
    if (tempo < 0) { tempo = mTempoBpm.load(); }
    long long adjustedOffsetQpcTicks = 0;
    for (auto & beat : beats) {
        long long adjustedOffsetMs = MathUtils::FpFloor<long long>(static_cast<long long>(beat) * (60.0 / tempo));
        adjustedOffsetQpcTicks += MathUtils::FpFloor<long long>((adjustedOffsetMs / MS_TO_SEC_CONVERSION_FACTOR) * mFrequencyHz);
    }
    
    return adjustedOffsetQpcTicks;
}

void MidiScheduler::changeTempo(double tempo, long long startQpcTime) {
    if (tempo <= 0) {
        throw std::runtime_error("Tempo must be greater than 0!");
    }
    mTempoScalingFactor.store(mTempoBpm.load() / tempo);
    mTempoBpm.store(tempo);
    mTempoChange.store(true);
    preCalculateBeats(startQpcTime);
}

std::vector<std::pair<long long, int>> MidiScheduler::getBeatSchedule() {
    std::lock_guard<std::mutex> lock(mBeatScheduleMutex);
    return mBeatSchedule;
}

long long MidiScheduler::getNextBeatByNumber(size_t beatNum, size_t measureNum) {
    int beatIndex = 0;
    int measureIndex = -1;
    std::pair<long long, int> beat = getBeatFromIndex(beatIndex);

    // If a beat was not successfully retrieved due to that beat having already passed
    while (beat.first == 0 && beat.second == 0) {
        beat = getBeatFromIndex(++beatIndex);
    }

    do {
        while (beat.second != beatNum) {
            beat = getBeatFromIndex(++beatIndex);
            if (beat.second == beatNum) {
                measureIndex++;
            }
        }
        if (measureNum != measureIndex) {
            beat = getBeatFromIndex(++beatIndex);
        }
    } while (measureNum != measureIndex);
    
    if (beat.second == beatNum) {
        return beat.first;
    }
    else {
        throw std::runtime_error("Beat index was incorrectly calculated.");
    }
}

long long MidiScheduler::getPreviouslyScheduledNoteQpcTimeTicks() {
    std::lock_guard<std::mutex> lock(mPreviouslyScheduledNoteQpcTimeMutex);
    return mPreviouslyScheduledNoteQpcTime;
}

double MidiScheduler::getTempo() {
    return mTempoBpm.load();
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

long long MidiScheduler::beatsToQpcTicks(Midi::NoteEvent &noteEvent, Midi::Beats offsetBeats) {
    if (noteEvent.tempo < 0) { noteEvent.tempo = mTempoBpm.load(); }
    long long adjustedOffsetMs = MathUtils::FpFloor<long long>(static_cast<long long>(offsetBeats) * (60.0 / noteEvent.tempo));
    long long adjustedOffsetQpcTicks = MathUtils::FpFloor<long long>((adjustedOffsetMs / MS_TO_SEC_CONVERSION_FACTOR) * mFrequencyHz);
    return adjustedOffsetQpcTicks;
}

void MidiScheduler::conditionallyPause() {
    std::unique_lock<std::mutex> lock(mPauseMutex);
    mPauseCv.wait(lock, [this]() { return !mPaused.load() || !mRunning.load(); });
    return;
}

size_t MidiScheduler::changeBeatLengthsIncrementally(size_t startIndex, long long qpcTime) {
    LARGE_INTEGER now;
    QueryPerformanceCounter(&now);

    std::priority_queue<Midi::MidiEvent> tempQueue = mQueue;
    size_t index = startIndex;
    Midi::MidiEvent previousQueueEvent;
    Midi::MidiEvent previousSwapQueueEvent;
    size_t queueSize = mQueue.size(); 
    while (tempQueue.size() > 0) {
        Midi::MidiEvent event = tempQueue.top();
        Midi::MidiEvent eventCopy = event;
        tempQueue.pop();
        if (index != startIndex) {
            long long timeDiff = event.qpcTime - previousQueueEvent.qpcTime;
            long long scaledTimeDiff = static_cast<long long>(mTempoScalingFactor.load() * timeDiff);
            event.qpcTime = previousSwapQueueEvent.qpcTime + scaledTimeDiff;
        }
        previousQueueEvent = eventCopy;
        previousSwapQueueEvent = event;
        mSwapQueue.push(event);
        ++index;

        QueryPerformanceCounter(&now);
        if (now.QuadPart > qpcTime - mBudgetTicks) {
            break; 
        }
        else if (mSwapQueue.size() >= queueSize && tempQueue.empty()) {
            std::cout << "Finished adjusting tempo for scheduled notes..." << std::endl;
            mQueue.swap(mSwapQueue);
            mSwapQueue.swap(std::priority_queue<Midi::MidiEvent>());
            mTempoChangeIndex.store(0);
            mTempoChange.store(false);
            break;
        }
    }
    return index; 
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

void MidiScheduler::preCalculateBeats(long long startQpcTime) {
    std::lock_guard<std::mutex> lock(mBeatScheduleMutex);
    mBeatSchedule.clear();
    double secondsPerBeat = 60.0 / mTempoBpm.load();
    long long qpcTicksPerBeat = static_cast<long long>(secondsPerBeat * mFrequencyHz);

    long long currentQpcTime = startQpcTime;
    int beatNumber = 1;
    
    while (currentQpcTime - startQpcTime < FIVE_MINUTES_TICKS) {
        mBeatSchedule.emplace_back(currentQpcTime, beatNumber);

        currentQpcTime += qpcTicksPerBeat;
        beatNumber++;
        if (beatNumber > mBeatUnit) {
            beatNumber = 1;
        }
    }
}

void MidiScheduler::pruneExpiredBeatsIncrementally(long long qpcTime) {
    LARGE_INTEGER now;
    QueryPerformanceCounter(&now);

    double secondsPerBeat = 60.0 / mTempoBpm.load();
    long long qpcTicksPerBeat = static_cast<long long>(secondsPerBeat * mFrequencyHz);

    std::lock_guard<std::mutex> lock(mBeatScheduleMutex);
    while (mBeatSchedule.at(0).first < now.QuadPart) {
        mBeatSchedule.erase(mBeatSchedule.begin());
        std::pair<long long, int> last = mBeatSchedule.back();

        long long newQpcTime = last.first + qpcTicksPerBeat;
        int newBeatNumber = last.second + 1;
        if (newBeatNumber > mBeatsPerMeasure) {
            newBeatNumber = 1;
        }

        mBeatSchedule.emplace_back(newQpcTime, newBeatNumber);

        QueryPerformanceCounter(&now);
        if (now.QuadPart > qpcTime - mBudgetTicks) {
            break; 
        }
    }
    return;
}

void MidiScheduler::resetPreviouslyScheduledNoteQpcTime() {
    std::lock_guard<std::mutex> lock(mPreviouslyScheduledNoteQpcTimeMutex);
    mPreviouslyScheduledNoteQpcTime = 0;
}

std::pair<long long, int> MidiScheduler::getBeatFromIndex(size_t index) {
    if (index < 0 || index >= 600) {
        throw std::runtime_error("Index provided to getBeatFromIndex() is out of range! Got " + index);
    }
    long long now = mTimer->qpcGetTicks();
    std::lock_guard<std::mutex> lock(mBeatScheduleMutex);
    std::pair<long long, int> beat = mBeatSchedule.at(index);
    if (beat.first < now) {
        beat.first = 0;
        beat.second = 0;
    }
    return beat;
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
        noteEvent.scheduledTimeTicks = mPreviouslyScheduledNoteQpcTime;
    }
 
    // Set the MidiEvent Qpc time to the scheduled time in both the case where it has been adjusted and when it has not
    noteEvent.event.qpcTime = noteEvent.scheduledTimeTicks + getRandomOffset();

    // Negative tempos are treated as a signal to use the default tempo
    if (noteEvent.tempo < 0) { 
        noteEvent.tempo = mTempoBpm.load(); 
    }

    // This converts the duration in from a beat representation (i.e. quarter note) to a ms and QPC ticks representation 
    long long adjustedDurationMs = MathUtils::FpFloor<long long>(static_cast<long long>(noteEvent.duration) * (60.0 / noteEvent.tempo));
    long long adjustedDurationQpcTicks = MathUtils::FpFloor<long long>((adjustedDurationMs / MS_TO_SEC_CONVERSION_FACTOR) * mFrequencyHz);

    // The qpc ticks time marker get's placed at the tail of the currently scheduled note, i.e. if a quarter note is played at the beat where it is released (NOTE_OFF)
    // Note though that this may not be the actual length that the note way played for (beatTicks), but rather the length of time the note was meant to occupy symbolically (adjustedDurationQpcTicks, or in our previous example: a quarter note)
    mPreviouslyScheduledNoteQpcTime = noteEvent.scheduledTimeTicks + std::abs(adjustedDurationQpcTicks);

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

void MidiScheduler::shiftBeats(long long offsetTicks) {
     mShiftBeats.store(true);
     mOffsetTicks.store(offsetTicks);
}

size_t MidiScheduler::shiftBeatsIncrementally(size_t startIndex, long long qpcTime) {
    LARGE_INTEGER now;
    QueryPerformanceCounter(&now);

    size_t index = startIndex;
    std::lock_guard<std::mutex> lock(mBeatScheduleMutex);
    while (index < mBeatSchedule.size()) {
        mBeatSchedule[index].first += mOffsetTicks.load();
        ++index;

        QueryPerformanceCounter(&now);
        if (now.QuadPart > qpcTime - mBudgetTicks) {
            break; 
        }
    }
    return index; 
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
        else if (mShiftBeats.load()) {
            size_t lastIndex = shiftBeatsIncrementally(mShiftIndex.load(), qpcTime);
            mShiftIndex.store(lastIndex);
            std::lock_guard<std::mutex> lock(mBeatScheduleMutex);
            if (lastIndex == mBeatSchedule.size() - 1) {
                std::cout << "Finished shifting beats" <<std::endl;
                mShiftBeats.store(false);
                mShiftIndex.store(0);
            }
        }
        else if (mTempoChange.load()) {
            size_t lastIndex = changeBeatLengthsIncrementally(mTempoChangeIndex.load(), qpcTime);
            mTempoChangeIndex.store(lastIndex);
        }
        else {
            pruneExpiredBeatsIncrementally(qpcTime);
        }
        QueryPerformanceCounter(&now);
    } while (now.QuadPart < qpcTime - mBudgetTicks);
}

