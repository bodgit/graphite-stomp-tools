cmake_minimum_required(VERSION 2.8.8)

project(graphite-stomp-tools C)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -Wshadow -Wpointer-arith -Wcast-qual -Wsign-compare")
set(CMAKE_INCLUDE_CURRENT_DIR ON)

include(FindBISON)
include(FindPkgConfig)
pkg_check_modules(EVENT REQUIRED libevent_openssl>=2)
pkg_check_modules(OPENSSL REQUIRED openssl)
pkg_check_modules(PCRE REQUIRED libpcre)

find_program(GZIP_TOOL
	NAMES gzip
	PATHS /usr/local/bin /usr/bin /bin)

include(CheckStructHasMember)

set(CMAKE_EXTRA_INCLUDE_FILES sys/types.h netinet/in.h sys/socket.h)

check_struct_has_member("struct sockaddr" sa_len
	"${CMAKE_EXTRA_INCLUDE_FILES}" HAVE_STRUCT_SOCKADDR_SA_LEN)
check_struct_has_member("struct sockaddr_in" sin_len
	"${CMAKE_EXTRA_INCLUDE_FILES}" HAVE_STRUCT_SOCKADDR_IN_SIN_LEN)
check_struct_has_member("struct sockaddr_in6" sin6_len
	"${CMAKE_EXTRA_INCLUDE_FILES}" HAVE_STRUCT_SOCKADDR_IN6_SIN6_LEN)

set(CMAKE_EXTRA_INCLUDE_FILES)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.h.in ${CMAKE_CURRENT_BINARY_DIR}/config.h)

# Only on Linux
if(CMAKE_SYSTEM_NAME STREQUAL Linux)
	add_definitions(-D_GNU_SOURCE)
endif()

set(PROJECT_VERSION "0.1")
set(ARCHIVE_NAME ${CMAKE_PROJECT_NAME}-${PROJECT_VERSION})
add_custom_target(dist
	COMMAND python git-archive-all/git-archive-all --prefix=${ARCHIVE_NAME}/
		${CMAKE_BINARY_DIR}/${ARCHIVE_NAME}.tar.gz
	WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

include_directories(
	${CMAKE_CURRENT_BINARY_DIR}
	${CMAKE_CURRENT_SOURCE_DIR}/common
	${CMAKE_CURRENT_SOURCE_DIR}/stomp
	${CMAKE_CURRENT_SOURCE_DIR}/graphite
	${EVENT_INCLUDE_DIRS}
	${OPENSSL_INCLUDE_DIRS}
	${PCRE_INCLUDE_DIRS}
)

link_directories(
	${EVENT_LIBRARY_DIRS}
	${OPENSSL_LIBRARY_DIRS}
	${PCRE_LIBRARY_DIRS}
)

add_subdirectory(common)
add_subdirectory(stomp)
add_subdirectory(graphite)
add_subdirectory(enqueue)
add_subdirectory(dequeue)
add_subdirectory(rewrite)
