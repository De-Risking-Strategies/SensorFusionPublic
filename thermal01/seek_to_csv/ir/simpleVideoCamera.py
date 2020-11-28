import cv2
import numpy as np
import numpy as cv
#import cv2 as cv
from irCamera_SeekMosaic import irCamera_SeekMosaic
#from PIL import Image

vlcamera = cv2.VideoCapture(0)
ircamera = irCamera_SeekMosaic(54339)

dsize = (1, 1) #default is no resizing
vlret = False
irret = False

while 1:
    if vlcamera is not None:
        vlret, visible_image = vlcamera.read()
    
    if ircamera is not None:
        irret, thermal_image_data_fixedpoint = ircamera.read()

        #resize the image data so we can see it later
        height, width = thermal_image_data_fixedpoint.shape[:2]
        if height < 320:
            # make this a little bit larger to view it clearly
            dsize = (width * 4, height * 4)
        else:
            dsize = (width * 2, height * 2)
   
        thermal_image_data_fixedpoint_enlarged = cv2.resize(thermal_image_data_fixedpoint, dsize)
        #find min and max pixel values so we can optimize the image contrast
        [minVal, maxVal, minLoc, maxLoc] = cv2.minMaxLoc(thermal_image_data_fixedpoint_enlarged)
        
        #Now create a version of the data to show on the screen or run through an inferencing model
        imageDelta = maxVal - minVal
        offsetImg = thermal_image_data_fixedpoint_enlarged - minVal
        scaledImg = offsetImg / imageDelta

        #thermal_img_normalized = cv2.normalize(thermal_image_data_fixedpoint_enlarged, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)

    # then we'll just show the images in OpenCV windows
    if vlret:
        cv2.imshow('Visible', visible_image)
    if irret:
        #cv2.imshow('Thermal IR', thermal_img_normalized)
        cv2.imshow('Presentation IR', scaledImg)
    k=cv2.waitKey(1)

#
# And finally cleanup
#

if vlcamera is not None:
    vlcamera.release()
    
if ircamera is not None:
    ircamera.release()

cv.destroyAllWindows()


