"""Train the X-ray model. Run in Google Colab (free GPU): python train_xray.py
Data: Kaggle 'Chest X-Ray Images (Pneumonia)' unzipped to folder chest_xray/ (train/ and test/)."""
import torch, torch.nn as nn
from torchvision import datasets, models, transforms as T

dev = "cuda" if torch.cuda.is_available() else "cpu"
norm = T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
train_tf = T.Compose([T.Resize((224, 224)), T.RandomRotation(10), T.ToTensor(), norm])
test_tf = T.Compose([T.Resize((224, 224)), T.ToTensor(), norm])
train = datasets.ImageFolder("chest_xray/train", train_tf)   # NORMAL=0, PNEUMONIA=1
test = datasets.ImageFolder("chest_xray/test", test_tf)
tl = torch.utils.data.DataLoader(train, batch_size=32, shuffle=True)
vl = torch.utils.data.DataLoader(test, batch_size=32)

model = models.resnet18(weights="IMAGENET1K_V1")             # pre-trained on ImageNet
model.fc = nn.Linear(model.fc.in_features, 2)                # new 2-class head
model.to(dev)
counts = torch.bincount(torch.tensor(train.targets)).float()
loss_fn = nn.CrossEntropyLoss(weight=(counts.sum() / counts).to(dev))  # fixes class imbalance
opt = torch.optim.Adam(model.parameters(), lr=1e-4)

for epoch in range(3):
    model.train()
    for x, y in tl:
        x, y = x.to(dev), y.to(dev)
        opt.zero_grad(); loss_fn(model(x), y).backward(); opt.step()
    print("epoch", epoch + 1, "done")

model.eval(); tp = tn = fp = fn = 0
with torch.no_grad():
    for x, y in vl:
        p = model(x.to(dev)).argmax(1).cpu()
        tp += ((p == 1) & (y == 1)).sum().item(); tn += ((p == 0) & (y == 0)).sum().item()
        fp += ((p == 1) & (y == 0)).sum().item(); fn += ((p == 0) & (y == 1)).sum().item()
print(f"accuracy {(tp+tn)/(tp+tn+fp+fn):.2%} | sensitivity {tp/(tp+fn):.2%} | specificity {tn/(tn+fp):.2%}")
torch.save(model.state_dict(), "xray_model.pt")
