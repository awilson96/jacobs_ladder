#include <iostream>
#include <string>

#include "Notes.h"
#include "Intervals.h"


namespace Fundamentals 
{
    std::string determineChord(Note bass, Note tenor, Note treble)
    {
        // Get the intervals between all three notes
        Interval bassTenor = tenor - bass;
        Interval tenorTreble = treble - tenor;
        Interval bassTreble = treble - bass;

    }
}

int main()
{
    
    return 0;
}