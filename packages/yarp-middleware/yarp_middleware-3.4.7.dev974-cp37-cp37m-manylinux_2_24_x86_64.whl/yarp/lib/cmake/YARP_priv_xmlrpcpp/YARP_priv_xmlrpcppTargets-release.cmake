#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "YARP::YARP_priv_xmlrpcpp" for configuration "Release"
set_property(TARGET YARP::YARP_priv_xmlrpcpp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::YARP_priv_xmlrpcpp PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libYARP_priv_xmlrpcpp.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::YARP_priv_xmlrpcpp )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::YARP_priv_xmlrpcpp "${_IMPORT_PREFIX}/lib/libYARP_priv_xmlrpcpp.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
