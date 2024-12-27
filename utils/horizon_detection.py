import cv2
import numpy as np


def trim_horizon(img):
    img299 = cv2.resize(img, (299, 299))
    processed = img299.copy()
    processed = cv2.GaussianBlur(processed, (7, 7), 3)
    processed = cv2.Canny(processed, 50, 90)
    hitmiss_kernel = np.array(
        [[0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]]
    )
    processed = cv2.morphologyEx(processed, cv2.MORPH_HITMISS, hitmiss_kernel)
    processed = cv2.morphologyEx(processed, cv2.MORPH_DILATE, np.ones((7, 19)))
    processed = cv2.morphologyEx(processed, cv2.MORPH_ERODE, np.ones((1, 29)))
    processed = cv2.morphologyEx(processed, cv2.MORPH_DILATE, np.ones((9, 1)))

    lines = cv2.HoughLines(processed, 1, np.pi/36, 180, min_theta=np.pi/2-np.pi/64, max_theta=np.pi/2+np.pi/64)
    if lines is not None:
        horizon_count = 0
        img_horizons = []
        for line in lines:
            if horizon_count >= 10:
                break
            for rho, theta in line:
                x1 = 0
                x2 = img299.shape[0]
                y1 = int((rho - x1 * np.cos(theta)) / np.sin(theta))
                y2 = int((rho - x2 * np.cos(theta)) / np.sin(theta))
                if y1 > img299.shape[0]/3 or y2 > img299.shape[0]/3:
                    horizon_count += 1
                    if y1 < img299.shape[0]-10 and y2 < img299.shape[0]-10:
                        img_horizons.append(((x1, y1), (x2, y2)))

        if len(img_horizons):
            horizon = max(img_horizons, key=lambda e: min(e[0][1], e[1][1]))
            print(f"Horizon line detected (y1={horizon[0][1]}, y2={horizon[1][1]})")
            cut = img299[:min(horizon[0][1], horizon[1][1]),:]
            return cv2.resize(cut, (img299.shape[0], img299.shape[1]))

    print("No horizon line detected")
    return img