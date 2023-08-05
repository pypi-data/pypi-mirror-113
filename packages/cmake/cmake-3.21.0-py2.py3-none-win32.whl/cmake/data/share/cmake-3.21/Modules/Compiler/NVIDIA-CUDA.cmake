include(Compiler/CMakeCommonCompilerMacros)

set(CMAKE_CUDA_COMPILER_HAS_DEVICE_LINK_PHASE True)
set(CMAKE_CUDA_VERBOSE_FLAG "-v")
set(CMAKE_CUDA_VERBOSE_COMPILE_FLAG "-Xcompiler=-v")

set(_CMAKE_COMPILE_AS_CUDA_FLAG "-x cu")
set(_CMAKE_CUDA_PTX_FLAG "-ptx")
set(_CMAKE_CUDA_DEVICE_CODE "-dc")

if (CMAKE_CUDA_COMPILER_VERSION VERSION_GREATER_EQUAL 10.2.89)
  # The -forward-unknown-to-host-compiler flag was only
  # added to nvcc in 10.2 so before that we had no good
  # way to invoke the CUDA compiler and propagate unknown
  # flags such as -pthread to the host compiler
  set(_CMAKE_CUDA_EXTRA_FLAGS "-forward-unknown-to-host-compiler")
else()
  set(_CMAKE_CUDA_EXTRA_FLAGS "")
endif()

if(CMAKE_CUDA_COMPILER_VERSION VERSION_GREATER_EQUAL "8.0.0")
  set(_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS "-Wno-deprecated-gpu-targets")
else()
  set(_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS "")
endif()

if(CMAKE_CUDA_HOST_COMPILER AND NOT CMAKE_GENERATOR MATCHES "Visual Studio")
  string(APPEND _CMAKE_CUDA_EXTRA_FLAGS " -ccbin=<CMAKE_CUDA_HOST_COMPILER>")
endif()

if (CMAKE_CUDA_COMPILER_VERSION VERSION_GREATER_EQUAL 10.2.89)
  # The -MD flag was only added to nvcc in 10.2 so
  # before that we had to invoke the compiler twice
  # to get header dependency information
  set(CMAKE_DEPFILE_FLAGS_CUDA "-MD -MT <DEP_TARGET> -MF <DEP_FILE>")
else()
  set(CMAKE_CUDA_DEPENDS_EXTRA_COMMANDS "<CMAKE_CUDA_COMPILER> ${_CMAKE_CUDA_EXTRA_FLAGS} <DEFINES> <INCLUDES> <FLAGS> ${_CMAKE_COMPILE_AS_CUDA_FLAG} -M <SOURCE> -MT <OBJECT> -o <DEP_FILE>")
endif()
set(CMAKE_CUDA_DEPFILE_FORMAT gcc)
if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
    AND CMAKE_GENERATOR MATCHES "Makefiles|WMake")
  set(CMAKE_CUDA_DEPENDS_USE_COMPILER TRUE)
endif()

if(NOT "x${CMAKE_CUDA_SIMULATE_ID}" STREQUAL "xMSVC")
  set(CMAKE_CUDA_COMPILE_OPTIONS_PIE -Xcompiler=-fPIE)
  set(CMAKE_CUDA_COMPILE_OPTIONS_PIC -Xcompiler=-fPIC)
  set(CMAKE_CUDA_COMPILE_OPTIONS_VISIBILITY -Xcompiler=-fvisibility=)
  # CMAKE_SHARED_LIBRARY_CUDA_FLAGS is sent to the host linker so we
  # don't need to forward it through nvcc.
  set(CMAKE_SHARED_LIBRARY_CUDA_FLAGS -fPIC)
  string(APPEND CMAKE_CUDA_FLAGS_INIT " ")
  string(APPEND CMAKE_CUDA_FLAGS_DEBUG_INIT " -g")
  string(APPEND CMAKE_CUDA_FLAGS_RELEASE_INIT " -O3 -DNDEBUG")
  string(APPEND CMAKE_CUDA_FLAGS_MINSIZEREL_INIT " -O1 -DNDEBUG")
  string(APPEND CMAKE_CUDA_FLAGS_RELWITHDEBINFO_INIT " -O2 -g -DNDEBUG")
endif()
set(CMAKE_SHARED_LIBRARY_CREATE_CUDA_FLAGS -shared)
set(CMAKE_INCLUDE_SYSTEM_FLAG_CUDA -isystem=)

if (CMAKE_CUDA_SIMULATE_ID STREQUAL "GNU")
  set(CMAKE_CUDA_LINKER_WRAPPER_FLAG "-Wl,")
  set(CMAKE_CUDA_LINKER_WRAPPER_FLAG_SEP ",")
elseif(CMAKE_CUDA_SIMULATE_ID STREQUAL "Clang")
  set(CMAKE_CUDA_LINKER_WRAPPER_FLAG "-Xlinker" " ")
  set(CMAKE_CUDA_LINKER_WRAPPER_FLAG_SEP)
