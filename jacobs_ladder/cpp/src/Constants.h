#ifndef CONSTANTS_H
#define CONSTANTS_H

#include <cstdint>

static const double MS_TO_SEC_CONVERSION_FACTOR = 1000;
static const double US_TO_SEC_CONVERSION_FACTOR = 1000000;
static const double NS_TO_SEC_CONVERSION_FACTOR = 1000000000;

static const long long TEN_MILLISECOND_BUDGET_TICKS = 100000;
static const long long ONE_MILLISECOND_MIN_SEPARATION_TICKS = 10000;
static const long long QPC_FREQUENCY = 10000000;
static const long long ONE_POINT_FIVE_MS_IN_TICKS = 15000;

static constexpr int TICKS_PER_QUARTER_NOTE = 960;
static constexpr int MS_PER_MINUTE = 60000;
static constexpr double DEFAULT_BPM = 60.0;

constexpr uint8_t ALL_NOTES_OFF = 0x7B;
constexpr uint8_t VALUE_OFF     = 0x00;



#endif // CONSTANTS_H
