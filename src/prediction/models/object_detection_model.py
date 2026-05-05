
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet50
from torchvision.models import ResNet50_Weights
import pickle
from sklearn.preprocessing import LabelEncoder
import time
import cv2
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, "detector.pth")
LE_FILE = os.path.join(BASE_DIR, "le.pickle")
DEVICE = "cpu" # torch.device("cuda" if torch.cuda.is_available() else "cpu")

#model
class ObjectDetectionModel(nn.Module):
    def __init__(self, baseModel, numClasses):
        super(ObjectDetectionModel, self).__init__()

        self.baseModel = baseModel
        self.numClasses = numClasses

        # İşaretleyici
        self.regressor = nn.Sequential(
            nn.Linear(self.baseModel.fc.in_features, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 4),
            nn.Sigmoid(),
        )

        # Sınıflandırıcı
        self.classifier = nn.Sequential(
            nn.Linear(self.baseModel.fc.in_features, 512),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(),
			      nn.Linear(512, self.numClasses)
		    )

        self.baseModel.fc = nn.Identity()

    def forward(self, x):

        features = self.baseModel(x)
        bboxes = self.regressor(features)
        classLogits = self.classifier(features)

        return (bboxes, classLogits)
    
ODModel = None
def get_model():
    global ODModel, ODLabelEncoder

    le = get_lebel_encoder()
    if le is None:
        return

    if ODModel is None:
        resnet = resnet50(weights=ResNet50_Weights.DEFAULT);
        for param in resnet.parameters():
            param.requires_grad = False
        ODModel = ObjectDetectionModel(resnet,len(le.classes_))
        print("Loading {}".format(MODEL_FILE))
        ODModel = torch.load(MODEL_FILE, map_location=DEVICE, weights_only=False)
        ODModel.eval()
        print(ODModel)

    return ODModel

ODLabelEncoder = None
def get_lebel_encoder():
    global ODLabelEncoder
    if ODLabelEncoder is None:
        ODLabelEncoder = LabelEncoder()
        print("Loading {}".format(LE_FILE));
        ODLabelEncoder = pickle.loads(open(LE_FILE, "rb").read())

    return ODLabelEncoder


__MEAN_ = [0.485, 0.456, 0.406]
__STD_ = [0.229, 0.224, 0.225]

__PreprocesTransform__ = transforms.Compose([
	transforms.ToPILImage(),
	transforms.ToTensor(),
	transforms.Normalize(mean=__MEAN_, std=__STD_)
])

def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))

    image = torch.from_numpy(image)
    image = image.permute(2, 0, 1)
    image = __PreprocesTransform__(image)
    image = image.unsqueeze(0)

    return image

def predict(input_batch):
    le = get_lebel_encoder()
    if le is None:
        return
    
    model = get_model()
    if model is None:
        return
    
    model.to(DEVICE)
    model.eval()
    input_batch = input_batch.to(DEVICE)

    with torch.no_grad():
        inference_time = time.time()
        (boxPreds, labelPreds) = model(input_batch)
        inference_time = time.time() - inference_time

    labels_percentage = torch.nn.functional.softmax(labelPreds, dim=1)[0] * 100
    print(labels_percentage.shape)
    print(labelPreds.shape)

    _, best_label_indices = torch.sort(labelPreds, descending=True)
    best_label_indices = best_label_indices.squeeze(0)
    print(best_label_indices[0].item())
    return [(le.inverse_transform([i.item()])[0], labels_percentage[i].item()) for i in best_label_indices[:5]]


    