endif()

set(CMAKE_CUDA_DEVICE_COMPILER_WRAPPER_FLAG "-Xcompiler=")
set(CMAKE_CUDA_DEVICE_COMPILER_WRAPPER_FLAG_SEP ",")
set(CMAKE_CUDA_DEVICE_LINKER_WRAPPER_FLAG "-Xlinker=")
set(CMAKE_CUDA_DEVICE_LINKER_WRAPPER_FLAG_SEP ",")

set(CMAKE_CUDA_RUNTIME_LIBRARY_LINK_OPTIONS_STATIC  "cudadevrt;cudart_static")
set(CMAKE_CUDA_RUNTIME_LIBRARY_LINK_OPTIONS_SHARED  "cudadevrt;cudart")
set(CMAKE_CUDA_RUNTIME_LIBRARY_LINK_OPTIONS_NONE    "")

if(UNIX AND NOT (CMAKE_SYSTEM_NAME STREQUAL "QNX"))
  list(APPEND CMAKE_CUDA_RUNTIME_LIBRARY_LINK_OPTIONS_STATIC "rt" "pthread" "dl")
endif()

if("x${CMAKE_CUDA_SIMULATE_ID}" STREQUAL "xMSVC")
  # MSVC requires c++14 as the minimum level
  set(CMAKE_CUDA03_STANDARD_COMPILE_OPTION "")
  set(CMAKE_CUDA03_EXTENSION_COMPILE_OPTION "")

  # MSVC requires c++14 as the minimum level
  set(CMAKE_CUDA11_STANDARD_COMPILE_OPTION "")
  set(CMAKE_CUDA11_EXTENSION_COMPILE_OPTION "")

  if (NOT CMAKE_CUDA_COMPILER_VERSION VERSION_LESS 9.0)
    if(CMAKE_CUDA_SIMULATE_VERSION VERSION_GREATER_EQUAL 19.10.25017)
      set(CMAKE_CUDA14_STANDARD_COMPILE_OPTION "-std=c++14")
      set(CMAKE_CUDA14_EXTENSION_COMPILE_OPTION "-std=c++14")
    else()
      set(CMAKE_CUDA14_STANDARD_COMPILE_OPTION "")
      set(CMAKE_CUDA14_EXTENSION_COMPILE_OPTION "")
    endif()
  endif()

  if (NOT CMAKE_CUDA_COMPILER_VERSION VERSION_LESS 11.0)
    if(CMAKE_CUDA_SIMULATE_VERSION VERSION_GREATER_EQUAL 19.11.25505)
      set(CMAKE_CUDA17_STANDARD_COMPILE_OPTION "-std=c++17")
      set(CMAKE_CUDA17_EXTENSION_COMPILE_OPTION "-std=c++17")
    endif()
  endif()

else()
  set(CMAKE_CUDA03_STANDARD_COMPILE_OPTION "")
  set(CMAKE_CUDA03_EXTENSION_COMPILE_OPTION "")

  set(CMAKE_CUDA11_STANDARD_COMPILE_OPTION "-std=c++11")
  set(CMAKE_CUDA11_EXTENSION_COMPILE_OPTION "-std=c++11")

  if (NOT CMAKE_CUDA_COMPILER_VERSION VERSION_LESS 9.0)
    set(CMAKE_CUDA03_STANDARD_COMPILE_OPTION "-std=c++03")
    set(CMAKE_CUDA03_EXTENSION_COMPILE_OPTION "-std=c++03")
    set(CMAKE_CUDA14_STANDARD_COMPILE_OPTION "-std=c++14")
    set(CMAKE_CUDA14_EXTENSION_COMPILE_OPTION "-std=c++14")
  endif()

  if (NOT CMAKE_CUDA_COMPILER_VERSION VERSION_LESS 11.0)
    set(CMAKE_CUDA17_STANDARD_COMPILE_OPTION "-std=c++17")
    set(CMAKE_CUDA17_EXTENSION_COMPILE_OPTION "-std=c++17")
  endif()

endif()

# FIXME: investigate use of --options-file.
# Tell Makefile generator that nvcc does not support @<rspfile> syntax.
set(CMAKE_CUDA_USE_RESPONSE_FILE_FOR_INCLUDES 0)
set(CMAKE_CUDA_USE_RESPONSE_FILE_FOR_LIBRARIES 0)
set(CMAKE_CUDA_USE_RESPONSE_FILE_FOR_OBJECTS 0)

if (CMAKE_CUDA_COMPILER_VERSION VERSION_GREATER_EQUAL "9.0")
  set(CMAKE_CUDA_RESPONSE_FILE_DEVICE_LINK_FLAG "--options-file ")
  set(CMAKE_CUDA_RESPONSE_FILE_FLAG "--options-file ")
endif()

__compiler_check_default_language_standard(CUDA 6.0 03)
