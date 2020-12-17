#/bashfile

cd /home/pi/SensorFusion/Demo90

source Demo90-env/bin/activate

python3 TFLite_detection_webcam.py --modeldir=Sample_TFLite_model

