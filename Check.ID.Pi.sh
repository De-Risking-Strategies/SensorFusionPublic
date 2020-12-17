#!/bin/bash

cd /home/pi/SensorFusion/checkid

source checkid-env/bin/activate

python3 TFLite_detection_webcam_old.py --modeldir=Sample_TFLite_model