import cv2
import numpy as np

curent_ovosh = " "

def detect_ovosh(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_black = np.array([0, 19, 0])
    upper_black = np.array([239, 182, 142])

    lower_red = np.array([0, 132, 31])
    upper_red = np.array([12, 255, 255])

    lower_yellow = np.array([16, 66, 135])
    upper_yellow = np.array([38, 255, 255])

    lower_green = np.array([0, 99, 0])
    upper_green = np.array([255, 241, 163])


    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imshow("frame red", mask_red)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    cv2.imshow("frame yellow", mask_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    cv2.imshow("frame green", mask_green)


    pixel_count_red = cv2.countNonZero(mask_red)
    pixel_count_yellow = cv2.countNonZero(mask_yellow)
    pixel_count_green = cv2.countNonZero(mask_green)
    #print(f"red: {pixel_count_red} | yellow: {pixel_count_yellow} | green: {pixel_count_green}")


    if  pixel_count_red > pixel_count_green and pixel_count_red > pixel_count_yellow:
        curent_ovosh = "red_perec"
    elif pixel_count_yellow > pixel_count_green and pixel_count_yellow > pixel_count_red:
        curent_ovosh = "lemon"
    elif pixel_count_green > pixel_count_yellow and pixel_count_green > pixel_count_red:
        curent_ovosh = "grysha"

    print(curent_ovosh)

    return curent_ovosh
