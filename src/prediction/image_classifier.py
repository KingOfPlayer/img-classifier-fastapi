from src.utils.image import load_image
from prediction.models.object_detection_model import predict, preprocess_image

def Object_detection(image: str):
    image = load_image(image)
    image = preprocess_image(image)
    output = predict(image)
    
    return output