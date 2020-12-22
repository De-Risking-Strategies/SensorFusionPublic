### Sensor Fusion MIT License	 CHANGELOG  
(C) 2020 - De-Risking Strategies, LLC 
DRS ML/AI Flask API                   
Authors:  Drew A, Puskar P, Sharon B

----

## SENSOR FUSION CHANGELOG                     
----
## December 21, 2020
- Consolidated all the models in one environment.
- Added new models for custom models placeholder (in PreLoadedModels).
- changed the scripts to work in the SF environment.

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
