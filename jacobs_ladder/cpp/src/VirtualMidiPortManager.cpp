#ifdef _WIN32

#include "VirtualMIDIPortManager.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdexcept>

namespace py = pybind11;

// Constructor
VirtualMIDIPortManager::VirtualMIDIPortManager(bool print_msgs) : print_msgs_(print_msgs) {}

// Destructor
VirtualMIDIPortManager::~VirtualMIDIPortManager() {
    if (running.load()) {
        close();
    }
}

// Callback function for MIDI events
void CALLBACK VirtualMIDIPortManager::teVMCallback(LPVM_MIDI_PORT midiPort, LPBYTE midiDataBytes, DWORD length, DWORD_PTR dwCallbackInstance) {
    if (!midiDataBytes || length == 0) {
        return;
    }
    if (!virtualMIDISendData(midiPort, midiDataBytes, length)) {
        return;
    }
}

// Initializes virtual MIDI ports from name-count pairs
void VirtualMIDIPortManager::initialize(const std::vector<std::pair<std::string, int>>& name_count_pairs) {
    pybind11::gil_scoped_acquire acquire;

    for (const auto& pair : name_count_pairs) {
        const std::string& prefix = pair.first;
        int numPorts = pair.second;

        std::wstring portNameDefault = std::wstring(prefix.begin(), prefix.end());
            LPVM_MIDI_PORT portDefault = virtualMIDICreatePortEx2(
                portNameDefault.c_str(), teVMCallback, 0, MAX_SYSEX_BUFFER, TE_VM_FLAGS_PARSE_RX);

        if (!portDefault) {
            throw std::runtime_error("Could not create port: " + std::string(prefix));
        }
        ports.push_back(portDefault);
        if (print_msgs_)
            std::wcout << "Created virtual MIDI port: " << portNameDefault << std::endl;

        for (int j = 0; j < numPorts; ++j) {
            std::wstring portName = std::wstring(prefix.begin(), prefix.end()) + L"_" + std::to_wstring(j);
            LPVM_MIDI_PORT port = virtualMIDICreatePortEx2(
                portName.c_str(), teVMCallback, j + 1, MAX_SYSEX_BUFFER, TE_VM_FLAGS_PARSE_RX);

            if (!port) {
                throw std::runtime_error("Could not create port: " + std::string(prefix) + "_" + std::to_string(j));
            }
            ports.push_back(port);
            if (print_msgs_)
                std::wcout << "Created virtual MIDI port: " << portName << std::endl;
        }
    }
}

// Starts the MIDI manager in a separate thread
void VirtualMIDIPortManager::start(const std::vector<std::pair<std::string, int>>& name_count_pairs) {
    workerThread = std::thread(&VirtualMIDIPortManager::initialize, this, name_count_pairs);
}

// Stops the MIDI manager and cleans up ports
void VirtualMIDIPortManager::close() {
    running.store(false);

    if (workerThread.joinable()) {
        workerThread.join();
    }

    for (LPVM_MIDI_PORT port : ports) {
        virtualMIDIClosePort(port);
    }
    if (print_msgs_)
        std::cout << "All virtual MIDI ports closed." << std::endl;
}

#endif // _WIN32