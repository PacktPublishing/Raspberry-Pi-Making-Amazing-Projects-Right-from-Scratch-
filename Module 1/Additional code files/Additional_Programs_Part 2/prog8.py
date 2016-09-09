import cv2
import numpy as np
import time

#Image Transitioning Effect in OpenCV and Python

img1 = cv2.imread('/home/pi/book/test_set/4.2.03.tiff',1)
img2 = cv2.imread('/home/pi/book/test_set/4.2.04.tiff',1)

for i in np.linspace(0,1,40):
	alpha=i
	beta=1-alpha
	print 'ALPHA ='+ str(alpha)+' BETA ='+str (beta)  
	cv2.imshow('Image Transition',cv2.addWeighted(img1,alpha,img2,beta,0))
	time.sleep(0.05)
	if cv2.waitKey(1) == 27 :
		break

cv2.destroyAllWindows()
