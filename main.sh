#/bashfile

cd /home/pi/Demo90

source Demo90-env/bin/activate

python3 TFLite_detection_webcam_api.py --modeldir=Sample_TFLite_model --edgetpu
