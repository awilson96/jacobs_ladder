#ifndef VirtualMIDIPortManager_H
#define VirtualMIDIPortManager_H

#ifdef _WIN32

#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <atomic>
#include <vector>
#include <mutex>
#include <condition_variable>
#include <nlohmann/json.hpp>
#include "teVirtualMIDI.h"

#define MAX_SYSEX_BUFFER 65535

using json = nlohmann::json;

class VirtualMIDIPortManager {
private:
    bool print_msgs_;
    std::vector<LPVM_MIDI_PORT> ports;
    std::string jsonFile;
    std::thread workerThread;
    std::atomic<bool> running {false};

    static void CALLBACK teVMCallback(LPVM_MIDI_PORT midiPort, LPBYTE midiDataBytes, DWORD length, DWORD_PTR dwCallbackInstance);
    void initialize(const std::vector<std::pair<std::string, int>>& name_count_pairs);

public:
    VirtualMIDIPortManager(bool print_msgs = false);
    ~VirtualMIDIPortManager();

    // Delete copy constructor and copy assignment operator
    VirtualMIDIPortManager(const VirtualMIDIPortManager&) = delete;
    VirtualMIDIPortManager& operator=(const VirtualMIDIPortManager&) = delete;

    void start(const std::vector<std::pair<std::string, int>>& name_count_pairs);
    void close();
};

#endif // _WIN32
#endif // VirtualMIDIPortManager_H
