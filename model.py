import torch
from torchvision import models
import torch.nn as nn

def process_images(saved_files):
    return {
            "landfill": True,
            "score": 50,
            "processed_images":saved_files
    }

def resnet_load(device):
    model = models.resnet18(pretrained=False) 
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 1)

    model = model.to(device)

    model.load_state_dict(torch.load("model.pth")) 
    model.eval() 
    print("Model loaded and ready for testing.")
    return model