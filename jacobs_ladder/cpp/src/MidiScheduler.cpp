#include "MidiScheduler.h"
#include "MidiUtils.h"

#include <cstdlib>

MidiScheduler::MidiScheduler(const std::string& outputPortName) {
    mTimer = std::make_unique<QpcUtils>();
    mFrequencyHz = mTimer->qpcGetFrequency();
    try {
        mMidiOut = std::make_unique<RtMidiOut>();

        unsigned int portCount = mMidiOut->getPortCount();
        bool portFound = false;

        for (unsigned int i = 0; i < portCount; ++i) {
            std::string rawName = mMidiOut->getPortName(i);
            std::string normalizedName = normalizePortName(rawName);
            std::cout << "MIDI output port " << i << ": " << normalizedName << "\n";
            if (normalizedName == outputPortName) {
                mMidiOut->openPort(i);
                std::cout << "Opened MIDI output port: " << normalizedName << "\n";
                portFound = true;
                break;
            }
        }

        if (!portFound) {
            throw std::runtime_error("Could not find MIDI output port: " + outputPortName);
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
    mMidiOut->closePort();
}

bool MidiScheduler::addEvent(MidiEvent event) {
    // TODO: Only push when the event time is greater than the current time
    // TODO: Only push when scheduler is sleeping 
    mQueue.push(event);
    return true;
}

bool MidiScheduler::addEvent(MidiEvent event, int offset) {
    // TODO: Only push when the event time is greater than the current time
    // TODO: Only push when scheduler is sleeping 
    if (offset < 0)
        return false;

    event.qpcTime += offset;
    return addEvent(event);
}

bool MidiScheduler::addEvents(std::vector<MidiEvent> events) {
    // TODO: Only push when the event time is greater than the current time
    // TODO: Only push when scheduler is sleeping 
    for (const auto& event : events) {
        addEvent(event);
    }
    return true;
}

bool MidiScheduler::addEvents(std::vector<MidiEvent> events, int offset) {
    // TODO: Only push when the event time is greater than the current time
    // TODO: Only push when scheduler is sleeping 
    if (offset < 0)
        return false;

    for (auto& event : events) {
        event.qpcTime += offset;
        addEvent(event);
    }
    return true;
}

// TODO: Rework to use smart sleeps and absolute times instead of sleep times
void MidiScheduler::player() {
    while (!mQueue.empty()) {
        MidiEvent event = mQueue.top();
        mQueue.pop();

        std::cout << "Midi Event: \n"
                  << "Status: "   << static_cast<int>(event.status)   << "\n"
                  << "Note: "     << (int)event.note                  << "\n"
                  << "Velocity: " << (int)event.velocity              << "\n"
                  << "Time: "     << event.qpcTime                    << "\n\n";

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

