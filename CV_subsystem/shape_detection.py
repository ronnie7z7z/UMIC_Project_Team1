import numpy as np                                                                         #importing essential libraries 
import cv2
import scipy.ndimage
import os

cap = cv2.VideoCapture('recording.avi')                                                    #testing on a recorded video from camera feed
i = 0

def empty(a):
	pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", 227, 255, empty)                            #creating trackbars for canny edge detection- to be able to determine most favourable values
cv2.createTrackbar("Threshold2", "Parameters", 50, 255, empty)
cv2.createTrackbar("Area", "Parameters", 2000, 30000, empty)                               #area trackbar for tweaking minimum area parameter

current_directory = os.getcwd()                                                            #section for creating new folder where the images of frames will be saved for further processing
final_directory = os.path.join(current_directory, r'saved_images')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
os.chdir(final_directory)

def getContours(img, imgContour, imgCopy, i):                                               #function for contour detection+drawing, along with saving images

	contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   #finding contours present

	for cnt in contours:                                                                    #iterating over all contours
		cv2.drawContours(imgContour, cnt, -1, (255,0,255), 7)
		perimeter = cv2.arcLength(cnt, True)               
		approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
		(x,y,w,h) = cv2.boundingRect(approx)                                                #bounding rectangle around contours to return dimensions
		ar = float(w/h)                                                                     #defining aspect ratio

		area = cv2.contourArea(cnt)                                                         #area of contour found
		areaMin = cv2.getTrackbarPos('Area', "Parameters")
		if area>areaMin and area<6000 and ar>0.7 and ar<2:                                  #applying certain threshold for area & aspect ratio to avoid unnecessary contours 
			#cv2.drawContours(imgContour, cnt, -1, (255,0,255), 7)
			
			cv2.rectangle(imgContour, (x,y), (x+w, y+h), (0,255,0), 5)                      #draws bounding rect
			ROI = imgCopy[y:y+h, x:x+w]                                                     #defining region of interest (ROI) to be saved

			#cv2.imshow('ROI', ROI)
			#print(i)
			#cv2.imwrite("{}.png".format(i+1), ROI)                                          #saving images of frames detected 

			i+=1

	return i


while True:                                                                                 #main loop over all frames of video
	success, img = cap.read()
	imgContour = img.copy()
	imgCopy = img.copy()
                                                                                            #Image processing segment-
	imgBlur = cv2.GaussianBlur(img, (7,7), 1)                                               #- applying gaussian blur
	imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)                                     #- converting to grayscale

	smooth = scipy.ndimage.median_filter(imgGray, size=2)                                   #- smoothening the image
	#ret,thresh = cv2.threshold(smooth,100,255,cv2.THRESH_BINARY)

	threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
	threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
	imgCanny = cv2.Canny(smooth, threshold1, threshold2)                                    #- canny edge detection with thresholds


	kernel = np.ones((5,5))
	imgDil = cv2.dilate(imgCanny, kernel, iterations=1)                                     #- dilating canny image

	i = getContours(imgDil, imgContour, imgCopy, i)                                         #- obtaining contours through get contour function

	cv2.imshow("Result", imgContour)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	