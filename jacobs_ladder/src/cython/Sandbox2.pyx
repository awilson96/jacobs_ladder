from libc.stdint cimport uint8_t, uint32_t, uintptr_t
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

cdef extern from "windows.h":
    ctypedef const wchar_t* LPCWSTR  # Fix wchar_t issue
    ctypedef void* LPVOID
    ctypedef int BOOL
    ctypedef void* HANDLE
    ctypedef unsigned long DWORD

ctypedef void (*MidiCallback)(HANDLE, uint8_t*, DWORD, uintptr_t)

cdef extern from "teVirtualMIDI.h":
    LPVOID virtualMIDIGetVersion()
    LPVOID virtualMIDIGetDriverVersion()
    HANDLE virtualMIDICreatePortEx2(LPCWSTR, MidiCallback, uintptr_t, DWORD, DWORD)
    BOOL virtualMIDISendData(HANDLE, uint8_t*, DWORD)
    void virtualMIDIClosePort(HANDLE)

# Define constants
MAX_SYSEX_BUFFER = 65535
TE_VM_FLAGS_PARSE_RX = 1

cdef class VirtualMIDI:
    cdef HANDLE port
    cdef MidiCallback callback

    def __init__(self, port_name: str = "Python MIDI Port"):
        cdef LPCWSTR port_name_w = port_name.encode('utf-16-le')  # Fix LPCWSTR string conversion
        self.callback = <MidiCallback>self.midi_callback
        self.port = virtualMIDICreatePortEx2(port_name_w, self.callback, 0, MAX_SYSEX_BUFFER, TE_VM_FLAGS_PARSE_RX)
        if not self.port:
            raise RuntimeError("Could not create MIDI port.")
        print(f"Virtual MIDI port '{port_name}' created.")
    
    cdef void midi_callback(self, HANDLE midi_port, uint8_t* midi_data, DWORD length, uintptr_t instance):
        if not midi_data or length == 0:
            print("Empty command received (driver likely shut down)")
            return
        
        data = bytes(<char[:length]> midi_data)  # Properly convert pointer to bytes
        print(f"Received MIDI: {data.hex(':')}")
        
        if not virtualMIDISendData(self.port, midi_data, length):
            print("Error sending data.")

    def send_midi(self, data: bytes):
        cdef uint8_t* midi_data = <uint8_t*> malloc(len(data) + 1)  # Fix memory allocation
        memcpy(midi_data, data, len(data))
        
        if not virtualMIDISendData(self.port, midi_data, len(data)):
            free(midi_data)
            raise RuntimeError("Error sending MIDI data.")
        
        free(midi_data)

    def close(self):
        virtualMIDIClosePort(self.port)
        print("MIDI port closed.")

if __name__ == "__main__":
    midi = VirtualMIDI()
    print("Using DLL version:", <uint32_t>virtualMIDIGetVersion())  # Convert LPVOID return type
    print("Using driver version:", <uint32_t>virtualMIDIGetDriverVersion())
    input("Press Enter to close the port...")
    midi.close()
