### Sensor Fusion MIT License	 CHANGELOG  
(C) 2020 - De-Risking Strategies, LLC 
----

## SENSOR FUSION CHANGELOG                     
----
## December 31 - Removed static label from Custom to fix switching issue

## December 30 - ReadMe/Train - Upload
- Fixed Readme - cd /Sensor Fusion
- Chaiged Train label to Upload Images
- Made heck.ID first custom item

## December 30 - Added CheckID support
- Added CheckID Support to Custom Model switcher
- Changed out Annotate image to 'Capture Images'
- Tweaked the Switching logic for Custom to PreLoaded
- Added Title and RowsxCols to Menu.sh to better place the spawned terminals

## December 28-29 - Added Multi Modal support for PreLoaded and Custom Models 
- Python pickle obj store for inter instance setting
- Added Cookies for inter instance model persistance
- Add PreLoaded Model support for ['Demo90','Model01.Deer', 'Model02.Head', 'Model03.Eyes', 'Model04.Tree'] - Click the 'Models' button to cycle through them
- Added Custom Model support for ['Custom.01','Custom.02', 'Custom.03', 'Custom.04'] - Click the 'Custom' button to cycle through them
- Added train Image On Off image

## December 27 - Annotate API enchancemant and check for existing dir on annotation
- Created a Path check fAPI in Python to check for existing Directory Names  - preventingf overwriting
- Added a status bar and removed the dialog when capturing images for annotation
- Made it so the F and Spacebar are disabled during annotation


## December 24 - Create config, routes and widgets packages
- Modularize configuration (globals)
- Create widgets.meter Package - move the meter bar out of the main line
- Create routes.api, login and register packages

## December 23 - Merge of Pushkar and Drew S changes
- Fixed Menu.sh (launch.sh) problem with large image captures under annotations
  NOTE - Browser has to be launched manually  (for) now
- Removed the Tensor Flow objects when capturing images
- Make the Video Camera Code reentratn! Press'q' key to Relaunch TF service and reload browser.  Also Use the Settings Restart menu.
- Updated the Capture Image Warning message
### December 21, 2020 - Pushkar's changes
- Consolidated all the models in one environment.
- Added new models for custom models placeholder (in PreLoadedModels).
- changed the scripts to work in the SF environment.
### December 18-22,2020 - Drew's Changes
- Merged Puskars' code from last week
- Added CSS @Media tags for small screens: 800 x 420 and 1024 x 768
- Added basic Meter/Scale for single person
- Modified launch.sh to get rid of the ERR_CONNECTION_REFUSED on launch message
- Added Backgrond Camera Off image
- Stubbed out Training - Upload File function 


## December 16, 2020
- Full screen toggle implemented
- Info screen implemented
- Fixups to Menu.sh

##December 15, 2020
- .gitigonre repaired
- Cosmetic fixes to Settings and Annotate dialogs
- README.md spell checked and cleaned up

## December 14, 2020
- Added Keyboard handler - Spacebar for Annotate, F key to toggle Frames per second on and off (off by default now)
- Enabled saving of annotations for: Directory/File name and number of images to save
- Added new images for MVP  - Annotate, train, settings
- Added simple Annotate empty field validation and confirmation messaging
- Made Score and Label Green per Don's spec
- Removed the background rectangle behind the Scores/Labels per Don' spec
 
## December 13, 2020
- Added Javascript to Python/Flask communication via POST,GET
- Created command structure for Capture Images, Labels toggle (and Score%)
- Created baseline Image Capture routine on Annotate spacebar function
- Enable toggle logic and graphics for scores and labels switches
- Worked on deleting Camera insstance for restart (not finished yet)
- Added Selection Dialog to Annotate workflow: Title, Description and Number of images to capture
- Added Main Menu - menu.sh and associated files

## December 4, 2020 - First Repo Update - DAnderson
- Expanded Javascript Templates and Static file archtecture and implemented running stack on Locahost
- Successfully exposed TFLite Python Camera Input as API endpoint in FLask for JS to consume
- Added graphics, toolbars, widgets, sliding sidnavigation left and right, modal dialog
- Inter layer communication end-point exposed Flask -> Javascript

## November 39, 2020 - Initial Release on Flask
- Initial checkin to Github
- Incorporated Flask API into Demo90 TFLite environment
- Initial JS layout, graphics and local tech stack created on top of Demo90 environment
