#ifndef TRIADS_H
#define TRIADS_H

// file includes
#include <iostream>
#include <string>

//project includes
#include "Notes.h"
#include "Intervals.h"

namespace Chord
{

enum class Triad : int
{                                     // Examples:
    major                       = 0,  // C  E  G  (4,7)
    minor                       = 1,  // C  Eb G  (3,7)
    augmented                   = 2,  // C  E  Ab (4,8) (note that there are no inversions for aumented chords since they produce the same intervals)
    diminished                  = 3,  // C  Eb Gb (3,6)
    sus2                        = 4,  // C  D  G  (2,7)
    sus4                        = 5,  // C  F  G  (5,7)
    rootlessDominant            = 6,  // C  Eb F  (3,5)
    rootedDominant              = 7,  // C  E  Bb (4,10)
    min7                        = 8,  // C  Eb Bb (3,10)
    majorFirstInv               = 9,  // E  G  C  (3,8)
    majorSecondInv              = 10, // G  C  E  (5,9)
    minorFirstInv               = 11, // Eb G  C  (4,9)
    minorSecondInv              = 12, // G  C  Eb (5,8)
    diminishedFirstInv          = 13, // Eb Gb C  (3,9)
    diminishedSecondInv         = 14, // Gb C  Eb (6,9)
    quartal                     = 15, // D  G  C  (5,10) (note that the only inversion for sus2 and sus4 is quartal since sus2 2nd inversion is sus4)
    rootlessDominantFirstInv    = 16, // Eb F  C  (2,9)  (pretty cool sound)
    rootlessDominantSecondInv   = 17, // F  C  Eb (7,10)
    rootedDominantFirstInv      = 18, // E  Bb C  (6,8)
    rootedDominantSecondInv     = 19, // Bb C  E  (2,6)
    min7FirstInv                = 20, // Eb Bb C  (7,9)
    min7SecondInv               = 21, // Bb C  Eb (2,5)
    unknown                     = 22  // unknown chord
};


    Triad determineChord(Note bass, Note tenor, Note treble);

}



#endif // TRIADS_H