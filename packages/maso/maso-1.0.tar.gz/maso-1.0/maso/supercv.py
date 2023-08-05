from cv2 import cv2 as cv

def showimg_by_path(image_path):
    image = cv.imread(image_path)
    cv.imshow('',image)
    cv.waitKey()
    cv.destroyAllWindows()

def showimg_by_ndarray(img_array):
    cv.imshow('',img_array)
    cv.waitKey()
    cv.destroyAllWindows()

def showimg_binary_img(img_array,threshold):
    gray = cv.cvtColor(img_array,cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray,threshold,255,cv.THRESH_BINARY)
    cv.imshow('',binary)
    cv.waitKey()
    cv.destroyAllWindows()
