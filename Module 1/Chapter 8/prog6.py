import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('morphological.tif',0)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 2)
dilation = cv2.dilate(img,kernel,iterations = 2)
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

titles=['Original','Erosion','Dilation','Gradient']
output=[img,erosion,dilation,gradient]

for i in xrange(4):
	plt.subplot(2,2,i+1),plt.imshow(output[i],cmap='gray')
	plt.title(titles[i]),plt.xticks([]),plt.yticks([])
plt.show()
