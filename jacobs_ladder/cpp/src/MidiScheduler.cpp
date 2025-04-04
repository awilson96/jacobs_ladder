#include "MidiScheduler.h"
#include "MidiUtils.h"

MidiScheduler::MidiScheduler(const std::string& outputPortName) {
    mTimer = std::make_unique<QpcUtils>();
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
    // Destructor implementation (if needed)
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

    event.time += offset;
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
        event.time += offset;
        addEvent(event);
    }
    return true;
}

