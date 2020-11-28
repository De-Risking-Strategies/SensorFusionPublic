import cv2
import numpy as np
#import numpy as cv
#import cv2 as cv
from seek_to_csv.ir.mosaic320.irCamera_SeekMosaic import irCamera_SeekMosaic
from PIL import Image
import os
#import tensorflow as tf
import sys
from skimage import img_as_ubyte
import os
import argparse
import importlib.util
import time

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
#parser.add_argument('--video', help='Name of the video file',
#                    default='test.mp4')
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()

MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
#VIDEO_NAME = args.video
min_conf_threshold = float(args.threshold)
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

# Path to video file
#VIDEO_PATH = os.path.join(CWD_PATH,VIDEO_NAME)

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

ircamera = irCamera_SeekMosaic(54339)
#imW = ircamera.get(cv2.CAP_PROP_FRAME_WIDTH)
#imH = ircamera.get(cv2.CAP_PROP_FRAME_HEIGHT)

while(1):
    
    fin_time = 0
    init_time = 0

    init_time = time.time()
    
    # Acquire frame and resize to expected shape [1xHxWx3]
    irret, thermal_image_data_fixedpoint = ircamera.read()
    #vlret, visible_image = vlcamera.read()
    
    #print(thermal_image_data_fixedpoint)
    #print(type(thermal_image_data_fixedpoint))
    #print(thermal_image_data_fixedpoint.shape)
    
    #fr1 = cv2.cvtColor(thermal_image_data_fixedpoint, cv2.COLOR_GRAY2BGR)
    #print(fr1.shape)
    
    #resize the image data so we can see it later
    heightt, widtht = thermal_image_data_fixedpoint.shape[:2]
    dsize = (widtht * 2, heightt * 2)
    #print(dsize)
    #print(dsize[0])
    #print(dsize[1])
    #break
    
    thermal_image_data_fixedpoint_4x = cv2.resize(thermal_image_data_fixedpoint, dsize)
    #visible_image = cv2.resize(visible_image, dsize)

    #find min and max pixel values so we can optimize the image contrast
    [minVal, maxVal, minLoc, maxLoc] = cv2.minMaxLoc(thermal_image_data_fixedpoint_4x)
    
    #Now create a version of the data to show on the screen or run through an inferencing model
    imageDelta = maxVal - minVal
    offsetImg = thermal_image_data_fixedpoint_4x - minVal
    scaledImg = offsetImg / imageDelta

    thermal_img_normalized = cv2.normalize(thermal_image_data_fixedpoint_4x, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)
    
    #print(thermal_img_normalized)
    #print(type(thermal_img_normalized))
    #print(thermal_img_normalized.shape)
    #print(scaledImg)
    #print(scaledImg.shape)
    
    frame = img_as_ubyte(scaledImg)
    ##print(frame)
    #print(frame.shape)
    #cv2.imwrite('tt.jpg', scaledImg)
    #np.save('ss.npy', scaledImg)
    
    
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    #ret, frame = video.read()
    if not irret:
      print('Reached the end of the video!')
      break
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
            ymin = int(max(1,(boxes[i][0] * dsize[1])))
            xmin = int(max(1,(boxes[i][1] * dsize[0])))
            ymax = int(min(dsize[1],(boxes[i][2] * dsize[1])))
            xmax = int(min(dsize[0],(boxes[i][3] * dsize[0])))
            
            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 4)

            # Draw label
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
            
    ###########################################################################
    # Object Counting Code - Pushkar

    #final_score = np.squeeze(scores)
    #final_classes = np.squeeze(classes).astype(np.int32)

    #labels_string_s = []
    #for i in category_index:
      #labels_string_s.append(category_index[i]['name'])

    #indices_to_access = np.where(final_score >=0.6)[0].tolist()

    #accessed_mapping = map(final_classes.__getitem__, indices_to_access)

    #accessed_list = list(accessed_mapping)

    #v_dict = {}
    #for i, j in enumerate(labels_string_s):

      #v_dict[j] = accessed_list.count(i+1)
    #print(v_dict)

    #mod_dict = {key:val for key, val in v_dict.items() if val != 0}
    #########################################################################

    #########################################################################
    # Display text on image - Pushkar

    #cV2.putText format is as follows:
    #cv2.putText(image,str(v_dict),
    #    bottomLeftCornerOfText,
    #    font,
    #    fontScale,
    #    fontColor,
    #    lineType)
    #if len(mod_dict)!=0:
        #cv2.putText(frame,str(mod_dict),
            #(1,472),
            #cv2.FONT_HERSHEY_SIMPLEX,
            #0.5,
            #(255,255,0),
            #1)
    #######################################################################        
            
    fin_time = time.time()
    frame_rate_calc = 1 / (fin_time - init_time)

    # Draw framerate in corner of frame
    #cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
    
    # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow('Object detector', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
video.release()
cv2.destroyAllWindows()
