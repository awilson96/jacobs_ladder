#include <iostream>
#include <vector>
#include <string>
#include <signal.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "teVirtualMIDI.h"

#define MAX_SYSEX_BUFFER	65535

namespace py = pybind11;

char *binToStr( const unsigned char *data, DWORD length ) {
	static char dumpBuffer[ MAX_SYSEX_BUFFER * 3 ];
	DWORD index = 0;

	while ( length-- ) {
		sprintf( dumpBuffer+index, "%02x", *data );
		if ( length ) {
			strcat( dumpBuffer, ":" );
		}
		index+=3;
		data++;
	}
	return dumpBuffer;
}

void CALLBACK teVMCallback( LPVM_MIDI_PORT midiPort, LPBYTE midiDataBytes, DWORD length, DWORD_PTR dwCallbackInstance ) {
    std::cout << "Midi Data:\n" << binToStr( midiDataBytes, length ) << std::endl;
	if ( ( NULL == midiDataBytes ) || ( 0 == length ) ) {
		printf( "empty command - driver was probably shut down!\n" );
		return;
	}
	if ( !virtualMIDISendData( midiPort, midiDataBytes, length ) ) {
		printf( "error sending data: %d\n" + GetLastError() );
		return;
	}
}

class VirtualMIDIPortManager {
private:
    bool mPrint = false; 
    int mTeFlag = 0;
    std::vector<LPVM_MIDI_PORT> mPorts;
    std::vector<std::string> mPortNames;

public:
    VirtualMIDIPortManager(const std::vector<std::pair<std::string, int>>& portConfigs, int teFlag, bool print = false) {
        virtualMIDILogging(TE_VM_LOGGING_MISC | TE_VM_LOGGING_RX | TE_VM_LOGGING_TX);
        mPrint = print; 
        mTeFlag = teFlag;

        if (mTeFlag == 1)
            mTeFlag = TE_VM_FLAGS_PARSE_RX;
        else if (mTeFlag == 2)
            mTeFlag = TE_VM_FLAGS_PARSE_TX;
        else if (mTeFlag == 4)
            mTeFlag = TE_VM_FLAGS_INSTANTIATE_RX_ONLY;
        else if (mTeFlag == 8)
            mTeFlag = TE_VM_FLAGS_INSTANTIATE_TX_ONLY;
        else if (mTeFlag == 12)
            mTeFlag = TE_VM_FLAGS_INSTANTIATE_BOTH;
        else
            throw std::runtime_error("Invalid teFlag");

        for (const auto& config : portConfigs) {
            std::string prefix = config.first;
            int numPorts = config.second;

            // Create one default port for each prefix used for Midi input 
            LPVM_MIDI_PORT inputPort = createDefaultPort(prefix);
            mPorts.push_back(inputPort);
            mPortNames.push_back(prefix);

            for (int i = 0; i < numPorts; ++i) {
                std::string portName = prefix + "_" + std::to_string(i);
                std::wstring widePortName(portName.begin(), portName.end());
                LPVM_MIDI_PORT port = virtualMIDICreatePortEx2(
                    widePortName.c_str(), teVMCallback, 0, MAX_SYSEX_BUFFER, mTeFlag);

                if (!port) {
                    std::cerr << "Failed to create port: " << portName << " Error: " << GetLastError() << std::endl;
                    continue;
                }

                mPorts.push_back(port);
                mPortNames.push_back(portName);
                if(mPrint)
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
            widePortName.c_str(), nullptr, 0, MAX_SYSEX_BUFFER, mTeFlag);

        if(mPrint)
            std::cout << "Created virtual MIDI port: " << name << std::endl;

        if (!port) {
            std::cerr << "Failed to create port: " << name << " Error: " << GetLastError() << std::endl;
        }
        return port;
    }

    void cleanup() {
        for (size_t i = 0; i < mPorts.size(); ++i) {
            if (mPorts[i]) {
                virtualMIDIClosePort(mPorts[i]);
                if(mPrint)
                    std::cout << "Closed virtual port: " << mPortNames[i] << std::endl;
            }
        }
        mPorts.clear();
        mPortNames.clear();
    }

    std::vector<std::string> getPortNames() const {
        return mPortNames;
    }
};

// Pybind11 wrapper
PYBIND11_MODULE(virtual_midi, m) {
    py::class_<VirtualMIDIPortManager>(m, "VirtualMIDIPortManager")
        .def(py::init<const std::vector<std::pair<std::string, int>>&, int, bool>(), py::arg("portConfigs"), py::arg("teFlag"), py::arg("print") = false)
        .def("cleanup", &VirtualMIDIPortManager::cleanup)
        .def("getPortNames", &VirtualMIDIPortManager::getPortNames);
}
