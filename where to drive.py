import cv2
import numpy
import math 

cam = cv2.VideoCapture(0)

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
    
    def seperation(line):
        rho = line[0][0]
        theta = line[0][1]
        a = math.cos(theta)
        x0 = a * rho
        return x0

    if lines is not None:

        vertical_lines = []
        similer_angle =[]
        
        for i in range(0,len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            if ((theta > 3*numpy.pi/4) or (theta <numpy.pi/4)):
                vertical_lines.append(lines[i])
        if len(vertical_lines) > 0:
            similer_angle.append(vertical_lines[0]) 

        for line in vertical_lines[1:]:
            if len(line) > 0:
                if((vertical_lines[0][0][1]/line[0][1]<1.5) and (vertical_lines[0][0][1]/line[0][1]>0.5)):#Getting the theta of first line in vertical_lines and dividng by the theta of other lines in vertical_lines to see if they have similer enough theta.
                    similer_angle.append(line)
        similer_angle.sort(key=seperation) 
        first = similer_angle[0]  
        last = similer_angle[-1]    
        woking = [first, last]
        for line in woking:        
            rho = line[0][0]
            theta = line[0][1]  
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho 
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(image, pt1, pt2, (0,0,255), 3, cv2.LINE_AA) 
            cv2.circle(image,(447,63), 63, (0,0,255), -1) 
            cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", image) 
        centerline = (first[0][0] + last[0][0])/2
        center = image_width/2
        if centerline - center > 0:
            while centerline - center > 0:
                #do turn stuff
                pass
        elif centerline - center < 0:
            while centerline - center < 0:
                #do other turn stuff
                pass
        else:
           #go stright  
           pass

    key = cv2.waitKey(1)
    if key == 27:
        break
cam.release()
cv2.destroyAllWindows()
