# ============================================================
# Module: gui.py
# Reconstructed from Python 3.14 bytecode
# NOTE: Function bodies need manual reconstruction
#       Class/function structure is accurate
# ============================================================

import os
import json
import shutil
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import customtkinter as ctk
from PIL import Image, ImageTk
from video_processor import VideoProcessor
from image_processor import ImageProcessor
from gif_optimizer import GifOptimizer
from gif_encoder import GifEncoder
from gif_deco_tab import GifDecoTab
from audio_video_studio_tab import AudioVideoStudioTab
from yt_downloader_tab import YtDownloaderTab

# --- Global variables/constants ---
C = {
    'bg_deep': '#0A0F1E',
    'bg_primary': '#0F172A',
    'bg_secondary': '#1A2540',
    'bg_surface': '#1E293B',
    'bg_card': '#243047',
    'bg_hover': '#334155',
    'sidebar_bg': '#080D1A',
    'sidebar_item': '#111827',
    'accent': '#6366F1',
    'accent_hover': '#4F46E5',
    'accent_light': '#818CF8',
    'success': '#10B981',
    'success_hover': '#059669',
    'danger': '#EF4444',
    'danger_muted': '#E11D48',
    'danger_hover': '#BE123C',
    'cyan': '#06B6D4',
    'cyan_hover': '#0891B2',
    'amber': '#F59E0B',
    'amber_hover': '#D97706',
    'text_primary': '#F1F5F9',
    'text_muted': '#64748B',
    'text_dim': '#475569',
    'border': '#1E293B',
    'progress_bg': '#0F172A',
    'progress_fg': '#6366F1',
    'gradient_start': '#6366F1',
    'gradient_end': '#8B5CF6'
}
FONT = 'Microsoft YaHei'


def __annotate__(format):
    # --- Auto-reconstructed from bytecode ---
    # constants used: ['2', "'color_str'", "'return'"]
    pass  # TODO: reconstruct body from bytecode


def parse_color_depth(color_str):
    """Parses color depth integer from OptionMenu display string."""
    for val in (16, 32, 64, 128, 256):
        if str(val) in color_str:
            return val
    return 256


def __annotate__(format):
    # --- Auto-reconstructed from bytecode ---
    # constants used: ['2', "'gif_path'", "'title'", "'info_text'", "'extra_buttons'"]
    pass  # TODO: reconstruct body from bytecode


def open_gif_preview_dialog(parent, app, gif_path, title, info_text, extra_buttons):
    """
Reusable GIF preview dialog. Opens an animated GIF player modal.
extra_buttons: list of (label, fg_color, hover_color, command_fn) tuples
"""
    win = ctk.CTkToplevel(parent)
    win.title(title)
    win.geometry('560x580')
    win.minsize(480, 500)
    win.lift()
    win.grab_set()
    win.configure(fg_color=C['bg_primary'])
    win.grid_rowconfigure(1, weight=1)
    win.grid_columnconfigure(0, weight=1)
    lbl_info = ctk.CTkLabel(
        win,
        text=info_text,
        justify='center',
        font=ctk.CTkFont(family=FONT, size=13),
        text_color=C['text_primary'],
        fg_color=C['bg_secondary'],
        corner_radius=8
    )
    lbl_info.grid(row=0, column=0, padx=20, pady=(15, 8), sticky='ew', ipady=8)
    player = GifPreviewer(win)
    player.grid(row=1, column=0, padx=20, pady=5, sticky='nsew')
    player.load_gif(gif_path, max_width=480)
    btn_frame = ctk.CTkFrame(win, fg_color='transparent')
    btn_frame.grid(row=2, column=0, padx=20, pady=15, sticky='ew')
    all_buttons = list(extra_buttons) if extra_buttons else []
    all_buttons.append((
        '✕  关闭预览',
        C['bg_hover'],
        C['bg_card'],
        lambda: [win.grab_release(), win.destroy()]
    ))
    cols = len(all_buttons)
    for col, (lbl, fg, hov, cmd) in enumerate(all_buttons):
        btn_frame.grid_columnconfigure(col, weight=1)
        btn = ctk.CTkButton(
            btn_frame,
            text=lbl,
            fg_color=fg,
            hover_color=hov,
            height=40,
            font=ctk.CTkFont(family=FONT, size=13),
            command=cmd
        )
        btn.grid(row=0, column=col, padx=3, sticky='ew')
    win.protocol('WM_DELETE_WINDOW', lambda: [win.grab_release(), win.destroy()])
    return win


class BaseTab(ctk.CTkFrame):
    """BaseTab"""

    def __init__(self, master, app):
        """transparent"""
        super().__init__(master, fg_color='transparent')
        self.app = app
        self._cancel_event = threading.Event()

    def on_show(self):
        """Called when this tab becomes visible. Override in subclasses."""
        pass

    def on_hide(self):
        """Called before this tab is hidden. Override in subclasses."""
        pass

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # closure vars: ['__classdict__']
        # constants used: ['2', "'compile_text'", "'save_text'"]
        pass  # TODO: reconstruct body from bytecode

    def _build_bottom_bar(self, compile_text, save_text, compile_cmd, save_cmd):
        """Builds the standard compile + save + progress bar footer row."""
        bar = ctk.CTkFrame(self, fg_color=C['bg_surface'], corner_radius=12)
        bar.grid(row=1, column=0, columnspan=2, padx=0, pady=(10, 0), sticky='ew')
        bar.grid_columnconfigure(0, weight=1)
        
        action_row = ctk.CTkFrame(bar, fg_color='transparent')
        action_row.grid(row=0, column=0, padx=20, pady=(14, 8), sticky='ew')
        action_row.grid_columnconfigure(0, weight=1)
        
        self.btn_compile = ctk.CTkButton(
            action_row,
            text=compile_text,
            height=46,
            fg_color=C['accent'],
            hover_color=C['accent_hover'],
            font=ctk.CTkFont(size=15, weight='bold', family=FONT),
            command=compile_cmd,
            state='disabled'
        )
        self.btn_compile.grid(row=0, column=0, sticky='ew', padx=(0, 10))
        
        self.btn_save_gif = ctk.CTkButton(
            action_row,
            text=save_text,
            height=46,
            fg_color=C['success'],
            hover_color=C['success_hover'],
            font=ctk.CTkFont(size=15, weight='bold', family=FONT),
            command=save_cmd,
            state='disabled'
        )
        self.btn_cancel = ctk.CTkButton(
            action_row,
            text='✕ 取消任务',
            width=105,
            height=46,
            fg_color=C['danger_muted'],
            hover_color=C['danger_hover'],
            font=ctk.CTkFont(size=13, weight='bold', family=FONT),
            command=self._request_cancel,
            state='disabled'
        )
        self.btn_cancel.grid(row=0, column=1, padx=(0, 10))

        self.btn_save_gif.grid(row=0, column=2, sticky='e')
        
        self.lbl_status = ctk.CTkLabel(
            bar,
            text='就绪',
            text_color=C['text_muted'],
            anchor='w',
            font=ctk.CTkFont(family=FONT, size=12)
        )
        self.lbl_status.grid(row=1, column=0, padx=22, pady=(0, 4), sticky='ew')
        
        self.progress_bar = ctk.CTkProgressBar(
            bar,
            fg_color=C['progress_bg'],
            progress_color=C['progress_fg'],
            height=6,
            corner_radius=3
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, padx=20, pady=(0, 14), sticky='ew')
        
        return bar

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # closure vars: ['__classdict__']
        # constants used: ['2', "'val'", "'text'"]
        pass  # TODO: reconstruct body from bytecode

    def _update_progress(self, val, text):
        """Thread-safe progress + status update."""
        self.after(0, lambda: self.progress_bar.set(val))
        self.after(0, lambda: self.lbl_status.configure(text=text, text_color=C['text_muted']))

    def _begin_task(self):
        self._cancel_event.clear()
        self.btn_compile.configure(state='disabled')
        self.btn_save_gif.configure(state='disabled')
        self.btn_cancel.configure(state='normal')

    def _finish_task(self):
        self.btn_compile.configure(state='normal')
        self.btn_cancel.configure(state='disabled')

    def _request_cancel(self):
        self._cancel_event.set()
        self.btn_cancel.configure(state='disabled')
        self.lbl_status.configure(text='正在安全取消任务...', text_color=C['amber'])

    def _raise_if_cancelled(self):
        if self._cancel_event.is_set():
            raise InterruptedError('操作已由用户取消')

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # closure vars: ['__classdict__']
        # constants used: ['2', "'source_path'", "'save_title'"]
        pass  # TODO: reconstruct body from bytecode

    def _safe_save_gif(self, source_path, save_title):
        """Opens a save dialog and copies the temp GIF to user path."""
        if not os.path.exists(source_path):
            messagebox.showwarning('无文件', '尚未生成输出文件，请先运行转换。')
            return
        dest = filedialog.asksaveasfilename(
            title=save_title,
            defaultextension='.gif',
            filetypes=[('GIF Image', '*.gif')]
        )
        if not dest:
            return
        try:
            shutil.copy(source_path, dest)
            if hasattr(self.app, 'workspace_dir') and os.path.exists(self.app.workspace_dir):
                ws_dest = os.path.join(self.app.workspace_dir, os.path.basename(dest))
                shutil.copy(source_path, ws_dest)
            self.lbl_status.configure(
                text=f"✅ 已导出 → {os.path.basename(dest)}",
                text_color=C['success']
            )
            messagebox.showinfo('导出成功', f"文件已保存至：\n{dest}")
        except Exception as e:
            messagebox.showerror('导出失败', f"写入文件时出错：\n{str(e)}")

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # closure vars: ['__classdict__']
        # constants used: ['2', "'err'"]
        pass  # TODO: reconstruct body from bytecode

    def _on_thread_error(self, err, compile_btn_to_restore):
        """Standard thread error handler."""
        if isinstance(err, InterruptedError):
            self.after(0, self._show_cancelled)
            return
        self.after(0, lambda: messagebox.showerror('操作失败', f"发生错误：\n{str(err)}"))
        self.after(0, lambda: self.lbl_status.configure(text=f"❌ 失败: {str(err)[:80]}", text_color=C['danger']))
        self.after(0, lambda: self.progress_bar.set(0))
        if compile_btn_to_restore:
            self.after(0, lambda: compile_btn_to_restore.configure(state='normal'))
        if hasattr(self, 'btn_cancel'):
            self.after(0, lambda: self.btn_cancel.configure(state='disabled'))

    def _show_cancelled(self):
        self.progress_bar.set(0)
        self.lbl_status.configure(text='任务已取消', text_color=C['amber'])
        self._finish_task()


