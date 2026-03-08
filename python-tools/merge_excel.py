#!/usr/bin/env python3
# Excel 数据合并脚本
# 用法：python merge_excel.py <文件夹路径> <输出文件名>

import pandas as pd
import os
import sys

def merge_excel_files(folder_path, output_file="merged.xlsx"):
    """合并文件夹内所有 Excel 文件"""
    files = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.xls'))]
    
    if not files:
        print("❌ 未找到 Excel 文件")
        return
    
    print(f"📊 找到 {len(files)} 个 Excel 文件，开始合并...\n")
    
    dfs = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_excel(file_path)
            df['来源文件'] = file
            dfs.append(df)
            print(f"✅ 已读取：{file} ({len(df)} 行)")
        except Exception as e:
            print(f"❌ 读取失败 {file}: {e}")
    
    if dfs:
        merged = pd.concat(dfs, ignore_index=True)
        merged.to_excel(output_file, index=False)
        print(f"\n🎉 完成！共 {len(merged)} 行，保存到 {output_file}")
    else:
        print("\n⚠️  没有成功读取任何文件")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("📖 用法：python merge_excel.py <文件夹路径> [输出文件名]")
        print("📝 示例：python merge_excel.py ./reports 2024_summary.xlsx")
        sys.exit(1)
    
    folder = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "merged.xlsx"
    merge_excel_files(folder, output)
