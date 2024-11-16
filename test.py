import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import torch.nn as nn
import model

# Преобразования
transform = transforms.Compose([
    transforms.ToTensor(),
])

# Загрузка тестового набора
test_dataset = datasets.ImageFolder(root="dataset-binary/test", transform=transform)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.resnet_load(device)

# Тестирование
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = torch.sigmoid(model(images))
        predictions = (outputs > 0.5).float()
        correct += (predictions == labels.unsqueeze(1)).sum().item()
        total += labels.size(0)

print(f"Test Accuracy: {100 * correct / total:.2f}%")
