#!/usr/bin/env python3
# 生成产品封面图片

from PIL import Image, ImageDraw, ImageFont
import os

# 创建图片目录
img_dir = "/root/可交付文件/图片"
os.makedirs(img_dir, exist_ok=True)

# 颜色方案
colors = {
    "AI 指南": ("#4F46E5", "#818CF8"),  # 蓝紫色
    "Notion": ("#000000", "#333333"),   # 黑白
    "Python": ("#3776AB", "#FFD43B"),   # Python 蓝黄
    "副业": ("#DC2626", "#F87171"),     # 红色
}

def create_cover(title, subtitle, color_top, color_bottom, filename):
    """创建产品封面图"""
    # 创建图片 800x800
    width, height = 800, 800
    img = Image.new('RGB', (width, height), color=color_top)
    draw = ImageDraw.Draw(img)
    
    # 渐变背景
    for y in range(height // 2, height):
        ratio = (y - height // 2) / (height // 2)
        r = int(int(color_top[1:3], 16) * (1 - ratio) + int(color_bottom[1:3], 16) * ratio)
        g = int(int(color_top[3:5], 16) * (1 - ratio) + int(color_bottom[3:5], 16) * ratio)
        b = int(int(color_top[5:7], 16) * (1 - ratio) + int(color_bottom[5:7], 16) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 绘制标题（使用默认字体）
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", 60)
        font_medium = ImageFont.truetype("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", 36)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # 标题文字
    draw.text((width // 2, height // 3), title, fill="white", anchor="mm", font=font_large)
    draw.text((width // 2, height // 2), subtitle, fill="#E5E7EB", anchor="mm", font=font_medium)
    
    # 底部装饰
    draw.rectangle([(0, height - 50), (width, height)], fill="#111827")
    draw.text((width // 2, height - 25), "数字产品 · 自动发货", fill="#9CA3AF", anchor="mm", font=font_medium)
    
    # 保存图片
    filepath = os.path.join(img_dir, filename)
    img.save(filepath, 'JPEG', quality=90)
    print(f"✅ 已生成：{filepath}")
    return filepath

# 生成 4 个产品封面
products = [
    ("AI 使用指南", "高效提问技巧 · 效率翻倍", colors["AI 指南"][0], colors["AI 指南"][1], "AI 使用指南封面.jpg"),
    ("Notion 模板", "任务管理系统 · 告别拖延", colors["Notion"][0], colors["Notion"][1], "Notion 模板封面.jpg"),
    ("Python 脚本", "5 个自动化脚本 · 节省时间", colors["Python"][0], colors["Python"][1], "Python 脚本封面.jpg"),
    ("定制服务", "Python 开发 · 数据处理", colors["副业"][0], colors["副业"][1], "定制服务封面.jpg"),
]

print("🎨 开始生成产品封面...\n")
for title, subtitle, c1, c2, filename in products:
    create_cover(title, subtitle, c1, c2, filename)

print(f"\n✅ 完成！图片保存在：{img_dir}")
