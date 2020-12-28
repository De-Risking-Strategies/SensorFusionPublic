#Sensor Fusion Config module

#Global flags
global videostream


#VideoStream Instance
global instance
instance = []

#TensorFlow
global object_name   #Score+Label
global scores
global classes
global person_found
person_found=True
global top      

#UX/UI controls
global anno_images 
global kill_tensorFlow
kill_tensorFlow = "False"

#meter
global start_point
global end_point
global bottom 
global thickness 
global left 
global top


#Constants
#capture_flag = 'False' # Capture Enableg
capture_image_limit = 2000 #Capture LImit
left = 13
bottom = 400
thickness = 14

