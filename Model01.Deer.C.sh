#!/bin/bash

cd /home/pi/SensorFusion/

source SF-env/bin/activate

cd /home/pi/SensorFusion/PreLoadedModels/Model01.Deer/

python3 TFLite_detection_webcam.py --modeldir=Sample_TFLite_model --edgetpu

