import cv2
import numpy
import math 

cam = cv2.VideoCapture(0)

vertical_lines = []
similer_angle =[]

while True:
    check, frame = cam.read()
    image = cv2.resize(frame,(320,240))
    image_height, image_width, _ = image.shape
    cv2.imshow('image', image)
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blur_image = cv2.GaussianBlur(gray_image, (5,5), 0)

    cannyImage = cv2.Canny(blur_image, 80, 200)
    cv2.imshow('cannyImage', cannyImage)

    lines = cv2.HoughLines(cannyImage, 1, numpy.pi / 220, 80, None, 0, 0)

    if lines is not None:
        for i in range(0,len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            if ((theta > 3*numpy.pi/4) or (theta <numpy.pi/4)):
                vertical_lines.append(lines[i])
        similer_angle.append(verical_lines[0])
    if line is not None:
        for line in vertical_lines[1:]:
            if((vertical_lines[0][0][1]/line[0][1]<2) and (vertical_lines[0][0][1]/line[0][1]>0)):
                similer_angle.append(line)
    if line is not None:
        for line in similer_angle[1:]:
            if((similer_angle[0][0][0]/line[0][0]>2) and (similer_angle[0][0][0]/line[0][0]<0)):
                rho = line[0][0]
                theta = line[0][1]  
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho 
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv2.line(image, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)  
                cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", image)

    key = cv2.waitKey(1)
    if key == 27:
        break
cam.release()
cv2.destroyAllWindows()