class GifPreviewer(ctk.CTkFrame):
    """GifPreviewer"""

    def __init__(self, master):
        """bg_primary"""
        super().__init__(master, fg_color=C['bg_primary'], corner_radius=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._placeholder = ctk.CTkLabel(
            self,
            text='🌟 GIF 预览区域',
            text_color=C['text_dim'],
            font=ctk.CTkFont(size=14, weight='bold', family=FONT)
        )
        self._placeholder.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        self._lbl = None
        self.gif_frames = []
        self.delays = []
        self._frame_idx = 0
        self._playing = False
        self._after_id = None

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # closure vars: ['__classdict__']
        # constants used: ['2', "'file_path'", "'max_width'"]
        pass  # TODO: reconstruct body from bytecode

    def load_gif(self, file_path, max_width):
        self.stop()
        self._placeholder.grid_remove()
        if self._lbl:
            self._lbl.destroy()
        self._lbl = ctk.CTkLabel(self, text='', fg_color='transparent')
        self._lbl.grid(row=0, column=0, sticky='nsew', padx=8, pady=8)
        self.gif_frames = []
        self.delays = []
        try:
            with Image.open(file_path) as img:
                w, h = img.size
                scale = min(1.0, max_width / w)
                pw, ph = int(w * scale), int(h * scale)
                for i in range(getattr(img, 'n_frames', 1)):
                    img.seek(i)
                    frame = img.copy().convert('RGBA').resize((pw, ph), Image.Resampling.LANCZOS)
                    self.gif_frames.append(ctk.CTkImage(light_image=frame, dark_image=frame, size=(pw, ph)))
                    dur = img.info.get('duration', 100)
                    self.delays.append(max(20, dur))
            self._frame_idx = 0
            self._playing = True
            self._play_loop()
        except Exception as e:
            self.stop()
            self._placeholder.configure(text=f"无法预览: {str(e)}")
            self._placeholder.grid()

    def _play_loop(self):
        if not self._playing or not self.gif_frames:
            return
        if self._lbl:
            self._lbl.configure(image=self.gif_frames[self._frame_idx])
        delay = self.delays[self._frame_idx]
        self._frame_idx = (self._frame_idx + 1) % len(self.gif_frames)
        self._after_id = self.after(delay, self._play_loop)

    def stop(self):
        self._playing = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None
        self.gif_frames.clear()
        self.delays.clear()


class GIFStudioApp(ctk.CTk):
    """GIFStudioApp"""

    def __init__(self):
        """✨ GIF Studio Pro — 极客影音 GIF 创作工坊"""
        super().__init__()
        self.title('✨ GIF Studio Pro — 极客影音 GIF 创作工坊')
        self.geometry('1200x800')
        self.minsize(1080, 720)
        self.configure(fg_color=C['bg_deep'])
        
        self.video_processor = VideoProcessor()
        self.image_processor = ImageProcessor()
        self.gif_optimizer = GifOptimizer()
        self.gif_encoder = GifEncoder()
        
        _tmp = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp')
        os.makedirs(_tmp, exist_ok=True)
        self.temp_gif_path = os.path.join(_tmp, 'gif_studio_temp.gif')
        self.temp_opt_path = os.path.join(_tmp, 'gif_studio_optimized.gif')
        self.settings_dir = os.path.join(os.environ.get('LOCALAPPDATA', _tmp), 'GIF Studio Pro')
        self.settings_path = os.path.join(self.settings_dir, 'settings.json')
        self.settings = self._load_settings()
        self.recent_files = [
            item for item in self.settings.get('recent_files', [])
            if os.path.exists(item.get('path', ''))
        ]
        
        import sys
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.workspace_dir = os.path.join(base_dir, 'output')
        os.makedirs(self.workspace_dir, exist_ok=True)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self._create_sidebar()
        self._create_content_panels()
        self._restore_video_settings()
        self.select_tab(self.settings.get('last_tab', 'VideoToGif'))
        self.protocol('WM_DELETE_WINDOW', self._on_close)

    def _on_close(self):
        for frame in getattr(self, 'frames', {}).values():
            if hasattr(frame, '_cancel_event'):
                frame._cancel_event.set()
            if hasattr(frame, 'stop_play'):
                frame.stop_play()
        self._save_settings()
        self.video_processor.release()
        self.destroy()

    def _load_settings(self):
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data if isinstance(data, dict) else {}
        except (OSError, ValueError, TypeError):
            return {}

    def _save_settings(self):
        video_tab = self.frames.get('VideoToGif') if hasattr(self, 'frames') else None
        if video_tab:
            self.settings['video_settings'] = {
                'fps': video_tab.val_fps.get(),
                'scale': video_tab.val_scale.get(),
                'speed': video_tab.val_speed.get(),
                'loop': video_tab.val_loop.get(),
                'colors': video_tab.val_colors.get(),
                'filter': video_tab.val_filter.get()
            }
        self.settings['appearance'] = self.appearance_option.get() if hasattr(self, 'appearance_option') else 'Dark'
        self.settings['recent_files'] = self.recent_files[:10]
        os.makedirs(self.settings_dir, exist_ok=True)
        temp_path = self.settings_path + '.tmp'
        try:
            with open(temp_path, 'w', encoding='utf-8') as file:
                json.dump(self.settings, file, ensure_ascii=False, indent=2)
            os.replace(temp_path, self.settings_path)
        except OSError as error:
            print(f'Save settings error: {error}')

    def _restore_video_settings(self):
        values = self.settings.get('video_settings', {})
        tab = self.frames['VideoToGif']
        try:
            tab.val_fps.set(float(values.get('fps', 12)))
            tab.val_scale.set(float(values.get('scale', 0.5)))
            tab.val_speed.set(float(values.get('speed', 1.0)))
            tab.val_loop.set(values.get('loop', 'Normal'))
            tab.val_colors.set(values.get('colors', '256 (超清)'))
            tab.val_filter.set(values.get('filter', 'None'))
            tab._update_basic_lbls(None)
        except (TypeError, ValueError, tk.TclError):
            pass

    def record_recent_file(self, path, kind):
        path = os.path.abspath(path)
        self.recent_files = [item for item in self.recent_files if item.get('path') != path]
        self.recent_files.insert(0, {'path': path, 'kind': kind})
        self.recent_files = self.recent_files[:10]
        self._save_settings()

    def _create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=C['sidebar_bg'])
        sidebar.grid(row=0, column=0, sticky='nsew')
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(9, weight=1)
        self._sidebar = sidebar
        
        brand_frame = ctk.CTkFrame(sidebar, fg_color=C['bg_primary'], corner_radius=0)
        brand_frame.grid(row=0, column=0, sticky='ew')
        
        ctk.CTkLabel(
            brand_frame,
            text='✨ GIF Studio Pro',
            font=ctk.CTkFont(size=21, weight='bold', family=FONT),
            text_color=C['accent_light']
        ).grid(row=0, column=0, padx=22, pady=(22, 3))
        
        ctk.CTkLabel(
            brand_frame,
            text='极客影音  GIF  创作工坊',
            text_color=C['text_dim'],
            font=ctk.CTkFont(size=11, family=FONT)
        ).grid(row=1, column=0, padx=22, pady=(0, 18))
        
        ctk.CTkFrame(sidebar, height=1, fg_color=C['bg_secondary']).grid(row=1, column=0, sticky='ew')
        
        nav_items = [
            ('VideoToGif', '🎥', '视频转 GIF'),
            ('ImagesToGif', '🖼️', '图片合成 GIF'),
            ('GifOptimize', '⚡', 'GIF 压缩优化'),
            ('AudioExtract', '🎬', '智能影音工作室'),
            ('GifDeco', '🎨', 'GIF 涂鸦装饰'),
            ('YtDownloader', '🌐', '网页视频下载'),
            ('Workspace', '📁', '工作区管理')
        ]
        
        self.nav_buttons = {}
        for i, (key, icon, label) in enumerate(nav_items):
            btn = ctk.CTkButton(
                sidebar,
                text=f"{icon}   {label}",
                anchor='w',
                height=46,
                font=ctk.CTkFont(size=14, family=FONT),
                fg_color='transparent',
                text_color=C['text_primary'],
                hover_color=C['sidebar_item'],
                corner_radius=8,
                command=lambda k=key: self.select_tab(k)
            )
            btn.grid(row=i + 2, column=0, padx=12, pady=3, sticky='ew')
            self.nav_buttons[key] = btn
            
        ctk.CTkFrame(sidebar, height=1, fg_color=C['bg_secondary']).grid(row=9, column=0, sticky='ew', pady=(0, 8))
        
        ctk.CTkLabel(
            sidebar,
            text='界面配色模式',
            anchor='w',
            text_color=C['text_dim'],
            font=ctk.CTkFont(size=11, family=FONT)
        ).grid(row=10, column=0, padx=16, pady=(6, 2), sticky='w')
        
        self.appearance_option = ctk.CTkOptionMenu(
            sidebar,
            values=['Dark', 'Light'],
            command=self._set_appearance_mode,
            fg_color=C['bg_surface'],
            button_color=C['accent'],
            button_hover_color=C['accent_hover'],
            font=ctk.CTkFont(family=FONT)
        )
        self.appearance_option.grid(row=11, column=0, padx=16, pady=(0, 8), sticky='ew')
        appearance = self.settings.get('appearance', 'Dark')
        self.appearance_option.set(appearance)
        ctk.set_appearance_mode(appearance)
        
        ctk.CTkLabel(
            sidebar,
            text='v2.1  ·  GIF Studio Pro',
            text_color=C['text_dim'],
            font=ctk.CTkFont(size=10, family=FONT)
        ).grid(row=12, column=0, padx=16, pady=(0, 16))

    def _set_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)
        self.settings['appearance'] = mode
        self._save_settings()

    def _create_content_panels(self):
        """transparent"""
        self._container = ctk.CTkFrame(self, fg_color='transparent')
        self._container.grid(row=0, column=1, sticky='nsew', padx=18, pady=18)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)
        self.frames = {
            'VideoToGif': VideoToGifTab(self._container, self),
            'ImagesToGif': ImagesToGifTab(self._container, self),
            'GifOptimize': GifOptimizeTab(self._container, self),
            'AudioExtract': AudioVideoStudioTab(self._container, self),
            'GifDeco': GifDecoTab(self._container, self),
            'YtDownloader': YtDownloaderTab(self._container, self),
            'Workspace': WorkspaceTab(self._container, self)
        }
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky='nsew')

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # closure vars: ['__classdict__']
        # constants used: ['2', "'name'"]
        pass  # TODO: reconstruct body from bytecode

    def select_tab(self, name):
        """accent"""
        if name not in self.frames:
            name = 'VideoToGif'
        self.settings['last_tab'] = name
        for tab_key, btn in self.nav_buttons.items():
            active = (tab_key == name)
            btn.configure(
                fg_color=C['accent'] if active else 'transparent',
                text_color='white' if active else C['text_primary']
            )
        for key, frame in self.frames.items():
            if key == name:
                frame.grid()
                frame.on_show()
            else:
                if frame.winfo_viewable() and hasattr(frame, 'on_hide'):
                    frame.on_hide()
                frame.grid_remove()


def __annotate__(format):
    # --- Auto-reconstructed from bytecode ---
    # constants used: ['2', "'text'", "'row'"]
    pass  # TODO: reconstruct body from bytecode


def _section_title(parent, text, row):
    ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=13, weight='bold', family=FONT),
        text_color=C['accent_light']
    ).grid(row=row, column=0, columnspan=3, padx=14, pady=(12, 6), sticky='w')


