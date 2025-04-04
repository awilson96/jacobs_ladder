#include <sstream>
#include <regex>

std::string normalizePortName(const std::string& portName) {
    std::istringstream iss(portName);
    std::string token, lastToken;
    std::string result;

    while (iss >> token) {
        if (!result.empty()) result += " ";
        result += lastToken;
        lastToken = token;
    }

    size_t lastSpace = result.find_last_of(' ');
    if (lastSpace != std::string::npos) {
        return result.substr(0, lastSpace);
    } else {
        return result;
    }
}
