/*
 * 2020-10-31
 * modified to add a socket parameter to which 16-bit grayscale 
 * PNGs will be sent.
 *
 *
 *
 *
 *
 */

/*Copyright (c) [2019] [Seek Thermal, Inc.]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The Software may only be used in combination with Seek cores/products.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *
 * Project:     Seek Thermal SDK Demo
 * Purpose:     Demonstrates how to communicate with Seek Thermal Cameras
 * Author:      Seek Thermal, Inc.
 *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <signal.h>
#include <math.h>
#include <time.h>

#include <netdb.h> 
#include <netinet/in.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#include <sys/types.h> 
#include <unistd.h>
#define MAX 80 
#define PORT 8081 
#define SA struct sockaddr 


#ifdef _WIN32
#include <windows.h>
#include <winnt.h>
#define inline __inline
#endif

#if defined(__linux__) || defined(__APPLE__)
#include <sys/time.h>
#endif

//#include <seekware/seekware.h>
#include <seekware.h>

#define NUM_CAMS            	5
#define LOG_THERMOGRAPHY_DATA	true

bool exit_requested = false;
float* thermography_data = NULL;
uint16_t* filtered_data = NULL;
int16_t* thermography_data_fixedpoint = NULL;
int thermography_data_fixedpoint_buffer_length = 0;

struct sockaddr_in servaddr; 



psw camera = NULL;
psw camera_list[NUM_CAMS];
sw_sdk_info sdk_info;
int num_cameras_found = 0;
size_t camera_pixels = 0;




static inline double wall_clock_s(void) {
#ifdef _WIN32
	LARGE_INTEGER time;
	LARGE_INTEGER freq;
	QueryPerformanceFrequency(&freq);
	QueryPerformanceCounter(&time);
	return (double)time.QuadPart / freq.QuadPart;
#else
	struct timeval time;
	gettimeofday(&time, NULL);
	return (double)time.tv_sec + (double)time.tv_usec * .000001;
#endif
}

static inline void print_fw_info(psw camera)
{
    sw_retcode status; 
    int therm_ver;

    printf("Model Number:%s\n",camera->modelNumber);
    printf("SerialNumber: %s\n", camera->serialNumber);
    printf("Manufacture Date: %s\n", camera->manufactureDate);

    printf("Firmware Version: %u.%u.%u.%u\n",
            camera->fw_version_major,
			camera->fw_version_minor,
            camera->fw_build_major,
			camera->fw_build_minor);

	status = Seekware_GetSettingEx(camera, SETTING_THERMOGRAPHY_VERSION, &therm_ver, sizeof(therm_ver));
	if (status != SW_RETCODE_NONE) {
		fprintf(stderr, "Error: Seek GetSetting returned %i\n", status);
	}
    printf("Themography Version: %i\n", therm_ver);

	sw_sdk_info sdk_info;
	Seekware_GetSdkInfo(NULL, &sdk_info);
	printf("Image Processing Version: %u.%u.%u.%u\n",
		sdk_info.lib_version_major,
		sdk_info.lib_version_minor,
		sdk_info.lib_build_major,
		sdk_info.lib_build_minor);

	printf("\n");
    fflush(stdout);
}

static void signal_callback(int signum)
{
    printf("Exit requested!\n");
    exit_requested = true;
}

int OpenServerSocket(int portnumber)
{
    int sockfd; 
  
    // socket create and verification 
    sockfd = socket(AF_INET, SOCK_STREAM, 0); 
    if (sockfd == -1) { 
        printf("socket creation failed...\n"); 
        exit(0); 
    } 
    else
        printf("Socket successfully created..\n"); 
    bzero(&servaddr, sizeof(servaddr)); 
  
    // assign IP, PORT 
    servaddr.sin_family = AF_INET; 
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY); 
    servaddr.sin_port = htons(portnumber); 
  
    // Binding newly created socket to given IP and verification 
    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) { 
        printf("socket bind failed...\n"); 
        exit(0); 
    } 
    else
        printf("Socket successfully bound to port %d..\n",portnumber); 
  
    // Now server is ready to listen and verification 
    if ((listen(sockfd, 5)) != 0) { 
        printf("Listen failed...\n"); 
        exit(0); 
    } 
    else
        printf("Server listening..\n"); 

    return sockfd;
}


sw_retcode FindCameras()
{
	sw_retcode status;
	status = Seekware_Find(camera_list, NUM_CAMS, &num_cameras_found);
	if (status != SW_RETCODE_NONE || num_cameras_found == 0) {
		printf("Cannot find any cameras...exiting\n");
		return 1;
	}

	camera = camera_list[0];
	status = Seekware_Open(camera);
	if (status != SW_RETCODE_NONE) {
		fprintf(stderr, "Cannot open camera : %d\n", status);
		status = 1;
	}

	// Must read firmware info AFTER the camera has been opened
	printf("::Camera Firmware Info::\n");
	print_fw_info(camera);

	return status;
}



int InitCameraDataVariables(psw camera)
{
    int result = 0;
    if (0 == result)
    {
    	camera_pixels = (size_t)camera->frame_cols * (size_t)camera->frame_rows;
	}
    
	//Allocate buffers for holding thermal data
	thermography_data = (float*)malloc(camera_pixels * sizeof(float));
	if (thermography_data == NULL) {
		fprintf(stderr, "Cannot allocate thermography buffer!\n");
		result = 1;
	}
    if (0 == result)
    {
	    filtered_data = (uint16_t*)malloc((camera_pixels + camera->frame_cols) * sizeof(uint16_t));
	    if (filtered_data == NULL) {
		    fprintf(stderr, "Cannot allocate filtered buffer!\n");
    		result = 1;
	    }
	}
	
    if (0 == result)
    {
	    thermography_data_fixedpoint_buffer_length = camera_pixels * sizeof(int16_t);
	    thermography_data_fixedpoint = (int16_t*)malloc(thermography_data_fixedpoint_buffer_length);
	    if (thermography_data_fixedpoint == NULL) {
		    fprintf(stderr, "Cannot allocate thermography_data_fixedpoint buffer!\n");
    		result = 1;
	    }
    }
	return result;
}


int main(int argc, char * argv [])
{
	// keep socket state info in these variables
    int sockfd, connfd, len; 
    struct sockaddr_in servaddr, cli; 

	double start = 0.0f;
	double stop = 0.0f;
	double frametime = 0.0f;
	double framerate = 0.0f;

	float spot = 0;
	float min = 0;
	float max = 0;
	float timestamp_s = 0.0f;

	uint32_t field_count = 0;
	uint32_t enable = 1;
	uint64_t timestamp_us = 0;
	uint64_t frame_count = 0;

	sw_retcode status;

	signal(SIGINT, signal_callback);
	signal(SIGTERM, signal_callback);

	printf("seekware-server - A simple data capture/server utility for Seek Thermal cameras\n\n");

	sockfd = OpenServerSocket(54339); // TODO: read from cmd args
        len = sizeof(cli); 

	do
	{
    	// Accept the data packet from client and verification 
	    connfd = accept(sockfd, (SA*)&cli, &len); 
	    if (connfd < 0) 
	    { 
	        printf("server acccept failed...\n"); 
	        exit(0); 
	    } 
	    else
	    {
	        printf("server acccepting the client connection...\n"); 
	    }

	    Seekware_GetSdkInfo(NULL, &sdk_info);
	    printf("SDK Version: %u.%u\n\n", sdk_info.sdk_version_major, sdk_info.sdk_version_minor);

	    status = FindCameras();

	    int initOK = InitCameraDataVariables(camera);
        if (0 != initOK)
        {
            goto cleanup;
        }
	    Seekware_SetSettingEx(camera, SETTING_ENABLE_TIMESTAMP, &enable, sizeof(enable));
	    Seekware_SetSettingEx(camera, SETTING_RESET_TIMESTAMP, &enable, sizeof(enable));

	    start = wall_clock_s();

	    /* * * * * * * * * * * * * Data Capture Loop * * * * * * * * * * * * * * */
        int finishedSocketSession = 0;
	    do {
		    //printf("Waiting for request...\n");
	        char cmdBuffer[16];
	        memset(cmdBuffer, 0, sizeof(cmdBuffer));
	        int readCount = read(connfd, cmdBuffer, sizeof(cmdBuffer)-1);
		    //printf("Got %d bytes...\n", readCount);
	        cmdBuffer[readCount] = '\0';
	        if ((readCount < 4) ||
	            (strstr(cmdBuffer, "THERM") == 0))
	        {
		        printf("unrecognized request: '%s'\n", cmdBuffer);
	            continue;
            }

		    //printf("Calling GetImageEx ...\n");
	    
		    status = Seekware_GetImageEx(camera, filtered_data, thermography_data, NULL);
		    if (status == SW_RETCODE_NOFRAME) {
			    printf("Seek Camera Timeout ...\n");
		    }
		    if (status == SW_RETCODE_DISCONNECTED) {
			    printf("Seek Camera Disconnected ...\n");
		    }
		    if (status != SW_RETCODE_NONE) {
			    printf("Seek Camera Error : %u ...\n", status);
			    break;
		    }

		    //status = Seekware_GetSpot(camera, &spot, &min, &max);
		    //if (status != SW_RETCODE_NONE) {
			//    break;
		    //}

		    ++frame_count;

		    // Calculate the frame rate
		    stop = wall_clock_s();
		    frametime = stop - start;
		    framerate = (1 / frametime);
		    start = wall_clock_s();

		    //Writes every thermography frame to the socket
    
		    //printf("Converting to fixed-point image data ...\n");
            int index = 0;
		    for (uint16_t i = 0; i < camera->frame_rows; ++i) 
	        {
			    for (uint16_t j = 0; j < camera->frame_cols; ++j) 
			    {
				    float value = thermography_data[(i * camera->frame_cols) + j];
				    float rounded_value = roundf(100.0f * value);
				    thermography_data_fixedpoint[index++] = (int16_t)rounded_value;
			    }
		    }

            // Extract telemetry data
            //field_count = *(uint32_t*)&filtered_data[camera_pixels];
            //timestamp_us = *(uint64_t*)& filtered_data[camera_pixels + 5];
            //timestamp_s = (float)timestamp_us / 1.0e6f;

            //printf("sending length of image data = %d ...\n",thermography_data_fixedpoint_buffer_length);
            int bytesWritten = 0;
            uint32_t structureLength = thermography_data_fixedpoint_buffer_length;
            bytesWritten = write(connfd, &structureLength, 
                                    sizeof(structureLength));
            //printf("sent image length data, bytesWritten=%d...\n",bytesWritten);
            if (bytesWritten > 0)
            {		     
                //printf("sending image data ...\n");
                bytesWritten = write(connfd, thermography_data_fixedpoint, 
                                     thermography_data_fixedpoint_buffer_length);
            }
            //printf("sent image data, bytesWritten=%d...\n",bytesWritten);
            finishedSocketSession = (bytesWritten < 0);

	    } while (!exit_requested && (0 == finishedSocketSession));
    } while (!exit_requested);
    
/* * * * * * * * * * * * * Cleanup * * * * * * * * * * * * * * */
cleanup:
	
	printf("Exiting...\n");

	if (camera != NULL) {
		Seekware_Close(camera);
	}

	if (thermography_data != NULL) {
		free(thermography_data);
	}

	if (filtered_data != NULL){
		free(filtered_data);
	}

	if (thermography_data_fixedpoint != NULL) {
		free(thermography_data_fixedpoint);
	}

	return 0;
}