class VideoToGifTab(BaseTab):
    """VideoToGifTab"""

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=3)
        self.video_loaded = False
        self.current_video_path = ''
        self._current_frame_pil = None
        self._canvas_img_tk = None
        self._crop_rect = None
        self._sel_start = None
        self._sel_rect_id = None
        self._zoom_level = 1.0
        self._is_zoom_auto = True
        self._canvas_w = 1
        self._canvas_h = 1
        self._img_display_offset = (0, 0)
        self._scrub_pending = False
        self._next_scrub_time = None
        self._is_playing = False
        self._play_after_id = None
        self._play_started_at = 0.0
        self._play_started_position = 0.0
        self._build_left_panel()
        self._build_right_panel()
        self._build_bottom_bar(
            compile_text='🚀 运行转换 —— 生成高质量 GIF',
            save_text='💾 导出另存为...',
            compile_cmd=self._start_conversion,
            save_cmd=lambda: self._safe_save_gif(self.app.temp_gif_path, '导出 GIF')
        )
        self.app.bind('<Left>', self._on_key_left)
        self.app.bind('<Right>', self._on_key_right)
        self.app.bind('<space>', self._on_key_space)

    def _build_left_panel(self):
        self.left_frame = ctk.CTkFrame(self, fg_color=C['bg_surface'], corner_radius=12)
        self.left_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky='nsew')
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        hdr = ctk.CTkFrame(self.left_frame, fg_color='transparent')
        hdr.grid(row=0, column=0, padx=14, pady=(14, 6), sticky='ew')
        hdr.grid_columnconfigure(3, weight=1)
        ctk.CTkButton(hdr, text='📂 导入视频', fg_color=C['accent'], hover_color=C['accent_hover'], font=ctk.CTkFont(family=FONT, weight='bold'), command=self._import_video, width=120, height=34).grid(row=0, column=0, padx=(0, 8))
        ctk.CTkButton(hdr, text='📚 批量转换', fg_color=C['cyan_hover'], hover_color=C['cyan'], font=ctk.CTkFont(family=FONT, weight='bold'), command=self._start_batch_conversion, width=105, height=34).grid(row=0, column=1, padx=(0, 8))
        zoom_frame = ctk.CTkFrame(hdr, fg_color='transparent')
        zoom_frame.grid(row=0, column=2)
        ctk.CTkButton(zoom_frame, text='➕', width=34, height=34, fg_color=C['bg_card'], hover_color=C['bg_hover'], command=self._zoom_in).grid(row=0, column=0, padx=2)
        ctk.CTkButton(zoom_frame, text='自适应', width=54, height=34, fg_color=C['bg_card'], hover_color=C['bg_hover'], command=self._zoom_reset, font=ctk.CTkFont(size=11, family=FONT)).grid(row=0, column=1, padx=2)
        ctk.CTkButton(zoom_frame, text='➖', width=34, height=34, fg_color=C['bg_card'], hover_color=C['bg_hover'], command=self._zoom_out).grid(row=0, column=2, padx=2)
        self.lbl_zoom = ctk.CTkLabel(zoom_frame, text='100%', text_color=C['text_muted'], font=ctk.CTkFont(size=11))
        self.lbl_zoom.grid(row=0, column=3, padx=(6, 0))
        self.lbl_filename = ctk.CTkLabel(hdr, text='未载入视频', text_color=C['text_dim'], anchor='w', font=ctk.CTkFont(size=11, family=FONT))
        self.lbl_filename.grid(row=0, column=3, padx=12, sticky='ew')
        canvas_container = ctk.CTkFrame(self.left_frame, fg_color=C['bg_primary'], corner_radius=8)
        canvas_container.grid(row=1, column=0, padx=14, pady=6, sticky='nsew')
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)
        self._canvas = tk.Canvas(canvas_container, bg='#0A0F1E', highlightthickness=0, cursor='crosshair')
        self._canvas.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)
        self._canvas.bind('<ButtonPress-1>', self._on_mouse_down)
        self._canvas.bind('<B1-Motion>', self._on_mouse_drag)
        self._canvas.bind('<ButtonRelease-1>', self._on_mouse_up)
        self._canvas.bind('<Motion>', self._on_mouse_move)
        self._canvas.bind('<Configure>', self._on_canvas_resize)
        self._canvas_placeholder_id = self._canvas.create_text(300, 200, text='🎞️  导入视频后在此预览\n\n拖拽选框以裁剪区域 · 滚轮或按钮缩放', fill='#334155', font=('Microsoft YaHei', 13), justify='center')
        crop_bar = ctk.CTkFrame(self.left_frame, fg_color='transparent')
        crop_bar.grid(row=2, column=0, padx=14, pady=(4, 6), sticky='ew')
        crop_bar.grid_columnconfigure(1, weight=1)
        self.lbl_crop_info = ctk.CTkLabel(crop_bar, text='📐 未选取区域 — 将转换整帧', text_color=C['amber'], font=ctk.CTkFont(size=11, family=FONT), anchor='w')
        self.lbl_crop_info.grid(row=0, column=0, sticky='w')
        ctk.CTkButton(crop_bar, text='✕ 清除选框', width=90, height=28, fg_color=C['bg_hover'], hover_color=C['danger_muted'], font=ctk.CTkFont(size=11, family=FONT), command=self._clear_crop).grid(row=0, column=2, sticky='e')
        timeline = ctk.CTkFrame(self.left_frame, fg_color='transparent')
        timeline.grid(row=3, column=0, padx=14, pady=(0, 12), sticky='ew')
        timeline.grid_columnconfigure(0, weight=0)
        timeline.grid_columnconfigure(1, weight=1)
        timeline.grid_columnconfigure(2, weight=0)
        self.slider_scrub = ctk.CTkSlider(timeline, from_=0, to=100, number_of_steps=1000, command=self._on_scrub, state='disabled', button_color=C['accent'], progress_color=C['accent'])
        self.slider_scrub.set(0)
        self.slider_scrub.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 4))
        self.lbl_scrub_time = ctk.CTkLabel(timeline, text='0.00s / 0.00s', text_color=C['text_muted'], font=ctk.CTkFont(size=11))
        self.lbl_scrub_time.grid(row=1, column=0, sticky='w')
        step_grp = ctk.CTkFrame(timeline, fg_color='transparent')
        step_grp.grid(row=1, column=1, padx=10)
        self.btn_play = ctk.CTkButton(step_grp, text='▶ 播放', width=72, height=26, fg_color=C['accent'], hover_color=C['accent_hover'], text_color='white', font=ctk.CTkFont(family=FONT, size=11, weight='bold'), command=self._toggle_playback, state='disabled')
        self.btn_play.grid(row=0, column=0, padx=(2, 6))
        self.btn_prev_frame = ctk.CTkButton(step_grp, text='◀ 上一帧', width=65, height=26, fg_color='transparent', border_width=1, border_color=C['accent_light'], text_color=C['accent_light'], hover_color=C['bg_hover'], font=ctk.CTkFont(family=FONT, size=11), command=lambda: self._step_frame(-1), state='disabled')
        self.btn_prev_frame.grid(row=0, column=1, padx=2)
        self.entry_frame_step = ctk.CTkEntry(step_grp, width=45, height=26, font=ctk.CTkFont(family=FONT, size=11), justify='center', border_color=C['border'], fg_color=C['bg_primary'])
        self.entry_frame_step.insert(0, '1')
        self.entry_frame_step.grid(row=0, column=2, padx=2)
        self.lbl_frame_unit = ctk.CTkLabel(step_grp, text='帧', font=ctk.CTkFont(family=FONT, size=11), text_color=C['text_muted'])
        self.lbl_frame_unit.grid(row=0, column=3, padx=(0, 4))
        self.btn_next_frame = ctk.CTkButton(step_grp, text='下一帧 ▶', width=65, height=26, fg_color='transparent', border_width=1, border_color=C['accent_light'], text_color=C['accent_light'], hover_color=C['bg_hover'], font=ctk.CTkFont(family=FONT, size=11), command=lambda: self._step_frame(1), state='disabled')
        self.btn_next_frame.grid(row=0, column=4, padx=2)
        btn_grp = ctk.CTkFrame(timeline, fg_color='transparent')
        btn_grp.grid(row=1, column=2, sticky='e')
        self.btn_set_start = ctk.CTkButton(btn_grp, text='[ 📌 起点 ]', width=80, height=26, fg_color='transparent', border_width=1, border_color=C['cyan'], text_color=C['cyan'], hover_color=C['bg_hover'], command=self._set_trim_start, state='disabled')
        self.btn_set_start.grid(row=0, column=0, padx=4)
        self.btn_set_end = ctk.CTkButton(btn_grp, text='[ 📌 终点 ]', width=80, height=26, fg_color='transparent', border_width=1, border_color=C['cyan'], text_color=C['cyan'], hover_color=C['bg_hover'], command=self._set_trim_end, state='disabled')
        self.btn_set_end.grid(row=0, column=1, padx=4)
        self.btn_export_frame = ctk.CTkButton(btn_grp, text='📸 导出帧', width=80, height=26, fg_color='transparent', border_width=1, border_color=C['cyan'], text_color=C['cyan'], hover_color=C['bg_hover'], command=self._export_current_frame, state='disabled')
        self.btn_export_frame.grid(row=0, column=2, padx=4)

    def on_hide(self):
        self._stop_playback()

    def _build_right_panel(self):
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color=C['bg_surface'], corner_radius=12, label_text='⚙️ GIF 核心参数', label_font=ctk.CTkFont(size=13, weight='bold', family=FONT))
        self.right_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky='nsew')
        self.right_frame.grid_columnconfigure(0, weight=1)
        sec0 = ctk.CTkFrame(self.right_frame, fg_color=C['bg_card'], corner_radius=10)
        sec0.grid(row=0, column=0, padx=6, pady=8, sticky='ew')
        sec0.grid_columnconfigure((0, 1), weight=1)
        _section_title(sec0, '🚀 智能画质一键预设', 0)
        presets = [
            ('💬 微信表情包 (体极轻)', 10, 0.35, '32 (极压)', True, True, 'Normal', '体积小于 1MB，超小分辨率与极低色彩，适合微信/QQ直接发送。'),
            ('🎬 高清大图 (高清细节)', 20, 0.8, '256 (超清)', True, True, 'Normal', '极致清晰度，保留丰富视频色彩与高帧率，体积较大，适合网页/博客展示。'),
            ('⚡ 极速预览 (低配置首选)', 5, 0.5, '128 (标准)', False, True, 'Normal', '快速渲染，关闭像素抖动以节省 CPU 算力，适合初步效果预览。'),
            ('🔄 鬼畜往复 (Ping-Pong)', 12, 0.5, '256 (超清)', True, True, 'Ping-Pong', '自动实现正序+倒序往复播放，非常适合制作趣味鬼畜或表情包。'),
            ('📱 手机配图 (中等平衡)', 15, 0.6, '128 (标准)', True, True, 'Normal', '平衡画质与体积，适合移动端网页、自媒体配图，加载迅速且观感极佳。'),
            ('🎮 游戏高帧 (丝滑顺畅)', 24, 0.7, '256 (超清)', True, True, 'Normal', '24 FPS 极流畅度，适合展示动作细节、游戏高光瞬间等镜头。')
        ]
        for idx, (name, fps, scale, colors, dither, global_p, loop_style, desc) in enumerate(presets):
            r = 1 + idx // 2
            c = idx % 2
            btn = ctk.CTkButton(
                sec0,
                text=name,
                height=32,
                fg_color=C['bg_hover'],
                hover_color=C['accent_hover'],
                text_color=C['text_primary'],
                font=ctk.CTkFont(family=FONT, size=11, weight='bold'),
                command=lambda f=fps, s=scale, col=colors, d=dither, gp=global_p, ls=loop_style, name_lbl=name, dsc=desc: self._apply_preset(f, s, col, d, gp, ls, name_lbl, dsc)
            )
            btn.grid(row=r, column=c, padx=6, pady=6, sticky='ew')
        self.preset_desc_frame = ctk.CTkFrame(sec0, fg_color=C['bg_primary'], corner_radius=8, border_width=1, border_color=C['border'])
        self.preset_desc_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=(10, 10), sticky='ew')
        self.preset_desc_frame.grid_columnconfigure(0, weight=1)
        self.lbl_preset_desc_title = ctk.CTkLabel(
            self.preset_desc_frame,
            text='💡 预设说明 → 微信表情包 (体极轻)',
            font=ctk.CTkFont(family=FONT, size=11, weight='bold'),
            text_color=C['cyan']
        )
        self.lbl_preset_desc_title.grid(row=0, column=0, padx=12, pady=(8, 2), sticky='w')
        self.lbl_preset_desc_body = ctk.CTkLabel(
            self.preset_desc_frame,
            text='体积小于 1MB，超小分辨率与极低色彩，适合微信/QQ聊天直接发送。\n• 帧率: 10 fps  |  分辨率缩放: 35%  |  循环样式: 标准正放\n• 颜色深度: 32 (极压)  |  Floyd-Steinberg 抖动: 已启用',
            font=ctk.CTkFont(family=FONT, size=10),
            text_color=C['text_muted'],
            justify='left',
            anchor='w'
        )
        self.lbl_preset_desc_body.grid(row=1, column=0, padx=12, pady=(0, 8), sticky='w')
        sec1 = ctk.CTkFrame(self.right_frame, fg_color=C['bg_card'], corner_radius=10)
        sec1.grid(row=1, column=0, padx=6, pady=8, sticky='ew')
        sec1.grid_columnconfigure(1, weight=1)
        _section_title(sec1, '📹 基础参数', 0)
        ctk.CTkLabel(sec1, text='帧率 (FPS):', anchor='w').grid(row=1, column=0, padx=14, pady=5, sticky='w')
        self.val_fps = ctk.CTkSlider(sec1, from_=1, to=30, number_of_steps=29, command=self._update_basic_lbls, button_color=C['accent'], progress_color=C['accent'])
        self.val_fps.set(12)
        self.val_fps.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        self.lbl_fps = ctk.CTkLabel(sec1, text='12 fps', text_color=C['text_muted'], width=60, anchor='e')
        self.lbl_fps.grid(row=1, column=2, padx=(0, 14), pady=5)
        ctk.CTkLabel(sec1, text='分辨率缩放:', anchor='w').grid(row=2, column=0, padx=14, pady=5, sticky='w')
        self.val_scale = ctk.CTkSlider(sec1, from_=0.1, to=1.0, number_of_steps=18, command=self._update_basic_lbls, button_color=C['accent'], progress_color=C['accent'])
        self.val_scale.set(0.5)
        self.val_scale.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        self.lbl_scale = ctk.CTkLabel(sec1, text='50%', text_color=C['text_muted'], width=60, anchor='e')
        self.lbl_scale.grid(row=2, column=2, padx=(0, 14), pady=5)
        ctk.CTkLabel(sec1, text='速度倍率:', anchor='w').grid(row=3, column=0, padx=14, pady=5, sticky='w')
        self.val_speed = ctk.CTkSlider(sec1, from_=0.25, to=4.0, number_of_steps=15, command=self._update_basic_lbls, button_color=C['accent'], progress_color=C['accent'])
        self.val_speed.set(1.0)
        self.val_speed.grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        self.lbl_speed = ctk.CTkLabel(sec1, text='1.0×', text_color=C['text_muted'], width=60, anchor='e')
        self.lbl_speed.grid(row=3, column=2, padx=(0, 14), pady=5)
        ctk.CTkLabel(sec1, text='循环样式:', anchor='w').grid(row=4, column=0, padx=14, pady=5, sticky='w')
        self.val_loop = ctk.CTkOptionMenu(sec1, values=['Normal', 'Reverse', 'Ping-Pong'], fg_color=C['bg_surface'], button_color=C['accent'], command=lambda _: self._update_export_estimate())
        self.val_loop.set('Normal')
        self.val_loop.grid(row=4, column=1, columnspan=2, padx=14, pady=8, sticky='ew')
        self.lbl_export_estimate = ctk.CTkLabel(
            sec1,
            text='📊 导入视频后显示导出预估',
            text_color=C['cyan'],
            fg_color=C['bg_primary'],
            corner_radius=7,
            justify='left',
            anchor='w',
            font=ctk.CTkFont(family=FONT, size=10)
        )
        self.lbl_export_estimate.grid(row=5, column=0, columnspan=3, padx=12, pady=(4, 12), sticky='ew')
        sec2 = ctk.CTkFrame(self.right_frame, fg_color=C['bg_card'], corner_radius=10)
        sec2.grid(row=2, column=0, padx=6, pady=8, sticky='ew')
        sec2.grid_columnconfigure((1, 3), weight=1)
        _section_title(sec2, '✂️ 剪辑范围 (秒)', 0)
        ctk.CTkLabel(sec2, text='起点:', anchor='w').grid(row=1, column=0, padx=14, pady=6, sticky='w')
        self.entry_start = ctk.CTkEntry(sec2, placeholder_text='0.00')
        self.entry_start.insert(0, '0.00')
        self.entry_start.grid(row=1, column=1, padx=(0, 6), pady=6, sticky='ew')
        self.entry_start.bind('<KeyRelease>', lambda _: self._update_export_estimate())
        ctk.CTkLabel(sec2, text='终点:', anchor='w').grid(row=1, column=2, padx=6, pady=6, sticky='w')
        self.entry_end = ctk.CTkEntry(sec2, placeholder_text='0.00')
        self.entry_end.insert(0, '0.00')
        self.entry_end.grid(row=1, column=3, padx=(0, 14), pady=6, sticky='ew')
        self.entry_end.bind('<KeyRelease>', lambda _: self._update_export_estimate())
        sec3 = ctk.CTkFrame(self.right_frame, fg_color=C['bg_card'], corner_radius=10)
        sec3.grid(row=3, column=0, padx=6, pady=8, sticky='ew')
        sec3.grid_columnconfigure(1, weight=1)
        _section_title(sec3, '🎨 滤镜与水印', 0)
        ctk.CTkLabel(sec3, text='滤镜:', anchor='w').grid(row=1, column=0, padx=14, pady=5, sticky='w')
        self.val_filter = ctk.CTkOptionMenu(sec3, values=['None', 'Grayscale', 'Sepia', 'Invert', 'Vintage', 'High Contrast'], fg_color=C['bg_surface'], button_color=C['accent'])
        self.val_filter.set('None')
        self.val_filter.grid(row=1, column=1, padx=14, pady=5, sticky='ew')
        ctk.CTkLabel(sec3, text='水印文字:', anchor='w').grid(row=2, column=0, padx=14, pady=5, sticky='w')
        self.entry_overlay = ctk.CTkEntry(sec3, placeholder_text='输入字幕或 meme 文字...')
        self.entry_overlay.grid(row=2, column=1, padx=14, pady=5, sticky='ew')
        ctk.CTkLabel(sec3, text='水印位置:', anchor='w').grid(row=3, column=0, padx=14, pady=5, sticky='w')
        self.val_text_pos = ctk.CTkOptionMenu(sec3, values=['Bottom', 'Top', 'Center'], fg_color=C['bg_surface'], button_color=C['accent'])
        self.val_text_pos.set('Bottom')
        self.val_text_pos.grid(row=3, column=1, padx=14, pady=5, sticky='ew')
        ctk.CTkLabel(sec3, text='文字颜色:', anchor='w').grid(row=4, column=0, padx=14, pady=5, sticky='w')
        self._text_color = '#FFFFFF'
        self.btn_color = ctk.CTkButton(sec3, text='⬜ 白色', fg_color=C['bg_hover'], hover_color=C['bg_card'], command=self._choose_color)
        self.btn_color.grid(row=4, column=1, padx=14, pady=5, sticky='ew')
        ctk.CTkLabel(sec3, text='文字大小:', anchor='w').grid(row=5, column=0, padx=14, pady=5, sticky='w')
        self.val_text_size = ctk.CTkSlider(sec3, from_=10, to=80, number_of_steps=70, button_color=C['accent'], progress_color=C['accent'])
        self.val_text_size.set(24)
        self.val_text_size.grid(row=5, column=1, padx=14, pady=(5, 10), sticky='ew')
        sec4 = ctk.CTkFrame(self.right_frame, fg_color=C['bg_card'], corner_radius=10)
        sec4.grid(row=4, column=0, padx=6, pady=8, sticky='ew')
        sec4.grid_columnconfigure(1, weight=1)
        _section_title(sec4, '🛡️ 高保真编码', 0)
        ctk.CTkLabel(sec4, text='颜色深度:', anchor='w').grid(row=1, column=0, padx=14, pady=5, sticky='w')
        self.val_colors = ctk.CTkOptionMenu(sec4, values=['256 (超清)', '128 (标准)', '64 (中等)', '32 (极压)'], fg_color=C['bg_surface'], button_color=C['accent'], command=lambda _: self._update_export_estimate())
        self.val_colors.set('256 (超清)')
        self.val_colors.grid(row=1, column=1, padx=14, pady=5, sticky='ew')
        self.chk_global_palette = ctk.CTkCheckBox(sec4, text='全局最佳调色板 (防闪烁，推荐)', text_color=C['text_primary'], checkmark_color=C['accent'], fg_color=C['accent'])
        self.chk_global_palette.select()
        self.chk_global_palette.grid(row=2, column=0, columnspan=2, padx=14, pady=6, sticky='w')
        self.chk_dither = ctk.CTkCheckBox(sec4, text='Floyd-Steinberg 抖动 (渐变更平滑)', text_color=C['text_primary'], checkmark_color=C['accent'], fg_color=C['accent'])
        self.chk_dither.select()
        self.chk_dither.grid(row=3, column=0, columnspan=2, padx=14, pady=(0, 14), sticky='w')

    def _zoom_in(self):
        self._is_zoom_auto = False
        self._zoom_level = min(4.0, self._zoom_level * 1.25)
        self._redraw_canvas()

    def _zoom_out(self):
        self._is_zoom_auto = False
        self._zoom_level = max(0.2, self._zoom_level / 1.25)
        self._redraw_canvas()

    def _zoom_reset(self):
        """Resets to auto-fit zoom mode and recalculates scale factor."""
        self._is_zoom_auto = True
        if self._current_frame_pil:
            pw, ph = self._current_frame_pil.size
            fit_z = min(self._canvas_w / pw, self._canvas_h / ph)
            self._zoom_level = round(fit_z, 2)
        else:
            self._zoom_level = 1.0
        self._redraw_canvas()

    def _on_canvas_resize(self, event):
        self._canvas_w = event.width
        self._canvas_h = event.height
        if self._is_zoom_auto and self._current_frame_pil:
            pw, ph = self._current_frame_pil.size
            fit_z = min(self._canvas_w / pw, self._canvas_h / ph)
            self._zoom_level = round(fit_z, 2)
        self._redraw_canvas()

    def _redraw_canvas(self):
        if self._current_frame_pil is None:
            return
        self.lbl_zoom.configure(text=f"{int(self._zoom_level * 100)}%")
        pw, ph = self._current_frame_pil.size
        dw = int(pw * self._zoom_level)
        dh = int(ph * self._zoom_level)
        cw = max(1, self._canvas_w)
        ch = max(1, self._canvas_h)
        ox = max(0, (cw - dw) // 2)
        oy = max(0, (ch - dh) // 2)
        self._img_display_offset = (ox, oy)
        self._img_display_size = (dw, dh)
        resized = self._current_frame_pil.resize((dw, dh), Image.Resampling.LANCZOS)
        self._canvas_img_tk = ImageTk.PhotoImage(resized)
        self._canvas.delete('frame_img')
        self._canvas.delete('placeholder')
        self._canvas.create_image(ox, oy, anchor='nw', image=self._canvas_img_tk, tags='frame_img')
        if self._sel_rect_id:
            self._canvas.delete(self._sel_rect_id)
            self._sel_rect_id = None
        if self._crop_rect:
            self._draw_crop_overlay()

    def _draw_crop_overlay(self):
        """Draws the crop selection rectangle and dim overlay on canvas."""
        if not self._crop_rect:
            return
        cx, cy, cw, ch = self._crop_rect
        ox, oy = self._img_display_offset
        z = self._zoom_level
        x1 = ox + int(cx * z)
        y1 = oy + int(cy * z)
        x2 = ox + int((cx + cw) * z)
        y2 = oy + int((cy + ch) * z)
        self._canvas.delete('crop_overlay')
        self._canvas.create_rectangle(x1, y1, x2, y2, outline='#F59E0B', width=2, dash=(6, 3), tags='crop_overlay')
        sz = 6
        for px, py in ((x1, y1), (x2, y1), (x1, y2), (x2, y2)):
            self._canvas.create_rectangle(px - sz, py - sz, px + sz, py + sz, fill='#F59E0B', outline='#FFFFFF', width=1, tags='crop_overlay')
        self._canvas.create_text(
            (x1 + x2) // 2,
            y1 - 12,
            text=f"  {cw} × {ch} px  ",
            fill='#F59E0B',
            font=('Consolas', 10),
            tags='crop_overlay'
        )

    def _canvas_to_video_coords(self, cx, cy):
        """Converts canvas pixel coords to video pixel coords."""
        ox, oy = self._img_display_offset
        z = self._zoom_level
        vx = (cx - ox) / z
        vy = (cy - oy) / z
        if self._current_frame_pil:
            pw, ph = self._current_frame_pil.size
            vx = max(0, min(vx, pw))
            vy = max(0, min(vy, ph))
        return (vx, vy)

    def _on_mouse_down(self, event):
        if not self.video_loaded:
            return
        self._sel_start = (event.x, event.y)
        self._canvas.delete('crop_overlay')
        self._crop_rect = None
        self.lbl_crop_info.configure(text='📐 正在选取区域...', text_color=C['amber'])

    def _on_mouse_drag(self, event):
        if not self._sel_start or not self.video_loaded:
            return
        self._canvas.delete('crop_overlay')
        x0, y0 = self._sel_start
        x1, y1 = event.x, event.y
        self._canvas.create_rectangle(x0, y0, x1, y1, outline='#F59E0B', width=2, dash=(6, 3), tags='crop_overlay')

    def _on_mouse_up(self, event):
        if not self._sel_start or not self.video_loaded:
            return
        x0, y0 = self._sel_start
        x1, y1 = event.x, event.y
        self._sel_start = None
        if abs(x1 - x0) < 8 or abs(y1 - y0) < 8:
            self._clear_crop()
            return
        vx0, vy0 = self._canvas_to_video_coords(min(x0, x1), min(y0, y1))
        vx1, vy1 = self._canvas_to_video_coords(max(x0, x1), max(y0, y1))
        vw = int(vx1 - vx0)
        vh = int(vy1 - vy0)
        if vw > 10 and vh > 10:
            self._crop_rect = (int(vx0), int(vy0), vw, vh)
            self.lbl_crop_info.configure(
                text=f"✅ 裁剪区域  ({int(vx0)}, {int(vy0)})  →  {vw} × {vh} px",
                text_color=C['success']
            )
            self._draw_crop_overlay()
            self._update_export_estimate()
        else:
            self._clear_crop()

    def _on_mouse_move(self, event):
        """Shows magnifier tooltip while hovering over video."""
        if not self.video_loaded or self._current_frame_pil is None:
            return
        vx, vy = self._canvas_to_video_coords(event.x, event.y)
        if self._current_frame_pil:
            pw, ph = self._current_frame_pil.size
            if 0 <= vx <= pw:
                if 0 <= vy <= ph:
                    self._canvas.delete('coord_tip')
                    self._canvas.create_text(
                        event.x + 12,
                        event.y - 12,
                        text=f"({int(vx)}, {int(vy)})",
                        fill='#94A3B8',
                        font=('Consolas', 9),
                        anchor='w',
                        tags='coord_tip'
                    )

    def _clear_crop(self):
        self._crop_rect = None
        self._canvas.delete('crop_overlay')
        self.lbl_crop_info.configure(text='📐 未选取区域 — 将转换整帧', text_color=C['amber'])
        self._update_export_estimate()

    def _import_video(self):
        """选择视频文件"""
        self._stop_playback()
        path = filedialog.askopenfilename(
            title='选择视频文件',
            filetypes=[('视频文件', '*.mp4 *.avi *.mkv *.mov *.webm *.gif'), ('全部文件', '*.*')]
        )
        if not path:
            return
        self.lbl_status.configure(text='正在读取视频元数据...', text_color=C['text_muted'])
        self.progress_bar.set(0.1)
        self.update_idletasks()
        try:
            meta = self.app.video_processor.load_video(path)
            self.app.record_recent_file(path, 'video')
            self.current_video_path = path
            self.video_loaded = True
            self.lbl_filename.configure(
                text=f"{meta['filename']} | {meta['width']}×{meta['height']} | {meta['duration']:.1f}s",
                text_color=C['success']
            )
            self.slider_scrub.configure(state='normal', from_=0, to=meta['duration'])
            self.slider_scrub.set(0)
            self.btn_set_start.configure(state='normal')
            self.btn_set_end.configure(state='normal')
            self.btn_prev_frame.configure(state='normal')
            self.btn_next_frame.configure(state='normal')
            self.btn_play.configure(state='normal')
            self.btn_export_frame.configure(state='normal')
            self.btn_compile.configure(state='normal')
            self.entry_start.delete(0, tk.END)
            self.entry_start.insert(0, '0.00')
            self.entry_end.delete(0, tk.END)
            self.entry_end.insert(0, f"{meta['duration']:.2f}")
            self._is_zoom_auto = True
            self._clear_crop()
            self._load_frame_to_canvas(0.0)
            self.lbl_status.configure(
                text='视频载入成功 ✓  空格播放/暂停 · 左右方向键逐帧 · 拖拽画面选取裁剪区域',
                text_color=C['success']
            )
            self.progress_bar.set(0)
            self._update_export_estimate()
        except Exception as e:
            self.lbl_status.configure(text=f"载入失败: {e}", text_color=C['danger'])
            self.progress_bar.set(0)
            messagebox.showerror('载入失败', str(e))

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # closure vars: ['__classdict__']
        # constants used: ['2', "'seconds'"]
        pass  # TODO: reconstruct body from bytecode

    def _load_frame_to_canvas(self, seconds):
        """Fetches frame from video and draws it on the canvas at current zoom."""
        try:
            img = self.app.video_processor.get_frame_at_time(seconds)
            if img is None:
                return
            self._current_frame_pil = img
            self.update_idletasks()
            self._canvas_w = self._canvas.winfo_width()
            self._canvas_h = self._canvas.winfo_height()
            if self._canvas_w < 5:
                self._canvas_w = 560
                self._canvas_h = 380
            if self._is_zoom_auto:
                pw, ph = img.size
                fit_z = min(self._canvas_w / pw, self._canvas_h / ph)
                self._zoom_level = round(fit_z, 2)
            self._redraw_canvas()
            dur = self.app.video_processor.metadata.get('duration', 0)
            self.lbl_scrub_time.configure(text=f"{seconds:.2f}s / {dur:.2f}s")
        except Exception as e:
            print(f"Canvas frame error: {e}")

    def _on_scrub(self, value):
        """Ultra-smooth lag-free timeline scrub queue. Limits decoding frequency to at most 25 FPS."""
        if self._is_playing:
            self._stop_playback()
        self._next_scrub_time = float(value)
        if not self._scrub_pending:
            self._scrub_pending = True
            self.after(40, self._process_pending_scrub)

    def _process_pending_scrub(self):
        """Processes the most recent scrub seek request and clears the queue."""
        if self._next_scrub_time is not None:
            t = self._next_scrub_time
            self._next_scrub_time = None
            self._load_frame_to_canvas(t)
        self._scrub_pending = False

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # closure vars: ['__classdict__']
        # constants used: ['2', "'direction'"]
        pass  # TODO: reconstruct body from bytecode

    def _step_frame(self, direction):
        """
        Steps backward or forward by the specified number of frames.
        direction: -1 for backward, 1 for forward
        """
        if not self.video_loaded or not self.app.video_processor:
            return
        self._stop_playback()
        fps = self.app.video_processor.metadata.get('fps', 24.0)
        duration = self.app.video_processor.metadata.get('duration', 0.0)
        total_frames = self.app.video_processor.metadata.get('total_frames', 0)
        if fps <= 0 or duration <= 0 or total_frames <= 0:
            return
        step_val_str = self.entry_frame_step.get().strip()
        try:
            step_val = int(step_val_str)
            if step_val <= 0:
                step_val = 1
        except ValueError:
            step_val = 1
        current_time = self.slider_scrub.get()
        current_frame_idx = round(current_time * fps)
        target_frame_idx = current_frame_idx + direction * step_val
        target_frame_idx = max(0, min(target_frame_idx, total_frames - 1))
        target_time = target_frame_idx / fps
        target_time = max(0.0, min(target_time, duration))
        self.slider_scrub.set(target_time)
        self._load_frame_to_canvas(target_time)

    def _toggle_playback(self):
        if not self.video_loaded:
            return
        if self._is_playing:
            self._stop_playback()
            return
        duration = self.app.video_processor.metadata.get('duration', 0.0)
        if duration <= 0:
            return
        if self.slider_scrub.get() >= duration:
            self.slider_scrub.set(0)
            self._load_frame_to_canvas(0.0)
        self._is_playing = True
        self._play_started_at = time.monotonic()
        self._play_started_position = self.slider_scrub.get()
        self.btn_play.configure(text='⏸ 暂停', fg_color=C['danger'], hover_color=C['danger_hover'])
        self._schedule_next_frame()

    def _schedule_next_frame(self):
        if not self._is_playing:
            return
        fps = self.app.video_processor.metadata.get('fps', 24.0)
        frame_delay = max(15, round(1000 / max(1.0, fps)))
        self._play_after_id = self.after(frame_delay, self._play_next_frame)

    def _play_next_frame(self):
        self._play_after_id = None
        if not self._is_playing or not self.winfo_viewable():
            self._stop_playback()
            return
        metadata = self.app.video_processor.metadata
        duration = metadata.get('duration', 0.0)
        elapsed = time.monotonic() - self._play_started_at
        next_time = (self._play_started_position + elapsed) % duration
        self.slider_scrub.set(next_time)
        self._load_frame_to_canvas(next_time)
        self._schedule_next_frame()

    def _stop_playback(self):
        self._is_playing = False
        if self._play_after_id is not None:
            try:
                self.after_cancel(self._play_after_id)
            except (tk.TclError, ValueError):
                pass
            self._play_after_id = None
        if hasattr(self, 'btn_play'):
            self.btn_play.configure(text='▶ 播放', fg_color=C['accent'], hover_color=C['accent_hover'])

    def _on_key_left(self, event):
        if not self.video_loaded or not self.winfo_viewable():
            return
        focused = self.focus_get()
        if focused:
            cls_name = str(focused).lower()
            if 'entry' in cls_name or 'text' in cls_name:
                return
        self._step_frame(-1)

    def _on_key_right(self, event):
        if not self.video_loaded or not self.winfo_viewable():
            return
        focused = self.focus_get()
        if focused:
            cls_name = str(focused).lower()
            if 'entry' in cls_name or 'text' in cls_name:
                return
        self._step_frame(1)

    def _on_key_space(self, event):
        if not self.video_loaded or not self.winfo_viewable():
            return
        focused = self.focus_get()
        if focused:
            cls_name = str(focused).lower()
            if 'entry' in cls_name or 'text' in cls_name:
                return
        self._toggle_playback()
        return 'break'

    def _set_trim_start(self):
        val = self.slider_scrub.get()
        self.entry_start.delete(0, tk.END)
        self.entry_start.insert(0, f"{val:.2f}")
        self.lbl_status.configure(text=f"起点设为 {val:.2f}s")
        self._update_export_estimate()

    def _set_trim_end(self):
        val = self.slider_scrub.get()
        self.entry_end.delete(0, tk.END)
        self.entry_end.insert(0, f"{val:.2f}")
        self.lbl_status.configure(text=f"终点设为 {val:.2f}s")
        self._update_export_estimate()

    def _export_current_frame(self):
        """Saves the current frame displayed on the canvas as an image file."""
        if not self.video_loaded or self._current_frame_pil is None:
            return
        path = filedialog.asksaveasfilename(
            title='导出当前帧为图片',
            defaultextension='.png',
            filetypes=[('PNG Image', '*.png'), ('JPEG Image', '*.jpg;*.jpeg'), ('All Files', '*.*')]
        )
        if not path:
            return
        try:
            self._current_frame_pil.save(path)
            if hasattr(self.app, 'workspace_dir') and os.path.exists(self.app.workspace_dir):
                ws_dest = os.path.join(self.app.workspace_dir, os.path.basename(path))
                self._current_frame_pil.save(ws_dest)
            self.lbl_status.configure(
                text=f"✅ 帧已成功导出 → {os.path.basename(path)}",
                text_color=C['success']
            )
            messagebox.showinfo('导出成功', f"当前帧已成功保存至：\n{path}")
        except Exception as e:
            messagebox.showerror('导出失败', f"保存帧图片时出错：\n{str(e)}")

    def _choose_color(self):
        """选择水印颜色"""
        c = colorchooser.askcolor(initialcolor=self._text_color, title='选择水印颜色')
        if c[1]:
            self._text_color = c[1]
            self.btn_color.configure(text=f"■ {c[1]}", text_color=c[1])

    def _update_basic_lbls(self, _):
        """ fps"""
        self.lbl_fps.configure(text=f"{int(self.val_fps.get())} fps")
        self.lbl_scale.configure(text=f"{int(self.val_scale.get() * 100)}%")
        spd = self.val_speed.get()
        self.lbl_speed.configure(text=f"{spd:.2f}×")
        self._update_export_estimate()

    def _update_export_estimate(self):
        if not hasattr(self, 'lbl_export_estimate') or not self.video_loaded:
            return
        metadata = self.app.video_processor.metadata
        try:
            start = max(0.0, float(self.entry_start.get()))
            end = min(float(self.entry_end.get()), metadata.get('duration', 0.0))
        except ValueError:
            self.lbl_export_estimate.configure(text='📊 请输入有效起止时间以计算导出预估')
            return
        duration = max(0.0, end - start)
        fps = max(1.0, float(self.val_fps.get()))
        speed = max(0.01, float(self.val_speed.get()))
        scale = float(self.val_scale.get())
        if self._crop_rect:
            source_width, source_height = self._crop_rect[2], self._crop_rect[3]
        else:
            source_width = metadata.get('width', 0)
            source_height = metadata.get('height', 0)
        width = max(16, int(source_width * scale))
        height = max(16, int(source_height * scale))
        width -= width % 2
        height -= height % 2
        frame_count = max(1, round(duration * fps / speed))
        if self.val_loop.get() == 'Ping-Pong' and frame_count > 1:
            frame_count = frame_count * 2 - 2
        output_duration = frame_count / fps
        colors = parse_color_depth(self.val_colors.get())
        complexity = 0.08 + (colors / 256.0) * 0.22
        estimated_mb = width * height * frame_count * complexity / 1048576
        low_mb = estimated_mb * 0.55
        high_mb = estimated_mb * 1.8
        self.lbl_export_estimate.configure(
            text=(
                f'📊 预计 {width}×{height} · {frame_count} 帧 · {output_duration:.1f}s\n'
                f'文件大小约 {low_mb:.1f}–{high_mb:.1f} MB（按画面复杂度估算）'
            )
        )

    def _apply_preset(self, fps, scale, colors, dither, global_p, loop_style, name, desc):
        """Applies the selected preset parameters to all the widgets directly."""
        self.val_fps.set(fps)
        self.val_scale.set(scale)
        self.val_loop.set(loop_style)
        self.val_colors.set(colors)
        if dither:
            self.chk_dither.select()
        else:
            self.chk_dither.deselect()
        if global_p:
            self.chk_global_palette.select()
        else:
            self.chk_global_palette.deselect()
        self._update_basic_lbls(None)
        self.lbl_preset_desc_title.configure(text=f"💡 预设说明 → {name}")
        dither_text = '已启用' if dither else '已关闭'
        if loop_style == 'Ping-Pong':
            loop_cn = '往返 (Ping-Pong)'
        elif loop_style == 'Reverse':
            loop_cn = '倒放'
        else:
            loop_cn = '标准正放'
        self.lbl_preset_desc_body.configure(text=f"{desc}\n• 帧率: {fps} fps  |  分辨率缩放: {int(scale * 100)}%  |  循环样式: {loop_cn}\n• 颜色深度: {colors}  |  Floyd-Steinberg 抖动: {dither_text}")
        self.lbl_status.configure(text=f"✨ 已应用智能预设配方 → {name}", text_color=C['success'])

    def _start_conversion(self):
        self._stop_playback()
        if not self.video_loaded:
            return
        try:
            start_t = float(self.entry_start.get())
            end_t = float(self.entry_end.get())
        except ValueError:
            messagebox.showerror('格式错误', '请输入有效数字作为起终点时间。')
            return
        if start_t >= end_t:
            messagebox.showerror('区间错误', '起点时间必须小于终点时间！')
            return
        options = {
            'fps': float(self.val_fps.get()),
            'scale': float(self.val_scale.get()),
            'speed': float(self.val_speed.get()),
            'loop': self.val_loop.get(),
            'filter': self.val_filter.get(),
            'crop': self._crop_rect,
            'text_config': {
                'text': self.entry_overlay.get(),
                'position': self.val_text_pos.get(),
                'font_size': int(self.val_text_size.get()),
                'color': self._text_color
            } if self.entry_overlay.get() else None,
            'encoder_options': {
                'colors': parse_color_depth(self.val_colors.get()),
                'dither': bool(self.chk_dither.get()),
                'global_palette': bool(self.chk_global_palette.get())
            },
            '_cancel_event': self._cancel_event
        }
        options['encoder_options']['_cancel_event'] = self._cancel_event
        self._begin_task()
        self.progress_bar.set(0)
        self.lbl_status.configure(text='初始化转换线程...', text_color=C['text_muted'])
        threading.Thread(
            target=self._thread_convert,
            args=(start_t, end_t, options),
            daemon=True
        ).start()

    def _start_batch_conversion(self):
        paths = filedialog.askopenfilenames(
            title='选择要批量转换的视频',
            filetypes=[('视频文件', '*.mp4 *.avi *.mkv *.mov *.webm'), ('全部文件', '*.*')]
        )
        if not paths:
            return
        output_dir = filedialog.askdirectory(title='选择批量 GIF 输出目录')
        if not output_dir:
            return
        options = {
            'fps': float(self.val_fps.get()),
            'scale': float(self.val_scale.get()),
            'speed': float(self.val_speed.get()),
            'loop': self.val_loop.get(),
            'filter': self.val_filter.get(),
            'crop': None,
            'text_config': {
                'text': self.entry_overlay.get(),
                'position': self.val_text_pos.get(),
                'font_size': int(self.val_text_size.get()),
                'color': self._text_color
            } if self.entry_overlay.get() else None,
            '_cancel_event': self._cancel_event,
            'encoder_options': {
                'colors': parse_color_depth(self.val_colors.get()),
                'dither': bool(self.chk_dither.get()),
                'global_palette': bool(self.chk_global_palette.get()),
                '_cancel_event': self._cancel_event
            }
        }
        self._begin_task()
        self.progress_bar.set(0)
        self.lbl_status.configure(text=f'准备批量转换 {len(paths)} 个视频...', text_color=C['text_muted'])
        threading.Thread(
            target=self._thread_batch_convert,
            args=(list(paths), output_dir, options),
            daemon=True
        ).start()

    def _thread_batch_convert(self, paths, output_dir, options):
        completed = []
        try:
            total = len(paths)
            for index, path in enumerate(paths):
                self._raise_if_cancelled()
                processor = VideoProcessor(path)
                try:
                    duration = processor.metadata.get('duration', 0.0)

                    def update_item_progress(value, text, item=index, count=total):
                        overall = (item + value) / count
                        self._update_progress(overall, f'[{item + 1}/{count}] {os.path.basename(path)} · {text}')

                    frames = processor.extract_frames_range(
                        0.0, duration, options, progress_callback=update_item_progress
                    )
                    self._raise_if_cancelled()
                    if not frames:
                        raise ValueError(f'未能从 {os.path.basename(path)} 提取视频帧')
                    output_path = self._unique_batch_output_path(output_dir, path)
                    self.app.gif_encoder.save_gif(
                        frames, output_path, fps=options['fps'],
                        options=options['encoder_options'], progress_callback=update_item_progress
                    )
                    completed.append(output_path)
                finally:
                    processor.release()
            self.after(0, lambda: self._show_batch_results(completed, output_dir))
        except Exception as error:
            self._on_thread_error(error, self.btn_compile)

    @staticmethod
    def _unique_batch_output_path(output_dir, video_path):
        stem = os.path.splitext(os.path.basename(video_path))[0]
        candidate = os.path.join(output_dir, f'{stem}.gif')
        suffix = 2
        while os.path.exists(candidate):
            candidate = os.path.join(output_dir, f'{stem}_{suffix}.gif')
            suffix += 1
        return candidate

    def _show_batch_results(self, completed, output_dir):
        self._finish_task()
        self.progress_bar.set(1.0)
        self.lbl_status.configure(
            text=f'✅ 批量转换完成：已生成 {len(completed)} 个 GIF',
            text_color=C['success']
        )
        messagebox.showinfo('批量转换完成', f'已生成 {len(completed)} 个 GIF：\n{output_dir}')

    def _thread_convert(self, start_t, end_t, options):
        try:
            frames = self.app.video_processor.extract_frames_range(
                start_t, end_t, options, progress_callback=self._update_progress
            )
            self._raise_if_cancelled()
            if not frames:
                raise ValueError('未提取到有效帧，请检查时间范围。')
            self._update_progress(0.9, '帧提取完成，开始编码 GIF...')
            result = self.app.gif_encoder.save_gif(
                frames,
                self.app.temp_gif_path,
                fps=options['fps'],
                options=options['encoder_options'],
                progress_callback=self._update_progress
            )
            self.after(0, lambda: self._show_results(result))
        except Exception as e:
            self._on_thread_error(e, self.btn_compile)

    def _show_results(self, result):
        """✅ 转换成功！"""
        self.lbl_status.configure(
            text=f"✅ 转换成功！{result['size_mb']:.2f} MB | {result['total_frames']} 帧",
            text_color=C['success']
        )
        self.progress_bar.set(1.0)
        self._finish_task()
        self.btn_save_gif.configure(state='normal')
        info = f"生成成功 ✓  大小: {result['size_mb']:.2f} MB | {result['total_frames']} 帧"
        if self._crop_rect:
            cx, cy, cw, ch = self._crop_rect
            info += f"\n裁剪区域: ({cx}, {cy}) → {cw}×{ch} px"

        def go_deco():
            win.grab_release()
            win.destroy()
            self.app.select_tab('GifDeco')
            self.app.frames['GifDeco'].load_gif_from_path(self.app.temp_gif_path)

        win = open_gif_preview_dialog(
            self,
            self.app,
            self.app.temp_gif_path,
            '🎉 转换完成！GIF 预览',
            info,
            extra_buttons=[
                ('🎨 导入装饰', C['accent'], C['accent_hover'], go_deco),
                ('💾 另存导出', C['success'], C['success_hover'], lambda: [win.grab_release(), win.destroy(), self._safe_save_gif(self.app.temp_gif_path)])
            ]
        )

    def load_video_file(self, path):
        """Public API to load a video file (used by YtDownloaderTab redirect)."""
        if not os.path.exists(path):
            return
        self._stop_playback()
        self.current_video_path = path
        try:
            meta = self.app.video_processor.load_video(path)
            self.app.record_recent_file(path, 'video')
            self.video_loaded = True
            self.lbl_filename.configure(
                text=f"{meta['filename']} | {meta['width']}×{meta['height']} | {meta['duration']:.1f}s",
                text_color=C['success']
            )
            self.slider_scrub.configure(state='normal', from_=0, to=meta['duration'])
            self.slider_scrub.set(0)
            self.btn_set_start.configure(state='normal')
            self.btn_set_end.configure(state='normal')
            self.btn_prev_frame.configure(state='normal')
            self.btn_next_frame.configure(state='normal')
            self.btn_play.configure(state='normal')
            self.btn_export_frame.configure(state='normal')
            self.btn_compile.configure(state='normal')
            self.entry_start.delete(0, tk.END)
            self.entry_start.insert(0, '0.00')
            self.entry_end.delete(0, tk.END)
            self.entry_end.insert(0, f"{meta['duration']:.2f}")
            self._is_zoom_auto = True
            self._clear_crop()
            self._load_frame_to_canvas(0.0)
        except Exception as e:
            messagebox.showerror('载入失败', str(e))


class ImagesToGifTab(BaseTab):
    """ImagesToGifTab"""

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=3)
        self._build_left_list()
        self._build_right_panel()
        self._build_bottom_bar(
            '🚀 合成幻灯片 GIF',
            '💾 导出另存为...',
            self._start_compilation,
            lambda: self._safe_save_gif(self.app.temp_gif_path, '导出合成 GIF')
        )

    def _build_left_list(self):
        frame = ctk.CTkFrame(self, fg_color=C['bg_surface'], corner_radius=12)
        frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky='nsew')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        hdr = ctk.CTkFrame(frame, fg_color='transparent')
        hdr.grid(row=0, column=0, padx=14, pady=(14, 6), sticky='ew')

        btn_import = ctk.CTkButton(
            hdr,
            text='➕ 批量导入图片',
            fg_color=C['accent'],
            hover_color=C['accent_hover'],
            command=self._import_images
        )
        btn_import.grid(row=0, column=0, padx=(0, 8))

        btn_clear = ctk.CTkButton(
            hdr,
            text='🧹 清空',
            fg_color=C['danger_muted'],
            hover_color=C['danger_hover'],
            width=80,
            command=self._clear_images
        )
        btn_clear.grid(row=0, column=1)

        self.list_box = ctk.CTkScrollableFrame(
            frame,
            fg_color=C['bg_primary'],
            corner_radius=8,
            label_text='📸 图片帧序列 (从上至下)',
            label_font=ctk.CTkFont(size=12, family=FONT)
        )
        self.list_box.grid(row=1, column=0, padx=14, pady=(0, 14), sticky='nsew')
        self.list_box.grid_columnconfigure(0, weight=1)

        self._empty_lbl = ctk.CTkLabel(
            self.list_box,
            text='列表为空\n\n导入图片开始合成',
            text_color=C['text_dim'],
            font=ctk.CTkFont(family=FONT, size=13)
        )
        self._empty_lbl.grid(row=0, column=0, padx=20, pady=40)
        self._list_items = []

    def _build_right_panel(self):
        frame = ctk.CTkScrollableFrame(
            self,
            fg_color=C['bg_surface'],
            corner_radius=12,
            label_text='⚙️ 合成参数',
            label_font=ctk.CTkFont(size=13, weight='bold', family=FONT)
        )
        frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky='nsew')
        frame.grid_columnconfigure(0, weight=1)

        # Section 1: Dimensions
        sec1 = ctk.CTkFrame(frame, fg_color=C['bg_card'], corner_radius=10)
        sec1.grid(row=0, column=0, padx=6, pady=8, sticky='ew')
        sec1.grid_columnconfigure(1, weight=1)
        _section_title(sec1, '📐 尺寸设置', 0)

        ctk.CTkLabel(sec1, text='尺寸模式:', anchor='w').grid(
            row=1, column=0, padx=14, pady=5, sticky='w'
        )

        self.val_resize_mode = ctk.CTkOptionMenu(
            sec1,
            values=['Match First', 'Original', 'Custom'],
            command=self._on_resize_change,
            fg_color=C['bg_surface'],
            button_color=C['accent']
        )
        self.val_resize_mode.set('Match First')
        self.val_resize_mode.grid(row=1, column=1, padx=14, pady=5, sticky='ew')

        self._custom_frame = ctk.CTkFrame(sec1, fg_color='transparent')
        self._custom_frame.grid(row=2, column=0, columnspan=2, padx=14, pady=4, sticky='ew')
        self._custom_frame.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(self._custom_frame, text='宽:').grid(row=0, column=0, padx=4)
        self.entry_w = ctk.CTkEntry(self._custom_frame, placeholder_text='400', width=70)
        self.entry_w.insert(0, '400')
        self.entry_w.grid(row=0, column=1, sticky='ew')

        ctk.CTkLabel(self._custom_frame, text='高:').grid(row=0, column=2, padx=4)
        self.entry_h = ctk.CTkEntry(self._custom_frame, placeholder_text='300', width=70)
        self.entry_h.insert(0, '300')
        self.entry_h.grid(row=0, column=3, sticky='ew')

        self._custom_frame.grid_remove()

        ctk.CTkLabel(sec1, text='整体缩放:', anchor='w').grid(
            row=3, column=0, padx=14, pady=5, sticky='w'
        )

        self.val_scale = ctk.CTkSlider(
            sec1,
            from_=0.1,
            to=1.0,
            number_of_steps=18,
            command=self._update_lbls,
            button_color=C['accent'],
            progress_color=C['accent']
        )
        self.val_scale.set(1.0)
        self.val_scale.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

        self.lbl_scale = ctk.CTkLabel(
            sec1,
            text='100%',
            text_color=C['text_muted'],
            width=50,
            anchor='e'
        )
        self.lbl_scale.grid(row=3, column=2, padx=(0, 14))

        # Section 2: Frame Speed
        sec2 = ctk.CTkFrame(frame, fg_color=C['bg_card'], corner_radius=10)
        sec2.grid(row=1, column=0, padx=6, pady=8, sticky='ew')
        sec2.grid_columnconfigure(1, weight=1)
        _section_title(sec2, '⏱️ 帧速控制', 0)

        ctk.CTkLabel(sec2, text='每帧时长 (ms):', anchor='w').grid(
            row=1, column=0, padx=14, pady=5, sticky='w'
        )

        self.val_delay = ctk.CTkSlider(
            sec2,
            from_=50,
            to=2000,
            number_of_steps=39,
            command=self._update_lbls,
            button_color=C['accent'],
            progress_color=C['accent']
        )
        self.val_delay.set(500)
        self.val_delay.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        self.lbl_delay = ctk.CTkLabel(
            sec2,
            text='500 ms',
            text_color=C['text_muted'],
            width=60,
            anchor='e'
        )
        self.lbl_delay.grid(row=1, column=2, padx=(0, 14))

        # Section 3: Transition
        sec3 = ctk.CTkFrame(frame, fg_color=C['bg_card'], corner_radius=10)
        sec3.grid(row=2, column=0, padx=6, pady=8, sticky='ew')
        sec3.grid_columnconfigure(1, weight=1)
        _section_title(sec3, '🔮 过场动画', 0)

        ctk.CTkLabel(sec3, text='过场样式:', anchor='w').grid(
            row=1, column=0, padx=14, pady=5, sticky='w'
        )

        self.val_transition = ctk.CTkOptionMenu(
            sec3,
            values=['None', 'Crossfade'],
            fg_color=C['bg_surface'],
            button_color=C['accent']
        )
        self.val_transition.set('None')
        self.val_transition.grid(row=1, column=1, padx=14, pady=5, sticky='ew')

        ctk.CTkLabel(sec3, text='过渡时长 (ms):', anchor='w').grid(
            row=2, column=0, padx=14, pady=5, sticky='w'
        )

        self.val_trans_dur = ctk.CTkSlider(
            sec3,
            from_=100,
            to=1000,
            number_of_steps=18,
            command=self._update_lbls,
            button_color=C['accent'],
            progress_color=C['accent']
        )
        self.val_trans_dur.set(200)
        self.val_trans_dur.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

        self.lbl_trans = ctk.CTkLabel(
            sec3,
            text='200 ms',
            text_color=C['text_muted'],
            width=60,
            anchor='e'
        )
        self.lbl_trans.grid(row=2, column=2, padx=(0, 14))

        # Section 4: Encoding Quality
        sec4 = ctk.CTkFrame(frame, fg_color=C['bg_card'], corner_radius=10)
        sec4.grid(row=3, column=0, padx=6, pady=8, sticky='ew')
        sec4.grid_columnconfigure(1, weight=1)
        _section_title(sec4, '🛡️ 编码质量', 0)

        ctk.CTkLabel(sec4, text='颜色深度:', anchor='w').grid(
            row=1, column=0, padx=14, pady=5, sticky='w'
        )

        self.val_colors = ctk.CTkOptionMenu(
            sec4,
            values=['256 (超清)', '128 (标准)', '64 (中等)', '32 (极压)'],
            fg_color=C['bg_surface'],
            button_color=C['accent']
        )
        self.val_colors.set('256 (超清)')
        self.val_colors.grid(row=1, column=1, padx=14, pady=5, sticky='ew')

        self.chk_dither = ctk.CTkCheckBox(
            sec4,
            text='Floyd-Steinberg 抖动',
            text_color=C['text_primary'],
            fg_color=C['accent']
        )
        self.chk_dither.select()
        self.chk_dither.grid(row=2, column=0, columnspan=2, padx=14, pady=(0, 14), sticky='w')

    def _on_resize_change(self, mode):
        if mode == 'Custom':
            self._custom_frame.grid()
        else:
            self._custom_frame.grid_remove()

    def _update_lbls(self, _):
        self.lbl_scale.configure(text=f"{int(self.val_scale.get() * 100)}%")
        self.lbl_delay.configure(text=f"{int(self.val_delay.get())} ms")
        self.lbl_trans.configure(text=f"{int(self.val_trans_dur.get())} ms")

    def _import_images(self):
        paths = filedialog.askopenfilenames(
            title='选择图片',
            filetypes=[('图像文件', '*.png *.jpg *.jpeg *.bmp *.webp'), ('全部文件', '*.*')]
        )
        if not paths:
            return
        added = self.app.image_processor.add_images(paths)
        for path in paths:
            self.app.record_recent_file(path, 'image')
        self.lbl_status.configure(text=f"已添加 {added} 张图片")
        self._refresh_list()

    def _clear_images(self):
        self.app.image_processor.clear()
        self.lbl_status.configure(text='列表已清空')
        self._refresh_list()

    def _refresh_list(self):
        for item in self._list_items:
            item.destroy()
        self._list_items = []

        items = self.app.image_processor.get_images_list()
        if not items:
            self._empty_lbl.grid()
            self.btn_compile.configure(state='disabled')
            return

        self._empty_lbl.grid_remove()
        self.btn_compile.configure(state='normal')

        for idx, info in enumerate(items):
            row = ctk.CTkFrame(self.list_box, fg_color=C['bg_surface'], corner_radius=6, height=42)
            row.grid(row=idx, column=0, padx=4, pady=3, sticky='ew')
            row.grid_columnconfigure(1, weight=1)
            row.grid_propagate(False)

            ctk.CTkLabel(
                row,
                text=f"#{idx + 1}",
                width=30,
                text_color=C['accent_light'],
                font=ctk.CTkFont(weight='bold')
            ).grid(row=0, column=0, padx=(8, 4))

            ctk.CTkLabel(
                row,
                text=f"{info['filename']} ({info['width']}×{info['height']})",
                anchor='w',
                text_color=C['text_primary']
            ).grid(row=0, column=1, sticky='ew')

            ctrl = ctk.CTkFrame(row, fg_color='transparent')
            ctrl.grid(row=0, column=2, padx=6)

            for col, (t, cmd) in enumerate([
                ('▲', lambda i=idx: [self.app.image_processor.move_image(i, -1), self._refresh_list()]),
                ('▼', lambda i=idx: [self.app.image_processor.move_image(i, 1), self._refresh_list()]),
                ('✕', lambda i=idx: [self.app.image_processor.remove_image_at(i), self._refresh_list()])
            ]):
                btn = ctk.CTkButton(
                    ctrl,
                    text=t,
                    width=26,
                    height=26,
                    fg_color=C['bg_card'] if t != '✕' else C['danger_muted'],
                    hover_color=C['bg_hover'] if t != '✕' else C['danger_hover'],
                    command=cmd
                )
                btn.grid(row=0, column=col, padx=2)

            self._list_items.append(row)

    def _start_compilation(self):
        try:
            cw = int(self.entry_w.get())
            ch = int(self.entry_h.get())
        except ValueError:
            messagebox.showerror('格式错误', '自定义宽高必须为整数！')
            return

        options = {
            'resize_mode': self.val_resize_mode.get(),
            'scale': float(self.val_scale.get()),
            'custom_width': cw,
            'custom_height': ch,
            'delay': int(self.val_delay.get()),
            'transition_type': self.val_transition.get(),
            'transition_duration': int(self.val_trans_dur.get()),
            'fps': 12.0,
            '_cancel_event': self._cancel_event
        }
        enc_opts = {
            'colors': parse_color_depth(self.val_colors.get()),
            'dither': bool(self.chk_dither.get()),
            'global_palette': True,
            '_cancel_event': self._cancel_event
        }
        self._begin_task()
        self.progress_bar.set(0)
        self.lbl_status.configure(text='正在拼合图片帧...', text_color=C['text_muted'])
        threading.Thread(
            target=self._thread_compile,
            args=(options, enc_opts),
            daemon=True
        ).start()

    def _thread_compile(self, options, enc_opts):
        try:
            frames, delays = self.app.image_processor.process_frames(
                options, progress_callback=self._update_progress
            )
            self._raise_if_cancelled()
            if not frames:
                raise ValueError('未生成有效帧，请检查图片列表。')
            self._update_progress(0.9, '帧处理完成，编码 GIF...')
            enc_opts['delays'] = delays
            result = self.app.gif_encoder.save_gif(
                frames, self.app.temp_gif_path, options=enc_opts, progress_callback=self._update_progress
            )
            self.after(0, lambda: self._show_results(result))
        except Exception as e:
            self._on_thread_error(e, self.btn_compile)

    def _show_results(self, result):
        self.lbl_status.configure(
            text=f"✅ 合成成功！{result['size_mb']:.2f} MB | {result['total_frames']} 帧",
            text_color=C['success']
        )
        self.progress_bar.set(1.0)
        self._finish_task()
        self.btn_save_gif.configure(state='normal')

        win = None
        def go_deco():
            win.grab_release()
            win.destroy()
            self.app.select_tab('GifDeco')
            self.app.frames['GifDeco'].load_gif_from_path(self.app.temp_gif_path)

        win = open_gif_preview_dialog(
            self,
            self.app,
            self.app.temp_gif_path,
            '🎉 图片合成 GIF 预览',
            f"合成成功 ✓  大小: {result['size_mb']:.2f} MB | {result['total_frames']} 帧",
            extra_buttons=[
                ('🎨 导入装饰', C['accent'], C['accent_hover'], go_deco),
                ('💾 另存导出', C['success'], C['success_hover'], lambda: [win.grab_release(), win.destroy(), self._safe_save_gif(self.app.temp_gif_path)])
            ]
        )


