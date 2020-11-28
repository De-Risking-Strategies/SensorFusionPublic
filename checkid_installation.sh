# Pushkar Khairnar
#!/bin/bash

git clone https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi.git

mv TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi checkid

cd checkid

sudo pip3 install virtualenv

python3 -m venv checkid-env

source checkid-env/bin/activate

bash get_pi_requirements.sh

pip3 install tensorflow==1.14.0

pip3 install Pillow

pip3 install scikit-image

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update

sudo apt-get install libedgetpu1-std

sudo apt-get install python3-edgetpu



