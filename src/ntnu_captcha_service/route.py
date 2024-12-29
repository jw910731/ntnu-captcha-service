import cv2
import numpy as np
from fastapi import Depends, FastAPI
from PIL import Image

from ntnu_captcha_service.captcha import CaptchaSolver
from ntnu_captcha_service.requests import image_request

app = FastAPI()


@app.post("/solve")
def solve(img: Image = Depends(image_request)):
    solver = CaptchaSolver(image=cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
    return {"response": solver.solve()}