class GifOptimizeTab(BaseTab):
    """GifOptimizeTab"""

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=3)
        self._gif_loaded = False
        self._source_path = ''
        self._preview_player = None
        self._build_left_panel()
        self._build_right_panel()
        self._build_bottom_bar(
            '⚡ 运行深度压缩优化',
            '💾 导出优化后 GIF',
            self._start_optimization,
            lambda: self._safe_save_gif(self.app.temp_opt_path, '导出优化 GIF')
        )
        self.btn_compile.configure(text='⚡ 运行深度压缩优化')

    def _build_left_panel(self):
        frame = ctk.CTkFrame(self, fg_color=C['bg_surface'], corner_radius=12)
        frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky='nsew')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        hdr = ctk.CTkFrame(frame, fg_color='transparent')
        hdr.grid(row=0, column=0, padx=14, pady=(14, 6), sticky='ew')
        hdr.grid_columnconfigure(1, weight=1)

        self.lbl_filename = ctk.CTkLabel(
            hdr,
            text='未载入 GIF',
            text_color=C['text_dim'],
            anchor='w',
            font=ctk.CTkFont(size=11, family=FONT)
        )
        btn_load = ctk.CTkButton(
            hdr,
            text='📂 载入 GIF',
            fg_color=C['accent'],
            hover_color=C['accent_hover'],
            command=self._load_gif,
            width=110,
            height=34
        )
        btn_load.grid(row=0, column=0, padx=(0, 8))
        self.lbl_filename.grid(row=0, column=1, sticky='ew')

        self.lbl_meta = ctk.CTkLabel(
            frame,
            text='📊 载入 GIF 后显示元数据',
            text_color=C['accent_light'],
            font=ctk.CTkFont(family=FONT, size=12, weight='bold')
        )
        self.lbl_meta.grid(row=1, column=0, padx=14, pady=(0, 6), sticky='ew')

        self._preview_container = ctk.CTkFrame(frame, fg_color=C['bg_primary'], corner_radius=8)
        self._preview_container.grid(row=2, column=0, padx=14, pady=(0, 14), sticky='nsew')
        self._preview_container.grid_rowconfigure(0, weight=1)
        self._preview_container.grid_columnconfigure(0, weight=1)

        self._preview_placeholder = ctk.CTkLabel(
            self._preview_container,
            text='📽️  GIF 预览区\n\n载入文件后循环播放',
            text_color=C['text_dim'],
            font=ctk.CTkFont(family=FONT, size=13)
        )
        self._preview_placeholder.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

    def _build_right_panel(self):
        frame = ctk.CTkScrollableFrame(
            self,
            fg_color=C['bg_surface'],
            corner_radius=12,
            label_text='⚡ 压缩参数',
            label_font=ctk.CTkFont(size=13, weight='bold', family=FONT)
        )
        frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky='nsew')
        frame.grid_columnconfigure(0, weight=1)

        sec0 = ctk.CTkFrame(frame, fg_color=C['bg_card'], corner_radius=10)
        sec0.grid(row=0, column=0, padx=6, pady=8, sticky='ew')
        sec0.grid_columnconfigure((0, 1), weight=1)
        _section_title(sec0, '⚡ 一键深度压缩预设', 0)

        presets = [
            ('💬 微信极省流 (大压缩)', '32 (省60%)', '隔帧丢弃 (1/2帧)', 0.5, '极限抽帧与色彩缩减，专为微信/QQ等受限平台大图表情包设计。'),
            ('🎬 高清无损保真 (微压缩)', '256 (不减色)', '不抽帧 (全帧)', 0.9, '不丢帧，保留完美画质与顺滑色彩渐变，仅轻微缩放尺寸。'),
            ('📱 自媒体平衡 (中压缩)', '128 (省20%)', '不抽帧 (全帧)', 0.7, '适用于自媒体配图，保留流畅动作，色彩与分辨率轻度优化。'),
            ('🎮 游戏精彩抽帧 (强压缩)', '128 (省20%)', '隔帧丢弃 (1/2帧)', 0.6, '针对超长高帧率游戏GIF，隔帧丢弃并压缩颜色深度，减小文件体积。')
        ]

        for idx, (name, colors, skip, scale, desc) in enumerate(presets):
            r = 1 + idx // 2
            c = idx % 2
            btn = ctk.CTkButton(
                sec0,
                text=name,
                height=32,
                fg_color=C['bg_hover'],
                hover_color=C['accent_hover'],
                text_color=C['text_primary'],
                font=ctk.CTkFont(family=FONT, size=11, weight='bold'),
                command=lambda col=colors, sk=skip, sc=scale, name_lbl=name, dsc=desc: self._apply_preset(col, sk, sc, name_lbl, dsc)
            )
            btn.grid(row=r, column=c, padx=6, pady=6, sticky='ew')

        self.preset_desc_frame = ctk.CTkFrame(
            sec0, fg_color=C['bg_primary'], corner_radius=8, border_width=1, border_color=C['border']
        )
        self.preset_desc_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 10), sticky='ew')
        self.preset_desc_frame.grid_columnconfigure(0, weight=1)

        self.lbl_preset_desc_title = ctk.CTkLabel(
            self.preset_desc_frame,
            text='💡 压缩说明 → 微信极省流 (大压缩)',
            font=ctk.CTkFont(family=FONT, size=11, weight='bold'),
            text_color=C['cyan']
        )
        self.lbl_preset_desc_title.grid(row=0, column=0, padx=12, pady=(8, 2), sticky='w')

        self.lbl_preset_desc_body = ctk.CTkLabel(
            self.preset_desc_frame,
            text='极限抽帧与色彩缩减，专为微信/QQ等受限平台大图表情包设计。\n• 颜色深度: 32 (省60%)  |  抽帧模式: 隔帧丢弃 (1/2帧)\n• 分辨率缩放: 50%',
            font=ctk.CTkFont(family=FONT, size=10),
            text_color=C['text_muted'],
            justify='left',
            anchor='w'
        )
        self.lbl_preset_desc_body.grid(row=1, column=0, padx=12, pady=(0, 8), sticky='w')

        # Section 1: Colors
        sec1 = ctk.CTkFrame(frame, fg_color=C['bg_card'], corner_radius=10)
        sec1.grid(row=1, column=0, padx=6, pady=8, sticky='ew')
        sec1.grid_columnconfigure(1, weight=1)
        _section_title(sec1, '🎨 减色压缩', 0)

        ctk.CTkLabel(sec1, text='颜色数量:', anchor='w').grid(row=1, column=0, padx=14, pady=5, sticky='w')

        self.val_colors = ctk.CTkOptionMenu(
            sec1,
            values=['256 (不减色)', '128 (省20%)', '64 (省45%)', '32 (省60%)', '16 (像素风)'],
            fg_color=C['bg_surface'],
            button_color=C['accent']
        )
        self.val_colors.set('256 (不减色)')
        self.val_colors.grid(row=1, column=1, padx=14, pady=8, sticky='ew')

        # Section 2: Skip Frames
        sec2 = ctk.CTkFrame(frame, fg_color=C['bg_card'], corner_radius=10)
        sec2.grid(row=2, column=0, padx=6, pady=8, sticky='ew')
        sec2.grid_columnconfigure(1, weight=1)
        _section_title(sec2, '⏳ 抽帧压缩', 0)

        ctk.CTkLabel(sec2, text='抽帧模式:', anchor='w').grid(row=1, column=0, padx=14, pady=5, sticky='w')

        self.val_skip = ctk.CTkOptionMenu(
            sec2,
            values=['不抽帧 (全帧)', '隔帧丢弃 (1/2帧)', '每三帧留一 (1/3帧)'],
            fg_color=C['bg_surface'],
            button_color=C['accent']
        )
        self.val_skip.set('不抽帧 (全帧)')
        self.val_skip.grid(row=1, column=1, padx=14, pady=8, sticky='ew')

        # Section 3: Scale
        sec3 = ctk.CTkFrame(frame, fg_color=C['bg_card'], corner_radius=10)
        sec3.grid(row=3, column=0, padx=6, pady=8, sticky='ew')
        sec3.grid_columnconfigure(1, weight=1)
        _section_title(sec3, '🔍 分辨率缩放', 0)

        ctk.CTkLabel(sec3, text='缩放比例:', anchor='w').grid(row=1, column=0, padx=14, pady=5, sticky='w')

        self.val_scale = ctk.CTkSlider(
            sec3,
            from_=0.1,
            to=1.0,
            number_of_steps=18,
            command=self._update_lbl,
            button_color=C['accent'],
            progress_color=C['accent']
        )
        self.val_scale.set(1.0)
        self.val_scale.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        self.lbl_scale = ctk.CTkLabel(sec3, text='100%', text_color=C['text_muted'], width=60, anchor='e')
        self.lbl_scale.grid(row=1, column=2, padx=(0, 14))

    def _apply_preset(self, colors, skip_mode, scale, name, desc):
        self.val_colors.set(colors)
        self.val_skip.set(skip_mode)
        self.val_scale.set(scale)
        self._update_lbl(None)
        self.lbl_preset_desc_title.configure(text=f"💡 压缩说明 → {name}")
        self.lbl_preset_desc_body.configure(
            text=f"{desc}\n• 颜色深度: {colors}  |  抽帧模式: {skip_mode}\n• 分辨率缩放: {int(scale * 100)}%"
        )
        self.lbl_status.configure(text=f"✨ 已应用深度压缩预设 → {name}", text_color=C['success'])

    def _update_lbl(self, _=None):
        v = self.val_scale.get()
        self.lbl_scale.configure(text=f"{int(v * 100)}%" + (' (原尺寸)' if v == 1.0 else ''))

    def _load_gif(self):
        path = filedialog.askopenfilename(
            title='选择 GIF 文件',
            filetypes=[('GIF', '*.gif')]
        )
        if not path:
            return
        self.lbl_status.configure(text='正在分析 GIF...', text_color=C['text_muted'])
        self.progress_bar.set(0.1)
        self.update_idletasks()
        try:
            meta = self.app.gif_optimizer.get_gif_metadata(path)
            self.app.record_recent_file(path, 'gif')
            self._source_path = path
            self._gif_loaded = True
            self.lbl_filename.configure(
                text=f"{meta['filename']} | {meta['width']}×{meta['height']} | {meta['size_mb']:.2f} MB",
                text_color=C['success']
            )
            self.lbl_meta.configure(
                text=f"📊 {meta['width']}×{meta['height']}  |  {meta['total_frames']} 帧  |  avg {meta['avg_delay']:.0f}ms ({meta['fps']:.1f} FPS)  |  {meta['size_mb']:.2f} MB"
            )
            self._show_preview(path)
            self.btn_compile.configure(state='normal')
            self.lbl_status.configure(text='GIF 载入成功 ✓  设置参数后运行压缩', text_color=C['success'])
            self.progress_bar.set(0)
        except Exception as e:
            self.lbl_status.configure(text=f"载入失败: {e}", text_color=C['danger'])
            self.progress_bar.set(0)
            messagebox.showerror('载入失败', str(e))

    def _show_preview(self, path):
        if self._preview_player:
            self._preview_player.stop()
            self._preview_player.destroy()
        self._preview_placeholder.grid_remove()
        player = GifPreviewer(self._preview_container)
        player.grid(row=0, column=0, sticky='nsew', padx=8, pady=8)
        self.update_idletasks()
        max_w = max(200, self._preview_container.winfo_width() - 20)
        player.load_gif(path, max_width=max_w)
        self._preview_player = player

    def _start_optimization(self):
        if not self._gif_loaded:
            return
        skip_str = self.val_skip.get()
        if '1/3' in skip_str:
            skip_step = 3
        elif '1/2' in skip_str:
            skip_step = 2
        else:
            skip_step = 1

        options = {
            'colors': parse_color_depth(self.val_colors.get()),
            'skip_step': skip_step,
            'scale': float(self.val_scale.get()),
            '_cancel_event': self._cancel_event
        }

        self._begin_task()
        self.progress_bar.set(0)
        self.lbl_status.configure(text='正在压缩 GIF...', text_color=C['text_muted'])
        threading.Thread(
            target=self._thread_optimize,
            args=(options,),
            daemon=True
        ).start()

    def _thread_optimize(self, options):
        try:
            result = self.app.gif_optimizer.optimize(
                self._source_path, self.app.temp_opt_path, options, progress_callback=self._update_progress
            )
            self.after(0, lambda: self._show_results(result))
        except Exception as e:
            self._on_thread_error(e, self.btn_compile)

    def _show_results(self, result):
        orig = result['original_size'] / 1048576
        new = result['new_size'] / 1048576
        saved = result['ratio'] * 100
        self.lbl_status.configure(
            text=f"✅ 压缩成功！节省 {saved:.1f}%  ({orig:.2f}MB → {new:.2f}MB)",
            text_color=C['success']
        )
        self.progress_bar.set(1.0)
        self._finish_task()
        self.btn_save_gif.configure(state='normal')

        win = None
        win = open_gif_preview_dialog(
            self,
            self.app,
            self.app.temp_opt_path,
            '🎉 压缩优化完成',
            f"🎉 优化成功！体积减少 {saved:.1f}%\n原始: {orig:.2f} MB  →  压缩后: {new:.2f} MB",
            extra_buttons=[
                ('💾 另存导出', C['success'], C['success_hover'], lambda: [win.grab_release(), win.destroy(), self._safe_save_gif(self.app.temp_opt_path)])
            ]
        )


