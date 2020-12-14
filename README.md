#########################################
# Sensor Fusion MIT License	 READ ME    #
# (C) 2020 - De-Risking Strategies, LLC #
# DRS ML/AI Flask API                   #
# Authors:  Drew A                      #
# Update 12-14-2020                     #
#########################################


##DRS Sensor Fusion Client Setup 	
````						    
This is a basic readme for developers with experience in Linux, Python and Git.
      
It also assumes you have a current Sensor Fusion image installed on your Raspberry Pi. (December 4, 2020 or later)      
      
      
## Basic Git Hub Instructions to Pul Latest Code
````
### 1. Open a terminal window to the root of the Sensor Fusion directory, which is currently /home/pi

NOTE: You may grab latest code from GitHub Remote Repo, which is located here:

https://github.com/De-Risking-Strategies/SensorFusion.git

### 2. Check your Git locally
To Pull a copy of the release branch, at a command line (with GitHub installed and credentials handy):
EX: git pull <remote> <branch>
 
Type: 
git pull https://github.com/De-Risking-Strategies/SensorFusion.git master

You will be prompted for Username:
Username for 'https://github.com':

Type in your GitHub Username and press Enter.

You will be prompted for your (2-Factor*) GitHub password:

You should see something similar to:

Password for 'https://DrewAnderson@github.com': 
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 4 (delta 0), reused 1 (delta 0), pack-reused 0
Unpacking objects: 100% (4/4), done.
From https://github.com/De-Risking-Strategies/SensorFusion
 * branch            master     -> FETCH_HEAD
Updating b0a15b0..21acd67
Fast-forward
 .gitconfig | 3 ---
 1 file changed, 3 deletions(-)
 delete mode 100644 .gitconfig


>NOTE - If you are not editing code, yu may jump down to the section below to run it:
>see the ##Start Sensor Fusion section below



### 3. Check in your changes 
After doing a Git Pull from Master to ensure you have the latest baseline, always check your code into your own branch

#### First - check your branch, at the terminal window type:

git branch

You should see:
pi@raspberrypi:~ $ git branch
* drew
  master

Make sure the '*' is on your branch, and not on 'master' (See online info for creating, checking out and updating a branch in Git).

#### Second - Git Add updated/added/deleted files
Add any changed, deleted or added files to your branch.  First check the files and make sure your not adding any test or 'garbage' files.  You may need to edit the hideen .gitignore file, expecially if you've installed other folders or programs on your /home/pi.

type:
git status

You should see something like the below (depending on your changes, whcih will be different)




#### Third - Commit updated/added/deleted files








##Update Packages
===================
Bwe sure your Pi is upto date (requires a wifi connection)
System:
$ sudo apt-get update
Installed:
$ sudo apt-get dist-upgrade


##Install SQL
============
https://iot4beginners.com/sqlite-database-on-raspberry-pi/
NOTE - This should be installed in the image, but if not follow the steps below.

$ sudo apt-get install sqlite3


##Activate Environment
================
In a separate terminal window:
NOTE - This should be installed in the image, but if not follow the steps below.

$ cd ./Demo90

Type
(Demo90)$ source Demo90-env/bin/activate


##Install Flask
=============
NOTE - This should be installed in the image, but if not follow the steps below.

$ pip install Flask==0.12.1
$ pip freeze > requirements.txt

Add Flask to Demo-90 env

Go to the Demo90 Directory,
Type
$ pip

$(demo-90)$ pip install -m flask

###Check it:
---------
Type: 'pip list'.  You should see similar to the below:
(Demo90-env) pi@raspberrypi:~/Demo90 $ pip list
Package              Version    
-------------------- -----------
absl-py              0.11.0     
astor                0.8.1      
cached-property      1.5.2      
click                7.1.2      
Flask                1.1.2      
gast                 0.4.0      
google-pasta         0.2.0      
grpcio               1.33.2     
h5py                 3.1.0      
importlib-metadata   2.0.0      
itsdangerous         1.1.0      
Jinja2               2.11.2     
Keras-Applications   1.0.8      
Keras-Preprocessing  1.1.2      
Markdown             3.3.3      
MarkupSafe           1.1.1      
numpy                1.19.4     git 
opencv-python        3.4.6.27   
pip                  18.1       
pkg-resources        0.0.0      
protobuf             3.14.0     
setuptools           40.8.0     
six                  1.15.0     
tensorboard          1.13.1     
tensorflow           1.13.1     
tensorflow-estimator 1.14.0     
termcolor            1.1.0      
tflite-runtime       2.1.0.post1
Werkzeug             1.0.1      
wheel                0.35.1     
wrapt                1.12.1     
zipp                 3.4.0      

-------------------------------------

###Exit the Demo90-env:
$ deactivate


##Start Sensor Fusion
=====================
in $/home/pi

$ bash shell.sh

NOTE - You may also use bash main.py to launch the service without the menu commands

~~~~~~~~~~~~~~~~~~~~~~~~~

NOTE - Exit terminal window to kill processes!

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
