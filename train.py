import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from torchvision.models import ResNet18_Weights
import graphics

transform = transforms.Compose([
    transforms.ToTensor(),
])

# Загрузка данных
train_dataset = datasets.ImageFolder(root="dataset-binary/train", transform=transform)
valid_dataset = datasets.ImageFolder(root="dataset-binary/valid", transform=transform)

train_losses = []
valid_mAPs = []

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
valid_loader = DataLoader(valid_dataset, batch_size=32, shuffle=False)

# Классы
classes = train_dataset.classes
print("Classes:", classes)

# Загрузка модели
model = models.resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 1)  # Бинарная классификация

# Для совместной разработки
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Функция потерь и оптимизатор
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Обучение
num_epochs = 50
valid_mAPs = []  # Список для хранения mAP на каждой эпохе

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.float().to(device).unsqueeze(1)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    train_losses.append(running_loss / len(train_loader))
    
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {train_losses[-1]}")

    # Валидация
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in valid_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = torch.sigmoid(model(images))
            predictions = (outputs > 0.5).float()
            correct += (predictions == labels.unsqueeze(1)).sum().item()
            total += labels.size(0)

    valid_mAP = correct / total
    valid_mAPs.append(valid_mAP)

graphics.draw_mAP(num_epochs, valid_mAPs)
graphics.draw_train_loss(num_epochs, train_losses)

torch.save(model.state_dict(), "model.pth")
print("Model saved to model.pth")