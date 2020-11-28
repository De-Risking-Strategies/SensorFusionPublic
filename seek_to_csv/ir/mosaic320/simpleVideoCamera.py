import cv2
import numpy as np
import numpy as cv
#import cv2 as cv
from irCamera_SeekMosaic import irCamera_SeekMosaic
from PIL import Image


## read an image from the current folder
#image = cv2.imread('cat.jpg')

vlcamera = cv2.VideoCapture(0)

ircamera = irCamera_SeekMosaic(54339)

while 1:
    irret, thermal_image_data_fixedpoint = ircamera.read()
    vlret, visible_image = vlcamera.read()
    
    #resize the image data so we can see it later
    height, width = thermal_image_data_fixedpoint.shape[:2]
    dsize = (width * 2, height * 2)
    
    thermal_image_data_fixedpoint_4x = cv2.resize(thermal_image_data_fixedpoint, dsize)
    visible_image = cv2.resize(visible_image, dsize)

    #find min and max pixel values so we can optimize the image contrast
    [minVal, maxVal, minLoc, maxLoc] = cv2.minMaxLoc(thermal_image_data_fixedpoint_4x)
    
    #Now create a version of the data to show on the screen or run through an inferencing model
    imageDelta = maxVal - minVal
    offsetImg = thermal_image_data_fixedpoint_4x - minVal
    scaledImg = offsetImg / imageDelta

    thermal_img_normalized = cv2.normalize(thermal_image_data_fixedpoint_4x, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)

    # then we'll just show the images in OpenCV windows
    if vlret:
        cv2.imshow('Visible', visible_image)
    if irret:
        cv2.imshow('Thermal IR', thermal_img_normalized)
        cv2.imshow('Presentation IR', scaledImg)
    k=cv2.waitKey(1)

vlcamera.release()
ircamera.release()
cv.destroyAllWindows()


