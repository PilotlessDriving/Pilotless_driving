# -*- coding: utf-8 -*-
# @Author: yucheng

import sys
import cv2
import numpy as np


def preprocess(gray):
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    median = cv2.medianBlur(gaussian, 5)
    # sobel算子 x方向求梯度
    sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize=3)
    # 二值化
    ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
    dilation = cv2.dilate(binary, element2, iterations=1)
    erosion = cv2.erode(dilation, element1, iterations=1)
    dilation2 = cv2.dilate(erosion, element2, iterations=3)
    # cv2.imshow('dilation2', dilation2)
    # cv2.waitKey(0)
    return dilation2


def findPlateNumberRegion(img):
    region = []

    _, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        cnt = contours[i]

        area = cv2.contourArea(cnt)

        epsilon = 0.001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        rect = cv2.minAreaRect(cnt)
        print('rect is:'+str(rect))

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        ratio = float(width) / float(height)
        print(ratio)
        if ratio > 5 or ratio < 2:
            continue
        region.append(box)

    return region


def detect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dilation = preprocess(gray)

    region = findPlateNumberRegion(dilation)

    for box in region:
        cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

        ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
        xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]

        ys_sorted_index = np.argsort(ys)
        xs_sorted_index = np.argsort(xs)

        x1 = box[xs_sorted_index[0], 0]
        x2 = box[xs_sorted_index[3], 0]

        y1 = box[ys_sorted_index[0], 1]
        y2 = box[ys_sorted_index[3], 1]

        img_org2 = img.copy()
        img_plate = img_org2[y1:y2, x1:x2]
        cv2.imshow('number plate', img_plate)
        cv2.imwrite('./test_pic/number_plate.jpg', img_plate)

        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        cv2.imshow('img', img)
        cv2.imwrite('./test_pic/contours.png', img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    imagePath = './test_pic/10.jpg'

    img = cv2.imread(imagePath)
    detect(img)

