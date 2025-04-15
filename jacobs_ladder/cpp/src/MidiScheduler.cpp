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

bool MidiScheduler::addEvent(MidiEvent event) {
    if (event.qpcTime >= mTimer->qpcGetTicks()) {
        mQueue.push(event);
        return true;
    }
    return false;
}

bool MidiScheduler::addEvent(MidiEvent event, int offsetNs) {
    if (offsetNs < 0)
        return false;

    event.qpcTime += offsetNs;
    return addEvent(event);
}

bool MidiScheduler::addEvents(std::vector<MidiEvent> events) {
    for (const auto& event : events) {
        addEvent(event);
    }
    return true;
}

bool MidiScheduler::addEvents(std::vector<MidiEvent> events, int offsetNs) {
    if (offsetNs < 0)
        return false;

    for (auto& event : events) {
        event.qpcTime += offsetNs;
        addEvent(event);
    }
    return true;
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
    std::priority_queue<MidiEvent> empty;
    mQueue.swap(empty);
}

// TODO: Rework to use smart sleeps and absolute times instead of sleep times
void MidiScheduler::player() {
    while (mRunning.load()) {

        {
            std::unique_lock<std::mutex> lock(mPauseMutex);
            mPauseCv.wait(lock, [this]() { return !mPaused.load() || !mRunning.load(); });
            if (!mRunning.load()) 
                break;
        }

        if (mQueue.empty())
            continue;

        MidiEvent event = mQueue.top();
        mQueue.pop();

        if (mPrintMsgs.load()) {
            std::cout << "Midi Event: \n"
                  << "Status: "   << static_cast<int>(event.status)   << "\n"
                  << "Note: "     << (int)event.note                  << "\n"
                  << "Velocity: " << (int)event.velocity              << "\n"
                  << "Time: "     << event.qpcTime                    << "\n\n";
        }
        
        LARGE_INTEGER start, now;
        if (QueryPerformanceCounter(&start)) {

            // TODO: If requested time is greater than consumer add() budget, add items until budget is met
            // This is a kind of smart sleep
            do {
                QueryPerformanceCounter(&now);
            } while (now.QuadPart < event.qpcTime);
        }
        
        // Send the MIDI message
        std::vector<unsigned char> message = { static_cast<unsigned char>(event.status),
                                               static_cast<unsigned char>(event.note),
                                               static_cast<unsigned char>(event.velocity) };
        mMidiOut->sendMessage(&message);
    }
}

