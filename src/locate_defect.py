#!/usr/bin/env python3
"""
缺陷定位脚本（简易版）
工业场景：标注缺陷位置，方便质检员复核
"""

import torch
from PIL import Image
from torchvision import transforms
import cv2
import numpy as np
from pathlib import Path

class DefectLocator:
    """缺陷定位器"""
    
    def __init__(self, model_path):
        """初始化模型"""
        print(f"加载模型：{model_path}")
        self.model = torch.load(model_path, map_location='cpu', weights_only=False)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        print("✅ 模型加载完成")
    
    def locate_defect(self, image_path, output_path=None, grid_size=4, threshold=0.7):
        """
        定位缺陷位置（滑动窗口简易版）
        
        Args:
            image_path: 输入图片路径
            output_path: 输出标注图片路径（默认自动生成）
            grid_size: 网格大小（默认 4x4）
            threshold: 缺陷判定阈值
        
        Returns:
            defect_regions: 缺陷区域列表
            annotated_path: 标注图片路径
        """
        # 加载图片
        img_pil = Image.open(image_path).convert('RGB')
        img_cv = cv2.imread(str(image_path))
        
        if img_cv is None:
            print(f"❌ 无法读取图片：{image_path}")
            return [], None
        
        h, w = img_pil.size[1], img_pil.size[0]
        grid_h, grid_w = h // grid_size, w // grid_size
        
        defect_regions = []
        
        print(f"\n分析图片：{image_path}")
        print(f"网格大小：{grid_size}x{grid_size}")
        print("-" * 50)
        
        # 滑动窗口检测
        for i in range(grid_size):
            for j in range(grid_size):
                # 裁剪网格
                left = j * grid_w
                top = i * grid_h
                right = left + grid_w
                bottom = top + grid_h
                
                crop = img_pil.crop((left, top, right, bottom))
                x = self.transform(crop).unsqueeze(0)
                
                # 预测
                with torch.no_grad():
                    out = self.model(x)
                    prob = torch.softmax(out, dim=1)[0, 1].item()
                
                # 如果这个网格缺陷概率高，记录下来
                if prob > threshold:
                    defect_regions.append({
                        'position': (left, top, right, bottom),
                        'confidence': prob,
                        'grid': (i, j)
                    })
        
        # 在原图上标注
        for region in defect_regions:
            left, top, right, bottom = region['position']
            cv2.rectangle(img_cv, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(img_cv, f"{region['confidence']:.0%}", 
                       (left, top+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # 保存标注后的图片
        if output_path is None:
            output_path = str(Path(image_path).parent / f"{Path(image_path).stem}_annotated.png")
        
        cv2.imwrite(output_path, img_cv)
        
        # 打印结果
        if defect_regions:
            print(f"发现 {len(defect_regions)} 个疑似缺陷区域：")
            for region in defect_regions:
                i, j = region['grid']
                print(f"  - 网格 [{i},{j}]: 置信度 {region['confidence']:.1%}")
            print(f"\n✅ 标注已保存：{output_path}")
        else:
            print("未发现明显缺陷区域")
            print(f"\n✅ 标注已保存：{output_path}")
        
        return defect_regions, output_path
    
    def locate_folder(self, input_folder, output_folder=None, grid_size=4, threshold=0.7):
        """批量定位整个文件夹的图片"""
        input_path = Path(input_folder)
        
        if output_folder is None:
            output_folder = input_path / 'annotated'
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n开始批量定位：{input_folder}")
        print("=" * 50)
        
        total_defects = 0
        
        for img_path in input_path.glob('*.png'):
            if '_annotated' in str(img_path):
                continue  # 跳过已标注的图片
            
            regions, _ = self.locate_defect(str(img_path), str(output_path / img_path.name), grid_size, threshold)
            total_defects += len(regions)
        
        print("\n" + "=" * 50)
        print(f"批量定位完成！")
        print(f"标注图片保存至：{output_path}")
        print(f"共发现 {total_defects} 个疑似缺陷区域")
        print("=" * 50)


def main():
    """主函数"""
    import sys
    
    # 默认参数
    model_path = 'models/defect.pth'
    image_path = 'data/bad/0.png'
    grid_size = 4
    threshold = 0.7
    
    # 命令行参数
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
    if len(sys.argv) > 2:
        image_path = sys.argv[2]
    if len(sys.argv) > 3:
        grid_size = int(sys.argv[3])
    if len(sys.argv) > 4:
        threshold = float(sys.argv[4])
    
    # 定位
    locator = DefectLocator(model_path)
    locator.locate_defect(image_path, grid_size=grid_size, threshold=threshold)


if __name__ == '__main__':
    main()
