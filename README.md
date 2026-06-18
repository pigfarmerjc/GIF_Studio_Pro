# ✨ GIF Studio Pro — 极客影音 GIF 创作工坊

GIF Studio Pro 是一款基于 Python 3.14 + CustomTkinter 打造的现代化桌面级 GIF 综合创作与编辑工具。软件集成了视频切片、幻灯片合成、无损优化压缩、画布涂鸦装饰以及 YouTube 视频提取等一整套完整的工作流。

---

## 🚀 核心功能板块

1. **🎬 视频转 GIF (Video to GIF)**
   - 支持高精度视频帧预览与时间轴拖拽。
   - 物理级的裁剪框（Crop Overlay），可任意缩放、移动选区，支持原片/Match First/Custom 尺寸模式。
   - 提供丰富的高级参数配置：帧率（FPS）、缩放比例（Scale）、颜色深度限制（Palette）、抖动（Dithering）。

2. **📸 幻灯片转 GIF (Slides to GIF)**
   - 支持多张图片批量导入，可对帧顺序进行一键调整、移动或删除。
   - 内置多种过渡效果（None, Fade, Slide Left, Slide Up, Cross Dissolve）并支持自定义过渡时长。
   - 实时根据设定的每帧延迟（Frame Delay）输出顺滑动画。

3. **⚙️ GIF 压缩器 (GIF Compressor)**
   - 针对已有 GIF 文件进行极致压缩，提供多种优化预设（Tiny, Web, Standard, Lossy High）。
   - 支持局部调色盘重映射、丢帧过滤、尺寸二次缩放等，体积大幅缩减，画质损耗极低。

4. **🎨 涂鸦装饰工坊 (GIF Doodle Tab)**
   - Canvas 画布级的高级多图层编辑器。
   - 支持**文本图层、Emoji 表情图层、贴纸图片图层**的无缝叠加与混合。
   - 内置精美文字艺术样式：渐变色文字、外发光发光字（Glow）、自定义阴影（Shadow）及背景边框。
   - 支持图层深度排序、物理属性动画（Rotation, Scaling, Pos）。

5. **📥 YouTube 下载器 (YouTube Downloader)**
   - 集成 `yt-dlp` 内核，输入链接即可快速解析并提取 YouTube 视频。
   - 下载完成后支持一键重定向至“视频转 GIF”面板，工作流无缝连接。

6. **📁 创意工坊 (Workspace)**
   - 本地化文件浏览器，自动收录并分类管理在工作流中导出的所有临时与成品 GIF。
   - 快速预览、删除、或在系统文件管理器中打开。

---

## 🛠️ 技术栈

* **GUI 框架**：[CustomTkinter](https://github.com/tomschw/customtkinter)（基于 Tkinter 的现代暗黑风扁平化组件库）
* **图像处理**：[Pillow (PIL)](https://python-pillow.org/)
* **视频处理**：[OpenCV (cv2)](https://opencv.org/) & `imageio-ffmpeg`
* **视频下载**：[yt-dlp](https://github.com/yt-dlp/yt-dlp)
* **打包编译**：[PyInstaller](https://pyinstaller.org/)
* **运行环境**：Python 3.14+

---

## 📦 快速开始

### 方式 A：直接运行 `.exe` 单文件版（推荐）
我们已为您将所有代码和第三方静态依赖项整体打包封装为了独立的可执行文件。
* 双击运行：[dist/GIF_Studio_Pro.exe](file:///C:/临时文件/GIF_Studio_Pro_source/dist/GIF_Studio_Pro.exe) 即可启动软件，无需配置任何 Python 环境。

### 方式 B：从源代码启动

#### 1. 安装项目依赖
打开命令行，执行以下命令安装核心依赖包：
```bash
pip install customtkinter Pillow opencv-python numpy yt-dlp imageio-ffmpeg
```

#### 2. 启动应用
在项目根目录下运行：
```bash
python main.py
```

---

## 📁 源代码文件结构

```bash
GIF_Studio_Pro_source/
├── main.py                    # 应用唯一主入口
├── gui.py                     # 全局布局控制、BaseTab 基类与通用组件
├── gif_deco_tab.py            # 涂鸦装饰标签页（界面）
├── gif_deco_processor.py      # 涂鸦装饰的核心图层渲染器
├── video_processor.py         # 视频读取、裁剪、帧提取
├── image_processor.py         # 图片读取、过渡动画帧生成
├── gif_encoder.py             # 高效 GIF 文件渲染保存逻辑
├── gif_optimizer.py           # GIF 文件的 Palette 调色板重构与优化算法
├── yt_downloader.py          # YouTube 下载逻辑内核
├── yt_downloader_tab.py      # YouTube 下载标签页（界面）
├── audio_video_studio_tab.py  # 音视频工作室标签页
├── dist/
│   └── GIF_Studio_Pro.exe     # 打包好的单文件版 EXE 应用程序
└── .gitignore                 # Git 忽略配置文件
```
