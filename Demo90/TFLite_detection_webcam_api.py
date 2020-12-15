#########################################
# Sensor Fusion API                     #
# (C) 2020 - De-Risking Strategies, LLC #
# Flask API                             #
#########################################
import os
import argparse
import cv2 
import numpy as np
import sys
import time
from threading import Thread
import importlib.util

#Flask - ATA - November 24, 2020
import json
# import logging
from flask import Flask, jsonify, request, render_template, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sf.db'
app.secret_key = 'dont tell anyone'

#from sf-db import *
db = SQLAlchemy(app)

'''
handler = logging.FileHandler("test.log")  # Create the file logger
app.logger.addHandler(handler)             # Add it to the built-in logger
app.logger.setLevel(logging.DEBUG)
'''

class User(db.Model):
    User_ID = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128),nullable=False)
    last_name = db.Column(db.String(128),nullable=False)
    email_address = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(10),nullable=False)
    #date_created = db.Column(db.DateTime(), nullable=False,default=datetime.utcnow)
    model_limit = db.Column(db.Integer,)
    threshold_max = db.Column(db.Integer,default=128)
    tipping_point_a = db.Column(db.Integer,default=50)
    threshold_min = db.Column(db.Integer,default=-128)
    camera_count = db.Column(db.Integer,default=1)
    training_limit = db.Column(db.Integer,default=0)
    purchase_level = db.Column(db.Integer)

    installed_image_version = db.Column(db.Integer) # should be type long
    static_models = db.Column(db.Integer)  # should be type array?
    custom_models = db.Column(db.Integer)  # should be type array?

    # specifies the format in which we want to print our user object
    def __repr__(self):
        return f"User('{self.User_ID}','{self.first_name}','{self.last_name}','{self.email_address}')"

#def __init__(self,User_ID,first_name,last_name,email_address):
    #self.User_ID = User_ID
    #self.first_name = first_name
    #self.last_name = last_name
    #self.email_address = email_address

@app.route('/login') 
def login():
   embedVar='Login'
   return render_template('login.html',embed=embedVar )

@app.route('/register', methods=["GET","POST"]) 
def register():
   embedVar='Register'
   if request.method == "POST":
       #print(request.headers)
       first_name = request.form.get("first")
       last_name = request.form.get("last")
       email_address = request.form.get("email")
       password = request.form.get("password")
       reEnterPassword = request.form.get("re-enterPassword")
       agree_term = request.form.get('agree-term')
       privacy_term = request.form.get('privacy-term')
       age_term = request.form.get('age-term')

       for key, value in request.form.items():
           #if len(value) > 64:
               
               #print('Yeah, what he said') # goes to console
               #return 'Something is wrong' # goes to webpage
           print("key: {0}, value: {1}".format(key, value))
       type(age_term)
       print(type(age_term))

       # validation checks

       # both first and last name need to be between 4 and 128 characters
       #   - should we have alpha numeric checks for names?
       #   - there are people with first and last names that are shorter than 4 characters, 
       #     so should we decrease the lower bound?
       if len(first_name) < 4 or len(first_name) > 128: 
           print('First name either too long or too short')
           return 'First name is either too long or too short'
       if len(last_name) < 4 or len(last_name) > 128: 
           print('Last_name either too long or too short')
           return 'Last name is either too long or too short'

       # email_address should be between 8 and 255 characters and should not already exist in the table
       if len(email_address) < 8 or len(email_address) > 255: 
           # check to make sure this email does not already exist in the database
           print('Email address either too long or too short')
           return 'Email address is either too long or too short'

       # password should be at least 8 characters long, encrypted, and should have the specified requirements
       if len(password) < 8:
           # encrypt password to be saved in database
           print('Password too short')
           return 'Password is too short'
       # check for other password validation requirements?

       # re-enterPassword should match password
       if reEnterPassword != password: 
           print('Passwords do not match')
           return 'Your passwords do not match'

       # check if terms of service were accepted
       if agree_term == None or privacy_term == None or age_term == None:
           print('Not all terms were accepted')
           return('Not all terms were accepted')



       #print(first_name)
       #add_user_response = {{ url_for('collection', method='POST') }}
       #add_user_response = make_response({{ url_for('collection') }})
       #add_user = redirect(url_for('collection', method='POST'))
       #print(add_user.headers)

       #response = request.post({{ url_for('collection',data=data,headers=headers) }})
       #response = redirect({{ url_for('collection', method='POST', firstName = first_name, lastName = last_name,  email = email_address, captureLimit = 5) }})
       res = redirect("api/user", 303)
       print(request.form)
       print('redirected')
       print(res)
       #result = collection()
       #print(result)

   #print('hello world')
   return render_template('register.html',embed=embedVar )

