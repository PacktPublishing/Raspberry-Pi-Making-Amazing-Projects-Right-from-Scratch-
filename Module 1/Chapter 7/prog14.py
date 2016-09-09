import cv2
import matplotlib.pyplot as plt

img = cv2.imread('4.2.07.tiff',1)
img = cv2.cvtColor ( img , cv2.COLOR_BGR2RGB )
plt.imshow ( img ) , plt.title ('COLOR IMAGE'), plt.xticks([]) , plt.yticks([])
plt.show()