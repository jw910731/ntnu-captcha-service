import dataclasses
import re
import string
from dataclasses import dataclass

import cv2
import easyocr
import numpy as np

reader = easyocr.Reader(["en"], gpu=False)


@dataclass
class CaptchaSolver:
    image: np.ndarray
    reader: easyocr.Reader = dataclasses.field(default=None)

    def __post_init__(self) -> np.ndarray:
        hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, np.array([0, 100, 64]), np.array([255, 255, 255]))
        mask = cv2.resize(
            ~mask,
            (self.image.shape[1] * 3, self.image.shape[0] * 3),
            interpolation=cv2.INTER_LANCZOS4,
        )
        mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, np.ones((3, 3)))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3)))
        mask = mask[:, :, np.newaxis]
        mask = np.repeat(mask, repeats=3, axis=2)
        self.image = mask

    def solve(self):
        allow_lists = [
            (string.ascii_lowercase, r"^[a-z]+$", []),
            (string.digits + "x+-=", r"^[0-9][+\-x][0-9]", [("=", "")]),
        ]

        def process(allowlist: str, regex: str, replace_rules: list[tuple[str, str]]):
            text = "".join(reader.readtext(self.image, detail=0, allowlist=allowlist, link_threshold=0))
            mtch = re.match(regex, text)
            if not mtch:
                return None
            text = mtch[0]
            for replace_rule in replace_rules:
                text = text.replace(*replace_rule)
            return text.replace(" ", "")

        result = [process(*allow) for allow in allow_lists]
        return [x for x in result if x is not None]
