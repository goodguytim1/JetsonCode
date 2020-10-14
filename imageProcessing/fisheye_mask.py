import cv2
import numpy as np


def create_fisheye_mask(prev, next, mask_radius=3):
    """Creates a mask for the fisheye lens"""
    h, w, ch = prev.shape
    center = (int(w / 2), int(h / 2))
    radius = int(w / mask_radius)

    mask = np.zeros(shape=prev.shape, dtype="uint8")
    cv2.circle(mask, center, radius, (255, 255, 255), -1, 8, 0)

    maskedPrev = np.zeros_like(prev)
    maskedPrev[mask > 0] = prev[mask > 0]

    maskedNext = np.zeros_like(next)
    maskedNext[mask > 0] = next[mask > 0]
    # cv2.imshow("fisheye masked", maskedPrev)
    # cv2.waitKey(0)
    return maskedPrev, maskedNext


def image_crop(img, mask_radius_ratio=3.5):
    """Crops the inputted image according to mask radius ratio"""
    w = img.shape[0]
    h = img.shape[1]
    s = w / mask_radius_ratio

    top_edge = int(h/2-s)
    bottom_edge = int(h/2 + s)

    left_edge = int(w/2-s)
    right_edge = int(w/2 + s)

    croppedImg = img[left_edge:right_edge,  top_edge:bottom_edge, :]
    # cv2.imshow("Cropped image", croppedImg)
    # cv2.waitKey(0)
    return croppedImg


def create_mask_displayed(frame):
    """Ugly manual way of creating a mask w/ a trackbar"""
    h, w, ch = frame.shape
    halfsies = (int(w / 4), int(h / 4))
    frame = cv2.resize(frame, halfsies)

    quarterlies = (int(halfsies[0] / 2), int(halfsies[1] / 2))

    def nothing(*arg):
        pass

    cv2.namedWindow('og')
    cv2.namedWindow('masked_og')
    cv2.createTrackbar('mask_radius', 'masked_og', int(
        halfsies[0]/3), halfsies[0], nothing)

    while True:
        mask_radi = cv2.getTrackbarPos('mask_radius', 'masked_og')

        mask = np.zeros(shape=frame.shape, dtype="uint8")
        mask = cv2.resize(mask, halfsies)
        cv2.circle(mask, quarterlies, mask_radi, (255, 255, 255), -1, 8, 0)

        cv2.imshow('og', frame)
        masked = np.zeros_like(frame)
        masked[mask > 0] = frame[mask > 0]
        cv2.imshow('masked_og', masked)

        # Wait 30s for ESC and return false if pressed
        k = cv2.waitKey(30) & 0xff
        if (k == 27):
            break

    cv2.destroyAllWindows()
