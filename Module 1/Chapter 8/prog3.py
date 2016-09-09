import cv2
import numpy as np
from matplotlib import pyplot as plt

input = cv2.imread('GaussianTest.png',1)

#input = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

#Image blurring/smoothing by Gaussian Blurring

output = cv2.GaussianBlur(input,(3,3),0)

cv2.imshow("Input",input)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Output",output)
cv2.waitKey(0)
cv2.destroyAllWindows()