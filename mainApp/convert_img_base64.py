import cv2
import numpy as np
import io
from PIL import Image
import base64

def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def readb64(base64_data):
    jpg_original = base64.b64decode(base64_data)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    imageBGR = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
    return image

def read64_np(base64_data):
    jpg_original = base64.b64decode(base64_data)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    imageBGR = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
    return np.asarray(image)