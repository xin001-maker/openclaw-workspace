#!/usr/bin/env python3
# 文件批量重命名脚本
# 用法：python rename_files.py <文件夹路径> <前缀>

import os
import sys

def rename_files(folder_path, prefix="file"):
    """批量重命名文件"""
    if not os.path.exists(folder_path):
        print(f"❌ 文件夹不存在：{folder_path}")
        return
    
    files = os.listdir(folder_path)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    files.sort()
    
    if not files:
        print("⚠️  文件夹内没有文件")
        return
    
    print(f"📁 找到 {len(files)} 个文件，开始重命名...\n")
    
    for i, filename in enumerate(files, 1):
        name, ext = os.path.splitext(filename)
        new_name = f"{prefix}_{i:03d}{ext}"
        
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)
        
        os.rename(old_path, new_path)
        print(f"✅ {filename} → {new_name}")
    
    print(f"\n🎉 完成！共重命名 {len(files)} 个文件")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("📖 用法：python rename_files.py <文件夹路径> [前缀]")
        print("📝 示例：python rename_files.py ./photos photo")
        sys.exit(1)
    
    folder = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else "file"
    rename_files(folder, prefix)
