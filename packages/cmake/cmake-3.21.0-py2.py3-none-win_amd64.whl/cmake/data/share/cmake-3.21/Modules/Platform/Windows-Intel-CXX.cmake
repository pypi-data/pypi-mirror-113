include(Platform/Windows-Intel)
set(_COMPILE_CXX " /TP")
__windows_compiler_intel(CXX)

set(CMAKE_DEPFILE_FLAGS_CXX "-QMMD -QMT <DEP_TARGET> -QMF <DEP_FILE>")
set(CMAKE_CXX_DEPFILE_FORMAT gcc)

if(CMAKE_GENERATOR MATCHES "^Ninja")
  if(_CMAKE_NINJA_VERSION VERSION_LESS 1.9)
    # This ninja version is too old to support the Intel depfile format.
    # Fall back to msvc depfile format.
    set(CMAKE_DEPFILE_FLAGS_CXX "/showIncludes")
    set(CMAKE_CXX_DEPFILE_FORMAT msvc)
  endif()
endif()

if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
    AND CMAKE_GENERATOR MATCHES "Makefiles|WMake")
  # dependencies are computed by the compiler itself
 set(CMAKE_CXX_DEPENDS_USE_COMPILER TRUE)
endif()

if("${CMAKE_SOURCE_DIR}${CMAKE_BINARY_DIR}" MATCHES " ")
  # The Intel compiler does not properly escape spaces in a depfile.
  # Fall back to msvc depfile format.
  set(CMAKE_DEPFILE_FLAGS_CXX "/showIncludes")
  set(CMAKE_CXX_DEPFILE_FORMAT msvc)
endif()
