#!/bin/bash

cd /home/pi/SensorFusion/

source SF-env/bin/activate

cd /home/pi/SensorFusion/checkid

python3 TFLite_detection_webcam_old.py --modeldir=Sample_TFLite_model