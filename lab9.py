import cv2
import numpy as np
 
image = cv2.imread('input.jpg')
 

if image is None:
    print('Could not read image')
 

kernel_identity = np.array([[0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]])
 
identity = cv2.filter2D(src=image, ddepth=-1, kernel=kernel_identity)
 
cv2.imshow('Original', image)
cv2.imshow('Identity', identity)
cv2.waitKey()
cv2.imwrite('identity.jpg', identity)
cv2.destroyAllWindows()
 

kernel_blur = np.ones((5, 5), np.float32) / 25
blurred = cv2.filter2D(src=image, ddepth=-1, kernel=kernel_blur)
 
cv2.imshow('Original', image)
cv2.imshow('Kernel Blur', blurred)  
cv2.waitKey()
cv2.imwrite('blur_kernel.jpg', blurred)
cv2.destroyAllWindows()
