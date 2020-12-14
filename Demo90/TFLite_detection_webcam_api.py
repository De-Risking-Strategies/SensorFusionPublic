#########################################
# Sensor Fusion API                     #
# (C) 2020 - De-Risking Strategies, LLC #
# DRS ML/AI Flask API                   #
# Authors: Pushkar K / Drew A           #
# Sunday 12-132020                      #
#########################################
import os
import argparse
import cv2 
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
   

#import subprocess
#subprocess.Popen("/home/pi/labelImg-master/labelImg.py 1", shell=True)
#subprocess.Popen(["ls","foo bar"],shell=True)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #Disable Flask Cache as it interferes with streaming

video_camera_flag = True# Video Stream class enable
capture_flag = 'False' # Capture Enable
capture_image_limit = 20 #Capture LImit

#Client Commands
os.environ['labels_flag'] = 'labels_on'
#print('Init: ', os.environ.get('labels_flag'))
os.environ['scores_flag'] = 'scores_on'

#VideoStream Instance
instance = []
 
@app.route('/',methods=['GET'])
def index():
   video_camera_flag = True
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
            sfCommand = 'annotate'
            #TO DO - get the posted data - name, image count, description
  
        if sfCommand == 'annotate':
            os.environ['cap_flag'] = 'True'
            print('Capture Flag Command =', os.environ['cap_flag'])
            
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
   #This is test code, under development ! 
   print("Reload")
   #print("restart now")  
   
   #these methods are too harsh!
   #print("argv was",sys.argv) 
   #print("sys.executable was", sys.executable)
    #or
   #quit()
   
   #trying to get the instance and delete it
   #print('The class instance is: ',instance)
   #newInstance = reload(instance)
   #instance = locals()['self']
   #del instance
   #locals = locals()
   #print(locals)
   
   video_camera_flag = True #if this is false the video class does not run
   
   #os.execv(sys.executable, ['python'] + sys.argv)
   #webbrowser.open_new('http://localhost:5000')
   #return render_template('base.html')
   return "OK", 200
   
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


def gen_frames():
# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/


    class VideoStream(object):
        """Camera object that controls video streaming from the Picamera"""
        def __init__(self,resolution=(640,480),framerate=30):
            
            
            # Initialize the PiCamera and the camera image stream
            self.stream = cv2.VideoCapture(0)
 
            #TO DO
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
    
    if video_camera_flag:#Using a Flag here - for future use
        if use_TPU:
            interpreter = Interpreter(model_path=PATH_TO_CKPT,
                                      experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
            print(PATH_TO_CKPT)
        else:
            interpreter = Interpreter(model_path=PATH_TO_CKPT)

    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    #pdb.set_trace()      
       
    # Initialize frame rate calculation
    #global frame_rate_calc
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()

    # Initialize video stream
    #global videostream
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
            boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
            scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
            #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)
           
            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

                    global ymin
                    global xmin
                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))
                    
                    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 3)


                    # Draw label (object_name) and score (%)                    
                    object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index                  
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
                    
                    #draw them
                    if state_ != 0:
                        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                        label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                    
                        #cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (237,237,237), cv2.FILLED) # Draw white box to put label text in                   
                        #cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255,0,255), cv2.FILLED) # Draw white box to put label text in                   
                       
                        cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2) # Draw label text
                    else:
                        cv2.rectangle(frame, (xmin,ymin), (xmin,ymin), (237,237,237), cv2.FILLED) # Draw frame with no label OR score text !
                    
                        
            # Draw framerate in corner of frame
            cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
            
            # All the results have been drawn on the frame, so it's time to display it.
            
            #cv2.imshow('Object detector', frame) ## Commented for the FLASK API 

            # SENSOR FUSION Flask API 
            #Brute Force Motion JPEG, OpenCV defaults to capture raw images,
            #so we must encode it into JPEG in order to correctly display the
            #video stream - NOTE need to work on this cv2.imencode tobytes slows the apparent frame rate by about 50%, plus the UI takes some
            #See: https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()            
           
            #Capture
            capture_flag = os.environ.get('cap_flag')
            #print('Capture Flag IN CAMERA =', capture_flag)
            
            if capture_flag == 'True' and img_counter < capture_image_limit:
                cv2.namedWindow("Capture Window")
                cv2.moveWindow("Capture Window", -500, -500)# push it off screen :)
                img_name="../Pictures/Drew/drew-sf-frame_{}.jpg".format(img_counter)
                cv2.imwrite(img_name, frame1)
                print('Wrote Image-'+ img_name)
                img_counter +=1
                
            #Clear Capture Flag when done grabbing images
            if  capture_flag == 'True' and img_counter >= capture_image_limit: 
                   os.environ['cap_flag'] = 'False'
                   img_counter = 0
                   
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            ## End API

            # Calculate framerate
            t2 = cv2.getTickCount()
            time1 = (t2-t1)/freq
            frame_rate_calc= 1/time1
            

            # Press 'q' to quit
            if cv2.waitKey(1) == ord('q'):
                break

        # Clean up
        cv2.destroyAllWindows()
        videostream.release()
        videostream.stop()
    except KeyboardInterrupt:
        pass

#########  run api  #########
if __name__ == '__main__':
     app.debug = True
     app.run()
   
