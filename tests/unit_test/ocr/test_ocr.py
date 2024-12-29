import os.path

import pytest
from fastapi.testclient import TestClient

from ntnu_captcha_service.route import app

client = TestClient(app)


class TestOcr:
    @pytest.mark.parametrize(
        "image_path,ans",
        [
            ("ocr1.jpeg", "kthz"),
            ("ocr2.jpeg", "rlwe"),
            ("ocr3.jpeg", "3-7"),
            ("ocr4.jpeg", "ufap"),
            ("ocr5.jpeg", "paot"),
            ("ocr6.jpeg", "fjcs"),
            ("ocr7.jpeg", "8+8"),
            ("ocr8.jpeg", "annz"),
            ("ocr9.jpeg", "1+4"),
            ("ocr10.jpeg", "5-9"),
        ],
    )
    def test_ocrs(self, image_path: str, ans: str):
        with open(os.path.join("tests/unit_test/ocr", image_path), "rb") as f:
            response = client.post("/solve", headers={"Content-Type": "image/jpeg"}, data=f)
            assert response.status_code == 200
            assert ans in response.json()["response"]
