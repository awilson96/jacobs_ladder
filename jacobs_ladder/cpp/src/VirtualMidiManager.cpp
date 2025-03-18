#include "VirtualMidiManager.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdexcept>


namespace py = pybind11;

// Constructor
VirtualMIDIManager::VirtualMIDIManager() = default;

// Destructor
VirtualMIDIManager::~VirtualMIDIManager() {
    if (running.load()) {
        close();
    }
}

// Callback function for MIDI events
void CALLBACK VirtualMIDIManager::teVMCallback(LPVM_MIDI_PORT midiPort, LPBYTE midiDataBytes, DWORD length, DWORD_PTR dwCallbackInstance) {
    if (!midiDataBytes || length == 0) {
        std::cout << "Empty command - driver was probably shut down!" << std::endl;
        return;
    }
    if (!virtualMIDISendData(midiPort, midiDataBytes, length)) {
        std::cout << "Error sending data: " << GetLastError() << std::endl;
        return;
    }
    std::cout << "Port " << dwCallbackInstance << " Command received." << std::endl;
}

// Blocks execution until close() is called
void VirtualMIDIManager::wait_for_close() {
    while (running.load()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

// Initializes virtual MIDI ports from name-count pairs
void VirtualMIDIManager::initialize(const std::vector<std::pair<std::string, int>>& name_count_pairs) {
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
        std::wcout << "Created virtual MIDI port: " << portNameDefault << std::endl;

        for (int j = 0; j < numPorts; ++j) {
            std::wstring portName = std::wstring(prefix.begin(), prefix.end()) + L"_" + std::to_wstring(j);
            LPVM_MIDI_PORT port = virtualMIDICreatePortEx2(
                portName.c_str(), teVMCallback, j + 1, MAX_SYSEX_BUFFER, TE_VM_FLAGS_PARSE_RX);

            if (!port) {
                throw std::runtime_error("Could not create port: " + std::string(prefix) + "_" + std::to_string(j));
            }
            ports.push_back(port);
            std::wcout << "Created virtual MIDI port: " << portName << std::endl;
        }
    }

    // running.store(true);
    // wait_for_close();  // Blocking call within the same thread
}

// Starts the MIDI manager in a separate thread
void VirtualMIDIManager::start(const std::vector<std::pair<std::string, int>>& name_count_pairs) {
    workerThread = std::thread(&VirtualMIDIManager::initialize, this, name_count_pairs);
}

// Stops the MIDI manager and cleans up ports
void VirtualMIDIManager::close() {
    running.store(false);

    if (workerThread.joinable()) {
        workerThread.join();
    }

    for (LPVM_MIDI_PORT port : ports) {
        virtualMIDIClosePort(port);
    }

    std::cout << "All virtual MIDI ports closed." << std::endl;
}

// Pybind11 bindings
PYBIND11_MODULE(virtual_midi, m) {
    py::class_<VirtualMIDIManager>(m, "VirtualMIDIManager")
        .def(py::init<>())
        .def("start", &VirtualMIDIManager::start, py::arg("name_count_pairs"))
        .def("close", &VirtualMIDIManager::close);
}

