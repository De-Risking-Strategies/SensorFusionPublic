
##LabelImg-master setup for SensorFusion - b                   Dec 18, 2020
----

In a terminal window, type the following commands:

pi@raspberrypi:~ $ cd SensorFusion/

pi@raspberrypi:~/SensorFusion $ git clone https://github.com/tzutalin/labelImg.git

pi@raspberrypi:~/SensorFusion $ mv /home/pi/SensorFusion/labelImg /home/pi/SensorFusion/labelImg-master

pi@raspberrypi:~/SensorFusion $ cd labelImg-master/

pi@raspberrypi:~/SensorFusion/labelImg-master $ pip3 install resources

pi@raspberrypi:~/SensorFusion/labelImg-master $ sudo pip3 install lxml

pi@raspberrypi:~/SensorFusion/labelImg-master $ sudo apt-get install pyqt5-dev-tools

pi@raspberrypi:~/SensorFusion/labelImg-master $ make qt5py3

output: pyrcc5 -o libs/resources.py resources.qrc

pi@raspberrypi:~/SensorFusion/labelImg-master $ python3 labelImg.py

The app should pop-up now!