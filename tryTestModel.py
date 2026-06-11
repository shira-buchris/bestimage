import torch
import torch.nn as nn
import cv2 
from PIL import Image
from torchvision import transforms
from torchvision.models import mobilenet_v3_large, MobileNet_V3_Large_Weights

MODEL_PATH = r"C:\myproject\best_smile_model.pth"
#IMAGE_PATH = r"C:\myproject\debug_faces\face_id_16.jpg"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_smile_model():
    model = mobilenet_v3_large(weights=MobileNet_V3_Large_Weights.DEFAULT)
    in_features = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(in_features, 1)
    return model


model = get_smile_model()
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


#מפההה
def predict_one_image(face_img):
    if face_img is None or face_img.size == 0:
        return 0.0

    # face_img מגיע מ־OpenCV ולכן הוא BGR
    face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

    # המרה ל־PIL כדי שה־transforms יעבדו
    image = Image.fromarray(face_rgb)

    # הכנה למודל
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(image)
        prob = torch.sigmoid(logits).item()

    return prob