#/bashfile/Poseestimation
#Pushkar Khairnar

cd /home/pi/project-posenet-master

sh install_requirements.sh

pip3 install tensorflow==1.14.0

sudo apt-get update

sudo apt-get install python3-edgetpu
