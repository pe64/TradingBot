#from turtle import color
#import easyocr
#import cv2
#from PIL import Image
#import numpy as np
#
#def ocr_fund51(path):
#    color_img = cv2.imread(path)
#    cropped = color_img[5:23, 7:85]
#    gray_img = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
#    thresh,gray_img = cv2.threshold(gray_img, 123, 255, cv2.THRESH_BINARY)
#    reader = easyocr.Reader(['en'])
#    ret = reader.readtext(gray_img)
#    gray = Image.fromarray(gray_img)
#    gray.save("cache/gray.png")
#    if len(ret) == 1: 
#       return ret[0][1]
#    
#def ocr_em(path):
#    color_img = cv2.imread(path)
#    print(color_img.shape)
#    cropped = color_img[0:36, 7:85]
#    gray_img = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
#    thresh,gray_img = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)
#    gray_img = cv2.dilate(gray_img,np.ones(shape=(3,1)))
#    #gray_img = cv2.erode(gray_img,np.ones(shape=(5,1)))
#    reader = easyocr.Reader(['en'])
#    ret = reader.readtext(gray_img)
#    gray = Image.fromarray(gray_img)
#    gray.save("cache/gray.png")
#    if len(ret) == 1: 
#       return ret[0][1]
#
#if __name__ == "__main__":
#
#    ret = ocr_fund51("cache/fund51.png")
#    print(ret)
#