# MyTempo

MyTempo 是一个简单的桌面应用程序，用于以电影片尾字幕滚动的方式阅读Markdown文件。

## 功能特点

- 支持拖拽或点击选择MD文件
- 半透明黑色背景的阅读界面
- 按住下键实现平滑的文字向上滚动效果
- 可调整窗口大小
- 支持Markdown格式
- 使用微软雅黑字体，清晰易读

## 安装要求

- Python 3.x
- 依赖包：
  - customtkinter==5.2.2
  - markdown==3.5.2
  - tkinterdnd2==0.3.0

## 安装方法

```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行程序：
```bash
python mytempo.py
```

2. 在打开的窗口中选择或拖入Markdown文件
3. 按住键盘下键开始滚动阅读
4. 松开下键停止滚动

## 版本

当前版本：0.1.0

## 许可证

MIT License 