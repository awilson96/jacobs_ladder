#ifndef INTERVALS_H
#define INTERVALS_H

// file includes
#include <iostream>
#include <string>

//project includes
#include "Notes.h"

enum class Interval : int
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
    octave          = 12,
    unknown         = 13
};

Interval createInterval(int interval)
{
    switch(interval)
    {
        case 1:
            return Interval::semitone;
        case 2:
            return Interval::wholeStep;
        case 3:
            return Interval::minorThird;
        case 4:
            return Interval::majorThird;
        case 5:
            return Interval::fourth;
        case 6:
            return Interval::tritone;
        case 7:
            return Interval::fifth;
        case 8:
            return Interval::minorSixth;
        case 9:
            return Interval::sixth;
        case 10:
            return Interval::minorSeventh;
        case 11:
            return Interval::majorSeventh;
        case 12:
            return Interval::octave;
        default:
            return Interval::unknown;
    }
}

Interval operator+(Interval lhs, Interval rhs) 
    { return static_cast<Interval>(static_cast<int>(lhs) + static_cast<int>(rhs)); }

Interval operator-(Interval lhs, Interval rhs) 
    { return static_cast<Interval>(static_cast<int>(lhs) - static_cast<int>(rhs)); }

Interval operator-(Note lhs, Note rhs) 
    { return createInterval(static_cast<int>(lhs) - static_cast<int>(rhs)); }

bool operator==(Interval lhs, Note rhs) { return static_cast<int>(lhs) == static_cast<int>(rhs); }
bool operator==(Note lhs, Interval rhs) { return static_cast<int>(lhs) == static_cast<int>(rhs); }
bool operator==(Interval lhs, int rhs) { return static_cast<int>(lhs) == rhs; }
bool operator==(int lhs, Interval rhs) { lhs == static_cast<int>(rhs); }

#endif // INTERVALS_H