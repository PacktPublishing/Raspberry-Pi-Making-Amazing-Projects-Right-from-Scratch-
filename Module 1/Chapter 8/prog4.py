import cv2
import numpy as np
import random
from matplotlib import pyplot as plt

img = cv2.imread('4.2.07.tiff',1)

input = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

output = cv2.bilateralFilter(input,19,75,75)

plt.subplot(121),plt.imshow(input),plt.title('Original Image')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(output),plt.title('Bilateral Filtering')
plt.xticks([]), plt.yticks([])
plt.show()
