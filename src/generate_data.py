#!/usr/bin/env python3
"""
生成模拟工业缺陷检测数据集
- 好零件：干净的金属表面
- 坏零件：带有划痕、斑点、脏污等缺陷
"""

import cv2
import numpy as np
import random
import os
from pathlib import Path

def generate_good_part(size=(224, 224)):
    """生成无缺陷的零件图片（模拟干净金属表面）"""
    img = np.ones(size, dtype=np.uint8) * 200
    
    # 添加一些金属纹理
    for _ in range(random.randint(3, 8)):
        x1, y1 = random.randint(0, size[1]-1), random.randint(0, size[0]-1)
        x2, y2 = x1 + random.randint(10, 50), y1 + random.randint(-5, 5)
        x2 = min(x2, size[1]-1)
        y2 = max(0, min(y2, size[0]-1))
        intensity = random.randint(180, 220)
        cv2.line(img, (x1, y1), (x2, y2), int(intensity), random.randint(1, 2))
    
    # 添加轻微噪点
    noise = np.random.normal(0, 5, size).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return img

def generate_defect_part(size=(224, 224), defect_type='random'):
    """生成有缺陷的零件图片"""
    img = generate_good_part(size)
    
    if defect_type == 'random':
        defect_type = random.choice(['scratch', 'spot', 'stain', 'crack'])
    
    if defect_type == 'scratch':
        # 划痕：细长的暗线
        num_scratches = random.randint(1, 4)
        for _ in range(num_scratches):
            x1 = random.randint(0, size[1]-1)
            y1 = random.randint(0, size[0]-1)
            length = random.randint(20, 80)
            angle = random.uniform(0, np.pi)
            x2 = int(x1 + length * np.cos(angle))
            y2 = int(y1 + length * np.sin(angle))
            x2 = max(0, min(x2, size[1]-1))
            y2 = max(0, min(y2, size[0]-1))
            cv2.line(img, (x1, y1), (x2, y2), random.randint(50, 100), random.randint(1, 3))
    
    elif defect_type == 'spot':
        # 斑点：圆形暗区
        num_spots = random.randint(2, 6)
        for _ in range(num_spots):
            center = (random.randint(10, size[1]-10), random.randint(10, size[0]-10))
            radius = random.randint(3, 12)
            cv2.circle(img, center, radius, random.randint(60, 120), -1)
    
    elif defect_type == 'stain':
        # 脏污：不规则暗区
        num_stains = random.randint(1, 3)
        for _ in range(num_stains):
            pts = np.array([
                [random.randint(0, size[1]), random.randint(0, size[0])],
                [random.randint(0, size[1]), random.randint(0, size[0])],
                [random.randint(0, size[1]), random.randint(0, size[0])],
                [random.randint(0, size[1]), random.randint(0, size[0])],
            ], np.int32)
            cv2.fillPoly(img, [pts], random.randint(80, 140))
    
    elif defect_type == 'crack':
        # 裂纹：曲折的细线
        num_cracks = random.randint(1, 2)
        for _ in range(num_cracks):
            x, y = random.randint(0, size[1]-1), random.randint(0, size[0]-1)
            points = [(x, y)]
            for _ in range(random.randint(5, 15)):
                x += random.randint(-10, 10)
                y += random.randint(-5, 5)
                x = max(0, min(x, size[1]-1))
                y = max(0, min(y, size[0]-1))
                points.append((x, y))
            pts = np.array(points, np.int32)
            cv2.polylines(img, [pts], False, random.randint(40, 80), 1)
    
    return img

def generate_dataset(output_dir, num_samples=100):
    """生成完整数据集"""
    good_dir = Path(output_dir) / 'good'
    bad_dir = Path(output_dir) / 'bad'
    
    good_dir.mkdir(parents=True, exist_ok=True)
    bad_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"生成 {num_samples} 张好零件图片...")
    for i in range(num_samples):
        img = generate_good_part()
        cv2.imwrite(str(good_dir / f'good_{i:04d}.png'), img)
    
    print(f"生成 {num_samples} 张缺陷零件图片...")
    defect_types = ['scratch', 'spot', 'stain', 'crack']
    for i in range(num_samples):
        defect_type = defect_types[i % len(defect_types)]
        img = generate_defect_part(defect_type=defect_type)
        cv2.imwrite(str(bad_dir / f'bad_{i:04d}_{defect_type}.png'), img)
    
    print(f"数据集生成完成！保存至：{output_dir}")
    print(f"  - 好零件：{num_samples} 张")
    print(f"  - 坏零件：{num_samples} 张")

if __name__ == '__main__':
    import sys
    output_dir = sys.argv[1] if len(sys.argv) > 1 else '../data'
    num_samples = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    generate_dataset(output_dir, num_samples)
