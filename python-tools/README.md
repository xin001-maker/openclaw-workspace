# 🛠️ Python 效率工具箱

一个实用的 Python 自动化脚本集合，帮你节省日常工作时间。

## ✨ 功能列表

- 📁 **文件批量重命名** - 一键整理混乱的文件
- 📊 **Excel 数据合并** - 自动合并多个 Excel 文件
- 🖼️ **图片批量压缩** - 压缩图片不失真
- 📝 **文本处理工具** - 批量替换、格式化文本
- 📋 **CSV 转换工具** - CSV 与 Excel 互转

## 🚀 快速开始

### 安装依赖

```bash
pip install pandas openpyxl Pillow
```

或使用国内镜像：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas openpyxl Pillow
```

### 使用方法

#### 1. 文件批量重命名

```bash
python rename_files.py /path/to/folder prefix_name
```

示例：
```bash
python rename_files.py ./photos photo
```

#### 2. Excel 数据合并

```bash
python merge_excel.py /path/to/excel_folder output.xlsx
```

#### 3. 图片批量压缩

```bash
python compress_images.py /path/to/images 80
```

参数说明：
- 第一个参数：图片文件夹路径
- 第二个参数：压缩质量（1-100，默认 80）

## 📦 脚本列表

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `rename_files.py` | 文件批量重命名 | 整理照片、文档 |
| `merge_excel.py` | Excel 数据合并 | 报表汇总 |
| `compress_images.py` | 图片批量压缩 | 网站图片优化 |
| `text_processor.py` | 文本批量处理 | 日志处理、数据清洗 |
| `csv_converter.py` | CSV 转换工具 | 数据格式转换 |

## 💡 使用示例

### 示例 1：整理下载文件夹

```bash
# 重命名所有下载的文件
python rename_files.py ~/Downloads download
```

### 示例 2：合并销售报表

```bash
# 合并所有月度报表
python merge_excel.py ./monthly_reports yearly_summary.xlsx
```

### 示例 3：压缩网站图片

```bash
# 压缩图片到 75% 质量
python compress_images.py ./website_images 75
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 💖 支持

如果这个项目对你有帮助，欢迎：

- ⭐ Star 这个项目
- 💰 [赞助作者](https://github.com/sponsors/用户名)
- 📢 推荐给朋友

---

**Made with ❤️ by xin001-maker**
