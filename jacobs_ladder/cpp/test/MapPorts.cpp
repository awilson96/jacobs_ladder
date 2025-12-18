#include "rtmidi/RtMidi.h"

#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <sstream>
#include <cstring>
#include <csignal>
#include <atomic>

// Atomic flag to control the main loop
std::atomic<bool> running{true};

// Signal handler to exit gracefully
void handleSignal(int) {
    running = false;
}

// Helper to strip trailing numbers from a port name
std::string basePortName(const std::string& fullName) {
    std::istringstream iss(fullName);
    std::vector<std::string> tokens;
    std::string token;
    while (iss >> token) tokens.push_back(token);
    if (tokens.empty()) return fullName;
    // Remove last token if it is a number
    try {
        (void)std::stoi(tokens.back());
        tokens.pop_back();
    } catch (...) {
        // last token is not a number, keep it
    }
    std::ostringstream oss;
    for (size_t i = 0; i < tokens.size(); ++i) {
        if (i > 0) oss << " ";
        oss << tokens[i];
    }
    return oss.str();
}

// Find a port index by substring match (case-sensitive)
int findPortByName(RtMidi& midi, const std::string& name) {
    unsigned int portCount = midi.getPortCount();
    for (unsigned int i = 0; i < portCount; ++i) {
        std::string portName = midi.getPortName(i);
        if (portName.find(name) != std::string::npos) {
            return static_cast<int>(i);
        }
    }
    return -1;
}

// List MIDI input ports only
void listInputPorts() {
    RtMidiIn midiIn;
    std::cout << "MIDI INPUT PORTS:\n";
    for (unsigned int i = 0; i < midiIn.getPortCount(); ++i) {
        std::cout << "  " << basePortName(midiIn.getPortName(i)) << "\n";
    }
}

// List MIDI output ports only
void listOutputPorts() {
    RtMidiOut midiOut;
    std::cout << "MIDI OUTPUT PORTS:\n";
    for (unsigned int i = 0; i < midiOut.getPortCount(); ++i) {
        std::cout << "  " << basePortName(midiOut.getPortName(i)) << "\n";
    }
}

// MIDI callback: forward everything
void midiCallback(
    double /*deltaTime*/,
    std::vector<unsigned char>* message,
    void* userData
) {
    auto* midiOut = static_cast<RtMidiOut*>(userData);
    if (!message->empty()) {
        midiOut->sendMessage(message);
    }
}

int main(int argc, char* argv[]) {
    std::string inputPortName;
    bool listInput = false;
    bool listOutput = false;

    // Register signal handlers
    std::signal(SIGINT, handleSignal);
    std::signal(SIGTERM, handleSignal);

    // Simple CLI parsing
    for (int i = 1; i < argc; ++i) {
        if (std::strcmp(argv[i], "-i") == 0 ||
            std::strcmp(argv[i], "--input-ports") == 0) {
            listInput = true;
        } else if (std::strcmp(argv[i], "-o") == 0 ||
                   std::strcmp(argv[i], "--output-ports") == 0) {
            listOutput = true;
        } else if ((std::strcmp(argv[i], "-p") == 0 ||
                    std::strcmp(argv[i], "--port") == 0) &&
                   i + 1 < argc) {
            inputPortName = argv[i + 1];
            ++i;
        }
    }

    if (listInput) {
        listInputPorts();
    }

    if (listOutput) {
        listOutputPorts();
    }

    // If we only listed ports, exit
    if (listInput || listOutput) {
        return 0;
    }

    if (inputPortName.empty()) {
        std::cerr
            << "Usage:\n"
            << "  MapPorts -i | --input-ports\n"
            << "  MapPorts -o | --output-ports\n"
            << "  MapPorts -p | --port \"<input_port_name>\"\n";
        return 1;
    }

    RtMidiIn midiIn;
    RtMidiOut midiOut;

    try {
        int inputIndex = findPortByName(midiIn, inputPortName);
        if (inputIndex < 0) {
            std::cerr << "ERROR: Input MIDI port not found: "
                      << inputPortName << "\n";
            return 1;
        }

        int outputIndex = findPortByName(midiOut, "jacobs_ladder");
        if (outputIndex < 0) {
            std::cerr << "ERROR: Output MIDI port 'jacobs_ladder' not found\n";
            return 1;
        }

        midiIn.openPort(inputIndex);
        midiOut.openPort(outputIndex);

        midiIn.ignoreTypes(false, false, false);
        midiIn.setCallback(&midiCallback, &midiOut);

        std::cout << "Routing MIDI from \"" 
                  << midiIn.getPortName(inputIndex) 
                  << "\" to \"" 
                  << midiOut.getPortName(outputIndex) 
                  << "\"\n";
        std::cout << "Press Ctrl+C to exit.\n";

        // Main loop controlled by signal
        while (running.load()) {
            std::this_thread::sleep_for(std::chrono::milliseconds(200));
        }

        std::cout << "Shutting down...\n";
    } catch (RtMidiError& e) {
        e.printMessage();
        return 1;
    }

    // Explicit cleanup
    if (midiIn.isPortOpen()) midiIn.closePort();
    if (midiOut.isPortOpen()) midiOut.closePort();

    return 0;
}
