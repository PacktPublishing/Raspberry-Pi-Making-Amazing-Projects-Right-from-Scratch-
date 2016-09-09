import cv2
img = cv2.imread('lena_color_512.tif',1)
cv2.imshow('Lena',img)
keyPress = cv2.waitKey(0)
if keyPress == ord('q'):	
	cv2.destroyWindow('Lena')					
elif keyPress == ord('s'):				
	cv2.imwrite('output.jpg',img)
	cv2.destroyWindow('Lena')
