#!/usr/bin/env python3
# 图片批量压缩脚本
# 用法：python compress_images.py <文件夹路径> [质量 1-100]

import os
import sys
from PIL import Image

def compress_images(folder_path, quality=80):
    """批量压缩图片"""
    if not os.path.exists(folder_path):
        print(f"❌ 文件夹不存在：{folder_path}")
        return
    
    output_folder = os.path.join(folder_path, "compressed")
    os.makedirs(output_folder, exist_ok=True)
    
    files = [f for f in os.listdir(folder_path) 
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not files:
        print("❌ 未找到图片文件")
        return
    
    print(f"🖼️  找到 {len(files)} 张图片，开始压缩...\n")
    
    total_saved = 0
    
    for filename in files:
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder, filename)
        
        try:
            original_size = os.path.getsize(input_path)
            img = Image.open(input_path)
            
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            compressed_size = os.path.getsize(output_path)
            saved = original_size - compressed_size
            saved_percent = (saved / original_size) * 100
            
            total_saved += saved
            print(f"✅ {filename}: {original_size/1024:.1f}KB → {compressed_size/1024:.1f}KB (节省 {saved_percent:.1f}%)")
        
        except Exception as e:
            print(f"❌ 处理失败 {filename}: {e}")
    
    print(f"\n🎉 完成！共处理 {len(files)} 张图片，总计节省 {total_saved/1024:.1f}KB")
    print(f"📁 输出文件夹：{output_folder}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("📖 用法：python compress_images.py <文件夹路径> [质量 1-100]")
        print("📝 示例：python compress_images.py ./photos 75")
        sys.exit(1)
    
    folder = sys.argv[1]
    quality = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    compress_images(folder, quality)
