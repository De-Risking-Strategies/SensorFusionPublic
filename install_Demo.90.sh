#/bashfile

# Install tensorflow object detection API on raspberry pi 4

#sudo apt-get update

#sudo apt-get upgrade

#git clone https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi.git

#mv TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/ Demo90

cd /home/pi/SensorFusion/Demo90

sudo pip3 install virtualenv

python3 -m venv Demo90-env

source Demo90-env/bin/activate

bash get_pi_requirements.sh

#pip3 install tensorflow==1.13.1

wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip

unzip coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip -d Sample_TFLite_model

cd /home/pi/SensorFusion/Demo90

source Demo90-env/bin/activate

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update

sudo apt-get install libedgetpu1-std

sudo apt-get install python3-edgetpu

wget https://dl.google.com/coral/canned_models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite

mv mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite Sample_TFLite_model/edgetpu.tflite









