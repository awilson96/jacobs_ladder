#include <iostream>
#include <string>

#include "Notes.h"
#include "Intervals.h"
#include "Triads.h"


namespace Chord 
{
    Triad determineChord(Note bass, Note tenor, Note treble)
    {
        // Get the intervals between bottom and middle notes, and between bottom and top notes
        Interval lower = tenor - bass;
        Interval upper = treble - bass;

        if (lower == Interval::wholeStep)
        {
            if (upper == Interval::perfectFourth)
                return Triad::min7SecondInv;
            else if (upper == Interval::tritone)
                return Triad::rootedDominantSecondInv;
            else if (upper == Interval::perfectFifth)
                return Triad::sus2;
            else if (upper == Interval::majorSixth)
                return Triad::rootlessDominantFirstInv;
            else
                return Triad::unknown;
        }
        else if (lower == Interval::minorThird)
        {
            if (upper == Interval::perfectFourth)
                return Triad::rootlessDominant;
            else if (upper == Interval::tritone)
                return Triad::diminished;
            else if (upper == Interval::perfectFifth)
                return Triad::minor;
            else if (upper == Interval::minorSixth)
                return Triad::majorFirstInv;
            else if (upper == Interval::majorSixth)
                return Triad::diminishedFirstInv;
            else if (upper == Interval::minorSeventh)
                return Triad::min7;
            else
                return Triad::unknown;
        }
        else if (lower == Interval::majorThird)
        {
            if (upper == Interval::perfectFifth)
                return Triad::major;
            else if (upper == Interval::minorSixth)
                return Triad::augmented;
            else if (upper == Interval::majorSixth)
                return Triad::minorFirstInv;
            else if (upper == Interval::minorSeventh)
                return Triad::rootedDominant;
            else
                return Triad::unknown;
        }
        else if (lower == Interval::perfectFourth)
        {
            if (upper == Interval::perfectFifth)
                return Triad::sus4;
            else if (upper == Interval::minorSixth)
                return Triad::minorSecondInv;
            else if (upper == Interval::minorSixth)
                return Triad::minorSecondInv;
            else if (upper == Interval::majorSixth)
                return Triad::majorSecondInv;
            else if (upper == Interval::minorSeventh)
                return Triad::quartal;
            else
                return Triad::unknown;
        }
        else if (lower == Interval::tritone)
        {
            if (upper == Interval::minorSixth)
                return Triad::rootedDominantFirstInv;
            else if (upper == Interval::majorSixth)
                return Triad::diminishedSecondInv;
            else
                return Triad::unknown;
        }
        else if (lower == Interval::perfectFifth)
        {
            if (upper == Interval::majorSixth)
                return Triad::min7FirstInv;
            else if (upper == Interval::minorSeventh)
                return Triad::rootlessDominantSecondInv;
            else
                return Triad::unknown;
        }
        else
            return Triad::unknown;
    }
}

int main()
{
    Note a3      = Note::A3;
    Note csharp3 = Note::CSharp3;
    Note e3      = Note::E3;
    Chord::Triad chord = Chord::determineChord(a3, csharp3, e3);
    return 0;
}