import cv2


cam = cv2.VideoCapture(0)
while True:
    check, frame = cam.read()
    image = cv2.resize(frame,(320,240))
    image_height, image_width, _ = image.shape
    cv2.imshow('image', image)
    

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale', gray_image)
    

    blur_image = cv2.GaussianBlur(gray_image, (5,5), 0)
    cv2.imshow('blur', blur_image)
     

    cannyImage = cv2.Canny(blur_image, 60, 180)
    cv2.imshow('cannyImage', cannyImage)

    sobelxy_image = cv2.Sobel(src=blur_image, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
    cv2.imshow('sobelxy', sobelxy_image)
    
    check,threshold_binary_image = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY) 
    cv2.imshow('threshold binary image',threshold_binary_image)

    threshold_binary_guassian_image = cv2.adaptiveThreshold(blur_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    cv2.THRESH_BINARY_INV,11,2)
    cv2.imshow('threshold binary guassian image',threshold_binary_guassian_image)


    key = cv2.waitKey(1)
    if key == 27:
        break
cam.release()
cv2.destroyAllWindows()