import cv2
import math
import numpy as np

# coding=utf-8

def edge_detection(img_path):
    image = cv2.imread(img_path)
    MAXLEN = 1000
    ratio = 1
    maxLen = max(image.shape[0], image.shape[1])  # 图片长宽
    if maxLen > MAXLEN:
        ratio = maxLen * 1.0 / MAXLEN
    image = cv2.resize(image, (int(image.shape[1] / ratio), int(image.shape[0] / ratio)))  # 缩放
    # print(image.shape)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 将BGR格式转化为灰度图片
    gray = cv2.GaussianBlur(gray, (9, 9), 0)  # 高斯滤波降噪
    edged = cv2.Canny(gray, 150, 10)  # 边缘检测
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # edged=cv2.erode(edged, kernel)
    edged = cv2.dilate(edged, kernel)
    # cv2.imshow('res', edged)
    # cv2.waitKey()

    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:5]  # 面积前5大的轮廓
    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)  # 轮廓的周长
        # c表示输入的点集，epsilon表示从原始轮廓到近似轮廓的最大距离，它是一个准确度参数
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # 4个点的时候就拿出来
        screenCnt = None
        # print(len(approx), cv2.contourArea(approx) * 9, edged.shape[0] * edged.shape[1])
        if len(approx) == 4 and math.fabs(cv2.contourArea(approx)) * 9.0 >= edged.shape[0] * edged.shape[1]:
            # print(len(approx))
            screenCnt = approx
            break
    if screenCnt is None:
        print("Could not found target bbox")
        return image

    res = cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    # cv2.imshow('res', res)
    # cv2.waitKey()
    # 摆正图片
    pts = screenCnt.reshape(4, 2)
    rect = np.zeros((4, 2), dtype='float32')
    # 按顺序找到对应的坐标0123 分别是左上，右上，右下，左下
    # 计算左上，右下
    # numpy.argmax(array, axis) 用于返回一个numpy数组中最大值的索引值
    s = pts.sum(axis=1)
    # print(s)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # 计算右上和左下
    # np.diff()  沿着指定轴计算第N维的离散差值  后者-前者
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    (tl, tr, br, bl) = rect
    # warped = image[int(tl[1]):int(bl[1]),int(tl[0]):int(tl[1])]

    # 计算输入的w和h的值
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # 获取右侧线和上侧线的夹角
    arr_a = np.array([(tl[0] - tr[0]), (tl[1] - tr[1])])
    arr_b = np.array([(tr[0] - br[0]), (tr[1] - br[1])])
    cos_value = arr_a.dot(arr_b) / (np.sqrt(arr_a.dot(arr_a)) * np.sqrt(arr_b.dot(arr_b)))
    angle = np.arccos(cos_value) * (180 / np.pi)
    # print("angle is", angle)
    gap = int(maxHeight * 0.04)
    # print("the gap is", abs(tl[1] - tr[1]))
    if angle > 91:
        # print("adjust gap to 0")
        gap = 0
    # 变化后对应坐标位置
    dst = np.array([
        [0, 0],
        # [maxWidth - 1, int(maxHeight*0.04)],
        [maxWidth - 1, gap],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]],
        dtype='float32')
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight), flags=cv2.INTER_LANCZOS4)
    # cv2.imshow('warped', warped)
    # cv2.waitKey()
    cv2.imwrite(img_path, warped)
