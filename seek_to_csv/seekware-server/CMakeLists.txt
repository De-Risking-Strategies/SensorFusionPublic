#Version-------------------------------------------------------------------------------------------------------------------#

#Sources-------------------------------------------------------------------------------------------------------------------#

set(SOURCES 
	src/seekware-server.c
)

#Project-------------------------------------------------------------------------------------------------------------------#

project(seekware-server DESCRIPTION "Seekware SDK Library")

#Targets-------------------------------------------------------------------------------------------------------------------#

set(TOOLCHAIN_DIR 
	armv7a-neon-vfpv4-linux-gnueabihf
)

add_executable(${PROJECT_NAME} ${SOURCES})

#add_library(seekware, SOURCES)

set_target_properties(${PROJECT_NAME} PROPERTIES 
	IMPORTED_LOCATION .${CMAKE_SOURCE_DIR}/../../lib/${TOOLCHAIN_DIR})

#Dependencies---------------------------------------------------------------------------------------------------------------#

#Extra Compile Options------------------------------------------------------------------------------------------------------#

#Include--------------------------------------------------------------------------------------------------------------------#

include_directories(
	${CMAKE_CURRENT_SOURCE_DIR}/include
)

#Link------------------------------------------------------------------------------------------------------------------------#

#seekware
target_link_libraries(${PROJECT_NAME} seekware)

link_directories(
	${CMAKE_CURRENT_SOURCE_DIR}/../../../lib/${TOOLCHAIN_DIR}
)


if(UNIX)
	target_link_libraries(${PROJECT_NAME} m)
endif()

#librt
if(NEEDS_LIBRT)
	target_link_libraries(${PROJECT_NAME} rt)
endif()

#Runtime Dependencies--------------------------------------------------------------------------------------------------------#

if(MSVC)
	get_target_property(SEEKWARE_IMPORT seekware IMPORTED)
	if(SEEKWARE_IMPORT)
		add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
			COMMAND ${CMAKE_COMMAND} -E copy_if_different
			$<TARGET_FILE_DIR:seekware>/seekware.dll
			$<TARGET_FILE_DIR:${PROJECT_NAME}>/seekware.dll
		)
	endif()
	add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
		COMMAND ${CMAKE_COMMAND} -E copy_if_different
		$<TARGET_FILE_DIR:usb-1.0>/libusb-1.0.dll
		$<TARGET_FILE_DIR:${PROJECT_NAME}>/libusb-1.0.dll
	)
endif()

#Install---------------------------------------------------------------------------------------------------------------------#

install(TARGETS ${PROJECT_NAME} DESTINATION bin)

file(GLOB SRC ${CMAKE_CURRENT_LIST_DIR}/src/*)
install(FILES ${SRC} DESTINATION src/${PROJECT_NAME}/src)

file(GLOB INC ${CMAKE_CURRENT_LIST_DIR}/include/*)
install(FILES ${INC} DESTINATION src/${PROJECT_NAME}/include)

install(FILES ${CMAKE_CURRENT_LIST_DIR}/Makefile DESTINATION src/${PROJECT_NAME})


