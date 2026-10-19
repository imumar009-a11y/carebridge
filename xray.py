"""xray.py - chest X-ray pneumonia screening demo (CNN, transfer learning)."""
import os
from functools import lru_cache

MODEL_PATH = os.environ.get("XRAY_MODEL", "xray_model.pt")
CLASSES = ["NORMAL", "PNEUMONIA"]


def available():
    return os.path.exists(MODEL_PATH)


@lru_cache(maxsize=1)
def load():
    import torch
    from torchvision import models
    m = models.resnet18()
    m.fc = torch.nn.Linear(m.fc.in_features, 2)
    m.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    return m.eval()


def predict(image):
    import torch
    from torchvision import transforms as T
    tf = T.Compose([T.Resize((224, 224)), T.ToTensor(),
                    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    x = tf(image.convert("RGB")).unsqueeze(0)
    with torch.no_grad():
        p = torch.softmax(load()(x), 1)[0]
    return {c: float(p[i]) for i, c in enumerate(CLASSES)}