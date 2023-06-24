#ifndef INTERVALS_H
#define INTERVALS_H

// file includes
#include <iostream>
#include <string>

//project includes
#include "Notes.h"

enum class Interval : int
{
    halfStep        = 1,
    wholeStep       = 2,
    minorThird      = 3,
    majorThird      = 4,
    perfectFourth   = 5,
    tritone         = 6,
    perfectFifth    = 7,
    minorSixth      = 8,
    majorSixth      = 9,
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
            return Interval::halfStep;
        case 2:
            return Interval::wholeStep;
        case 3:
            return Interval::minorThird;
        case 4:
            return Interval::majorThird;
        case 5:
            return Interval::perfectFourth;
        case 6:
            return Interval::tritone;
        case 7:
            return Interval::perfectFifth;
        case 8:
            return Interval::minorSixth;
        case 9:
            return Interval::majorSixth;
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

void printInterval(Interval interval)
{
    switch(interval)
    {
        case Interval::halfStep:
            std::cout << "Half Step";
        case Interval::wholeStep:
            std::cout << "Whole Step";
        case Interval::minorThird:
            std::cout << "Minor Third";
        case Interval::majorThird:
            std::cout << "Major Third";
        case Interval::perfectFourth:
            std::cout << "Perfect Fourth";
        case Interval::tritone:
            std::cout << "Tritone";
        case Interval::perfectFifth:
            std::cout << "Perfect Fifth";
        case Interval::minorSixth:
            std::cout << "Minor Sixth";
        case Interval::majorSixth:
            std::cout << "Major Sixth";
        case Interval::minorSeventh:
            std::cout << "MinorSeventh";
        case Interval::majorSeventh:
            std::cout << "Major Seventh";
        default:
            std::cout << "Unknown";
    }
}

Interval operator+(Interval lhs, Interval rhs) 
    { return static_cast<Interval>(static_cast<int>(lhs) + static_cast<int>(rhs)); }

Interval operator-(Interval lhs, Interval rhs) 
    { return static_cast<Interval>(static_cast<int>(lhs) - static_cast<int>(rhs)); }

Interval operator-(Note lhs, Note rhs) 
    { return createInterval(static_cast<int>(lhs) - static_cast<int>(rhs)); }

bool operator==(Interval lhs, int rhs) { return static_cast<int>(lhs) == rhs; }
bool operator==(int lhs, Interval rhs) { lhs == static_cast<int>(rhs); }

#endif // INTERVALS_H