# 🐍 Python 自动化脚本合集

*5 个实用脚本，帮你节省每天 1 小时*

---

## 脚本清单

| # | 脚本 | 功能 | 适用场景 |
|---|------|------|----------|
| 1 | rename_files.py | 文件批量重命名 | 整理照片、文档 |
| 2 | merge_excel.py | Excel 数据合并 | 报表汇总 |
| 3 | web_scraper.py | 网页内容抓取 | 数据采集 |
| 4 | compress_images.py | 图片批量压缩 | 网站图片优化 |
| 5 | reminder.py | 定时任务提醒 | 每日提醒 |

---

## 脚本 1：文件批量重命名 (rename_files.py)

```python
#!/usr/bin/env python3
# 文件批量重命名脚本
# 用法：python rename_files.py <文件夹路径> <前缀>

import os
import sys
from datetime import datetime

def rename_files(folder_path, prefix="file"):
    """批量重命名文件"""
    if not os.path.exists(folder_path):
        print(f"文件夹不存在：{folder_path}")
        return
    
    files = os.listdir(folder_path)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    files.sort()
    
    for i, filename in enumerate(files, 1):
        name, ext = os.path.splitext(filename)
        new_name = f"{prefix}_{i:03d}_{name}{ext}"
        
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)
        
        os.rename(old_path, new_path)
        print(f"{filename} → {new_name}")
    
    print(f"\n完成！共重命名 {len(files)} 个文件")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python rename_files.py <文件夹路径> [前缀]")
        print("示例：python rename_files.py ./photos photo")
        sys.exit(1)
    
    folder = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else "file"
    rename_files(folder, prefix)
```

**使用方法：**
```bash
python rename_files.py /path/to/folder photo
```

---

## 脚本 2：Excel 数据合并 (merge_excel.py)

```python
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
        print("未找到 Excel 文件")
        return
    
    dfs = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_excel(file_path)
            df['来源文件'] = file
            dfs.append(df)
            print(f"已读取：{file} ({len(df)} 行)")
        except Exception as e:
            print(f"读取失败 {file}: {e}")
    
    if dfs:
        merged = pd.concat(dfs, ignore_index=True)
        merged.to_excel(output_file, index=False)
        print(f"\n完成！共 {len(merged)} 行，保存到 {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python merge_excel.py <文件夹路径> [输出文件名]")
        sys.exit(1)
    
    folder = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "merged.xlsx"
    merge_excel_files(folder, output)
```

**使用方法：**
```bash
python merge_excel.py /path/to/excel_folder result.xlsx
```

**依赖安装：**
```bash
pip install pandas openpyxl
```

---

## 脚本 3：网页内容抓取 (web_scraper.py)

```python
#!/usr/bin/env python3
# 网页内容抓取脚本
# 用法：python web_scraper.py <URL> <选择器>

import requests
from bs4 import BeautifulSoup
import sys

def scrape_web(url, selector="h1"):
    """抓取网页指定内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.select(selector)
        
        print(f"找到 {len(elements)} 个匹配元素:\n")
        for i, elem in enumerate(elements, 1):
            text = elem.get_text(strip=True)
            if text:
                print(f"{i}. {text[:100]}...")
        
        return elements
    
    except Exception as e:
        print(f"抓取失败：{e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python web_scraper.py <URL> [CSS 选择器]")
        print("示例：python web_scraper.py https://example.com 'h2.title'")
        sys.exit(1)
    
    url = sys.argv[1]
    selector = sys.argv[2] if len(sys.argv) > 2 else "h1"
    scrape_web(url, selector)
```

**使用方法：**
```bash
python web_scraper.py "https://example.com" "h2.title"
```

**依赖安装：**
```bash
pip install requests beautifulsoup4
```

---

## 脚本 4：图片批量压缩 (compress_images.py)

```python
#!/usr/bin/env python3
# 图片批量压缩脚本
# 用法：python compress_images.py <文件夹路径> [质量 1-100]

import os
import sys
from PIL import Image

def compress_images(folder_path, quality=80):
    """批量压缩图片"""
    if not os.path.exists(folder_path):
        print(f"文件夹不存在：{folder_path}")
        return
    
    output_folder = os.path.join(folder_path, "compressed")
    os.makedirs(output_folder, exist_ok=True)
    
    files = [f for f in os.listdir(folder_path) 
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
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
            print(f"{filename}: {original_size/1024:.1f}KB → {compressed_size/1024:.1f}KB (节省 {saved_percent:.1f}%)")
        
        except Exception as e:
            print(f"处理失败 {filename}: {e}")
    
    print(f"\n完成！共处理 {len(files)} 张图片，总计节省 {total_saved/1024:.1f}KB")
    print(f"输出文件夹：{output_folder}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python compress_images.py <文件夹路径> [质量 1-100]")
        print("示例：python compress_images.py ./photos 75")
        sys.exit(1)
    
    folder = sys.argv[1]
    quality = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    compress_images(folder, quality)
```

**使用方法：**
```bash
python compress_images.py /path/to/photos 75
```

**依赖安装：**
```bash
pip install Pillow
```

---

## 脚本 5：定时任务提醒 (reminder.py)

```python
#!/usr/bin/env python3
# 定时任务提醒脚本
# 用法：python reminder.py <时间> <消息>

import schedule
import time
import sys
from datetime import datetime

def send_reminder(message):
    """发送提醒"""
    print(f"\n⏰ [{datetime.now().strftime('%H:%M:%S')}] 提醒：{message}")

def schedule_reminder(time_str, message):
    """设置定时提醒"""
    schedule.every().day.at(time_str).do(send_reminder, message)
    print(f"已设置提醒：每天 {time_str} - {message}")
    print("按 Ctrl+C 退出\n")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python reminder.py <时间 HH:MM> <消息>")
        print("示例：python reminder.py 09:00 '记得开会'")
        sys.exit(1)
    
    time_str = sys.argv[1]
    message = " ".join(sys.argv[2:])
    schedule_reminder(time_str, message)
```

**使用方法：**
```bash
python reminder.py 09:00 "记得开会"
```

**依赖安装：**
```bash
pip install schedule
```

---

## 环境准备

### 安装 Python

**Windows:**
1. 访问 https://www.python.org/downloads/
2. 下载并安装 Python 3.8+
3. 安装时勾选 "Add Python to PATH"

**Mac:**
```bash
brew install python
```

**Linux:**
```bash
sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo yum install python3 python3-pip  # CentOS/RHEL
```

### 安装依赖

```bash
pip install pandas openpyxl requests beautifulsoup4 Pillow schedule
```

或使用国内镜像：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas openpyxl requests beautifulsoup4 Pillow schedule
```

---

## 常见问题

**Q: 脚本不会用怎么办？**
A: 每个脚本都有使用说明，按照"使用方法"中的命令运行即可。

**Q: 提示缺少模块怎么办？**
A: 按照"依赖安装"中的命令安装所需模块。

**Q: 可以修改脚本吗？**
A: 当然可以！代码完全开源，随意定制。

**Q: 有其他需求可以定制吗？**
A: 可以！联系卖家定制开发，50 RMB 起。

---

*脚本版本：1.0 | 更新日期：2026-03-07*

**感谢购买！祝效率翻倍！🚀**
