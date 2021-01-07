#!/bin/bash
echo
echo ------------------------------------
echo  DRS SENSOR FUSION FILE UPLOAD TOOL 
echo  Provide a valid email, a full path
echo  to your .zip file, and a
echo  description.
echo ====================================
echo
read -p "Enter your email address: " email

#check blanks
if [ -z "$email" ]
then
    echo 'Email cannot be empty'
    exit 1
fi

#Validate email address
IFS="@"
set -- $email
if [ "${#@}" -ne 2 ];then
	echo 'Invalid email address!'
	exit 1
fi

#Validate file
read -p "Enter Sensor Fusion .ZIP file to upload: " file
if [ -z "$file" ]
then
    echo 'File cannot be empty'
    exit 1
fi


if [ -f "/home/pi/SensorFusion/Pictures/$file" ];then
	echo " File Exists: /home/pi/SensorFusion/Pictures/$file"
else
	echo "/home/pi/SensorFusion/Pictures/$file does not exist"
	exit 1
fi

#Get a description, ensure no quotes
read -p "Enter a description: " desc
if [[ $desc =~ "\"" ]]; then
   echo "Please do not put any or Symbols like quotation marks in the description."
   exit 1
fi
ESCAPED=$(python3 -c "import urllib.parse as ul; print(ul.quote_plus(\"$desc\"))")

echo 
echo ====================================
echo Processing:
echo "File to Upload: /home/pi/SensorFusion/Pictures/$file"
echo "Description: $desc"
echo "Account: $email"
echo ------------------------------------
read -rsp $"Press a key to continue, CTRL+C to halt..." n1 key
RESPONSE=$(curl -v "https://beo7gqvf3j.execute-api.us-east-2.amazonaws.com/production/get_upload_url/$email/$ESCAPED")

echo "Uploading URL: $RESPONSE"
curl -i --request PUT --upload-file "/home/pi/SensorFusion/Pictures/"$file $RESPONSE

echo 
echo ====================================
echo UPLOAD DONE!
echo

