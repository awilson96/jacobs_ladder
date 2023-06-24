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
    // Get the intervals between all three notes
    Interval bassTenor = tenor - bass;
    Interval tenorTreble = treble - tenor;
    Interval bassTreble = treble - bass;

}



#endif // TRIADS_H