# -*- coding: utf-8 -*-
"""HW5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W0euqSHRxvxXvAYlX86-rvyHwsEMDMFm

In this exercise, we will fine-tune a pre-trained deep network (ResNet34) for a particular two-class dataset which can be downloaded from the attached zip file. Code for pre-processing the dataset, and for loading ResNet34, can be found below. Since ResNet34 is for 1000 output classes, you will need to modify the last layer to reduce two classes. Train for 20 epochs and plot train and validation loss curves. Report your final train and validation accuracies.
"""

import torchvision
from torchvision import datasets, models, transforms 
import torch
import numpy as np
import matplotlib.pyplot as plt
transforms = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])])
train_set = datasets.ImageFolder("/data/train",transforms)
val_set = datasets.ImageFolder("data/val",transforms)
# train_set = datasets.ImageFolder("/content/drive/My Drive/data/train",transforms)
# val_set = datasets.ImageFolder("/content/drive/My Drive/data/val",transforms)
model = models.resnet34(pretrained=True)

# use dataloader to help process the data
trainDataLoader = torch.utils.data.DataLoader(train_set, batch_size=64, shuffle=True)
testDataLoader = torch.utils.data.DataLoader(val_set, batch_size=64, shuffle=False)
fc_features = model.fc.in_features
model.fc = torch.nn.Linear(fc_features, 2)

net = model.cuda()
Loss = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(net.parameters(), lr=0.1)
                            
train_loss_history = []
test_loss_history = []
# change the epoch to 20 times
num_epochs = 20


for epoch in range(num_epochs):
  train_loss = 0.0
  test_loss = 0.0
  for i, data in enumerate(trainDataLoader):
    images, labels = data
    images = images.cuda()
    labels = labels.cuda()
    optimizer.zero_grad()
    predicted_output = net(images)
    fit = Loss(predicted_output,labels)
    fit.backward()
    optimizer.step()
    train_loss += fit.item()
  for i, data in enumerate(testDataLoader):
    with torch.no_grad():
      images, labels = data
      images = images.cuda()
      labels = labels.cuda()
      predicted_output = net(images)
      fit = Loss(predicted_output,labels)
      test_loss += fit.item()
  train_loss = train_loss/len(trainDataLoader)
  test_loss = test_loss/len(testDataLoader)
  train_loss_history.append(train_loss)
  test_loss_history.append(test_loss)
  print('Epoch %s, Train loss %s, Test loss %s'%(epoch, train_loss, test_loss))

plt.plot(np.arange(num_epochs),train_loss_history,'-',linewidth=3,label='Train error')
plt.plot(np.arange(num_epochs),test_loss_history,'-',linewidth=3,label='Test error')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.grid(True)
plt.legend()