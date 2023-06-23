#ifndef TRIADS_H
#define TRIADS_H

// file includes
#include <iostream>
#include <string>

//project includes
#include "Notes.h"
#include "Intervals.h"

std::string determineChord(Note bass, Note tenor, Note treble) 
{
    int lowerInterval = tenor - bass;
    int upperInterval = treble - tenor;

    if (lowerInterval == Intervals::semitone)
    {

    }
    else if (lowerInterval == Intervals::wholeStep)
    {

    }
    else if (lowerInterval == Intervals::minorThird)
    {

    }
    else if (lowerInterval == Intervals::majorThird)
    {

    }
    else if (lowerInterval == Intervals::fourth)
    {

    }
    else if (lowerInterval == Intervals::tritone)
    {

    }
    else if (lowerInterval == Intervals::fifth)
    {

    }
    else if (lowerInterval == Intervals::minorSixth)
    {

    }
    else if (lowerInterval == Intervals::sixth)
    {

    }
    else if (lowerInterval == Intervals::minorSeventh)
    {

    }
    else if (lowerInterval == Intervals::majorSeventh)
    {

    }
}

#endif // TRIADS_H