#!/bin/bash
#!/bin/sh
#(C)2020 -De-Risking Strategies, LLC - All Rights REserved
#by DAnderson - Dec 14,2020
show_menu(){
    normal=`echo "\033[m"`
    menu=`echo "\033[36m"` #Blue
    number=`echo "\033[33m"` #yellow
    bgred=`echo "\033[41m"`
    fgred=`echo "\033[31m"`
    printf "\n${menu}**************~ SENSOR FUSION MAIN MENU ~**********${normal}\n"
    printf "${menu}**===================================================${normal}\n"
    printf "${menu}**${number} 1)${menu} Run Sensor Fusion  ${normal}\n"
    printf "${menu}**${number} 2)${menu} Stop Sensor Fusion  ${normal}\n"
    printf "${menu}**${number} 3)${menu} Run Image Labeler${normal}\n"
    printf "${menu}**${number} 4)${menu} CheckID Trained Model Folder ${normal}\n"
    printf "${menu}**${number} 5)${menu} Annotated Pictures Folder ${normal}\n"  
    printf "${menu}**===================================================${normal}\n"
    printf "Please enter a menu option and enter or ${fgred}x to exit. ${normal}"
    read opt
}

option_picked(){
    msgcolor=`echo "\033[01;31m"` # bold red
    normal=`echo "\033[00;00m"` # normal white
    message=${@:-"${normal}Error: No message passed"}
    printf "${msgcolor}${message}${normal}\n"
}

clear
show_menu
while [ $opt != '' ]
    do
    if [ $opt = '' ]; then
      exit;
    else
      case $opt in
        1) clear;
            option_picked "Run Sensor Fusion ";
            printf "Running Full System using: 'bash launch.sh'";
	    x-terminal-emulator -e "bash 'launch.sh'";
            show_menu;
        ;;
        2) clear;
            option_picked "Stop Sensor Fusion ";
            printf "sudo killall python";
	    x-terminal-emulator -e "bash -c 'bash killall.sh'";
            show_menu;
        ;;
        3) clear;
            option_picked "Run Image Labeler";
            printf "/home/pi/labelImg-master folder: python3 labelImg.py";
	    x-terminal-emulator -e "bash -c 'exec python3 ~/labelImg-master/labelImg.py'";
            show_menu;
        ;;
        4) clear;
            option_picked "Check.ID Trained Model Folder";
            printf "/checkid/Sample_tflite_model";
	    ls -al checkid/Sample_TFLite_model;
	    show_menu;
        ;;
        5) clear;
            option_picked "Annotated Pictures Folder";
            printf "Pictures";
	    ls -al Pictures;
	    show_menu;
        ;;
        x)exit;
        ;;
        \n)exit;
        ;;
        *)clear;
            option_picked "Pick an option from the menu";
            show_menu;
        ;;
      esac
    fi
done