class WorkspaceTab(BaseTab):
    """WorkspaceTab"""

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color=C['bg_surface'], corner_radius=12)
        self.main_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        hdr = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        hdr.grid(row=0, column=0, padx=20, pady=(20, 10), sticky='ew')
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hdr,
            text='📁 工作区输出文件管理器',
            font=ctk.CTkFont(size=18, weight='bold', family=FONT),
            text_color=C['accent_light']
        ).grid(row=0, column=0, sticky='w')

        self.lbl_path = ctk.CTkLabel(
            hdr,
            text=f"工作区路径: {self.app.workspace_dir}",
            text_color=C['text_muted'],
            font=ctk.CTkFont(size=12, family=FONT)
        )
        self.lbl_path.grid(row=1, column=0, sticky='w', pady=(2, 0))

        btn_grp = ctk.CTkFrame(hdr, fg_color='transparent')
        btn_grp.grid(row=0, column=1, rowspan=2, sticky='e')

        btn_open = ctk.CTkButton(
            btn_grp,
            text='📂 打开系统文件夹',
            fg_color=C['accent'],
            hover_color=C['accent_hover'],
            font=ctk.CTkFont(family=FONT, size=12, weight='bold'),
            command=self._open_in_explorer,
            height=32
        )
        btn_open.grid(row=0, column=0, padx=4)

        btn_refresh = ctk.CTkButton(
            btn_grp,
            text='🔄 刷新列表',
            fg_color=C['success'],
            hover_color=C['success_hover'],
            font=ctk.CTkFont(family=FONT, size=12, weight='bold'),
            command=self.refresh_list,
            height=32
        )
        btn_refresh.grid(row=0, column=1, padx=4)

        recent_values = self._recent_display_values()
        self.recent_menu = ctk.CTkOptionMenu(
            hdr,
            values=recent_values,
            width=260,
            fg_color=C['bg_card'],
            button_color=C['cyan_hover'],
            button_hover_color=C['cyan'],
            font=ctk.CTkFont(family=FONT, size=11)
        )
        self.recent_menu.grid(row=2, column=0, pady=(10, 0), sticky='w')
        self.btn_open_recent = ctk.CTkButton(
            hdr,
            text='打开最近文件',
            width=105,
            height=28,
            fg_color=C['cyan_hover'],
            hover_color=C['cyan'],
            command=self._open_recent
        )
        self.btn_open_recent.grid(row=2, column=1, pady=(10, 0), sticky='e')

        self.list_box = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color=C['bg_primary'],
            corner_radius=10,
            label_text='工作区输出文件列表 (支持 GIF、图片等)',
            label_font=ctk.CTkFont(size=13, weight='bold', family=FONT)
        )
        self.list_box.grid(row=1, column=0, padx=20, pady=(0, 20), sticky='nsew')
        self.list_box.grid_columnconfigure(0, weight=1)

        self._empty_lbl = ctk.CTkLabel(
            self.list_box,
            text='📁 工作区内暂无输出文件\n\n您在转换视频、导出单帧或合成GIF时，文件将自动汇总至此处',
            text_color=C['text_dim'],
            font=ctk.CTkFont(family=FONT, size=13),
            justify='center'
        )
        self._empty_lbl.grid(row=0, column=0, padx=20, pady=50)

        self._file_widgets = []

    def on_show(self):
        values = self._recent_display_values()
        self.recent_menu.configure(values=values)
        self.recent_menu.set(values[0])
        self.refresh_list()

    def _recent_display_values(self):
        if not self.app.recent_files:
            return ['暂无最近文件']
        return [
            f"{index + 1}. {os.path.basename(item['path'])}"
            for index, item in enumerate(self.app.recent_files)
        ]

    def _open_recent(self):
        if not self.app.recent_files:
            return
        try:
            index = int(self.recent_menu.get().split('.', 1)[0]) - 1
            item = self.app.recent_files[index]
        except (ValueError, IndexError):
            return
        path = item['path']
        if not os.path.exists(path):
            self.app.recent_files.pop(index)
            self.on_show()
            return
        kind = item.get('kind')
        if kind == 'video':
            self.app.select_tab('VideoToGif')
            self.app.frames['VideoToGif'].load_video_file(path)
        elif kind == 'gif':
            self.app.select_tab('GifDeco')
            self.app.frames['GifDeco'].load_gif_from_path(path)
        elif kind == 'image':
            self.app.image_processor.add_images([path])
            self.app.select_tab('ImagesToGif')
            self.app.frames['ImagesToGif']._refresh_list()

    def _open_in_explorer(self):
        if os.path.exists(self.app.workspace_dir):
            os.startfile(self.app.workspace_dir)

    def refresh_list(self):
        for w in self._file_widgets:
            w.destroy()
        self._file_widgets.clear()

        if not os.path.exists(self.app.workspace_dir):
            os.makedirs(self.app.workspace_dir, exist_ok=True)

        files = []
        try:
            for f in os.listdir(self.app.workspace_dir):
                full_path = os.path.join(self.app.workspace_dir, f)
                if os.path.isfile(full_path):
                    files.append((f, os.path.getsize(full_path), os.path.getmtime(full_path)))
            files.sort(key=lambda x: x[2], reverse=True)
        except Exception as e:
            print(f"Read workspace error: {e}")

        if not files:
            self._empty_lbl.grid()
            return

        self._empty_lbl.grid_remove()

        for idx, (filename, size, mtime) in enumerate(files):
            item = ctk.CTkFrame(self.list_box, fg_color=C['bg_secondary'], height=42, corner_radius=6)
            item.grid(row=idx, column=0, padx=8, pady=4, sticky='ew')
            item.grid_columnconfigure(1, weight=1)
            item.grid_propagate(False)

            ext = os.path.splitext(filename)[1].lower()
            is_video = ext in ('.mp4', '.avi', '.mov', '.mkv', '.webm')
            if ext in ('.gif', '.png', '.jpg', '.jpeg'):
                icon = '🖼️'
            elif is_video:
                icon = '🎥'
            else:
                icon = '📄'

            if ext == '.gif':
                icon = '🎞️'

            size_mb = size / 1048576

            lbl_info = ctk.CTkLabel(
                item,
                text=f"{icon}  {filename}  ({size_mb:.2f} MB)",
                anchor='w',
                font=ctk.CTkFont(family=FONT, size=13),
                text_color=C['text_primary']
            )
            lbl_info.grid(row=0, column=0, padx=12, pady=8, sticky='w')

            btn_frame = ctk.CTkFrame(item, fg_color='transparent')
            btn_frame.grid(row=0, column=2, padx=12, pady=4, sticky='e')

            full_path = os.path.join(self.app.workspace_dir, filename)

            if ext in ('.gif', '.png', '.jpg', '.jpeg') or is_video:
                btn_preview = ctk.CTkButton(
                    btn_frame,
                    text='▶️ 播放' if is_video else '👁️ 预览',
                    width=65,
                    height=28,
                    fg_color=C['accent'],
                    hover_color=C['accent_hover'],
                    font=ctk.CTkFont(family=FONT, size=11),
                    command=lambda p=full_path: self._preview_file(p)
                )
                btn_preview.grid(row=0, column=0, padx=2)

            btn_delete = ctk.CTkButton(
                btn_frame,
                text='🗑️ 删除',
                width=65,
                height=28,
                fg_color=C['danger_muted'],
                hover_color=C['danger_hover'],
                font=ctk.CTkFont(family=FONT, size=11),
                command=lambda p=full_path: self._delete_file(p)
            )
            btn_delete.grid(row=0, column=1, padx=2)

            self._file_widgets.append(item)

    def _preview_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ('.mp4', '.avi', '.mov', '.mkv', '.webm'):
            try:
                os.startfile(file_path)
            except Exception as e:
                messagebox.showerror('播放失败', f"无法播放视频：\n{e}")
            return

        if ext == '.gif':
            open_gif_preview_dialog(
                self,
                self.app,
                file_path,
                '工作区文件预览',
                f"文件名: {os.path.basename(file_path)}"
            )
            return

        if ext in ('.png', '.jpg', '.jpeg'):
            win = ctk.CTkToplevel(self)
            win.title('工作区图片预览')
            win.geometry('560x520')
            win.configure(fg_color=C['bg_primary'])
            win.grab_set()

            try:
                img = Image.open(file_path)
                w, h = img.size
                scale = min(1.0, 480 / w, 440 / h)
                pw = int(w * scale)
                ph = int(h * scale)
                resized = img.resize((pw, ph), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(resized)

                lbl = tk.Label(win, image=img_tk, bg=C['bg_primary'])
                lbl.image = img_tk
                lbl.pack(padx=20, pady=20, expand=True)
            except Exception as e:
                ctk.CTkLabel(win, text=f"无法预览: {e}").pack(padx=20, pady=20)

            ctk.CTkButton(
                win,
                text='关闭',
                fg_color=C['bg_hover'],
                hover_color=C['bg_card'],
                command=win.destroy
            ).pack(pady=10)

    def _delete_file(self, file_path):
        if not messagebox.askyesno('确认删除', f"确定要彻底删除该文件吗？此操作无法撤销：\n{os.path.basename(file_path)}"):
            return
        try:
            os.remove(file_path)
            self.refresh_list()
        except Exception as e:
            messagebox.showerror('删除失败', f"删除文件时出错：\n{e}")
