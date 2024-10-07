import torch
from torch import nn
import os
from pathlib import Path
import random
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision import transforms, datasets
import torchinfo
from torchinfo import summary
from tqdm.auto import tqdm

need_train = False

def train_step(model, data_loader, loss_fn, optimizer):
    model.train()
    train_loss, train_acc = 0.0, 0.0
    for batch, (images, labels) in enumerate(data_loader):
        images, labels = images.to(device), labels.to(device)
        y_pred = model(images)
        loss = loss_fn(y_pred, labels)
        train_loss += loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()  # 这三行的顺序不要写错

        y_pred_class = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
        train_acc += torch.sum(y_pred_class == labels).item()/len(y_pred)
    return train_loss/len(data_loader), train_acc/len(data_loader)

def test_step(model, data_loader, loss_fn):
    model.eval()
    test_loss, test_acc = 0.0, 0.0
    with torch.inference_mode():
        for batch, (images, labels) in enumerate(data_loader):
            images, labels = images.to(device), labels.to(device)
            y_pred = model(images)
            loss = loss_fn(y_pred, labels)
            test_loss += loss.item()

            y_pred_class = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
            test_acc += torch.sum(y_pred_class == labels).item()/len(y_pred)
    return test_loss/len(data_loader), test_acc/len(data_loader)
    
def train(model, train_dataloader, test_dataloader, optimizer, loss_fn, epochs):
    results = {
        "train_loss": [],
        "train_acc": [],
        "test_loss": [],
        "test_acc": []
    }
    for epoch in range(epochs):
        train_loss, train_acc = train_step(model, train_dataloader, loss_fn, optimizer)
        test_loss, test_acc = test_step(model, test_dataloader, loss_fn)
        print(f"Epoch: {epoch+1}/{epochs}, Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, Test Loss: {test_loss:.4f}, Test Acc: {test_acc:.4f}")
        results["train_loss"].append(train_loss.item() if isinstance(train_loss, torch.Tensor) else train_loss)
        results["train_acc"].append(train_acc.item() if isinstance(train_acc, torch.Tensor) else train_acc)
        results["test_loss"].append(test_loss.item() if isinstance(test_loss, torch.Tensor) else test_loss)
        results["test_acc"].append(test_acc.item() if isinstance(test_acc, torch.Tensor) else test_acc)
        if epoch > 8:
            torch.save(model.state_dict(), f"transfer_learning_{epoch+1}.pth")
    return results


def plot_loss_curves(results):
    plt.figure(figsize=(10, 7))
    plt.plot(results["train_loss"], label="Train Loss")
    plt.plot(results["test_loss"], label="Test Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    # save the plot
    plt.savefig("loss_curve_transferLearning.png")

def pred_and_plot_image(model, img_path, classes_names, image_size, transform, device):
    img = Image.open(img_path)
    if transform:
        image_transform = transform
    else:
        image_transform = None
    
    model.to(device)
    model.eval()
    with torch.inference_mode():
        transformed_img = image_transform(img).unsqueeze(0)
        y_pred = model(transformed_img.to(device))
        # y_pred_class = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
        target_image_pred_probs = torch.softmax(y_pred, dim=1)
        target_image_pred_label = torch.argmax(target_image_pred_probs, dim=1)
        plt.figure()
        plt.imshow(img)
        plt.title(f"Prediction: {classes_names[target_image_pred_label]}, Probability: {target_image_pred_probs.max()}")
        # 写一下概率排序
        for i, (class_name, prob) in enumerate(zip(classes_names, target_image_pred_probs[0])):
            plt.text(60, i*200 + 100, f"{class_name}: {prob:.4f}")
        plt.axis(False)
        # save
        plt.savefig("target_image_prediction.png")



torch.manual_seed(42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
image_path = Path("dataset/")
train_dir = image_path / "train"
test_dir = image_path / "test"

weights = torchvision.models.EfficientNet_B0_Weights.DEFAULT
auto_transform = weights.transforms()
# print(auto_transform)

train_data = datasets.ImageFolder(root=train_dir, transform=auto_transform, target_transform=None) # target_transform指的是对label的处理，这里不用处理
test_data = datasets.ImageFolder(root=test_dir, transform=auto_transform)
print(f"Train data: {len(train_data)}")
print(f"Test data: {len(test_data)}")

train_loader = DataLoader(dataset=train_data, batch_size=32, shuffle=True)
test_loader = DataLoader(dataset=test_data, batch_size=32, shuffle=False)
classes_names = train_data.classes

model = torchvision.models.efficientnet_b0(weights=weights).to(device)
# summary(model, input_size=(32, 3, 224, 224), col_names=["input_size", "output_size", "num_params", "trainable"],col_width=18, row_settings=["var_names"])

# freeze all the parameters in the feature extractor
for param in model.features.parameters():
    param.requires_grad = False

torch.manual_seed(42)
torch.cuda.manual_seed(42)
output_shape = len(classes_names)
model.classifier = nn.Sequential(
    nn.Linear(1280, 512, bias=True),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(512, output_shape)
).to(device)

if need_train:
    # summary(model, input_size=(32, 3, 224, 224), col_names=["input_size", "output_size", "num_params", "trainable"],col_width=18, row_settings=["var_names"])
    from timeit import default_timer as timer
    start = timer()
    NUM_EPOCHS = 10
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0005)
    results = train(model, train_loader, test_loader, optimizer, loss_fn, NUM_EPOCHS)
    end = timer()
    print(f"Time taken: {end-start:.2f} seconds")
    plot_loss_curves(results)

test_image_path = Path("test_jpgs/test_04.jpg")
transform = auto_transform
model.load_state_dict(torch.load("transfer_learning_10.pth"))
pred_and_plot_image(model, test_image_path, classes_names, 224, transform, device)

