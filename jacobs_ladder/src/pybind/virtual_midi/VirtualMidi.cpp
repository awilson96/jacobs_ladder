#include <iostream>
#include <vector>
#include <string>
#include <signal.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "teVirtualMIDI.h"

#define MAX_SYSEX_BUFFER	65535

namespace py = pybind11;

class VirtualMIDIPortManager {
private:
    std::vector<LPVM_MIDI_PORT> ports;
    std::vector<std::string> portNames;

public:
    VirtualMIDIPortManager(const std::vector<std::pair<std::string, int>>& portConfigs) {
        virtualMIDILogging(TE_VM_LOGGING_MISC | TE_VM_LOGGING_RX | TE_VM_LOGGING_TX);

        LPVM_MIDI_PORT jacobs_ladder = createDefaultPort("jacobs_ladder");
        LPVM_MIDI_PORT jacob = createDefaultPort("jacob");
        ports.push_back(jacobs_ladder);
        portNames.push_back("jacobs_ladder");
        ports.push_back(jacob);
        portNames.push_back("jacob");

        for (const auto& config : portConfigs) {
            std::string prefix = config.first;
            int numPorts = config.second;

            for (int i = 0; i < numPorts; ++i) {
                std::string portName = prefix + "_" + std::to_string(i);
                std::wstring widePortName(portName.begin(), portName.end());
                LPVM_MIDI_PORT port = virtualMIDICreatePortEx2(
                    widePortName.c_str(), nullptr, 0, MAX_SYSEX_BUFFER, TE_VM_FLAGS_PARSE_RX);


                if (!port) {
                    std::cerr << "Failed to create port: " << portName << " Error: " << GetLastError() << std::endl;
                    continue;
                }

                ports.push_back(port);
                portNames.push_back(portName);
                std::cout << "Created virtual MIDI port: " << portName << std::endl;
            }
        }
    }

    ~VirtualMIDIPortManager() {
        cleanup();
    }

    LPVM_MIDI_PORT createDefaultPort(std::string name) {
        std::wstring widePortName(name.begin(), name.end());
        LPVM_MIDI_PORT port = virtualMIDICreatePortEx2(
            widePortName.c_str(), nullptr, 0, MAX_SYSEX_BUFFER, TE_VM_FLAGS_PARSE_RX);

        std::cout << "Created virtual MIDI port: " << name << std::endl;

        if (!port) {
            std::cerr << "Failed to create port: " << name << " Error: " << GetLastError() << std::endl;
        }
        return port;
    }

    void cleanup() {
        for (size_t i = 0; i < ports.size(); ++i) {
            if (ports[i]) {
                virtualMIDIClosePort(ports[i]);
                std::cout << "Closed virtual port: " << portNames[i] << std::endl;
            }
        }
        ports.clear();
        portNames.clear();
    }

    std::vector<std::string> getPortNames() const {
        return portNames;
    }
};

// Pybind11 wrapper
PYBIND11_MODULE(virtual_midi, m) {
    py::class_<VirtualMIDIPortManager>(m, "VirtualMIDIPortManager")
        .def(py::init<const std::vector<std::pair<std::string, int>>&>())
        .def("cleanup", &VirtualMIDIPortManager::cleanup)
        .def("getPortNames", &VirtualMIDIPortManager::getPortNames);
}
