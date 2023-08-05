include(Compiler/GHS)

set(CMAKE_CXX_VERBOSE_FLAG "-v")
set(CMAKE_CXX_OUTPUT_EXTENSION ".o")

string(APPEND CMAKE_CXX_FLAGS_INIT " ")
string(APPEND CMAKE_CXX_FLAGS_DEBUG_INIT " -Odebug -g")
string(APPEND CMAKE_CXX_FLAGS_MINSIZEREL_INIT " -Ospace")
string(APPEND CMAKE_CXX_FLAGS_RELEASE_INIT " -O")
string(APPEND CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT " -O -g")
