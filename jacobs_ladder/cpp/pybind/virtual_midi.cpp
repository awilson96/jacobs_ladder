// Project includes
#include "VirtualMidiPortManager.h"

// System Includes
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// Pybind11 bindings
PYBIND11_MODULE(virtual_midi, m) {
    py::class_<VirtualMIDIPortManager>(m, "VirtualMIDIPortManager")
        .def(py::init<bool>(), py::arg("print_msgs") = false) 
        .def("start", &VirtualMIDIPortManager::start, py::arg("name_count_pairs"))
        .def("close", &VirtualMIDIPortManager::close);
}