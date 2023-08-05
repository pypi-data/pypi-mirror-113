from supercv import showimg_binary_img, showimg_by_path
import maso
from cv2 import cv2 as cv
print(dir(maso))
print(maso.test())

showimg_by_path(r'C:\Users\admin\anaconda3\envs\maso\Lib\site-packages\maso\圖片已上傳至：2021-7-14 12-23.png')


img = cv.imread(r'C:\Users\admin\anaconda3\envs\maso\Lib\site-packages\maso\圖片已上傳至：2021-7-14 12-23.png')
showimg_binary_img(img,127)