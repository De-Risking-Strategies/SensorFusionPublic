#########################################
# Sensor Fusion API                     #
# (C) 2020 - De-Risking Strategies, LLC #
# DRS ML/AI Flask API                   #
# Authors: Pushkar K / Drew A           #
# Updated 12-22-2020                    #
#########################################
import os
import argparse
import cv2 as cv2
import numpy as np
import sys
import time

from threading import Thread
import importlib.util

#Flask 
import json
from flask import Flask, jsonify, request, render_template, Response, session, stream_with_context
from importlib import reload 
import gc
import webbrowser

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #Disable Flask Cache as it interferes with streaming

global video_camera_flag
video_camera_flag = True# Video Stream class enable

capture_flag = 'False' # Capture Enableg


capture_image_limit = 2000 #Capture LImit
fps_flag = False #showing frames per second is false by default - controlled by 'F' keyboard command

#Client Commands
os.environ['labels_flag'] = 'labels_on'
#print('Init: ', os.environ.get('labels_flag'))
os.environ['scores_flag'] = 'scores_on'
#Capture
os.environ['cap_flag'] = 'False'
#kill_TF
os.environ['kill_tensorFlow'] = 'False'


#VideoStream Instance
instance = []

  
@app.route('/',methods=['GET'])
def index():
   video_camera_flag = True
   #On a reload
   quit_flag = os.environ.get('quit_flag')
   if quit_flag == 'quit':#
       cv2.destroyAllWindows()
       if videostream:
         #videostream.release()
         videostream.stop()


   return render_template('index.html' )

