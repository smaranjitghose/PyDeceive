
# Loading the libraries we need
import numpy as np
import cv2
import time

#Creating a VideoCapture object to read video from the primary camera
cap=cv2.VideoCapture(0)

#Creating a VideoWriterObject to save the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('wizard_smaran.avi' , fourcc, 20.0, (640,480))

#allow the system to sleep for 3 sec before webcam starts
time.sleep(2)

# Capture the background in range of 30 or 60 without you!
background = 0
for i in range(30):
    ret, background = cap.read()#capturing image

#Now we capture you in real time!
while(cap.isOpened()):
    ret, img = cap.read()
    
    if not ret:
        break
    
    # Converting the color space from BGR to HSV as BGR is more sensitive to light
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Generating mask for red range 1(0-10)
    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv , lower_red , upper_red)
    
    #Generating mask for red range 1(170-180)
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv , lower_red , upper_red)

    #Combining the masks obtained for both the ranges
    mask1 = mask1 + mask2 

    mask1=cv2.morphologyEx(mask1, cv2.MORPH_OPEN ,np.ones((3,3) , np.uint8) , iterations=2)    
    mask2=cv2.morphologyEx(mask1, cv2.MORPH_DILATE ,np.ones((3,3) , np.uint8) , iterations=1)

    # Segmenting out cloth color   
    mask2 = cv2.bitwise_not(mask1)
    
    # Segment the red color part out of the frame using bitwise and with the inverted mask
    layer1 = cv2.bitwise_and(background, background, mask=mask1)
    # Create image showing static background frame pixels only for the masked region
    layer2 = cv2.bitwise_and(img, img, mask=mask2)
    
    final_output = cv2.addWeighted(layer1 , 1, layer2 , 1, 0)
    
    cv2.imshow('Invisible Smaran' , final_output)
    k=cv2.waitKey(10)
    
    #Keyboard Interupt
    if k==27:
        break
        
cap.release()
cv2.destroyAllWindows()