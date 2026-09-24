import re
import cv2
import numpy as np

class OCRService:
    def extract(self, image_bytes: bytes) -> str | None:
        try:
            import pytesseract
        except ImportError:
            return None

        array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(array, cv2.IMREAD_COLOR)
        if image is None:
            return None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        text = pytesseract.image_to_string(
            gray,
            config="--psm 11 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        ).strip()

        # Keep a compact audit value. If OCR is imperfect, return its text
        # rather than inventing an ID.
        text = re.sub(r"\s+", " ", text)
        return text or None
