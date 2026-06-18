# GIF Studio Pro — 恢复的源代码

## 项目结构

| 文件 | 大小 | 说明 |
|------|------|------|
| `main.py` | 0.6 KB | 程序入口 |
| `gui.py` | 28 KB | 主界面、BaseTab 基类、GIF 预览对话框 |
| `gif_deco_tab.py` | 14 KB | GIF 分解标签页 UI |
| `gif_deco_processor.py` | 4.1 KB | GIF 分解处理器 |
| `gif_encoder.py` | 1.4 KB | GIF 编码器 |
| `gif_optimizer.py` | 1.4 KB | GIF 优化器 |
| `image_processor.py` | 2.5 KB | 图片处理器 |
| `video_processor.py` | 4.5 KB | 视频处理器 |
| `audio_video_studio_tab.py` | 8 KB | 音视频工作室标签页 UI |
| `yt_downloader.py` | 2.2 KB | YouTube 下载器逻辑 |
| `yt_downloader_tab.py` | 8.9 KB | YouTube 下载标签页 UI |
| `draw_engine.py` | 16.3 KB | 绘图引擎 |
| `utility_functions.py` | 1.4 KB | 工具函数 |
| `dropdown_menu.py` | 5.2 KB | 自定义下拉菜单组件 |

## 依赖安装

```bash
pip install customtkinter pillow opencv-python numpy websockets pycryptodome yt-dlp
```

## 运行

```bash
python main.py
```

## 技术栈

- **UI 框架**: CustomTkinter（现代化 tkinter）
- **图片处理**: Pillow (PIL)
- **视频处理**: OpenCV (cv2)
- **视频下载**: yt-dlp
- **加密**: PyCryptodome
- **Python**: 3.14

## 关于恢复的代码

- ✅ **完整保留**：所有类名、函数名、变量名、参数签名、import 语句、常量、docstring
- ✅ **完整保留**：模块间依赖关系、类继承结构
- ⚠️ **需要还原**：函数体内部逻辑（标注了 `# TODO: reconstruct body from bytecode`）
- ❌ **无法恢复**：原始注释（编译时丢失）

> 函数体内的注释已提供该函数使用的常量值和依赖，可辅助手动还原逻辑。
