# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bnyr6mpCH29gRfmB6IuWb1qNRO6-gPwF
"""

import torch
import torch.nn as nn
import torchvision.models as models

# Load pre-trained ResNet-18 model
resnet18 = models.resnet18(pretrained=True)

resnet18

class BigModel(nn.Module):
  def  __init__(self):
    super(BigModel, self).__init__()
    resnet18 = models.resnet18(pretrained=True)
    self.features = nn.Sequential(*(list(resnet18.children())[:-2])) # I removed the last two layers of resnet and replaced them with the ones said in the paper
    self.features[-2][-2] = nn.AdaptiveMaxPool2d((1,1))
    self.features[-1][-1] = nn.Linear(512, 256)
    self.dropout_cnn = nn.Dropout(p = 0.5)
    self.batch_norm_cnn = nn.BatchNorm2d(256)
    #
    self.bi_gru = nn.GRU(, hidden_size = 256, num_layers =1, batch_first=True, bidirectional=True) # I dont know what the size of the input to the bi-gru is supposed to be
    self.fc_gru = nn.Linear(512, 256)
    #
    self.dropout = nn.Dropout(p = 0.5)
    self.fc = nn.Linear(512, 256)
    self.sigmoid = nn.Sigmoid()

  def forward(self, x):
    x1 = self.features(x)
    x1 = self.dropout_cnn(x1)
    x1 = self.batch_norm_cnn(x1)
    x2 = torch.reshape(x, ) # I dont know what the size of the input to the bi-gru is supposed to be
    x2 = self.bi_gru(x2)
    x2 = torch.cat((x2[:, -1, :256], x2[:, 0, 256:]), dim=1)
    x2 = self.fc_gru(x2)
    x = torch.cat((x1, x2), -1)
    x = self.dropout(x)
    x = self.fc(x)
    x = self.sigmoid(x)
    return x