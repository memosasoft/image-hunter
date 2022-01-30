import cv2

def test():
    img = cv2.imread("vision.jpg")
    cv2.imshow('Original Image', img) 
    cv2.waitKey(0)

test()