#include "QpcUtils.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(qpc_utils, m) {
    py::class_<QpcUtils>(m, "QpcUtils")
        .def(py::init<>())
        .def("qpcGetFrequency", &QpcUtils::qpcGetFrequency)
        .def("qpcGetTicks", &QpcUtils::qpcGetTicks)
        .def("qpcCoarseSleep", &QpcUtils::qpcCoarseSleep)
        .def("qpcSleepMs", &QpcUtils::qpcSleepMs)
        .def("qpcSleepUs", &QpcUtils::qpcSleepUs)
        .def("qpcSleepNs", &QpcUtils::qpcSleepNs)
        .def("qpcPrintTimeDiffNs", &QpcUtils::qpcPrintTimeDiffNs)
        .def("qpcPrintTimeDiffUs", &QpcUtils::qpcPrintTimeDiffUs)
        .def("qpcPrintTimeDiffMs", &QpcUtils::qpcPrintTimeDiffMs)
        .def("qpcDisplayStatistics", &QpcUtils::qpcDisplayStatistics)
        .def("qpcCalculatePercentError", &QpcUtils::qpcCalculatePercentError);
}