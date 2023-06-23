#ifndef INTERVALS_H
#define INTERVALS_H

// file includes
#include <iostream>
#include <string>

//project includes
#include "Notes.h"

enum class Intervals : int
{
    semitone        = 1,
    wholeStep       = 2,
    minorThird      = 3,
    majorThird      = 4,
    fourth          = 5,
    tritone         = 6,
    fifth           = 7,
    minorSixth      = 8,
    sixth           = 9,
    minorSeventh    = 10,
    majorSeventh    = 11,
    octave          = 12
};

bool operator==(Intervals lhs, Note rhs) { return static_cast<int>(lhs) == static_cast<int>(rhs); }
bool operator==(Note lhs, Intervals rhs) { return static_cast<int>(lhs) == static_cast<int>(rhs); }
bool operator==(Intervals lhs, int rhs) { return static_cast<int>(lhs) == rhs; }
bool operator==(int lhs, Intervals rhs) { lhs == static_cast<int>(rhs); }

#endif // INTERVALS_H