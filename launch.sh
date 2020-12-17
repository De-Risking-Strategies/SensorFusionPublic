#!/usr/bin/python3

python3 -mwebbrowser http://localhost:5000

cd /home/pi/SensorFusion/Demo90

source Demo90-env/bin/activate

python3 TFLite_detection_webcam_api.py --modeldir=Sample_TFLite_model --edgetpu

