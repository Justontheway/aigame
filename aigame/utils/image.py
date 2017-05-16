import logging
from PIL import Image, ImageGrab
import cv2
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

class ImageTest(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def test(self):
        im = ImageGrab.grab()
        im.show()
        print(im)

    def objectDetection(self):
        '''
        http://blog.csdn.net/liqiancao/article/details/55670749
        '''
        # Step1. Load and convert
        image = cv2.imread("C:\\Users\\lenovo\\Desktop\\new_doc\\restart.jpg")
        image = cv2.imread("C:\\Users\\lenovo\\Desktop\\new_doc\\test.png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('image', gray)
        cv2.waitKey(0)
        # Step2. Sobel gradient
        gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
        # subtract the y-gradient from the x-gradient
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)

        # Step3. subtract noise
        # blur and threshold the image
        blurred = cv2.blur(gradient, (9, 9))
        (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
        # Step4. fill
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        # Step5. expand
        # perform a series of erosions and dilations
        closed = cv2.erode(closed, None, iterations=4)
        closed = cv2.dilate(closed, None, iterations=4)

        # Step6. find contours
        (_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

        # compute the rotated bounding box of the largest contour
        rect = cv2.minAreaRect(c)
        box = np.int0(cv2.boxPoints(rect))

        # draw a bounding box arounded the detected barcode and display the image
        cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
        cv2.imshow("Image", image)
        cv2.waitKey(0)

    def imageMatch(self):
        # Step1. Load and convert
        img = cv2.imread("C:\\Users\\lenovo\\Desktop\\new_doc\\Step2.jpg", 0)
        #img2 = img.copy()
        template = cv2.imread("C:\\Users\\lenovo\\Desktop\\new_doc\\chonglai.jpg", 0)
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        for meth in methods:
            self._imageMatch(img, template, meth)
        plt.show()

    def _imageMatch(self, img, template, meth):
        #img = img2.copy()
        method = eval(meth)
        w, h = template.shape[::-1]
        # Apply template Matching
        res = cv2.matchTemplate(img, template, method)
        _, _, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img, top_left, bottom_right, 255, 2)
        plt.figure()
        plt.subplot(121),plt.imshow(res, cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img, cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

if __name__ == "__main__":
    #ImageTest().test()
    #ImageTest().objectDetection()
    ImageTest().imageMatch()
