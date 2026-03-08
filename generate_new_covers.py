#!/usr/bin/env python3
# 生成新产品封面图片

from PIL import Image, ImageDraw, ImageFont
import os

# 图片目录
img_dir = "/root/可交付文件/图片"

# 颜色方案
colors = {
    "小红书": ("#FF2442", "#FF6B7A"),  # 小红书红
    "考公": ("#C41E3A", "#E5556E"),    # 中国红
    "AI 公文": ("#1E3A8A", "#3B82F6"),  # 公文蓝
}

def create_cover(title, subtitle, price, color_top, color_bottom, filename):
    """创建产品封面图"""
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
    
    # 标题文字
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", 55)
        font_medium = ImageFont.truetype("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", 35)
        font_price = ImageFont.truetype("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", 70)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_price = ImageFont.load_default()
    
    # 标题
    draw.text((width // 2, height // 4), title, fill="white", anchor="mm", font=font_large)
    
    # 副标题
    draw.text((width // 2, height // 2), subtitle, fill="#E5E7EB", anchor="mm", font=font_medium)
    
    # 价格标签
    draw.rectangle([(width//2 - 150, height*3//4 - 40), (width//2 + 150, height*3//4 + 40)], fill="#FFD700")
    draw.text((width // 2, height * 3 // 4), f"¥{price}", fill="#C41E3A", anchor="mm", font=font_price)
    
    # 底部装饰
    draw.rectangle([(0, height - 50), (width, height)], fill="#111827")
    draw.text((width // 2, height - 25), "虚拟资料 · 自动发货", fill="#9CA3AF", anchor="mm", font=font_medium)
    
    # 保存图片
    filepath = os.path.join(img_dir, filename)
    img.save(filepath, 'JPEG', quality=90)
    print(f"✅ 已生成：{filepath}")
    return filepath

# 生成 3 个新产品封面
products = [
    ("小红书爆款文案", "1000+ 条模板 · 直接复制", "15.9", colors["小红书"][0], colors["小红书"][1], "小红书文案封面.jpg"),
    ("考公面试话术", "800+ 条金句 · 高分必备", "19.9", colors["考公"][0], colors["考公"][1], "考公面试封面.jpg"),
    ("AI 公文写作", "500+ 条提示词 · 效率翻倍", "19.9", colors["AI 公文"][0], colors["AI 公文"][1], "AI 公文封面.jpg"),
]

print("🎨 开始生成新产品封面...\n")
for title, subtitle, price, c1, c2, filename in products:
    create_cover(title, subtitle, price, c1, c2, filename)

print(f"\n✅ 完成！")
