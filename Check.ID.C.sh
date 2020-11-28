#!/bin/bash

cd /home/pi/checkid

source checkid-env/bin/activate

python3 TFLite_detection_webcam.py --modeldir=Sample_TFLite_model --edgetpu