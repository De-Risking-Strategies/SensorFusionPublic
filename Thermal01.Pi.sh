#!/bin/bash

cd /home/pi/SensorFusion/

source SF-env/bin/activate

cd /home/pi/SensorFusion/thermal01/

python3 simpleVideoCamera.py --modeldir=Sample_TFLite_model