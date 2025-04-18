// Avoid max/min namespace collisions with <windows.h>
#ifndef NOMINMAX
#define NOMINMAX
#endif

#ifndef MATH_UTILS_H
#define MATH_UTILS_H

// #include <climits>
#include <cmath>
#include <iterator>
#include <limits>
#include <type_traits>
#include <utility>

// Avoid max/min namespace collisions with <windows.h>
#undef max
#undef min

namespace MathUtils {

    template <class I, class F>
    constexpr I
    FpFloor (F x)
    {
        return 
            x >= F (std::numeric_limits<I>::max())
            ? std::numeric_limits<I>::max()
            : x <= F (std::numeric_limits<I>::min())
            ? std::numeric_limits<I>::min()
            : I (std::floor(x));
    }

} // Namespace

#endif // MATH_UTILS_H