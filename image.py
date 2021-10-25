import numpy as np
import cv2 as cv
from bililine import double_biline

img = cv.imread('image.jpg',-1)

# (h,w,c[B,G,R])
img=np.array(img)
print(img.shape)

SSIZE=img.shape
DSIZE=[512,724]
#三通道分开处理
b,g,r = cv.split(img)

b=double_biline(b,SSIZE,DSIZE)
g=double_biline(g,SSIZE,DSIZE)
r=double_biline(r,SSIZE,DSIZE)
img = cv.merge((b,g,r))
# image=double_biline(img,SSIZE,DSIZE)
# img = cv.cvtColor(image, cv.COLOR_RGB2BGR)

cv.imshow('image', img)
cv.waitKey(0)
cv.imwrite("./out.jpg",img,[int(cv.IMWRITE_JPEG_QUALITY),100])
cv.destroyAllWindows()

