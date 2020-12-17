## labelImg-master Setup for Sensor Fusion			Dec 12, 2020
----

In a terminal window, type (Python3 assumed):

$ cd ~/labelImg-master

$ pip3 install pipenv

$ pip3 install pipenv


You will likeley see this:
Installing collected packages: virtualenv-clone, pipenv
  The script virtualenv-clone is installed in '/home/pi/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  The scripts pipenv and pipenv-resolver are installed in '/home/pi/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed pipenv-2020.11.15 virtualenv-clone-0.5.4

## Check your $PATH  

pi@raspberrypi: $ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games

## Add pipenv to your path:

$export PATH=/home/pi/.local/bin:$PATH

## Check your $PATH again:
pi@raspberrypi:~/labelImg-master $ echo $PATH
/home/pi/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games

You should see the above!

## Install pipenv
Type:
$pipenv run pip install pyqt5==5.12.1 lxml


Output should be similar to:
pi@raspberrypi:~/labelImg-master $ pipenv run pip install pyqt5==5.12.1 lxml
Creating a virtualenv for this project...
Pipfile: /home/pi/labelImg-master/Pipfile
Using /usr/bin/python3.7 (3.7.3) to create virtualenv...
⠧ Creating virtual environment...created virtual environment CPython3.7.3.final.0-32 in 1679ms
  creator CPython3Posix(dest=/home/pi/.local/share/virtualenvs/labelImg-master-jIiDiDx8, clear=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/pi/.local/share/virtualenv)
    added seed packages: pip==20.2.4, setuptools==50.3.2, wheel==0.35.1
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator

✔ Successfully created virtual environment! 
Virtualenv location: /home/pi/.local/share/virtualenvs/labelImg-master-jIiDiDx8
requirements.txt found, instead of Pipfile! Converting...
⠋ Importing requirements...


## Add qt5py3 to your virtual environment 
Type:
$pipenv run make qt5py3

Output looks like this:
pi@raspberrypi:~/labelImg-master $ pipenv run make qt5py3
pyrcc5 -o libs/resources.py resources.qrc

## Finally, run the labelImg program:

$python3 labelImg.py
The app should pop-up now

## DO NOT Add App Icon
$rm -rf build dist; python setup.py py2app -A;mv "dist/labelImg.app" /Applications
