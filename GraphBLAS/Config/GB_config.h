//------------------------------------------------------------------------------
// GraphBLAS/Config/GB_config.h: JIT configuration for GraphBLAS
//------------------------------------------------------------------------------

// SuiteSparse:GraphBLAS, Timothy A. Davis, (c) 2017-2023, All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0

//------------------------------------------------------------------------------

// The GraphBLAS/Config/GB_config.h file is configured by cmake from
// GraphBLAS/Config/GB_config.h.in.

#ifndef GB_CONFIG_H
#define GB_CONFIG_H

// GB_C_COMPILER: the C compiler used to compile GraphBLAS:
#ifndef GB_C_COMPILER
#define GB_C_COMPILER   "D:/Program Files/Microsoft Visual Studio/2022/Enterprise/VC/Tools/MSVC/14.36.32532/bin/Hostx64/x64/cl.exe"
#endif

// GB_C_FLAGS: the C compiler flags used to compile GraphBLAS.  Used
// for compiling and linking:
#ifndef GB_C_FLAGS
#define GB_C_FLAGS      "/DWIN32 /D_WINDOWS /O2 -wd\"4244\" -wd\"4146\" -wd\"4018\" -wd\"4996\" -wd\"4047\" -wd\"4554\" /O2 /Ob2 /DNDEBUG -openmp "
#endif

// GB_C_LINK_FLAGS: the flags passed to the C compiler for the link phase:
#ifndef GB_C_LINK_FLAGS
#define GB_C_LINK_FLAGS "/machine:x64"
#endif

// GB_LIB_PREFIX: library prefix (lib for Linux/Unix/Mac, empty for Windows):
#ifndef GB_LIB_PREFIX
#define GB_LIB_PREFIX   ""
#endif

// GB_LIB_SUFFIX: library suffix (.so for Linux/Unix, .dylib for Mac, etc):
#ifndef GB_LIB_SUFFIX
#define GB_LIB_SUFFIX   ".dll"
#endif

// GB_OBJ_SUFFIX: object suffix (.o for Linux/Unix/Mac, .obj for Windows):
#ifndef GB_OBJ_SUFFIX
#define GB_OBJ_SUFFIX   ".obj"
#endif

// GB_OMP_INC: -I includes for OpenMP, if in use by GraphBLAS:
#ifndef GB_OMP_INC
#define GB_OMP_INC      ""
#endif

// GB_OMP_INC_DIRS: include directories OpenMP, if in use by GraphBLAS,
// for cmake:
#ifndef GB_OMP_INC_DIRS
#define GB_OMP_INC_DIRS ""
#endif

// GB_C_LIBRARIES: libraries to link with when using direct compile/link:
#ifndef GB_C_LIBRARIES
#define GB_C_LIBRARIES  ""
#endif

// GB_CMAKE_LIBRARIES: libraries to link with when using cmake
#ifndef GB_CMAKE_LIBRARIES
#define GB_CMAKE_LIBRARIES  ""
#endif

#endif

