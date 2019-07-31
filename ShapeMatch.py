import cv2
def Semitrape(cnt):
    img1 = cv2.imread("shape/semi.jpg")
    img2 = cv2.imread("shape/trapezoid.jpg")
    # cv2.imshow("img1", img1)
    # cv2.imshow("img2", img2)

    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 127, 255,cv2.THRESH_BINARY_INV)
    ret, thresh2 = cv2.threshold(gray2, 127, 255,cv2.THRESH_BINARY_INV)

    # cv2.imshow("thresh", thresh)
    # cv2.imshow("thresh2", thresh2)

    contours1,hierarchy = cv2.findContours(thresh,2,1)
    cnt1 = contours1[0]
    # epsilon = 0.1*cv2.arcLength(cnt1,True)
    # approx = cv2.approxPolyDP(cnt1,epsilon,True)

    contours2,hierarchy = cv2.findContours(thresh2,2,1)
    cnt2 = contours2[0]
    # epsilon2 = 0.1*cv2.arcLength(cnt2,True)
    # approx2 = cv2.approxPolyDP(cnt2,epsilon2,True)

    # cv2.drawContours(img1,cnt1, -1, (0, 0, 255), 5)
    # cv2.drawContours(img2,cnt2, -1, (0, 0, 255), 5)

    # cv2.imshow("img1", img1)

    # cv2.namedWindow("img2", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("img2", 400, 400)
    # cv2.imshow("img2", img2)

    # cv2.waitKey(0)

    semi = cv2.matchShapes(cnt1,cnt,1,0.0)
    trape = cv2.matchShapes(cnt2,cnt,1,0.0)

    if semi < trape:
        result = "SEMICIRCLE"
    else:
        result = "TRAPEZOID"

    return result