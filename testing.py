import cv2
import numpy as np
import math

cam = cv2.VideoCapture(0)

while True:
    check, frame = cam.read()
    image = cv2.resize(frame, (320, 240))
    image_height, image_width, _ = image.shape
    cv2.imshow('image', image)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    cannyImage = cv2.Canny(blur_image, 80, 200)
    cv2.imshow('cannyImage', cannyImage)

    lines = cv2.HoughLines(cannyImage, 1, np.pi / 220, 80, None, 0, 0)

    if lines is not None:
        # Initialize a dictionary to store lines grouped by angle
        angle_lines_dict = {}

        for i in range(len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]

            # Calculate line strength (length)
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            length = int(math.sqrt(x0**2 + y0**2))

            # Group lines by angle
            if ((theta > 3 * np.pi / 4) or (theta < np.pi / 4)):
                if theta not in angle_lines_dict:
                    angle_lines_dict[theta] = []
                angle_lines_dict[theta].append((x0, y0, length))

        # Select the two strongest lines with different rho values from each angle group
        for angle, lines_list in angle_lines_dict.items():
            lines_list.sort(key=lambda x: x[2], reverse=True)
            strongest_lines = lines_list[:2]

            # Ensure different rho values
            if len(strongest_lines) == 2 and strongest_lines[0][0] != strongest_lines[1][0]:
                for x0, y0, _ in strongest_lines:
                    pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
                    pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
                    cv2.line(image, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

        cv2.imshow("Detected Lines (in red) - Custom Filter", image)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
