#!/usr/bin/env python3
"""
批量检测脚本
工业场景：一键检测整个文件夹的图片，自动分类存放，生成检测报告
"""

import torch
from PIL import Image
from torchvision import transforms
import json
from pathlib import Path
from datetime import datetime

class BatchDetector:
    """批量检测器"""
    
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
    
    def detect_folder(self, input_folder, output_folder, threshold=0.5):
        """
        检测整个文件夹的图片
        
        Args:
            input_folder: 输入文件夹路径
            output_folder: 输出文件夹路径
            threshold: 缺陷判定阈值（默认 0.5）
        
        Returns:
            results: 检测结果列表
        """
        input_path = Path(input_folder)
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 创建子文件夹
        good_dir = output_path / '合格品'
        bad_dir = output_path / '缺陷品'
        good_dir.mkdir(exist_ok=True)
        bad_dir.mkdir(exist_ok=True)
        
        results = []
        
        print(f"\n开始检测：{input_folder}")
        print("-" * 50)
        
        for img_path in input_path.glob('*.png'):
            # 检测
            img = Image.open(img_path).convert('RGB')
            x = self.transform(img).unsqueeze(0)
            
            with torch.no_grad():
                out = self.model(x)
                prob = torch.softmax(out, dim=1)[0, 1].item()
            
            # 判断
            is_defect = prob > threshold
            result = {
                'filename': img_path.name,
                'is_defect': is_defect,
                'confidence': prob,
                'defect_type': self._guess_defect_type(img_path.name)
            }
            results.append(result)
            
            # 分类存放
            dest_dir = bad_dir if is_defect else good_dir
            img.save(dest_dir / img_path.name)
            
            status = "❌ 缺陷" if is_defect else "✅ 合格"
            print(f"{img_path.name}: {status} (置信度：{prob:.1%})")
        
        # 生成报告
        self._generate_report(results, output_path, threshold)
        
        # 打印统计
        total = len(results)
        defect_count = sum(1 for r in results if r['is_defect'])
        good_count = total - defect_count
        
        print("\n" + "=" * 50)
        print(f"检测完成！")
        print(f"总数量：{total}")
        print(f"合格品：{good_count} ({good_count/total:.1%})")
        print(f"缺陷品：{defect_count} ({defect_count/total:.1%})")
        print(f"报告已保存：{output_path / '检测报告.md'}")
        print("=" * 50)
        
        return results
    
    def _guess_defect_type(self, filename):
        """根据文件名猜测缺陷类型"""
        filename_lower = filename.lower()
        if 'scratch' in filename_lower or '划痕' in filename_lower:
            return '划痕'
        elif 'spot' in filename_lower or '斑点' in filename_lower:
            return '斑点'
        elif 'stain' in filename_lower or '脏污' in filename_lower:
            return '脏污'
        elif 'crack' in filename_lower or '裂纹' in filename_lower:
            return '裂纹'
        elif 'RS' in filename_lower or '氧化皮' in filename_lower:
            return '氧化皮'
        elif 'PS' in filename_lower or '斑块' in filename_lower:
            return '斑块'
        elif 'Cr' in filename_lower or '开裂' in filename_lower:
            return '开裂'
        elif 'Pa' in filename_lower or '点蚀' in filename_lower:
            return '点蚀'
        elif 'In' in filename_lower or '内含物' in filename_lower:
            return '内含物'
        elif 'Sc' in filename_lower:
            return '划痕'
        else:
            return '未知'
    
    def _generate_report(self, results, output_path, threshold):
        """生成检测报告"""
        total = len(results)
        defect_count = sum(1 for r in results if r['is_defect'])
        good_count = total - defect_count
        
        report = f"""# 工业缺陷检测报告

**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**检测阈值**：{threshold:.0%}

---

## 📊 统计摘要

| 项目 | 数量 | 比例 |
|------|------|------|
| 总数量 | {total} | 100% |
| 合格品 | {good_count} | {good_count/total:.1%} |
| 缺陷品 | {defect_count} | {defect_count/total:.1%} |

---

## 🏷️ 缺陷类型分布

"""
        # 按类型统计
        type_count = {}
        for r in results:
            if r['is_defect']:
                t = r['defect_type']
                type_count[t] = type_count.get(t, 0) + 1
        
        if type_count:
            report += "| 缺陷类型 | 数量 | 占比 |\n"
            report += "|---------|------|------|\n"
            for t, c in sorted(type_count.items(), key=lambda x: x[1], reverse=True):
                report += f"| {t} | {c} | {c/defect_count:.1%} |\n"
        else:
            report += "*无缺陷品*\n"
        
        # 详细列表
        report += "\n---\n\n## 📋 详细列表\n\n"
        report += "| 序号 | 文件名 | 结果 | 置信度 | 缺陷类型 |\n"
        report += "|------|--------|------|--------|----------|\n"
        
        for idx, r in enumerate(results, 1):
            status = "❌ 缺陷" if r['is_defect'] else "✅ 合格"
            report += f"| {idx} | {r['filename']} | {status} | {r['confidence']:.1%} | {r['defect_type']} |\n"
        
        report += f"\n---\n\n**检测工具**：工业缺陷检测系统 v1.0\n"
        report += "**模型**：ResNet18 迁移学习\n"
        
        with open(output_path / '检测报告.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 报告已生成：{output_path / '检测报告.md'}")


def main():
    """主函数"""
    import sys
    
    # 默认参数
    model_path = 'models/defect.pth'
    input_folder = 'data'
    output_folder = 'detection_result'
    threshold = 0.5
    
    # 命令行参数
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
    if len(sys.argv) > 2:
        input_folder = sys.argv[2]
    if len(sys.argv) > 3:
        output_folder = sys.argv[3]
    if len(sys.argv) > 4:
        threshold = float(sys.argv[4])
    
    # 检测
    detector = BatchDetector(model_path)
    detector.detect_folder(input_folder, output_folder, threshold)


if __name__ == '__main__':
    main()
