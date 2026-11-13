# ImageCaptionStudio

**轻量级开源图片文本标注工具**

[English](README.md) | **简体中文**

## 项目介绍

ImageCaptionStudio 是一款基于 Python 和 PySide6 开发的轻量级图片文本标注工具。

主要用于图像描述（Image Caption）和提示词（Prompt）的人工标注与管理，适用于文生图模型训练、LoRA 微调及其他图文配对数据集的制作。

## 主要功能

- **图片管理：** 批量导入图片目录，支持图片浏览和快速切换。
- **文本标注：** 为图片编写、修改和保存 Caption / Prompt。
- **TXT 标注：** 自动关联图片与同名 `.txt` 标注文件。
- **灵活存储：** 支持标注文件与图片同目录保存，也可指定独立目录。
- **图片预览：** 支持放大、缩小及适应窗口。
- **进度统计：** 实时显示已标注和未标注图片数量。
- **词数统计：** 实时统计 Prompt 文本词数。
- **中英双语：** 支持简体中文与英文界面切换。
- **快捷键设置：** 支持自定义常用操作快捷键。
- **字体调整：** 支持调整界面及 Prompt 编辑区域字号。

## 软件截图

![ImageCaptionStudio](assets/screenshot.png)

## 下载安装

前往 [Releases](../../releases) 下载最新 Windows 绿色版。

解压 ZIP 文件后运行 `ImageCaptionStudio.exe`，无需安装 Python 环境。

## 源码运行

```bash
pip install -r requirements.txt
python main.py
```

## 开源协议

本项目自有源代码基于 [MIT License](LICENSE) 开源，第三方依赖遵循各自的许可证。

Copyright © 2026 Cao Jinhao.
