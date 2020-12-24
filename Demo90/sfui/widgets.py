#Widgets Package - DAnderson - 122320
import config
import cv2
def meter(frame,top):# Meter bar package
    color=(0,0,255)
    if top >= 100:
        top = 100
        color = (0, 255, 0)  # 1 BGR format
    #   It never sees 100%!
    elif top >= 98 <= 99:
        top = 120
        color = (0, 255, 0)  # Green
    elif top >= 96 <= 97:
        top = 130
        color = (0, 255, 0)  #
    elif top >= 94 <= 95:
        top = 140
        color = (0, 255, 0)  # Top
    elif top >= 92 <= 93:
        top = 150
        color = (0, 255, 36)
    elif top >= 90 <= 91:
        top = 160
        color = (0, 255, 52)
    elif top >= 88 <= 89:
        top = 170
        color = (0, 255, 69)
    elif top >= 86 <= 87:
        top = 180
        color = (0, 255, 85)
    elif top >= 84 <= 85:
        top = 190
        color = (0, 255, 102)
    elif top >= 81 <= 83:
        top = 200
        color = (0, 255, 110)
    elif top >= 78 <= 80:
        top = 210
        color = (0, 255, 136)
    elif top >= 75 <= 77:
        top = 220
        color = (0, 255, 153)

        # Yellow
    elif top >= 72 <= 74:
        top = 230
        color = (0, 255, 170)
    elif top >= 69 <= 71:
        top = 240
        color = (0, 255, 187)
    elif top >= 66 <= 68:
        top = 250
        color = (0, 255, 204)
    elif top >= 63 <= 65:
        top = 260
        color = (0, 255, 231)
    elif top >= 60 <= 62:
        top = 270
        color = (0, 255, 238)
    elif top >= 57 <= 59:
        top = 280
        color = (0, 255, 254)
    elif top >= 54 <= 56:
        top = 290
        color = (0, 255, 255)
    elif top >= 51 <= 53:
        top = 300
        color = (0, 255, 255)

        # anything below 50 is red
    elif top >= 40 <= 50:
        top = 310
        color = (0, 200, 255)
    elif top >= 30 <= 39:
        top = 330
        color = (0, 150, 255)
    elif top >= 20 <= 29:
        top = 340
        color = (0, 75, 255)
    elif top >= 10 <= 19:
        top = 350
        color = (0, 0, 255)
    elif top >= 0 <= 9:
        top = 360
        color = (0, 0, 255)  # 10    BGR Red

    else:  # no person detected
        top = 360
        color = (0, 0, 255)
    #print('Color: ', color)
    #print('Top: ', top)
    
    start_point = (config.left, top)
    end_point = (config.left, config.bottom)
    image = cv2.line(frame, start_point, end_point, color, config.thickness)
