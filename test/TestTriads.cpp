#include <../vendor/catch2/catch.hpp>
#include <iostream>
#include <string>

TEST_CASE("Description of test", "[jacobs-ladder][test]")
{
    SECTION("Create a section within a test case that can fail independently")
    {
        REQUIRE(true);
    }
}