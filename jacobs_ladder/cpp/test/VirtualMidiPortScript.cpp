#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <chrono>
#include <vector>
#include <nlohmann/json.hpp>  // Include the nlohmann JSON library
#include "teVirtualMIDI.h"

#define MAX_SYSEX_BUFFER 65535

using json = nlohmann::json;

char *binToStr(const unsigned char *data, DWORD length) {
    static char dumpBuffer[MAX_SYSEX_BUFFER * 3];
    DWORD index = 0;

    while (length--) {
        sprintf(dumpBuffer + index, "%02x", *data);
        if (length) {
            strcat(dumpBuffer, ":");
        }
        index += 3;
        data++;
    }
    return dumpBuffer;
}

// Callback function to process incoming MIDI data for all ports
void CALLBACK teVMCallback(LPVM_MIDI_PORT midiPort, LPBYTE midiDataBytes, DWORD length, DWORD_PTR dwCallbackInstance) {
    if (midiDataBytes == nullptr || length == 0) {
        // std::cout << "Empty command - driver was probably shut down!" << std::endl;
        return;
    }
    if (!virtualMIDISendData(midiPort, midiDataBytes, length)) {
        // std::cout << "Error sending data: " << GetLastError() << std::endl;
        return;
    }
    // std::cout << "Port " << dwCallbackInstance << " Command: " << binToStr(midiDataBytes, length) << std::endl;
}

int main(int argc, const char *argv[]) {
    std::vector<LPVM_MIDI_PORT> ports;
    std::string jsonFile = ""; // Default JSON file path

    // Parse command-line arguments
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if ((arg == "-f" || arg == "--file") && i + 1 < argc) {
            jsonFile = argv[++i]; // Set the JSON file path
        } else {
            std::cout << "Unknown argument: " << arg << std::endl;
            return 1;
        }
    }

    if (jsonFile.empty()) {
        std::cerr << "Usage: " << argv[0] << " -f <json_file>" << std::endl;
        return 1;
    }

    // Load and parse the JSON config file
    std::ifstream file(jsonFile);
    if (!file.is_open()) {
        std::cerr << "Could not open JSON file: " << jsonFile << std::endl;
        return 1;
    }

    json config;
    file >> config;

    // Validate JSON structure
    if (!config.contains("names") || !config.contains("counts")) {
        std::cerr << "JSON must contain 'names' and 'counts' arrays!" << std::endl;
        return 1;
    }

    auto names = config["names"];
    auto counts = config["counts"];

    if (!names.is_array() || !counts.is_array()) {
        std::cerr << "'names' and 'counts' must be arrays!" << std::endl;
        return 1;
    }

    if (names.size() != counts.size()) {
        std::cerr << "The size of 'names' must equal the size of 'counts'!" << std::endl;
        return 1;
    }

    // Check that all counts are greater than 0
    for (auto count : counts) {
        if (count <= 0) {
            std::cerr << "All counts must be greater than 0!" << std::endl;
            return 1;
        }
    }

    // Create the virtual MIDI ports based on JSON data
    for (size_t i = 0; i < names.size(); ++i) {
        std::string prefix = names[i];
        int numPorts = counts[i];

        std::wstring basePortName = std::wstring(prefix.begin(), prefix.end());
            LPVM_MIDI_PORT port = virtualMIDICreatePortEx2(
                basePortName.c_str(), teVMCallback, 0, MAX_SYSEX_BUFFER, TE_VM_FLAGS_PARSE_RX);

        ports.push_back(port);
        std::wcout << "Created virtual MIDI port: " << basePortName << std::endl;

        for (int j = 0; j < numPorts; ++j) {
            std::wstring portName = std::wstring(prefix.begin(), prefix.end()) + L"_" + std::to_wstring(j);
            LPVM_MIDI_PORT port = virtualMIDICreatePortEx2(
                portName.c_str(), teVMCallback, j + 1, MAX_SYSEX_BUFFER, TE_VM_FLAGS_PARSE_RX);

            if (!port) {
                std::wcout << "Could not create port " << portName << ": " << GetLastError() << std::endl;
                return 1;
            }
            ports.push_back(port);
            std::wcout << "Created virtual MIDI port: " << portName << std::endl;
        }
    }

    std::cout << "Virtual ports created - press enter to close ports..." << std::endl;
    std::cin.get(); // Wait for user input to close the ports

    // Close all created ports
    for (LPVM_MIDI_PORT port : ports) {
        virtualMIDIClosePort(port);
    }

    // Wait for 1 second before closing the ports
    std::this_thread::sleep_for(std::chrono::seconds(1));
    std::cout << "All ports closed." << std::endl;

    return 0;
}
