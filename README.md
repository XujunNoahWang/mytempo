# My Tempo

一个具有苹果风格设计的Markdown文档上传应用。

## 系统要求

- Python 3.7+
- Windows 10/11

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/mytempo.git
cd mytempo
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 功能特点

- 🎨 精美的苹果风格界面设计
  - 使用Inter字体显示英文
  - 使用Noto Sans SC字体显示中文
  - 遵循苹果设计规范的色彩和间距
- 📄 支持多种文件上传方式
  - 拖拽上传
  - 点击按钮选择文件
- ✨ 优雅的交互体验
  - 平滑的动画效果
  - 实时的视觉反馈
  - 清晰的错误提示
- 🔍 严格的文件格式验证
  - 支持.md和.markdown格式
  - 自动过滤非Markdown文件

## 开发说明

- 使用Python的tkinter和tkinterdnd2构建
- 采用面向对象的编程方式
- 支持类型提示
- 遵循PEP 8代码规范

## 待实现功能

- [ ] Markdown文件预览
- [ ] 文件内容编辑
- [ ] 导出为其他格式
- [ ] 自动保存

## 许可证

MIT License 