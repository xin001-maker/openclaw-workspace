#!/usr/bin/env python3
# 重新设计产品封面 - 学习参考图风格

from PIL import Image, ImageDraw, ImageFont
import os

img_dir = "/root/可交付文件/图片"

# 参考图风格分析：
# 1. 简洁大字
# 2. 鲜艳颜色
# 3. 突出核心卖点
# 4. 不要价格
# 5. 专业感

def create_modern_cover(title, subtitle, highlights, bg_color, text_color, filename):
    """现代风格封面"""
    width, height = 800, 800
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc", 70)
        font_medium = ImageFont.truetype("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", 40)
        font_small = ImageFont.truetype("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", 30)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 顶部标题（超大字）
    draw.text((width // 2, height // 4), title, fill=text_color, anchor="mm", font=font_large)
    
    # 中间副标题
    draw.text((width // 2, height // 2), subtitle, fill=text_color, anchor="mm", font=font_medium)
    
    # 底部卖点标签
    y_offset = height * 3 // 4
    for i, highlight in enumerate(highlights):
        # 标签背景
        label_width = 500
        label_height = 50
        x1 = (width - label_width) // 2
        y1 = y_offset + i * 60
        x2 = x1 + label_width
        y2 = y1 + label_height
        
        # 圆角矩形
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill=text_color)
        draw.text((width // 2, y1 + label_height // 2), highlight, fill=bg_color, anchor="mm", font=font_small)
    
    # 保存
    filepath = os.path.join(img_dir, filename)
    img.save(filepath, 'JPEG', quality=90)
    print(f"✅ 已生成：{filepath}")
    return filepath

# 新产品封面（简洁专业风格）
products = [
    (
        "小红书爆款文案",
        "1000+ 条模板 直接复制",
        ["✅ 爆款标题 200 条", "✅ 各品类文案 500 条", "✅ 运营工具 100+ 个"],
        "#FF2442",  # 小红书红
        "white",
        "小红书文案封面_new.jpg"
    ),
    (
        "考公面试话术",
        "800+ 条金句 高分必备",
        ["✅ 综合分析 200 条", "✅ 组织管理 150 条", "✅ 高分金句 200 条"],
        "#C41E3A",  # 中国红
        "white",
        "考公面试封面_new.jpg"
    ),
    (
        "AI 公文写作",
        "500+ 条提示词 效率翻倍",
        ["✅ 通知报告 180 条", "✅ 请示总结 140 条", "✅ 讲话稿 80 条"],
        "#1E3A8A",  # 公文蓝
        "white",
        "AI 公文封面_new.jpg"
    ),
]

print("🎨 重新设计封面（参考图风格）...\n")
for title, subtitle, highlights, bg, text, filename in products:
    create_modern_cover(title, subtitle, highlights, bg, text, filename)

print(f"\n✅ 完成！新封面已生成")
