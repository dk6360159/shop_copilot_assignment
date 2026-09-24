import cv2
import numpy as np
from app.cv.preprocessing import decode_image, preprocess

class DefectClassifier:
    """
    Lightweight classical-CV classifier for synthetic assignment images.

    It intentionally does not pretend to be production-grade metrology.
    The classifier detects visual patterns that the included image generator
    creates: scratch lines, crack-like connected lines, and dimensional
    deviation markers.
    """

    def classify(self, image_bytes: bytes) -> str:
        image = decode_image(image_bytes)
        gray, edges = preprocess(image)

        # Detect strong red/orange synthetic deviation marker.
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        red1 = cv2.inRange(hsv, (0, 80, 80), (15, 255, 255))
        red2 = cv2.inRange(hsv, (165, 80, 80), (180, 255, 255))
        red_ratio = float(np.count_nonzero(red1 | red2)) / red1.size

        if red_ratio > 0.005:
            return "dimensional_deviation"

        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=30,
            minLineLength=25,
            maxLineGap=8,
        )

        line_count = 0 if lines is None else len(lines)
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        irregular = sum(
            1 for c in contours
            if 10 < cv2.contourArea(c) < 5000
        )

        # The synthetic crack image contains many short connected segments.
        if line_count >= 10 or irregular >= 8:
            return "crack"

        if line_count >= 3:
            return "surface_scratch"

        return "no_defect"
