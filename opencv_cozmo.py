# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 18:38:26 2018

@author: William Egbert
"""

import numpy as np
import cv2
import cozmo
import scipy.misc as misc
import time

capture = cv2.VideoCapture(0)
face_detect=cv2.CascadeClassifier(
		'C:\\Users\\Student\\Anaconda3\\pkgs\\opencv3-3.1.0-py35_0\\Library\\etc\\haarcascades\\haarcascade_frontalface_default.xml')

def cozmo_prog (robot: cozmo.robot.Robot):
	robot.camera.image_stream_enabled = True
	
	while(True):
    # Capture frame-by-frame
		ret, frame = capture.read()
		print(0)
    # Our operations on the frame come here
		if ret is True:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces=face_detect.detectMultiScale(gray, 1.3, 5)
    #draw box around face? 
      
			for (x,y,w,h) in faces:
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
				roi_gray = gray[y:y+h, x:x+w]
				roi_color = frame[y:y+h, x:x+w]
            
				if len(roi_gray) != 0:
					_, thresh1 = cv2.threshold(roi_gray,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
					cozface = misc.toimage(cv2.resize(thresh1, (cozmo.oled_face.dimensions()), 0, 0))
					print(0)
					ledface = cozmo.oled_face.convert_image_to_screen_data(misc.toimage(cozface))
					robot.display_oled_face_image(screen_data = ledface, duration_ms = 10)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		cv2.imshow('frame',frame)
cozmo.run_program(cozmo_prog)

capture.release()
cv2.destroyAllWindows()