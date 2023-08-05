set(YARP_sig_VERSION 3.4.102+20210714.14+gitbac699cb6)


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was YARP_sigConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

####################################################################################

#### Expanded from @PACKAGE_DEPENDENCIES@ by install_basic_package_files() ####

include(CMakeFindDependencyMacro)
find_dependency(YARP_conf HINTS "${CMAKE_CURRENT_LIST_DIR}/.." NO_DEFAULT_PATH)
find_dependency(YARP_os HINTS "${CMAKE_CURRENT_LIST_DIR}/.." NO_DEFAULT_PATH)
find_dependency(ACE)
find_dependency(ZLIB)

###############################################################################


include("${CMAKE_CURRENT_LIST_DIR}/YARP_sigTargets.cmake")




