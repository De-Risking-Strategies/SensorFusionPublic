#!/bin/bash

#Pushkar Khairnar

sudo cp /home/pi/Seekware_SDK_3.6.0.0/driver/udev/10-seekthermal.rules /etc/udev/rules.d

sudo udevadm control --reload

sudo apt-get install libusb-1.0.0-dev

sudo apt-get install libsdl2-dev

sudo cp /home/pi/Seekware_SDK_3.6.0.0/lib/armv7a-neon-vfpv4-linux-gnueabihf/libseekware.so.3.6 /usr/lib

sudo cp /home/pi/Seekware_SDK_3.6.0.0/lib/armv7a-neon-vfpv4-linux-gnueabihf/libseekware.so /usr/lib

sudo cp /home/pi/Seekware_SDK_3.6.0.0/include/seekware/seekware.h /usr/include

cd /home/pi/Seekware_SDK_3.6.0.0/bin/armv7a-neon-vfpv4-linux-gnueabihf

sudo chmod +x *

#./seekware-sdl