'''
@app.route('/register', methods=['POST']) 
def test():
   embedVar='Test'
   #if(not request.form[firstName]):
       #flash('Please enter first name','error')
   #    flash('Please enter first name field')
   #if(not request.form[lastName]):
       #flash('Please enter last name','error')
   #    flash('Please enter last name field')
   #if(not request.form[email]):
       #flash('Please enter email','error')
   #    flash('Please enter email field')
   #if(not request.form[password]):
       #flash('Please enter password','error')
   #    flash('Please enter password field')
   #if(not request.form[re-enterPassword]):
       #flash('Please re-enter password','error')
   #    flash('Please enter re-enter password')
   #else:
   #    return request.form
   #print(request.form[first])
   print('hello world')
   list1=[]
   for key, value in request.form.items():
      list1.append("key: {0}, value: {1}".format(key, value))
   print(len(list1))
   return 'OK'
'''
  

@app.route('/video_feed')
def video_feed():
    #Video streaming route: goes into src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

  
@app.route('/')
def index():
   embedVar='Main'
   return render_template('index.html',embed=embedVar )


@app.route('/api/user', methods=['GET', 'POST'])
def collection():
    print("hello, it's me")
    if request.method == 'GET':
        all_users = get_all_users()
        return json.dumps(all_users)
    elif request.method == 'POST':
        data = request.form
        result = add_user(data['firstName'], data['lastName'], data['email'], data['captureLimit'])
        return jsonify(result)



@app.route('/api/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def resource(user_id):
    if request.method == 'GET':
        user = get_single_user(user_id)
        return json.dumps(user)
    elif request.method == 'PUT':
        data = request.form
        result = edit_user(
            user_id, data['firstName'], data['lastName'],  data['email'], data['captureLimit'])
        return jsonify(result)
    elif request.method == 'DELETE':
        result = delete_user(user_id)
        return jsonify(result)


# helper functions

def add_user(firstName, lastName, email, captureLimit):
    try:
        with sqlite3.connect('sf.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO user (firstName, lastName, email, captureLimit) values (?, ?, ?, ?);
                """, (firstName, lastName, email, captureLimit,))
            result = {'status': 1, 'message': 'User Added'}
    except:
        result = {'status': 0, 'message': 'error'}
    return result


def get_all_users():
    with sqlite3.connect('sf.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user ORDER BY id desc")
        all_users = cursor.fetchall()
        return all_users


def get_single_user(user_id):
    with sqlite3.connect('sf.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return user


def edit_user(user_id, firstName, lastName, email, captureLimit):
    try:
        with sqlite3.connect('sf.db') as connection:
            connection.execute("UPDATE user SET firstName = ?, lastName = ?,  email = ?, captureLimit = ? WHERE ID = ?;", (firstName, lastName, email, captureLimit, user_id,))
            result = {'status': 1, 'message': 'USER Edited'}
    except:
        result = {'status': 0, 'message': 'Error'}
    return result


def delete_user(user_id):
    try:
        with sqlite3.connect('sf.db') as connection:
            connection.execute("DELETE FROM user WHERE ID = ?;", (user_id,))
            result = {'status': 1, 'message': 'USER Deleted'}
    except:
        result = {'status': 0, 'message': 'Error'}
    return result


def gen_frames():
# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
    class VideoStream(object):
        """Camera object that controls video streaming from the Picamera"""
        def __init__(self,resolution=(640,480),framerate=30):
                        
            # Initialize the PiCamera and the camera image stream
            self.stream = cv2.VideoCapture(0)
            ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            ret = self.stream.set(3,resolution[0])
            ret = self.stream.set(4,resolution[1])
                
            # Read first frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

            # Variable to control when the camera is stopped
            self.stopped = False
        
        

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
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()


    # Initialize video stream
    videostream = VideoStream(resolution=(imW,imH),framerate=30).start()
    time.sleep(1)

    #for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    while True:

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

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))
                
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

                # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

        # Draw framerate in corner of frame
        cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)

        # All the results have been drawn on the frame, so it's time to display it.
        #cv2.imshow('Object detector', frame) ## Commented for the API version

        # Brute Force Motion JPEG, OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream - NOTE need to work on this cv2.imencode tobytes slows the apparent frame rate by about 50%, plus the UI takes some
        # See: https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        ## API
     

        # Calculate framerate
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc= 1/time1
        

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up
    cv2.destroyAllWindows()
    videostream.stop()


#########  run api  #########
if __name__ == '__main__':
   app.debug = True
   app.run()
