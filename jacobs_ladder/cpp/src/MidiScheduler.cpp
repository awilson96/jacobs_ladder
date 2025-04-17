#include "MidiScheduler.h"
#include "MidiUtils.h"

#include <cstdlib>

MidiScheduler::MidiScheduler(const std::string& outputPortName, bool startImmediately, bool printMsgs) {
    mTimer = std::make_unique<QpcUtils>();
    mFrequencyHz = mTimer->qpcGetFrequency();
    mPrintMsgs.store(printMsgs);
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
                    std::cout << "Opened MIDI output port: " << normalizedName << "\n";
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

void MidiScheduler::addEvent(const Midi::NoteDuration &noteDuration) {
    
}

void MidiScheduler::addEvent(const Midi::NoteDuration &noteDuration, double offsetMs) {
    
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

void MidiScheduler::addEvents(std::vector<Midi::NoteDuration> &noteDurations) {

}

void MidiScheduler::addEvents(std::vector<Midi::NoteDuration> &noteDurations, double offsetMs) {

}

void MidiScheduler::pause() {
    mPaused.store(true);
}

void MidiScheduler::resume() {
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

bool MidiScheduler::conditionallyPause() {
    std::unique_lock<std::mutex> lock(mPauseMutex);
    mPauseCv.wait(lock, [this]() { return !mPaused.load() || !mRunning.load(); });
    if (!mRunning.load()) 
        return true;
    return false;
}

// TODO: Rework to use smart sleeps
void MidiScheduler::player() {
    while (mRunning.load()) {

        // If the user has paused or stopped the player, conditionally pause.
        // Only returns true when mRunning has been set to false
        if (conditionallyPause())
            continue;

        if (mQueue.empty()) {
            std::lock_guard<std::mutex> lock(mBufferMutex);
            if (mBuffer.empty()) {
                continue;
            }
                
            while(!mBuffer.empty()) {
                if (scheduleEvent(mBuffer.top())) {
                    mBuffer.pop();
                    break;
                } 
                else if (mTimer->qpcGetTicks() > mBuffer.top().qpcTime + mBudgetNs) {
                    mBuffer.pop();
                }
                else {
                    break;
                }
            }
        }

        // If we have neither been told to pause or stop and the queue is not empty then process the soonest MidiEvent 
        // and query the performance counter for the current time
        Midi::MidiEvent event = mQueue.top();
        mQueue.pop();
        long long currentTime = mTimer->qpcGetTicks();

        // If the currentTime is 10 ms or more behind schedule then just move on without playing it
        if (currentTime > event.qpcTime + 10000000) {
            continue;
        } 
        // If the currentTime is somewhere between the scheduled time and 10 ms behind then play it immediately
        else if (currentTime > event.qpcTime && currentTime <= event.qpcTime + 10000000) {
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
        
        // Smart sleep adds MidiEvents to the priority queue while it is still within mBudgetNs nanoseconds of the scheduled event time
        // This budget was calculated as approximately 5 times the benchmarked time it takes to run the scheduleEvent() on average.
        // (i.e. 250 ns * 5 = 1250 ns) 
        smartSleep(event);

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

bool MidiScheduler::scheduleEvent(Midi::MidiEvent event) {
    if (event.qpcTime >= mTimer->qpcGetTicks()) {
        mQueue.push(event);
        return true;
    }
    return false;
}

bool MidiScheduler::scheduleEvents(std::vector<Midi::MidiEvent> events) {
    for (const auto& event : events) {
        scheduleEvent(event);
    }
    return true;
}

void MidiScheduler::smartSleep(Midi::MidiEvent &event) {
    LARGE_INTEGER now;
    std::lock_guard<std::mutex> lock(mBufferMutex);
    // Query the performance counter each cycle to determine the moment our time budget has run out 
    // and loop on the condition that we are within mBudgetNs nanoseconds of the scheduled event time
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
    } while (now.QuadPart < event.qpcTime - mBudgetNs);
}

