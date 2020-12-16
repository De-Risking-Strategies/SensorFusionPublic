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
     
>NOTE: Its convienent to setup your github environment beforehand, at a termina, type:
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"      
      
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

You should see something like the below (your changes will be different)
On branch drew
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   .gitignore
	modified:   Demo90/TFLite_detection_webcam_api.py
	modified:   Demo90/static/css/sidenav.css
	modified:   Demo90/static/css/style.css
	modified:   Demo90/static/js/data.js
	modified:   Demo90/static/js/globals.js
	modified:   Demo90/static/js/sidenav.js
	modified:   Demo90/static/js/utilities.js
	modified:   Demo90/templates/index.html
	modified:   main.sh

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	CHANGELOG.md
	Demo90/static/assets/favicon.ico
	Demo90/static/assets/favicon.png
	Demo90/static/js/index.js
	Demo90/templates/favicon.ico
	LICENSE.md
	README.md
	killall.sh
	labelImg-master_Setup.md
	launch.sh
	menu.sh

To add All these changes, type:

git add -A

(Or you can add them one by one, see online Git info for more).

If you type 'Git status' once more, you'll see a list of the changed and new files now staged for commit.


#### Third - Commit updated/added/deleted files

Next, its a best practice to commit your staged files with the -m flag, and write a brief comment as to the contents of the chan ge set.

git commit -m "added a new feature some files changed"

You should see something like this if successful:

pi@raspberrypi:~ $ git commit -m 'Major updates for JS controls, dialogs, and a Main Menu script'

[drew 17cb076] Major updates for JS controls, dialogs, and a Main Menu script
 21 files changed, 866 insertions(+), 191 deletions(-)
 create mode 100644 CHANGELOG.md
 create mode 100644 Demo90/static/assets/favicon.ico
 create mode 100644 Demo90/static/assets/favicon.png
 rewrite Demo90/static/js/data.js (100%)
 rewrite Demo90/static/js/globals.js (99%)
 create mode 100644 Demo90/static/js/index.js
 create mode 100644 Demo90/templates/favicon.ico
 create mode 100644 LICENSE.md
 create mode 100644 README.md
 create mode 100644 killall.sh
 create mode 100644 labelImg-master_Setup.md
 create mode 100644 launch.sh
 create mode 100644 menu.sh

#### Fourth - Git Push to you branch

To sync your changes to the repo, perform a Git Push command:

EX: git push origin <branch>

Type:
git push SensorFusion 'your branch name'

If you prompt you for you Git UserName and (long) password.

Your output if successful, will look like this:

Username for 'https://github.com': DrewAnderson 
Password for 'https://DrewAnderson@github.com': 
Enumerating objects: 44, done.
Counting objects: 100% (44/44), done.
Delta compression using up to 4 threads
Compressing objects: 100% (27/27), done.
Writing objects: 100% (27/27), 14.57 KiB | 678.00 KiB/s, done.
Total 27 (delta 11), reused 0 (delta 0)
remote: Resolving deltas: 100% (11/11), completed with 11 local objects.
remote: 
remote: GitHub found 12 vulnerabilities on De-Risking-Strategies/SensorFusion's default branch (2 high, 9 moderate, 1 low). To find out more, visit:
remote:      https://github.com/De-Risking-Strategies/SensorFusion/network/alerts
remote: 
To https://github.com/De-Risking-Strategies/SensorFusion.git
   b0a15b0..17cb076  drew -> drew


#### FINALLY - MAKE A Pull Request

After successfully checking in your changes, go to the Git Hub web site and create a Pull Request to have a reviewers look at and approve your changes for merging into the master branch.

Open your browser to:

https://github.com/De-Risking-Strategies/SensorFusion

You should see similar to this:
 drew had recent pushes 2 minutes ago

To the right is a big green button marked "Compare and Pull Request"

Click that guy, add comments and description from CHANGELOG.md.



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
