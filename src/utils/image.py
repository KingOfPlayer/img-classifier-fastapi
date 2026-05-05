
import cv2
import numpy as np

def load_image(image_uri: str):
    #print(image_uri);
    nparr = np.frombuffer(image_uri, np.uint8)

    # 2. Decode the array into an image (BGR format by default)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img