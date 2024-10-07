import torch
from torch import nn
import os
from pathlib import Path
import random
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, datasets
import torchinfo
from torchinfo import summary
from tqdm.auto import tqdm

class TinyVGG(nn.Module):
    def __init__(self, in_channels, num_classes, hidden_units):
        super().__init__()
        # [batch_size, 3, 64, 64]->[batch_size, hidden_units, 32, 32]
        self.conv_block_1 = nn.Sequential(
            nn.Conv2d(in_channels, hidden_units, kernel_size=3, stride=1, padding=1), 
            nn.ReLU(),
            nn.Conv2d(hidden_units, hidden_units, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # [batch_size, hidden_units, 32, 32]->[batch_size, hidden_units, 16, 16]
        self.conv_block_2 = nn.Sequential(
            nn.Conv2d(hidden_units, hidden_units, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hidden_units, hidden_units, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=hidden_units*64*64, out_features=num_classes),
        )
        self.dropout = nn.Dropout(p=0.5)
    
    def forward(self, x):
        # add dropout
        x = self.conv_block_1(x)
        x = self.conv_block_2(x)
        x = self.classifier(x)
        return self.dropout(x)
        return x
        
random.seed(30)
def walk_through_dir(dir_path):
    for dirpath, dirnames, filenames in os.walk(dir_path):
        print(f"There are {len(dirnames)} directories and {len(filenames)} images in '{dirpath}'.")

def visualize_image(image_path):
    image_path_list = list(image_path.glob("*/*/*.jpg"))  # 500
    print(f"Total images: {len(image_path_list)}")
    random_image_path = random.choice(image_path_list)
    image_class = random_image_path.parent.stem 
    img = Image.open(random_image_path)
    print(f"Image path: {random_image_path}")  # e.g.dataset/train/Neither/22.jpg
    print(f"Image class: {image_class}")
    print(f"Image shape: {img.size}")
    # img.show()

    # use matplotlib to show the image
    # img_as_array = np.asarray(img)
    # plt.figure(figsize=(10, 7))
    # plt.imshow(img_as_array)
    # plt.axis(False)
    # plt.show()
    # 保存图像到visualize_image文件夹
    img.save("visualize_image/random_image.jpg")  # 如果是linux，不好可视化，直接存起来看

train_data_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.TrivialAugmentWide(num_magnitude_bins=31),
    transforms.ToTensor(),
])

test_data_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
])

def plot_transformed_images(image_path, transform, n=3, seed=32):
    random.seed(seed)
    random_image_paths = random.sample(list(image_path.glob("*/*/*.jpg")), k=n)
    # 写入visualize_image文件夹，原图命名为original_{n}.jpg, transform后的图像命名为transformed_{n}.jpg
    for i, image_path in enumerate(random_image_paths):
        img = Image.open(image_path)
        transformed_img = transform(img)  # torch.Size([3, 64, 64])
        print(transformed_img.shape)
        img.save(f"visualize_image/original_{i}.jpg")
        transformed_img = transforms.ToPILImage()(transformed_img)
        transformed_img.save(f"visualize_image/transformed_{i}.jpg")

def debug_train_data_and_test_data(train_data, test_data):
    print(f"Train data classes: {train_data.classes}")
    print(f"class to index mapping: {train_data.class_to_idx}")
    print(train_data)
    print(test_data)
    # Test data: 5
    # Train data classes: ['Albedo', 'Ayaka', 'HuTao', 'Kokomi', 'Neither']
    # class to index mapping: {'Albedo': 0, 'Ayaka': 1, 'HuTao': 2, 'Kokomi': 3, 'Neither': 4}

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
        if epoch % 10 == 0:
            torch.save(model.state_dict(), f"tiny_vgg_{epoch+1}.pth")
    return results

def plot_loss_curves(results):
    plt.figure(figsize=(10, 7))
    plt.plot(results["train_loss"], label="Train Loss")
    plt.plot(results["test_loss"], label="Test Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    # save the plot
    plt.savefig("loss_curve.png")

print(torch.__version__)
image_path = Path("dataset/")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
walk_through_dir(image_path)

train_dir = image_path / "train"
test_dir = image_path / "test"
# print(train_dir, test_dir)  # dataset/train dataset/test
# visualize_image(image_path)
# plot_transformed_images(image_path, train_data_transform, n=3)
train_data = datasets.ImageFolder(root=train_dir, transform=train_data_transform, target_transform=None) # target_transform指的是对label的处理，这里不用处理
test_data = datasets.ImageFolder(root=test_dir, transform=test_data_transform)
print(f"Train data: {len(train_data)}")
print(f"Test data: {len(test_data)}")
# debug_train_data_and_test_data(train_data, test_data)
#img = train_data[0][0]
#label = train_data[0][1]
#print(img.shape, label)  # torch.Size([3, 64, 64]) 0

train_loader = DataLoader(dataset=train_data, batch_size=2, shuffle=True)
test_loader = DataLoader(dataset=test_data, batch_size=2, shuffle=False)
img, label = next(iter(train_loader))
# print(img.shape, label)  # torch.Size([1, 3, 64, 64]) tensor([2]), 2是因为我们做了shuffle
torch.manual_seed(42)
model = TinyVGG(in_channels=3, num_classes=len(train_data.classes), hidden_units=32).to(device)
# model.load_state_dict(torch.load("tiny_vgg_41.pth"))
# print(model)
# summary(model, input_size=[1, 3, 64, 64])
torch.cuda.manual_seed(42)
NUM_EPOCHS = 50
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

from timeit import default_timer as timer
start = timer()
results = train(model, train_loader, test_loader, optimizer, loss_fn, NUM_EPOCHS)
end = timer()
plot_loss_curves(results)
print(f"Time: {end-start:.2f} seconds")