@app.route('/api', methods = ['GET','POST'])
def api():
    # POST request - Sensor Fusion Commands
    if request.method == 'POST':
        print('Incoming command from Sensor Fusion client ...')
        sfCommand = request.get_json()
        print(sfCommand)  # parse as JSON
        
        first_char = sfCommand[0] 
        if first_char == 'a':
            chunks = sfCommand.split(',')
            sfCommand = 'annotate'
            
            #Get the annotation data - name, image count, description
            
            os.environ['annotate_name'] = str(chunks[1])
            os.environ['annotate_images'] = str(chunks[2])
            
            global anno_images 
            anno_images = str(chunks[2])
            
            os.environ['annotate_description'] = str(chunks[3])
        #kill TensorFlow
        if first_char == 'k':
            os.environ['kill_tensorFlow'] = 'True'
        #Restore Tensor Flow
        if first_char == 'r':
            os.environ['kill_tensorFlow'] = 'False'
            print('Restore Tensor Flow')
       
        #custom, model
        if first_char == 'c':
            print('Custom Model Changed')
       
        if first_char == 'm':
            print('Model changed')
            
        #Annotate    
        if sfCommand == 'annotate':
            capture_flag =  os.environ['cap_flag'] = 'True'
            print('Capture Flag Command =',capture_flag)
        #Labels    
        elif sfCommand == 'scores_off':
            os.environ['scores_flag'] = sfCommand
            print('Toggle Scores Command =', os.environ['scores_flag'])
        elif sfCommand == 'scores_on':
            os.environ['scores_flag'] = sfCommand
            print('Toggle Scores Command =', os.environ['scores_flag'])
            
        elif sfCommand == 'labels_off':
            os.environ['labels_flag'] = sfCommand
            print('Toggle Labels Command =', os.environ['labels_flag'])
        elif sfCommand == 'labels_on':
            os.environ['labels_flag'] = sfCommand
            print('Toggle Labels Command =', os.environ['labels_flag'])   
        elif sfCommand == 'fps':
            global fps_flag
            
            if fps_flag == False:#Show/Hide Frames per second
                fps_flag = True
            else:
                fps_flag = False
        elif sfCommand == 'quit':
            os.environ['quit_flag'] = sfCommand
            print('Quit command recieved')
                
        
        return 'OK', 200

    # GET request
    else:
        print('GET Request from Client');
        #session['cap_flag'] = True
        #print(session.get('capt_flag'))
        os.environ['cap_flag'] = 'True'
        print('Capture Flag Command =', os.environ['cap_flag'])
        
        message = {'Capture':'Capturing Images!'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/quit_camera/') 
def quit_camera():
   return "Not Implemented yet", 200
   
@app.route('/login') 
def login():
   embedVar='Login'
   return render_template('login.html',embed=embedVar )

@app.route('/register') 
def register():
   embedVar='Register'
   return render_template('register.html',embed=embedVar )
  
@app.route('/video_feed')
def video_feed():
    #Video streaming route: goes into src attribute of an img tag
    print('\nin FLASK: locals() value inside class\n', locals())
    
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ============================
def gen_frames():
# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
    class VideoStream(object):
        """Camera object that controls video streaming from the Picamera"""
        def __init__(self,resolution=(640,480),framerate=30,target=None,args=()):
           
            # Initialize the PiCamera and the camera image stream
            self.stream = cv2.VideoCapture(0)
 
            #VideoStream Instance
            global instance
            instance = VideoStream.__qualname__
            print('The class instance is: ',instance)
            #print('\nVIDEOSTREAM: locals() value inside class\n', locals())
            #print(dir(VideoStream))
 
            #Reload
            reloadClass = os.environ.get('reload')
            if reloadClass == 'True':
                print('Delete Self:')
                del self
                os.environ['reload'] = 'False'          
                        
            ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            ret = self.stream.set(3,resolution[0])
            ret = self.stream.set(4,resolution[1])
                
            # Read first frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

            # Variable to control when the camera is stopped
            self.stopped = False            
            
        def __del__(self):
            print ("Object destroyed");   

        def start(self):
        # Start the thread that reads frames from the video stream
            Thread(target=self.update,args=()).start()
            
            return self

        def update(self):
            # Keep looping indefinitely until the thread is stopped
            while True:
                # If the camera is stopped, stop the thread
                if self.stopped:
                    # Close camera resources
                    self.stream.release()
                    return
                    
                # Otherwise, grab the next frame from the stream
                (self.grabbed, self.frame) = self.stream.read()

        def read(self):
        # Return the most recent frame
            this_instance = self
            return self.frame

        def stop(self):
        # Indicate that the camera and thread should be stopped
            self.stopped = True

    # Define and parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                        required=True)
    parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                        default='detect.tflite')
    parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                        default='labelmap.txt')
    parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                        default=0.5)
    parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                        default='1280x720')
    parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                        action='store_true')

    args = parser.parse_args()

    MODEL_NAME = args.modeldir
    GRAPH_NAME = args.graph
    LABELMAP_NAME = args.labels
    min_conf_threshold = float(args.threshold)
    resW, resH = args.resolution.split('x')
    imW, imH = int(resW), int(resH)
    use_TPU = args.edgetpu

    # Import TensorFlow libraries
    # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
    # If using Coral Edge TPU, import the load_delegate library
    pkg = importlib.util.find_spec('tflite_runtime')
    print('TPU Runtime' + str(pkg))

    if pkg:
        from tflite_runtime.interpreter import Interpreter 
        if use_TPU:
            from tflite_runtime.interpreter import load_delegate 
    else:
        from tensorflow.lite.python.interpreter import Interpreter 
        if use_TPU:
            from tensorflow.lite.python.interpreter import load_delegate 

    # If using Edge TPU, assign filename for Edge TPU model
    if use_TPU:
        # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
        if (GRAPH_NAME == 'detect.tflite'):
            GRAPH_NAME = 'edgetpu.tflite'       

    # Get path to current working directory
    CWD_PATH = os.getcwd()

    # Path to .tflite file, which contains the model that is used for object detection
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

    # Load the label map
    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Have to do a weird fix for label map if using the COCO "starter model" from
    # https://www.tensorflow.org/lite/models/object_detection/overview
    # First label is '???', which has to be removed.
    if labels[0] == '???':
        del(labels[0])

    # Load the Tensorflow Lite model.
    # If using Edge TPU, use special load_delegate argument
    
    #if video_camera_flag:#Using a Flag here - for future use
    if use_TPU:
        interpreter = Interpreter(model_path=PATH_TO_CKPT,
                                  experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
        print('TPU Detected' + PATH_TO_CKPT)
    else:
        interpreter = Interpreter(model_path=PATH_TO_CKPT)
        print('No TPU detected!'+ PATH_TO_CKPT)            

    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    # Initialize frame rate calculation
    #global frame_rate_calc
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()

    # Initialize video stream
    global videostream
    videostream = VideoStream(resolution=(imW,imH),framerate=30).start()
    time.sleep(1)

    img_counter = 0
    
   
  
    #for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    try:
        #while True:
        while video_camera_flag:
            
            # Start timer (for calculating frame rate)
            t1 = cv2.getTickCount()

            # Grab frame from video stream
            frame1 = videostream.read()

            # Acquire frame and resize to expected shape [1xHxWx3]
            frame = frame1.copy()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (width, height))
            input_data = np.expand_dims(frame_resized, axis=0)
            
            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]['index'],input_data)
            interpreter.invoke()

            # Retrieve detection results
            global scores
            global classes
            global person_found
            
            person_found = False
            
            boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
            scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
            #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)
            
            #Kill TensofFlow while Annotating
            global kill_tensorFlow
            kill_tensorFlow = os.environ.get('kill_tensorFlow')
            #print("TensofFlow Status: " + str(kill_tensorFlow))

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                    
            
                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))
                    
                    #print("Kill TF Flag: "+ str(kill_tensorFlow))
                    if kill_tensorFlow != 'True':
                        cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 3)

                    # Draw label (object_name) and score (%)    
                    global object_name   
                    object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index 
                    #print(labels[int(classes[i])]+": "+str(i))  
                    
                    
                    if labels[int(classes[0])]== 'person':#NOTE - The bar is for one person only
                        #print('Person Found!')
                        person_found = True# used for bar below
                    
                    scores_flag = os.environ.get('scores_flag')
                    labels_flag = os.environ.get('labels_flag')
                    
                    #states
                    state_ = 11 #both on by default
                    if labels_flag == 'labels_off' and scores_flag == 'scores_off':
                        state_ = 0#00
                        label = object()
                    
                    if labels_flag == 'labels_on' and scores_flag == 'scores_on':                    
                        state_ = 11#11
                        label = '%s: %d%%' % (object_name.capitalize(), int(scores[i]*100)) # Example: 'person: 72%'
                    
                    if labels_flag == 'labels_off' and scores_flag == 'scores_on':
                        label = '%d%%' % (int(scores[i]*100)) # Example: '72%'
                        state_ = 1#01    
                        
                    if labels_flag == 'labels_on' and scores_flag == 'scores_off':
                        state_= 10 #10   
                        label = '%s: ' % (object_name.capitalize()) # Example: 'person: '
                    
                    #draw the labels, background score and box
                    if state_ != 0:
                        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size                        
                        label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window                    
                        #cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (237,237,237), cv2.FILLED) # Draw white box to put label text in                   
                        if kill_tensorFlow != 'True':
                            cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (128,128,128), cv2.FILLED) # Draw gray box to put label text in                   
                            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2) # Draw label text
                    else:
                        if kill_tensorFlow != 'True':
                            cv2.rectangle(frame, (xmin,ymin), (xmin,ymin), (237,237,237), cv2.FILLED) # Draw frame with no label OR score text !
                        
            # Draw framerate in corner of frame - use 'F' key to toggle on/off
            if fps_flag:
                cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
            else:
                pass
                
            # All the results have been drawn on the frame, so it's time to display it.
            #cv2.imshow('Object detector', frame) ## Commented for the FLASK API 
 
            #Draw vertical bar
            window_name ='Object detector'
                 
            top = int(scores[0]*100)
            color = (0, 0, 255)
            
            if person_found == True:
                #print('p')
                if top >= 100:
                    top = 100
                    color = (0, 255, 0) #1 BGR format 
                #   It never sees 100%! 
                elif top >= 98 <=99:
                    top = 120
                    color = (0, 255, 0) #Green                
                elif top >= 96 <=97:
                    top = 130
                    color = (0, 255, 0) #  
                elif top >= 94 <=95:
                    top = 140
                    color = (0, 255, 0)  #Top                 
                elif top >= 92 <=93:
                    top = 150
                    color = (0, 255, 36)        
                elif top >= 90 <=91:
                    top = 160
                    color = (0, 255, 52)       
                elif top >= 88 <=89:
                    top = 170
                    color = (0, 255, 69)        
                elif top >= 86 <=87:
                    top = 180
                    color = (0, 255, 85)       
                elif top >= 84 <=85:
                    top = 190
                    color = (0, 255, 102)       
                elif top >= 81 <=83:
                    top = 200
                    color = (0, 255, 110)  
                elif top >= 78 <=80:
                    top = 210
                    color = (0, 255, 136)  
                elif top >= 75 <=77:
                    top = 220
                    color = (0, 255, 153) 
                
                # Yellow   
                elif top >= 72 <=74:
                    top = 230
                    color = (0, 255, 170)            
                elif top >= 69 <=71:
                    top = 240
                    color = (0, 255, 187)           
                elif top >=66 <=68:
                    top = 250    
                    color = (0, 255, 204)  
                elif top >= 63 <=65:
                    top = 260
                    color = (0, 255, 231)            
                elif top >= 60 <=62:
                    top = 270
                    color = (0, 255, 238)           
                elif top >=57 <=59:
                    top = 280    
                    color = (0, 255, 254)  
                elif top >=54 <=56:
                    top = 290    
                    color = (0, 255, 255)  
                elif top >=51 <=53:
                    top = 300    
                    color = (0, 255, 255)  
                                
                # anything below 50 is red          
                elif top >=40 <=50:
                    top = 310    
                    color = (0, 200, 255)           
                elif top >=30 <=39:
                    top = 330    
                    color = (0, 150, 255)
                elif top >=20 <=29:
                    top = 340    
                    color = (0, 75, 255) 
                elif top >=10 <=19:
                    top = 350    
                    color = (0, 0, 255) 
                elif top >=0 <=9:
                    top = 360    
                    color = (0, 0, 255) #10    BGR Red         
              
            else:#no person detected
                  top = 360
                  color=(0,0,255)
                                        
            bottom = 400
            left = 13
            start_point = (left, top)
            end_point = (left,bottom)
            thickness = 14
            if kill_tensorFlow != 'True':
                image = cv2.line(frame, start_point, end_point, color, thickness)
           
            # Displaying the image - DO NOT USE!
            #cv2.imshow(window_name, image)  
          
            #SENSOR FUSION Flask VIDEO API 
            #Brute Force Motion JPEG, OpenCV defaults to capture raw images,
            #so we must encode it into JPEG in order to correctly display the
            #video stream - NOTE need to work on this cv2.imencode tobytes slows the apparent frame rate by about 50%, plus the UI takes some
            #See: https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()            
           
            #Capture Images and save to Annotate Named subdirectory under ~/Pictures
            capture_flag = os.environ.get('cap_flag')
            annotate_name = os.environ.get('annotate_name')           
            annotate_description = os.environ.get('annotate_description')# this is for future use - we'll write our own metadata file
                      
            if capture_flag == 'True':
                #Check limit
                try:
                    print("image limit: " + anno_images)
                    capture_image_limit = int(anno_images)
                except:
                    pass
      
            if capture_flag == 'True' and img_counter < capture_image_limit:
                #Create new or use existing directory
                path_to_directory = '../Pictures/' + annotate_name
                print("Saving to ", path_to_directory)
                try:
                    os.makedirs(path_to_directory)
                except FileExistsError:
                    #dir already exists, so overwrite existing (unless we datestamp)!
                    pass
                
                cv2.namedWindow("Capture Window")
                cv2.moveWindow("Capture Window", -500, -500)# push it off screen :)
                
                img_name="../Pictures/"+annotate_name+"/"+annotate_name+"sf-frame_{}.jpg".format(img_counter)
                cv2.imwrite(img_name, frame1)
                print('Wrote Image-'+ img_name)
                img_counter +=1
                
            #Clear Capture Flag when done grabbing images
            if capture_flag == 'True' and img_counter >= capture_image_limit: 
                   os.environ['cap_flag'] = 'False'
                   img_counter = 0
                   
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            ## End Video Stream API ###

            # Calculate framerate
            t2 = cv2.getTickCount()
            time1 = (t2-t1)/freq
            frame_rate_calc= 1/time1
                       
            # Press 'q' to quit
            if cv2.waitKey(1) == ord('q'):
                print("CV2 Break")
                break
        
            
            # Press 'q' to quit
            quit_flag = os.environ.get('quit_flag')
            if quit_flag == 'quit':#
                os.environ['quit_flag'] = ''
                print("CV2 Quit " + quit_flag)
                cv2.destroyAllWindows()
                if videostream:
                    #videostream.release()
                    videostream.stop()
                    print('Videostream stopped')
                break
            
                
            #print("quit_flag " + str(quit_flag))    
        # Clean up
        cv2.destroyAllWindows()
        if videostream:
            #videostream.release()
            videostream.stop()
        webbrowser.open('http://localhost:5000')
            
    except KeyboardInterrupt:
        pass

#########  run api  #########
if __name__ == '__main__':
     
     app.debug = True
     app.run()
     
