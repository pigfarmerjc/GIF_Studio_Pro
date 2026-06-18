# ============================================================
# Module: audio_video_studio_tab.py
# Reconstructed from Python 3.14 bytecode
# ============================================================

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk


class AudioVideoStudioTab(ctk.CTkFrame):
    """
    AudioVideoStudioTab - Provides lossless high-fidelity audio extraction
    and video/audio track mixing studio workbench.
    """

    def __init__(self, master, app):
        super().__init__(master, fg_color='transparent')
        self.app = app
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_panel = ctk.CTkFrame(self, fg_color='#1E293B', corner_radius=10)
        self.main_panel.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_rowconfigure(3, weight=1)

        title = ctk.CTkLabel(
            self.main_panel,
            text='🎬 智能影音工作室 - Smart Audio-Video Studio',
            font=ctk.CTkFont(size=20, weight='bold', family='Microsoft YaHei'),
            text_color='#818CF8'
        )
        title.grid(row=0, column=0, padx=30, pady=(25, 2), sticky='w')

        subtitle = ctk.CTkLabel(
            self.main_panel,
            text='极速无损提取！无需重编码视频，直接抓取高保真声音，或为视频配置炫酷背景音乐与独立混音轨。',
            font=ctk.CTkFont(size=12, family='Microsoft YaHei'),
            text_color='gray50'
        )
        subtitle.grid(row=1, column=0, padx=30, pady=(0, 15), sticky='w')

        self.mode_selector = ctk.CTkSegmentedButton(
            self.main_panel,
            values=['🎤 高保真音频提取大厅', '🎬 视频配音与多轨混音工作台'],
            command=self.switch_mode,
            font=ctk.CTkFont(size=13, weight='bold', family='Microsoft YaHei'),
            selected_color='#6366F1',
            selected_hover_color='#4F46E5',
            height=36
        )
        self.mode_selector.grid(row=2, column=0, padx=30, pady=(0, 15), sticky='w')
        self.mode_selector.set('🎤 高保真音频提取大厅')

        self.create_extract_panel()
        self.create_dubbing_panel()
        self.create_bottom_progress()

        self.switch_mode('🎤 高保真音频提取大厅')

    def on_show(self):
        pass

    def switch_mode(self, mode):
        """Swaps active sub-panel interface."""
        if mode == '🎤 高保真音频提取大厅':
            self.dubbing_panel.grid_remove()
            self.extract_panel.grid(row=3, column=0, padx=30, pady=(0, 5), sticky='nsew')
            self.lbl_status.configure(text='等待载入音频源视频文件...', text_color='gray60')
            self.progress_bar.set(0)
        else:
            self.extract_panel.grid_remove()
            self.dubbing_panel.grid(row=3, column=0, padx=30, pady=(0, 5), sticky='nsew')
            self.lbl_status.configure(text='等待载入视频及配音音频素材...', text_color='gray60')
            self.progress_bar.set(0)

    def create_extract_panel(self):
        self.extract_panel = ctk.CTkScrollableFrame(self.main_panel, fg_color='transparent')
        self.extract_panel.grid_columnconfigure(0, weight=1)

        self.ext_import_box = ctk.CTkFrame(self.extract_panel, fg_color='#0F172A', corner_radius=8)
        self.ext_import_box.grid(row=0, column=0, pady=6, sticky='ew')
        self.ext_import_box.grid_columnconfigure(1, weight=1)

        self.btn_ext_select = ctk.CTkButton(
            self.ext_import_box,
            text='📂 选择视频源文件',
            fg_color='#6366F1',
            hover_color='#4F46E5',
            font=ctk.CTkFont(weight='bold', family='Microsoft YaHei'),
            command=self.ext_select_video
        )
        self.btn_ext_select.grid(row=0, column=0, padx=15, pady=15)

        self.entry_ext_video_path = ctk.CTkEntry(
            self.ext_import_box,
            placeholder_text='当前未选择视频，请点击左侧按钮导入...',
            font=ctk.CTkFont(size=12)
        )
        self.entry_ext_video_path.grid(row=0, column=1, padx=(0, 15), pady=15, sticky='ew')

        self.ext_param_box = ctk.CTkFrame(self.extract_panel, fg_color='#0F172A', corner_radius=8)
        self.ext_param_box.grid(row=1, column=0, pady=8, sticky='ew')
        self.ext_param_box.grid_columnconfigure((1, 3), weight=1)

        lbl_title = ctk.CTkLabel(
            self.ext_param_box,
            text='⚙️ 高保真导出格式与比特率参数配置',
            font=ctk.CTkFont(size=13, weight='bold'),
            text_color='#818CF8'
        )
        lbl_title.grid(row=0, column=0, columnspan=4, padx=15, pady=(12, 8), sticky='w')

        lbl_format = ctk.CTkLabel(self.ext_param_box, text='音频导出格式:')
        lbl_format.grid(row=1, column=0, padx=15, pady=8, sticky='w')

        self.val_ext_format = ctk.CTkOptionMenu(
            self.ext_param_box,
            values=['MP3 (高兼容)', 'WAV (无损 PCM)', 'FLAC (无损压缩)', 'AAC (苹果编码)', 'M4A (高音质)'],
            command=self.on_ext_format_change
        )
        self.val_ext_format.set('MP3 (高兼容)')
        self.val_ext_format.grid(row=1, column=1, padx=(0, 15), pady=8, sticky='ew')

        self.lbl_ext_bitrate = ctk.CTkLabel(self.ext_param_box, text='高保真比特率:')
        self.lbl_ext_bitrate.grid(row=1, column=2, padx=15, pady=8, sticky='w')

        self.bitrate_ctrl_frame = ctk.CTkFrame(self.ext_param_box, fg_color='transparent')
        self.bitrate_ctrl_frame.grid(row=1, column=3, padx=(0, 15), pady=8, sticky='ew')
        self.bitrate_ctrl_frame.grid_columnconfigure(0, weight=1)

        self.val_ext_bitrate = ctk.CTkSlider(
            self.bitrate_ctrl_frame,
            from_=0,
            to=3,
            number_of_steps=3,
            command=self.update_bitrate_lbl
        )
        self.val_ext_bitrate.set(2)
        self.val_ext_bitrate.grid(row=0, column=0, sticky='ew', padx=(0, 8))

        self.lbl_ext_bitrate_disp = ctk.CTkLabel(
            self.bitrate_ctrl_frame,
            text='256 kbps',
            text_color='gray60',
            width=60
        )
        self.lbl_ext_bitrate_disp.grid(row=0, column=1)

        self.ext_crop_box = ctk.CTkFrame(self.extract_panel, fg_color='#0F172A', corner_radius=8)
        self.ext_crop_box.grid(row=2, column=0, pady=6, sticky='ew')
        self.ext_crop_box.grid_columnconfigure((1, 3), weight=1)

        lbl_crop_title = ctk.CTkLabel(
            self.ext_crop_box,
            text='✂️ 提取起终点范围裁剪微调 (留空默认提取整段)',
            font=ctk.CTkFont(size=13, weight='bold'),
            text_color='#818CF8'
        )
        lbl_crop_title.grid(row=0, column=0, columnspan=4, padx=15, pady=(10, 8), sticky='w')

        lbl_start = ctk.CTkLabel(self.ext_crop_box, text='开始秒数:')
        lbl_start.grid(row=1, column=0, padx=15, pady=8, sticky='w')

        self.entry_ext_start = ctk.CTkEntry(self.ext_crop_box, placeholder_text='例如: 0.00')
        self.entry_ext_start.grid(row=1, column=1, padx=(0, 15), pady=8, sticky='ew')

        lbl_end = ctk.CTkLabel(self.ext_crop_box, text='结束秒数:')
        lbl_end.grid(row=1, column=2, padx=15, pady=8, sticky='w')

        self.entry_ext_end = ctk.CTkEntry(self.ext_crop_box, placeholder_text='例如: 10.5')
        self.entry_ext_end.grid(row=1, column=3, padx=(0, 15), pady=8, sticky='ew')

        self.btn_ext_execute = ctk.CTkButton(
            self.extract_panel,
            text='🎵 智能高保真音频提取',
            height=45,
            fg_color='#10B981',
            hover_color='#059669',
            font=ctk.CTkFont(size=15, weight='bold', family='Microsoft YaHei'),
            command=self.execute_extract
        )
        self.btn_ext_execute.grid(row=3, column=0, pady=(15, 10), sticky='ew')
        self.btn_ext_execute.configure(state='disabled')

        self.ext_video_loaded = False
        self.ext_video_duration = 0.0

    def ext_select_video(self):
        """Loads video file for extraction."""
        path = filedialog.askopenfilename(
            title='选择要提取音频的视频源',
            filetypes=[('视频文件', '*.mp4 *.avi *.mkv *.mov *.webm *.flv'), ('全部文件', '*.*')]
        )
        if not path:
            return

        self.entry_ext_video_path.delete(0, tk.END)
        self.entry_ext_video_path.insert(0, path)

        try:
            meta = self.app.video_processor.load_video(path)
            self.ext_video_duration = meta['duration']
            self.ext_video_loaded = True

            ext = path.split('.')[-1].upper()
            info_str = f"视频源加载成功！格式: {ext} | 分辨率: {meta['width']}x{meta['height']} | 时长: {self.ext_video_duration:.2f} 秒"
            self.lbl_status.configure(text=info_str, text_color='#10B981')
            self.btn_ext_execute.configure(state='normal')
            
            self.entry_ext_start.delete(0, tk.END)
            self.entry_ext_end.delete(0, tk.END)
            self.entry_ext_end.insert(0, f"{self.ext_video_duration:.2f}")
        except Exception as e:
            self.lbl_status.configure(text=f"视频解析失败: {str(e)}", text_color='#EF4444')
            self.btn_ext_execute.configure(state='disabled')
            messagebox.showerror('读取失败', f"无法解析该视频文件:\n{str(e)}")

    def on_ext_format_change(self, value):
        """Switches UI states according to audio format (e.g. disabling bitrate for WAV/FLAC)."""
        if 'WAV' in value or 'FLAC' in value:
            self.val_ext_bitrate.configure(state='disabled')
            self.lbl_ext_bitrate_disp.configure(text='无损高采样', text_color='gray40')
        else:
            self.val_ext_bitrate.configure(state='normal')
            self.update_bitrate_lbl()

    def update_bitrate_lbl(self, val=None):
        """Converts bitrate slider step values to human-readable text."""
        steps = ['128 kbps', '192 kbps', '256 kbps', '320 kbps']
        idx = int(self.val_ext_bitrate.get())
        self.lbl_ext_bitrate_disp.configure(text=steps[idx], text_color='gray60')

    def execute_extract(self):
        """Validates and runs audio extraction."""
        if not self.ext_video_loaded:
            return

        video_path = self.entry_ext_video_path.get()
        if not os.path.exists(video_path):
            messagebox.showerror('文件不存在', '导入的视频源已失效，请重新加载！')
            return

        try:
            start_val = self.entry_ext_start.get().strip()
            start_t = float(start_val) if start_val else 0.0

            end_val = self.entry_ext_end.get().strip()
            end_t = float(end_val) if end_val else self.ext_video_duration
        except ValueError:
            messagebox.showerror('参数格式错误', '裁剪时限必须是有效的数值！')
            return

        if start_t >= end_t:
            messagebox.showerror('区间错误', '开始秒数必须小于结束秒数！')
            return

        fmt_str = self.val_ext_format.get()
        fmt_ext = '.mp3'
        audio_format = 'mp3'

        if 'WAV' in fmt_str:
            fmt_ext = '.wav'
            audio_format = 'wav'
        elif 'FLAC' in fmt_str:
            fmt_ext = '.flac'
            audio_format = 'flac'
        elif 'AAC' in fmt_str:
            fmt_ext = '.aac'
            audio_format = 'aac'
        elif 'M4A' in fmt_str:
            fmt_ext = '.m4a'
            audio_format = 'm4a'

        bitrates = ['128k', '192k', '256k', '320k']
        bitrate = bitrates[int(self.val_ext_bitrate.get())]

        default_name = os.path.splitext(os.path.basename(video_path))[0] + fmt_ext
        save_path = filedialog.asksaveasfilename(
            title=f"选择导出音频 ({audio_format.upper()}) 保存路径",
            initialfile=default_name,
            defaultextension=fmt_ext,
            filetypes=[(f"{audio_format.upper()} Audio", f"*{fmt_ext}")]
        )

        if not save_path:
            return

        self.btn_ext_execute.configure(state='disabled')
        self.btn_ext_select.configure(state='disabled')
        self.progress_bar.set(0)
        self.lbl_status.configure(text='正在初始化高保真音频提取线程...')

        t = threading.Thread(
            target=self._threaded_extract,
            args=(video_path, save_path, start_t, end_t, audio_format, bitrate),
            daemon=True
        )
        t.start()

    def _threaded_extract(self, video_path, save_path, start_t, end_t, audio_format, bitrate):
        def update_progress(val, status_txt):
            self.after(0, lambda: self.progress_bar.set(val))
            self.after(0, lambda: self.lbl_status.configure(text=status_txt))

        try:
            self.app.video_processor.extract_audio(
                video_path,
                save_path,
                start_time=start_t,
                end_time=end_t,
                audio_format=audio_format,
                bitrate=bitrate,
                progress_callback=update_progress
            )
            self.after(0, lambda: self.on_extraction_success(save_path))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror('提取失败', f"FFmpeg 编码音频时出错:\n{str(e)}"))
            self.after(0, lambda: self.lbl_status.configure(text=f"音频提取失败: {str(e)}", text_color='#EF4444'))
            self.after(0, lambda: self.progress_bar.set(0))
        finally:
            self.after(0, lambda: self.btn_ext_execute.configure(state='normal'))
            self.after(0, lambda: self.btn_ext_select.configure(state='normal'))

    def on_extraction_success(self, save_path):
        self.progress_bar.set(1.0)
        filename = os.path.basename(save_path)
        self.lbl_status.configure(text=f"高保真音频提取成功！已保存至 {filename}", text_color='#10B981')
        messagebox.showinfo('音频提取成功', f"恭喜！您的高保真音频已经成功提取并导出到:\n\n{save_path}")

    def create_dubbing_panel(self):
        self.dubbing_panel = ctk.CTkScrollableFrame(self.main_panel, fg_color='transparent')
        self.dubbing_panel.grid_columnconfigure(0, weight=1)

        self.dub_video_loaded = False
        self.dub_video_duration = 0.0
        self.dub_audio_loaded = False
        self.dub_audio_duration = 0.0

        self.import_cards_frame = ctk.CTkFrame(self.dubbing_panel, fg_color='transparent')
        self.import_cards_frame.grid(row=0, column=0, pady=4, sticky='ew')
        self.import_cards_frame.grid_columnconfigure((0, 1), weight=1)

        # Video card
        self.card_video = ctk.CTkFrame(self.import_cards_frame, fg_color='#0F172A', corner_radius=8)
        self.card_video.grid(row=0, column=0, padx=(0, 6), sticky='nsew')
        self.card_video.grid_columnconfigure(0, weight=1)

        lbl_video_title = ctk.CTkLabel(
            self.card_video,
            text='🎥 导入第一路：视频源素材',
            font=ctk.CTkFont(weight='bold', size=13),
            text_color='#818CF8'
        )
        lbl_video_title.grid(row=0, column=0, padx=15, pady=(12, 4), sticky='w')

        self.btn_dub_select_v = ctk.CTkButton(
            self.card_video,
            text='📂 导入视频文件',
            fg_color='#6366F1',
            hover_color='#4F46E5',
            command=self.dub_select_video
        )
        self.btn_dub_select_v.grid(row=1, column=0, padx=15, pady=8, sticky='w')

        self.lbl_dub_video_info = ctk.CTkLabel(
            self.card_video,
            text='未导入视频文件...',
            text_color='gray50',
            justify='left',
            anchor='w'
        )
        self.lbl_dub_video_info.grid(row=2, column=0, padx=15, pady=(2, 15), sticky='w')

        # Audio card
        self.card_audio = ctk.CTkFrame(self.import_cards_frame, fg_color='#0F172A', corner_radius=8)
        self.card_audio.grid(row=0, column=1, padx=(6, 0), sticky='nsew')
        self.card_audio.grid_columnconfigure(0, weight=1)

        lbl_audio_title = ctk.CTkLabel(
            self.card_audio,
            text='🎵 导入第二路：背景音乐/配音',
            font=ctk.CTkFont(weight='bold', size=13),
            text_color='#06B6D4'
        )
        lbl_audio_title.grid(row=0, column=0, padx=15, pady=(12, 4), sticky='w')

        self.btn_dub_select_a = ctk.CTkButton(
            self.card_audio,
            text='📂 导入配音音频',
            fg_color='#06B6D4',
            hover_color='#0891B2',
            command=self.dub_select_audio
        )
        self.btn_dub_select_a.grid(row=1, column=0, padx=15, pady=8, sticky='w')

        self.lbl_dub_audio_info = ctk.CTkLabel(
            self.card_audio,
            text='未导入配音文件...',
            text_color='gray50',
            justify='left',
            anchor='w'
        )
        self.lbl_dub_audio_info.grid(row=2, column=0, padx=15, pady=(2, 15), sticky='w')

        # Mixer Panel
        self.mixer_panel = ctk.CTkFrame(self.dubbing_panel, fg_color='#0F172A', corner_radius=8)
        self.mixer_panel.grid(row=1, column=0, pady=8, sticky='ew')
        self.mixer_panel.grid_columnconfigure(1, weight=1)

        lbl_mixer_title = ctk.CTkLabel(
            self.mixer_panel,
            text='🎚️ 智能配音混音调音台 (Tuning Desk)',
            font=ctk.CTkFont(size=14, weight='bold'),
            text_color='#818CF8'
        )
        lbl_mixer_title.grid(row=0, column=0, columnspan=3, padx=15, pady=(12, 8), sticky='w')

        lbl_v_vol = ctk.CTkLabel(self.mixer_panel, text='🔊 视频原声音量:')
        lbl_v_vol.grid(row=1, column=0, padx=15, pady=6, sticky='w')

        self.val_v_volume = ctk.CTkSlider(
            self.mixer_panel,
            from_=0.0,
            to=2.0,
            number_of_steps=20,
            command=self.update_mixer_lbls
        )
        self.val_v_volume.set(1.0)
        self.val_v_volume.grid(row=1, column=1, padx=10, pady=6, sticky='ew')

        self.lbl_v_vol_disp = ctk.CTkLabel(
            self.mixer_panel,
            text='100% (原声音量)',
            text_color='gray60',
            width=105,
            anchor='w'
        )
        self.lbl_v_vol_disp.grid(row=1, column=2, padx=(0, 15))

        lbl_a_vol = ctk.CTkLabel(self.mixer_panel, text='🎵 背景配配音音量:')
        lbl_a_vol.grid(row=2, column=0, padx=15, pady=6, sticky='w')

        self.val_a_volume = ctk.CTkSlider(
            self.mixer_panel,
            from_=0.0,
            to=2.0,
            number_of_steps=20,
            command=self.update_mixer_lbls
        )
        self.val_a_volume.set(1.0)
        self.val_a_volume.grid(row=2, column=1, padx=10, pady=6, sticky='ew')

        self.lbl_a_vol_disp = ctk.CTkLabel(
            self.mixer_panel,
            text='100% (配音音量)',
            text_color='gray60',
            width=105,
            anchor='w'
        )
        self.lbl_a_vol_disp.grid(row=2, column=2, padx=(0, 15))

        lbl_align = ctk.CTkLabel(self.mixer_panel, text='🔗 长度截断对齐策略:')
        lbl_align.grid(row=3, column=0, padx=15, pady=8, sticky='w')

        self.val_align_mode = ctk.CTkOptionMenu(
            self.mixer_panel,
            values=[
                '对齐原视频长度 (若背景声长自动截断，保留完整视频)',
                '背景乐无限循环 (若视频长，自动循环背景声直至视频完结)',
                '对齐配音音频长度 (若音频短自动截断视频，以配音为准)',
                '双声道取最短对齐 (任意一方播放完毕，合成立即结束)'
            ]
        )
        self.val_align_mode.set('对齐原视频长度 (若背景声长自动截断，保留完整视频)')
        self.val_align_mode.grid(row=3, column=1, columnspan=2, padx=(10, 15), pady=8, sticky='ew')

        # Dub Crop Panel
        self.dub_crop_panel = ctk.CTkFrame(self.dubbing_panel, fg_color='#0F172A', corner_radius=8)
        self.dub_crop_panel.grid(row=2, column=0, pady=6, sticky='ew')
        self.dub_crop_panel.grid_columnconfigure((1, 3), weight=1)

        lbl_dub_crop_title = ctk.CTkLabel(
            self.dub_crop_panel,
            text='✂️ 双轨精准分段截取 (可选/留空默认采用上述截断对齐策略)',
            font=ctk.CTkFont(size=13, weight='bold'),
            text_color='#818CF8'
        )
        lbl_dub_crop_title.grid(row=0, column=0, columnspan=4, padx=15, pady=(10, 8), sticky='w')

        lbl_v_start = ctk.CTkLabel(self.dub_crop_panel, text='视频裁剪 起始(秒):')
        lbl_v_start.grid(row=1, column=0, padx=15, pady=5, sticky='w')

        self.entry_trim_v_start = ctk.CTkEntry(self.dub_crop_panel, placeholder_text='例如: 0.0')
        self.entry_trim_v_start.grid(row=1, column=1, padx=(0, 15), pady=5, sticky='ew')

        lbl_v_end = ctk.CTkLabel(self.dub_crop_panel, text='视频裁剪 结束(秒):')
        lbl_v_end.grid(row=1, column=2, padx=15, pady=5, sticky='w')

        self.entry_trim_v_end = ctk.CTkEntry(self.dub_crop_panel, placeholder_text='例如: 10.0')
        self.entry_trim_v_end.grid(row=1, column=3, padx=(0, 15), pady=5, sticky='ew')

        lbl_a_start = ctk.CTkLabel(self.dub_crop_panel, text='配音裁剪 起始(秒):')
        lbl_a_start.grid(row=2, column=0, padx=15, pady=5, sticky='w')

        self.entry_trim_a_start = ctk.CTkEntry(self.dub_crop_panel, placeholder_text='例如: 0.0')
        self.entry_trim_a_start.grid(row=2, column=1, padx=(0, 15), pady=5, sticky='ew')

        lbl_a_end = ctk.CTkLabel(self.dub_crop_panel, text='配音裁剪 结束(秒):')
        lbl_a_end.grid(row=2, column=2, padx=15, pady=5, sticky='w')

        self.entry_trim_a_end = ctk.CTkEntry(self.dub_crop_panel, placeholder_text='例如: 30.0')
        self.entry_trim_a_end.grid(row=2, column=3, padx=(0, 15), pady=5, sticky='ew')

        self.btn_dub_execute = ctk.CTkButton(
            self.dubbing_panel,
            text='🚀 一键混音合成配音视频',
            height=48,
            fg_color='#10B981',
            hover_color='#059669',
            font=ctk.CTkFont(size=15, weight='bold', family='Microsoft YaHei'),
            command=self.execute_dubbing
        )
        self.btn_dub_execute.grid(row=3, column=0, pady=(15, 10), sticky='ew')
        self.btn_dub_execute.configure(state='disabled')

    def dub_select_video(self):
        """Loads video file for dubbing mixer."""
        path = filedialog.askopenfilename(
            title='选择配音的源视频',
            filetypes=[('视频文件', '*.mp4 *.avi *.mkv *.mov *.webm *.flv'), ('全部文件', '*.*')]
        )
        if not path:
            return

        try:
            meta = self.app.video_processor.load_video(path)
            self.dub_video_duration = meta['duration']
            self.dub_video_loaded = True

            filename = os.path.basename(path)
            info = f"文件名: {filename}\n分辨率: {meta['width']}x{meta['height']}\n时长: {self.dub_video_duration:.2f} 秒"
            self.lbl_dub_video_info.configure(text=info, text_color='#10B981')

            self.entry_trim_v_start.delete(0, tk.END)
            self.entry_trim_v_end.delete(0, tk.END)
            self.entry_trim_v_end.insert(0, f"{self.dub_video_duration:.2f}")

            self.lbl_status.configure(text='视频加载成功！请继续在右侧卡片导入背景声配音文件...')
            self.check_dub_ready_state()
        except Exception as e:
            self.lbl_status.configure(text=f"视频加载失败: {str(e)}", text_color='#EF4444')
            messagebox.showerror('读取失败', f"无法解析该视频文件:\n{str(e)}")

    def check_dub_ready_state(self):
        """Enables synthetic run button only when both source files are ready."""
        if self.dub_video_loaded and self.dub_audio_loaded:
            self.btn_dub_execute.configure(state='normal')
        else:
            self.btn_dub_execute.configure(state='disabled')

    def update_mixer_lbls(self, val=None):
        """Updates faders status indicator labels."""
        v_vol = self.val_v_volume.get()
        a_vol = self.val_a_volume.get()

        v_pct = int(v_vol * 100)
        v_suffix = ' (原音静音)' if v_vol == 0.0 else (' (原声放大)' if v_vol > 1.0 else '')
        self.lbl_v_vol_disp.configure(text=f"{v_pct}%{v_suffix}")

        a_pct = int(a_vol * 100)
        a_suffix = ' (配音静音)' if a_vol == 0.0 else (' (配音放大)' if a_vol > 1.0 else '')
        self.lbl_a_vol_disp.configure(text=f"{a_pct}%{a_suffix}")

    def execute_dubbing(self):
        """Triggers audio-video mixing compiler."""
        if not self.dub_video_loaded or not self.dub_audio_loaded:
            return

        video_path = self.app.video_processor.file_path
        if not (video_path and os.path.exists(video_path)):
            video_path = filedialog.askopenfilename(
                title='校验视频原路径',
                initialfile=os.path.basename(self.app.video_processor.file_path) if self.app.video_processor.file_path else None
            )

        if not video_path:
            return

        try:
            v_start_val = self.entry_trim_v_start.get().strip()
            v_start = float(v_start_val) if v_start_val else None

            v_end_val = self.entry_trim_v_end.get().strip()
            v_end = float(v_end_val) if v_end_val else None

            a_start_val = self.entry_trim_a_start.get().strip()
            a_start = float(a_start_val) if a_start_val else None

            a_end_val = self.entry_trim_a_end.get().strip()
            a_end = float(a_end_val) if a_end_val else None
        except ValueError:
            messagebox.showerror('参数格式错误', '裁剪的微调时间范围必须输入有效的数值！')
            return

        if v_start is not None and v_end is not None and v_start >= v_end:
            messagebox.showerror('区间错误', '视频裁剪起始点必须小于结束点！')
            return

        if a_start is not None and a_end is not None and a_start >= a_end:
            messagebox.showerror('区间错误', '配音裁剪起始点必须小于结束点！')
            return

        align_str = self.val_align_mode.get()
        align_mode = 'video'
        if '背景乐无限循环' in align_str:
            align_mode = 'loop_audio'
        elif '对齐配音音频长度' in align_str:
            align_mode = 'audio'
        elif '双声道取最短对齐' in align_str:
            align_mode = 'shortest'

        options = {
            'v_volume': self.val_v_volume.get(),
            'a_volume': self.val_a_volume.get(),
            'align_mode': align_mode,
            'v_start': v_start,
            'v_end': v_end,
            'a_start': a_start,
            'a_end': a_end
        }

        if not (hasattr(self, 'imported_audio_path') and os.path.exists(self.imported_audio_path)):
            messagebox.showerror('配音源失效', '导入的背景音频源文件已失效，请重新导入！')
            return

        audio_path = self.imported_audio_path

        default_name = os.path.splitext(os.path.basename(video_path))[0] + '_dubbed.mp4'
        save_path = filedialog.asksaveasfilename(
            title='选择合成后的配音视频保存路径',
            initialfile=default_name,
            defaultextension='.mp4',
            filetypes=[('MP4 Video', '*.mp4')]
        )

        if not save_path:
            return

        self.btn_dub_execute.configure(state='disabled')
        self.btn_dub_select_v.configure(state='disabled')
        self.btn_dub_select_a.configure(state='disabled')
        self.progress_bar.set(0)
        self.lbl_status.configure(text='正在调度 FFmpeg 进行多轨道高保真配音混音压制...')

        t = threading.Thread(
            target=self._threaded_dubbing,
            args=(video_path, audio_path, save_path, options),
            daemon=True
        )
        t.start()

    def dub_select_audio(self):
        """Loads audio file for dubbing mixer and sets imported_audio_path."""
        path = filedialog.askopenfilename(
            title='选择配音或背景乐音频文件',
            filetypes=[
                ('音频文件', '*.mp3 *.wav *.flac *.aac *.m4a *.wma *.ogg'),
                ('全部文件', '*.*')
            ]
        )
        if not path:
            return

        try:
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            import subprocess
            chk_cmd = [ffmpeg_exe, '-i', path]
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.Popen(
                chk_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo
            )
            stdout, stderr = process.communicate()
            output = stderr.decode('utf-8', errors='ignore') + stdout.decode('utf-8', errors='ignore')

            duration = 0.0
            if 'Duration:' in output:
                dur_str = output.split('Duration:')[1].split(',')[0].strip()
                h, m, s = dur_str.split(':')
                duration = float(h) * 3600 + float(m) * 60 + float(s)

            self.dub_audio_duration = duration if duration > 0.0 else 100.0
            self.imported_audio_path = path
            self.dub_audio_loaded = True

            filename = os.path.basename(path)
            ext = path.split('.')[-1].upper()
            info = f"文件名: {filename}\n音频格式: {ext}\n时长: {self.dub_audio_duration:.2f} 秒"
            self.lbl_dub_audio_info.configure(text=info, text_color='#06B6D4')

            self.entry_trim_a_start.delete(0, tk.END)
            self.entry_trim_a_end.delete(0, tk.END)
            self.entry_trim_a_end.insert(0, f"{self.dub_audio_duration:.2f}")

            self.lbl_status.configure(text='配音音频导入成功！请微调下方的调音推子与截断选项，开始合成')
            self.check_dub_ready_state()
        except Exception as e:
            self.lbl_status.configure(text=f"音频解析失败: {str(e)}", text_color='#EF4444')
            messagebox.showerror('读取失败', f"无法解析该音频文件，请确保格式正确:\n{str(e)}")

    def _threaded_dubbing(self, video_path, audio_path, save_path, options):
        def update_progress(val, status_txt):
            self.after(0, lambda: self.progress_bar.set(val))
            self.after(0, lambda: self.lbl_status.configure(text=status_txt))

        try:
            self.app.video_processor.merge_video_audio(
                video_path,
                audio_path,
                save_path,
                options,
                progress_callback=update_progress
            )
            self.after(0, lambda: self.on_dub_success(save_path))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror('配音合成失败', f"FFmpeg 混音时出错:\n{str(e)}"))
            self.after(0, lambda: self.lbl_status.configure(text=f"混音合成失败: {str(e)}", text_color='#EF4444'))
            self.after(0, lambda: self.progress_bar.set(0))
        finally:
            self.after(0, lambda: self.btn_dub_execute.configure(state='normal'))
            self.after(0, lambda: self.btn_dub_select_v.configure(state='normal'))
            self.after(0, lambda: self.btn_dub_select_a.configure(state='normal'))

    def on_dub_success(self, save_path):
        self.progress_bar.set(1.0)
        filename = os.path.basename(save_path)
        self.lbl_status.configure(text=f"多轨视频配音混音成功！已保存至 {filename}", text_color='#10B981')
        messagebox.showinfo('配音合成成功', f"恭喜！您的配音视频已经成功多轨混音合成！\n\n文件保存路径:\n{save_path}")

    def create_bottom_progress(self):
        self.bottom_frame = ctk.CTkFrame(self.main_panel, fg_color='transparent')
        self.bottom_frame.grid(row=4, column=0, padx=30, pady=(15, 25), sticky='ew')
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(
            self.bottom_frame,
            text='等待载入影音素材...',
            text_color='gray60',
            anchor='w',
            font=ctk.CTkFont(size=12)
        )
        self.lbl_status.grid(row=0, column=0, pady=(0, 4), sticky='ew')

        self.progress_bar = ctk.CTkProgressBar(
            self.bottom_frame,
            fg_color='#0F172A',
            progress_color='#10B981'
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, sticky='ew')
