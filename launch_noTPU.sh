#!/usr/bin/python3

cd /home/pi/SensorFusion/

source SF-env/bin/activate

cd /home/pi/SensorFusion/Demo90

python3 TFLite_detection_webcam_api.py --modeldir=Sample_TFLite_model |& python3 -mwebbrowser http://localhost:5000
