#ifndef VIRTUALMIDIMANAGER_H
#define VIRTUALMIDIMANAGER_H

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

class VirtualMIDIManager {
private:
    std::vector<LPVM_MIDI_PORT> ports;
    std::string jsonFile;
    std::thread workerThread;
    std::atomic<bool> running {false};

    static void CALLBACK teVMCallback(LPVM_MIDI_PORT midiPort, LPBYTE midiDataBytes, DWORD length, DWORD_PTR dwCallbackInstance);

    void wait_for_close();
    void initialize(const std::vector<std::pair<std::string, int>>& name_count_pairs);


public:
    VirtualMIDIManager();
    ~VirtualMIDIManager();

    void start(const std::vector<std::pair<std::string, int>>& name_count_pairs);
    void close();
};

#endif // VIRTUALMIDIMANAGER_H
