#!/usr/bin/env python3
"""
工业缺陷检测模型训练
使用 ResNet18 预训练模型进行迁移学习
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms
from PIL import Image
from pathlib import Path
import numpy as np
from tqdm import tqdm
import os

class DefectDataset(Dataset):
    """缺陷检测数据集"""
    
    def __init__(self, root_dir, transform=None):
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.samples = []
        self.labels = []
        
        # 加载好零件图片
        good_dir = self.root_dir / 'good'
        if good_dir.exists():
            for img_path in good_dir.glob('*.png'):
                self.samples.append(img_path)
                self.labels.append(0)  # 0 = 好
        
        # 加载坏零件图片
        bad_dir = self.root_dir / 'bad'
        if bad_dir.exists():
            for img_path in bad_dir.glob('*.png'):
                self.samples.append(img_path)
                self.labels.append(1)  # 1 = 坏
        
        print(f"加载数据集：{len(self.samples)} 张图片")
        print(f"  - 好零件：{sum(1 for l in self.labels if l == 0)} 张")
        print(f"  - 坏零件：{sum(1 for l in self.labels if l == 1)} 张")
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path = self.samples[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

def create_model(num_classes=2, pretrained=True):
    """创建 ResNet18 模型"""
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None)
    
    # 替换最后的全连接层
    num_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_features, 256),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(256, num_classes)
    )
    
    return model

def train_model(model, train_loader, val_loader, criterion, optimizer, scheduler, num_epochs=20, device='cuda'):
    """训练模型"""
    
    best_val_acc = 0.0
    best_model_state = None
    
    for epoch in range(num_epochs):
        print(f'\nEpoch {epoch+1}/{num_epochs}')
        print('-' * 30)
        
        # 训练阶段
        model.train()
        running_loss = 0.0
        running_corrects = 0
        
        for inputs, labels in tqdm(train_loader, desc='Training'):
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            
            with torch.set_grad_enabled(True):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
        
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = running_corrects.double() / len(train_loader.dataset)
        print(f'Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
        
        # 验证阶段
        model.eval()
        val_loss = 0.0
        val_corrects = 0
        
        with torch.no_grad():
            for inputs, labels in tqdm(val_loader, desc='Validating'):
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(preds == labels.data)
        
        val_loss = val_loss / len(val_loader.dataset)
        val_acc = val_corrects.double() / len(val_loader.dataset)
        print(f'Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}')
        
        # 学习率调整
        scheduler.step(val_loss)
        
        # 保存最佳模型
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_state = model.state_dict().copy()
            print(f'✨ 新的最佳模型！验证准确率：{val_acc:.4f}')
    
    # 加载最佳模型
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
    
    return model, best_val_acc

def main():
    # 配置
    data_dir = Path('../data')
    model_dir = Path('../models')
    model_dir.mkdir(exist_ok=True)
    
    # 检查 CUDA
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'使用设备：{device}')
    
    # 数据变换
    train_transform = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # 加载数据集
    full_dataset = DefectDataset(data_dir, transform=val_transform)
    
    # 划分训练集和验证集（8:2）
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        full_dataset, [train_size, val_size],
        generator=torch.Generator().manual_seed(42)
    )
    
    # 为训练集添加增强
    train_dataset.dataset.transform = train_transform
    
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False, num_workers=2)
    
    # 创建模型
    model = create_model(num_classes=2, pretrained=True)
    model = model.to(device)
    
    # 损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.001)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)
    
    # 训练
    print('\n开始训练...')
    model, best_acc = train_model(
        model, train_loader, val_loader,
        criterion, optimizer, scheduler,
        num_epochs=20, device=device
    )
    
    # 保存模型
    model_path = model_dir / 'defect_detection_resnet18.pth'
    torch.save({
        'model_state_dict': model.state_dict(),
        'best_val_acc': best_acc,
    }, model_path)
    print(f'\n模型已保存至：{model_path}')
    print(f'最佳验证准确率：{best_acc:.4f}')

if __name__ == '__main__':
    main()
