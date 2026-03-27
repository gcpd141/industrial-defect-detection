#!/usr/bin/env python3
"""
检测结果查看器
网页界面展示批量检测的结果
"""

import gradio as gr
from pathlib import Path
import json
from PIL import Image
import os

def load_results():
    """加载检测结果"""
    result_dir = Path('detection_result')
    
    if not result_dir.exists():
        return None, "❌ 未找到检测结果文件夹\n\n请先运行批量检测（3-batch.bat）"
    
    good_dir = result_dir / '合格品'
    bad_dir = result_dir / '缺陷品'
    report_file = result_dir / '检测报告.md'
    
    # 统计数量
    good_count = len(list(good_dir.glob('*.png'))) if good_dir.exists() else 0
    bad_count = len(list(bad_dir.glob('*.png'))) if bad_dir.exists() else 0
    total = good_count + bad_count
    
    # 生成统计信息
    stats = f"""
## 📊 检测统计

| 项目 | 数量 | 比例 |
|------|------|------|
| 总数量 | {total} | 100% |
| ✅ 合格品 | {good_count} | {good_count/total*100:.1f}% |
| ❌ 缺陷品 | {bad_count} | {bad_count/total*100:.1f}% |

    """
    
    # 读取报告
    report = ""
    if report_file.exists():
        report = report_file.read_text(encoding='utf-8')
    
    return stats, report

def show_images(category):
    """展示指定类别的图片"""
    result_dir = Path('detection_result')
    
    if category == "合格品":
        img_dir = result_dir / '合格品'
    else:
        img_dir = result_dir / '缺陷品'
    
    if not img_dir.exists():
        return [], f"❌ 未找到{category}文件夹"
    
    images = []
    for img_path in img_dir.glob('*.png'):
        try:
            img = Image.open(img_path)
            images.append((img, img_path.name))
        except:
            pass
    
    if not images:
        return [], f"❌ {category}文件夹中没有图片"
    
    return images, f"✅ 共找到 {len(images)} 张{category}图片"

def create_demo():
    """创建 Gradio 界面"""
    
    with gr.Blocks(title="检测结果查看器") as demo:
        gr.Markdown("# 🏭 工业缺陷检测 - 结果查看器")
        
        with gr.Tab("📊 统计概览"):
            stats_output = gr.Markdown()
            report_output = gr.Markdown()
            
            refresh_btn = gr.Button("🔄 刷新数据", variant="primary")
            refresh_btn.click(
                fn=load_results,
                outputs=[stats_output, report_output]
            )
        
        with gr.Tab("🖼️ 图片浏览"):
            gr.Markdown("### 选择要查看的类别")
            
            category_radio = gr.Radio(
                choices=["合格品", "缺陷品"],
                value="合格品",
                label="图片类别"
            )
            
            image_gallery = gr.Gallery(
                label="图片预览",
                show_label=False,
                elem_id="gallery",
                columns=4,
                height="auto"
            )
            
            image_info = gr.Markdown()
            
            category_radio.change(
                fn=show_images,
                inputs=[category_radio],
                outputs=[image_gallery, image_info]
            )
        
        # 初始化加载数据
        demo.load(
            fn=load_results,
            outputs=[stats_output, report_output]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_demo()
    demo.launch(server_name="0.0.0.0", server_port=7861)
    print("\n✅ 结果查看器已启动")
    print("📱 浏览器访问：http://localhost:7861")
