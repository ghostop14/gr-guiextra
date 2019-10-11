INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_GUIEXTRA guiextra)

FIND_PATH(
    GUIEXTRA_INCLUDE_DIRS
    NAMES guiextra/api.h
    HINTS $ENV{GUIEXTRA_DIR}/include
        ${PC_GUIEXTRA_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GUIEXTRA_LIBRARIES
    NAMES gnuradio-guiextra
    HINTS $ENV{GUIEXTRA_DIR}/lib
        ${PC_GUIEXTRA_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/guiextraTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GUIEXTRA DEFAULT_MSG GUIEXTRA_LIBRARIES GUIEXTRA_INCLUDE_DIRS)
MARK_AS_ADVANCED(GUIEXTRA_LIBRARIES GUIEXTRA_INCLUDE_DIRS)
