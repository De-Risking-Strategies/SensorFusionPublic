#!/bin/bash
echo
echo --------------------------------------
echo  DRS SENSOR FUSION ZIP Directory  TOOL 
echo  Provide a valid Directory Name to Zip
echo  /home/pi/SensorFusion/Pictures/YourDir 
echo ======================================
echo "Enter Directory to .ZIP, use proper Case!"
echo "EX: Directory Name:"
read -p ">" dir

#check blanks
if [ -z "$dir" ]
then
    echo 'Directory cannot be empty'
    exit 1
fi

if [ -d "/home/pi/SensorFusion/Pictures/$dir" ];then
	echo " Directory Exists: $dir"
else
	echo "$dir does not exist"
	exit 1
fi

echo 
echo ====================================
echo Processing:
echo "File to ZIP: /home/pi/SensorFusion/Pictures/$dir"
echo "NOTE: Large Zips will take awhile!"
echo "Output: "$dir
echo ------------------------------------
read -rsp $"Press a key to continue, CTRL+C to halt..." n1 key

echo "Zipping Directory: $dir"
echo 'zip -r '$dir.zip "/home/pi/SensorFusion/Pictures/"$dir
zip -r "/home/pi/SensorFusion/Pictures/"$dir.zip "/home/pi/SensorFusion/Pictures/"$dir
echo 
echo ====================================
echo ZIP DONE!
echo

