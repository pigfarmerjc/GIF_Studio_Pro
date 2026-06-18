# ============================================================
# Module: yt_downloader_tab.py
# Reconstructed from Python 3.14 bytecode
# ============================================================

import os
import io
import threading
import urllib.request as urllib
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from yt_downloader import YtDownloader


class YtDownloaderTab(ctk.CTkFrame):
    """
    Web Video Downloader Tab Panel. Provides high-fidelity link parsing,
    asynchronous thumbnail rendering, speed-monitored downloader streams,
    and automatic workflow transitions.
    """

    def __init__(self, master, app):
        super().__init__(master, fg_color='transparent')
        self.app = app
        self.downloader = YtDownloader()
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.parsed_metadata = None
        self.parsed_url = ''
        self.download_finished = False
        self.last_download_path = ''
        self.cookie_file_path = None
        self.create_top_input_panel()
        self.create_main_content_panel()
        self.create_bottom_progress_panel()

    def on_show(self):
        pass

    def create_top_input_panel(self):
        """Builds URL input row and cookie authorization options at the top."""
        self.input_frame = ctk.CTkFrame(self, fg_color='#1E293B', corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky='ew')
        self.input_frame.grid_columnconfigure(1, weight=1)

        lbl = ctk.CTkLabel(
            self.input_frame,
            text='🔗 网页多媒体 URL:',
            font=ctk.CTkFont(weight='bold', family='Microsoft YaHei')
        )
        lbl.grid(row=0, column=0, padx=(15, 10), pady=15)

        self.entry_url = ctk.CTkEntry(
            self.input_frame,
            placeholder_text='支持抓取解析 Instagram (图片/视频)、Bilibili (哔哩哔哩)、YouTube、抖音、TikTok、Twitter等链接...'
        )
        self.entry_url.grid(row=0, column=1, padx=(0, 15), pady=15, sticky='ew')

        self.btn_analyze = ctk.CTkButton(
            self.input_frame,
            text='🔍 一键智能解析',
            width=120,
            fg_color='#6366F1',
            hover_color='#4F46E5',
            font=ctk.CTkFont(weight='bold', family='Microsoft YaHei'),
            command=self.start_url_analysis
        )
        self.btn_analyze.grid(row=0, column=2, padx=(0, 15), pady=15)

        cookie_row = ctk.CTkFrame(self.input_frame, fg_color='transparent')
        cookie_row.grid(row=1, column=0, columnspan=3, padx=15, pady=(0, 12), sticky='ew')
        cookie_row.grid_columnconfigure(1, weight=1)

        lbl_cookie = ctk.CTkLabel(
            cookie_row,
            text='🔑 Cookie 授权 (解析/下载失败或要求登录时选用):',
            font=ctk.CTkFont(size=12, family='Microsoft YaHei'),
            text_color='gray60'
        )
        lbl_cookie.grid(row=0, column=0, padx=(0, 10), sticky='w')

        browser_selector_frame = ctk.CTkFrame(cookie_row, fg_color='transparent')
        browser_selector_frame.grid(row=0, column=1, sticky='ew')
        browser_selector_frame.grid_columnconfigure(4, weight=1)

        lbl_browser = ctk.CTkLabel(
            browser_selector_frame,
            text='浏览器提取:',
            font=ctk.CTkFont(size=11, family='Microsoft YaHei'),
            text_color='gray50'
        )
        lbl_browser.grid(row=0, column=0, padx=(0, 5), sticky='w')

        self.option_cookies_browser = ctk.CTkOptionMenu(
            browser_selector_frame,
            values=['🌐 自动探测浏览器 (推荐)', '无 (默认)', 'Chrome', 'Edge', 'Firefox', 'Opera', 'Safari', 'Vivaldi'],
            width=180,
            height=28,
            fg_color='#334155',
            command=self.on_browser_changed
        )
        self.option_cookies_browser.set('🌐 自动探测浏览器 (推荐)')
        self.option_cookies_browser.grid(row=0, column=1, sticky='w')

        lbl_or = ctk.CTkLabel(
            browser_selector_frame,
            text=' 或 ',
            font=ctk.CTkFont(size=12, family='Microsoft YaHei'),
            text_color='gray40'
        )
        lbl_or.grid(row=0, column=2, padx=10, sticky='w')

        self.btn_select_cookie_file = ctk.CTkButton(
            browser_selector_frame,
            text='📂 导入 cookies.txt',
            width=120,
            height=28,
            fg_color='#475569',
            hover_color='#64748B',
            font=ctk.CTkFont(size=11, family='Microsoft YaHei'),
            command=self.import_cookie_file
        )
        self.btn_select_cookie_file.grid(row=0, column=3, sticky='w')

        self.lbl_cookie_file_status = ctk.CTkLabel(
            browser_selector_frame,
            text='未载入文本',
            font=ctk.CTkFont(size=11, family='Microsoft YaHei'),
            text_color='gray40'
        )
        self.lbl_cookie_file_status.grid(row=0, column=4, padx=(10, 0), sticky='w')

    def create_main_content_panel(self):
        """Swappable panel for placeholder vs analyzed video metadata card."""
        self.content_container = ctk.CTkFrame(self, fg_color='#1E293B', corner_radius=10)
        self.content_container.grid(row=1, column=0, padx=0, pady=0, sticky='nsew')
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        self.lbl_placeholder = ctk.CTkLabel(
            self.content_container,
            text='🌐 极客多媒体抓取中心\n\n在上方粘贴网页链接并解析，将自动获取所有流数据画质分流',
            text_color='gray40',
            font=ctk.CTkFont(size=14, family='Microsoft YaHei')
        )
        self.lbl_placeholder.grid(row=0, column=0, sticky='nsew', padx=20, pady=80)

        self.card_frame = ctk.CTkFrame(self.content_container, fg_color='transparent')
        self.card_frame.grid_columnconfigure(1, weight=1)
        self.card_frame.grid_rowconfigure(0, weight=1)

        self.thumbnail_frame = ctk.CTkFrame(self.card_frame, fg_color='#0F172A', width=260, height=150, corner_radius=8)
        self.thumbnail_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky='nsew')
        self.thumbnail_frame.grid_rowconfigure(0, weight=1)
        self.thumbnail_frame.grid_columnconfigure(0, weight=1)

        self.lbl_cover = ctk.CTkLabel(self.thumbnail_frame, text='⏳ 正在加载网络封面...')
        self.lbl_cover.grid(row=0, column=0, padx=10, pady=10)

        self.details_frame = ctk.CTkFrame(self.card_frame, fg_color='transparent')
        self.details_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky='nsew')
        self.details_frame.grid_columnconfigure(1, weight=1)

        self.lbl_title = ctk.CTkLabel(
            self.details_frame,
            text='视频标题加载中...',
            justify='left',
            anchor='w',
            font=ctk.CTkFont(size=16, weight='bold', family='Microsoft YaHei'),
            text_color='white'
        )
        self.lbl_title.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 6))

        self.lbl_author = ctk.CTkLabel(
            self.details_frame,
            text='创作者: --',
            text_color='#818CF8',
            anchor='w'
        )
        self.lbl_author.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 4))

        self.lbl_duration = ctk.CTkLabel(
            self.details_frame,
            text='总时长: --',
            text_color='gray50',
            anchor='w'
        )
        self.lbl_duration.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 15))

        lbl_res = ctk.CTkLabel(self.details_frame, text='高清画质/声道选择:')
        lbl_res.grid(row=3, column=0, sticky='w', pady=5)

        self.option_resolution = ctk.CTkOptionMenu(self.details_frame)
        self.option_resolution.grid(row=3, column=1, sticky='ew', padx=(10, 0), pady=5)

        lbl_save = ctk.CTkLabel(self.details_frame, text='保存文件路径:')
        lbl_save.grid(row=4, column=0, sticky='w', pady=5)

        self.save_path_row = ctk.CTkFrame(self.details_frame, fg_color='transparent')
        self.save_path_row.grid(row=4, column=1, sticky='ew', padx=(10, 0), pady=5)
        self.save_path_row.grid_columnconfigure(0, weight=1)

        self.entry_save_path = ctk.CTkEntry(self.save_path_row, placeholder_text='选择保存路径...')
        self.entry_save_path.grid(row=0, column=0, sticky='ew', padx=(0, 8))

        self.btn_select_dir = ctk.CTkButton(
            self.save_path_row,
            text='📂 浏览',
            width=70,
            fg_color='#475569',
            hover_color='#64748B',
            command=self.browse_save_path
        )
        self.btn_select_dir.grid(row=0, column=1)

    def create_bottom_progress_panel(self):
        """Action Button and Threaded progress bars at the bottom."""
        self.bottom_frame = ctk.CTkFrame(self, fg_color='#1E293B', corner_radius=10)
        self.bottom_frame.grid(row=2, column=0, padx=0, pady=(10, 0), sticky='ew')
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.btn_download = ctk.CTkButton(
            self.bottom_frame,
            text='🚀 开始高品质极速抓取并自动合并',
            height=45,
            fg_color='#10B981',
            hover_color='#059669',
            font=ctk.CTkFont(size=15, weight='bold', family='Microsoft YaHei'),
            command=self.start_download
        )
        self.btn_download.grid(row=0, column=0, padx=20, pady=(15, 10), sticky='ew')
        self.btn_download.configure(state='disabled')

        self.lbl_status = ctk.CTkLabel(
            self.bottom_frame,
            text='等待输入链接并解析...',
            text_color='gray60',
            anchor='w',
            font=ctk.CTkFont(size=12)
        )
        self.lbl_status.grid(row=1, column=0, padx=20, pady=(0, 2), sticky='ew')

        self.progress_bar = ctk.CTkProgressBar(
            self.bottom_frame,
            fg_color='#0F172A',
            progress_color='#818CF8'
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, padx=20, pady=(0, 15), sticky='ew')

    def start_url_analysis(self):
        """Launches background thread for parsing url details with browser cookies if selected."""
        url = self.entry_url.get().strip()
        if not url:
            messagebox.showwarning('链接为空', '请输入需要解析的网页视频链接！')
            return

        self.btn_analyze.configure(state='disabled')
        self.btn_download.configure(state='disabled')
        self.lbl_status.configure(text='正在高精解析网页多媒体接口，解密加密签名...', text_color='gray60')
        self.progress_bar.set(0.2)

        self.lbl_placeholder.grid()
        self.card_frame.grid_remove()

        browser = self.option_cookies_browser.get()
        t = threading.Thread(
            target=self._threaded_analyze,
            args=(url, browser, self.cookie_file_path),
            daemon=True
        )
        t.start()

    def _threaded_analyze(self, url, browser, cookie_file):
        res = self.downloader.get_video_info(url, browser_name=browser, cookie_file=cookie_file)
        if res.get('success'):
            self.parsed_metadata = res
            self.parsed_url = url
            self.after(0, lambda: self.on_analysis_success(res))
        else:
            self.after(0, lambda: self.on_analysis_failed(res['error']))

    def on_analysis_success(self, meta):
        """Builds formats lists and loads uploader info onto UI card."""
        self.lbl_placeholder.grid_remove()
        self.card_frame.grid(row=0, column=0, sticky='nsew')

        title = meta['title']
        if len(title) > 42:
            title = title[:40] + '...'
        self.lbl_title.configure(text=title)
        self.lbl_author.configure(text=f"创作者: 👤 {meta['uploader']}")

        sec = meta['duration']
        if sec > 0:
            m, s = divmod(int(sec), 60)
            h, m = divmod(m, 60)
            if h > 0:
                dur_str = f"{h:02d}:{m:02d}:{s:02d}"
            else:
                dur_str = f"{m:02d}:{s:02d}"
            self.lbl_duration.configure(text=f"总时长: ⏱️ {dur_str}")
        else:
            self.lbl_duration.configure(text="总时长: ⏱️ 帖子/图文多媒体")

        self.res_list = meta['resolutions']
        option_values = [item[1] for item in self.res_list]
        self.option_resolution.configure(values=option_values)
        self.option_resolution.set(option_values[0])

        downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        safe_title = "".join([c for c in meta['title'] if c.isalpha() or c.isdigit() or c in ' _-']).rstrip()
        safe_title = safe_title[:45]

        is_playlist = meta.get('is_playlist', False)
        ext = '.jpg' if is_playlist else '.mp4'
        default_file = os.path.join(downloads_dir, f"{safe_title}{ext}")

        self.entry_save_path.delete(0, tk.END)
        self.entry_save_path.insert(0, default_file)

        self.lbl_cover.configure(text='⏳ 正在加载网络封面...')
        cover_t = threading.Thread(target=self._threaded_load_cover, args=(meta['thumbnail'],), daemon=True)
        cover_t.start()

        self.btn_analyze.configure(state='normal')
        self.btn_download.configure(state='normal')
        self.lbl_status.configure(text='网页解析成功！请选择画质与保存路径，开始极速下载', text_color='#10B981')
        self.progress_bar.set(0)

    def _threaded_load_cover(self, img_url):
        """Asynchronously downloads network uploader thumbnail."""
        if not img_url:
            self.after(0, lambda: self.lbl_cover.configure(text='❌ 暂无封面图'))
            return

        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img_data = response.read()
            pil_img = Image.open(io.BytesIO(img_data)).convert('RGBA')
            resized = pil_img.resize((240, 135), Image.Resampling.LANCZOS)
            self.after(0, lambda: self.display_cover_image(resized))
        except Exception as e:
            print(f"Error drawing web thumbnail: {e}")
            self.after(0, lambda: self.lbl_cover.configure(text='❌ 封面下载失败'))

    def display_cover_image(self, pil_img):
        """Renders PIL image to labels."""
        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(240, 135))
        self.lbl_cover.destroy()
        self.lbl_cover = ctk.CTkLabel(self.thumbnail_frame, image=ctk_img, text='')
        self.lbl_cover.grid(row=0, column=0, padx=5, pady=5)

    def on_analysis_failed(self, err_msg):
        self.btn_analyze.configure(state='normal')
        self.progress_bar.set(0)
        self.lbl_status.configure(
            text=f"解析失败: {err_msg[:45]}...",
            text_color='#EF4444'
        )
        messagebox.showerror(
            '解析失败',
            f"无法解析该网页链接。可能由于 network未连接，或者链接暂不支持:\n\n{err_msg}"
        )

    def browse_save_path(self):
        if not self.parsed_metadata:
            return

        choice = self.option_resolution.get()
        is_audio = '音频' in choice
        is_playlist = self.parsed_metadata.get('is_playlist', False)

        if is_audio:
            ext = '.mp3'
        elif is_playlist:
            ext = '.jpg'
        else:
            ext = '.mp4'

        default_file = os.path.basename(self.entry_save_path.get())
        if not default_file.endswith(ext):
            default_file = os.path.splitext(default_file)[0] + ext

        path = filedialog.asksaveasfilename(
            title='选择抓取流保存的路径前缀',
            initialfile=default_file,
            defaultextension=ext,
            filetypes=[('媒体文件', f"*{ext}")]
        )

        if path:
            self.entry_save_path.delete(0, tk.END)
            self.entry_save_path.insert(0, path)

    def start_download(self):
        """Starts background download operation."""
        if not self.parsed_metadata:
            return

        save_path = self.entry_save_path.get().strip()
        if not save_path:
            messagebox.showwarning('路径空', '请选择保存目标文件路径！')
            return

        choice_text = self.option_resolution.get()
        resolution_choice = 'audio'
        for h, text in self.res_list:
            if text == choice_text:
                resolution_choice = str(h)
                break

        is_playlist = self.parsed_metadata.get('is_playlist', False)
        if resolution_choice == 'audio':
            ext = '.mp3'
        elif resolution_choice == 'playlist':
            ext = '.jpg'
        else:
            ext = '.mp4'

        if not save_path.endswith(ext):
            save_path = os.path.splitext(save_path)[0] + ext
            self.entry_save_path.delete(0, tk.END)
            self.entry_save_path.insert(0, save_path)

        self.btn_download.configure(state='disabled')
        self.btn_analyze.configure(state='disabled')
        self.btn_select_dir.configure(state='disabled')
        self.progress_bar.set(0)
        self.lbl_status.configure(text='正在连接谷歌多媒体服务器，启动多通道下载...')

        browser = self.option_cookies_browser.get()
        cookie_config = self.parsed_metadata.get('cookie_config') if self.parsed_metadata else None

        t = threading.Thread(
            target=self._threaded_download,
            args=(self.parsed_url, resolution_choice, save_path, browser, self.cookie_file_path, cookie_config),
            daemon=True
        )
        t.start()

    def _threaded_download(self, url, choice, save_path, browser, cookie_file, cookie_config):
        def update_progress(percent, speed_mb, status_txt):
            if speed_mb > 0.0:
                info = f"{status_txt} | 进度: {percent * 100:.1f}% | 速度: {speed_mb:.2f} MB/s"
            else:
                info = f"{status_txt} | 进度: {percent * 100:.1f}%"
            self.after(0, lambda: self.progress_bar.set(percent))
            self.after(0, lambda: self.lbl_status.configure(text=info))

        try:
            self.downloader.download_video(
                url,
                choice,
                save_path,
                progress_callback=update_progress,
                browser_name=browser,
                cookie_file=cookie_file,
                cookie_config=cookie_config
            )
            self.after(0, lambda: self.on_download_success(save_path, choice))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror('下载失败', f"抓取合并过程中出错:\n{str(e)}"))
            self.after(0, lambda: self.lbl_status.configure(text=f"抓取失败: {str(e)}", text_color='#EF4444'))
            self.after(0, lambda: self.progress_bar.set(0))
        finally:
            self.after(0, lambda: self.btn_download.configure(state='normal'))
            self.after(0, lambda: self.btn_analyze.configure(state='normal'))
            self.after(0, lambda: self.btn_select_dir.configure(state='normal'))

    def on_download_success(self, save_path, choice):
        """Displays redirect options upon successful download."""
        self.progress_bar.set(1.0)
        filename = os.path.basename(save_path)
        if choice == 'playlist':
            self.lbl_status.configure(
                text=f"帖子内容全部下载保存成功！存入目录: {os.path.dirname(save_path)}",
                text_color='#10B981'
            )
        else:
            self.lbl_status.configure(
                text=f"多媒体合并成功！文件已存入: {filename}",
                text_color='#10B981'
            )
        self.last_download_path = save_path
        self.show_redirect_dialog(save_path, choice)

    def show_redirect_dialog(self, save_path, choice):
        """Spawns workflow redirects modal popups."""
        redirect_win = ctk.CTkToplevel(self)
        redirect_win.title('🎉 下载与轨道混流成功！')
        redirect_win.geometry('450x300')
        redirect_win.minsize(400, 260)
        redirect_win.lift()
        redirect_win.grab_set()

        redirect_win.grid_columnconfigure(0, weight=1)
        redirect_win.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(redirect_win, fg_color='transparent')
        container.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        container.grid_columnconfigure(0, weight=1)

        title_str = '🎉 网页多媒体帖子极速抓取成功！' if choice == 'playlist' else '🎉 网页视频极速下载合并成功！'
        lbl_title = ctk.CTkLabel(
            container,
            text=title_str,
            font=ctk.CTkFont(size=16, weight='bold', family='Microsoft YaHei'),
            text_color='#10B981'
        )
        lbl_title.grid(row=0, column=0, pady=(0, 8))

        if choice == 'playlist':
            desc_str = f"帖子内容已成功保存至 Downloads 目录。\n前缀文件为:\n{os.path.basename(save_path)}\n\n由于包含多个图片/视频文件，您可以打开文件夹查看全部。"
        else:
            desc_str = f"文件已保存至 Downloads 目录，名称为:\n{os.path.basename(save_path)}\n\n现在，您是否希望直接一键导入到创作面板开始编辑？"

        lbl_desc = ctk.CTkLabel(
            container,
            text=desc_str,
            font=ctk.CTkFont(size=12, family='Microsoft YaHei'),
            text_color='gray80'
        )
        lbl_desc.grid(row=1, column=0, pady=(0, 20))

        btn_frame = ctk.CTkFrame(container, fg_color='transparent')
        btn_frame.grid(row=2, column=0, sticky='ew')
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        def go_to_gif():
            if choice == 'playlist':
                messagebox.showwarning('格式不匹配', '当前下载的是多图帖子，无法直接进行视频转 GIF！')
                return
            if choice == 'audio':
                messagebox.showwarning('格式不匹配', '当前提取的是音频格式，无法进行视频转 GIF！')
                return
            redirect_win.grab_release()
            redirect_win.destroy()
            self.app.select_tab('VideoToGif')
            self.app.frames['VideoToGif'].load_video_file(save_path)

        def go_to_studio():
            if choice == 'playlist':
                messagebox.showwarning('格式不匹配', '当前下载的是多图多媒体帖子，不支持直接带入影音调音台混音！已为您保存全部图片。')
                return
            redirect_win.grab_release()
            redirect_win.destroy()
            self.app.select_tab('AudioExtract')

            audio_extract_frame = self.app.frames['AudioExtract']

            if choice == 'audio':
                audio_extract_frame.mode_selector.set('🎬 视频配音与多轨混音工作台')
                audio_extract_frame.switch_mode('🎬 视频配音与多轨混音工作台')
                audio_extract_frame.entry_trim_a_start.delete(0, tk.END)
                audio_extract_frame.entry_trim_a_end.delete(0, tk.END)

                import imageio_ffmpeg
                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                import subprocess
                chk_cmd = [ffmpeg_exe, '-i', save_path]
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

                audio_extract_frame.dub_audio_duration = duration if duration > 0.0 else 10.0
                audio_extract_frame.imported_audio_path = save_path
                audio_extract_frame.dub_audio_loaded = True

                filename = os.path.basename(save_path)
                info = f"文件名: {filename}\n音频格式: MP3\n时长: {audio_extract_frame.dub_audio_duration:.2f} 秒"
                audio_extract_frame.lbl_dub_audio_info.configure(text=info, text_color='#06B6D4')
                audio_extract_frame.entry_trim_a_end.insert(0, f"{audio_extract_frame.dub_audio_duration:.2f}")
                audio_extract_frame.lbl_status.configure(text='网页配音音频一键带入调音台！请继续导入视频源...')
                audio_extract_frame.check_dub_ready_state()
            else:
                audio_extract_frame.mode_selector.set('🎬 视频配音与多轨混音工作台')
                audio_extract_frame.switch_mode('🎬 视频配音与多轨混音工作台')
                audio_extract_frame.entry_video_path = save_path

                try:
                    meta = self.app.video_processor.load_video(save_path)
                    audio_extract_frame.dub_video_duration = meta['duration']
                    audio_extract_frame.dub_video_loaded = True

                    filename = os.path.basename(save_path)
                    info = f"文件名: {filename}\n分辨率: {meta['width']}x{meta['height']}\n时长: {meta['duration']:.2f} 秒"
                    audio_extract_frame.lbl_dub_video_info.configure(text=info, text_color='#10B981')
                    audio_extract_frame.entry_trim_v_start.delete(0, tk.END)
                    audio_extract_frame.entry_trim_v_end.delete(0, tk.END)
                    audio_extract_frame.entry_trim_v_end.insert(0, f"{meta['duration']:.2f}")
                    audio_extract_frame.lbl_status.configure(text='网页视频源一键带入混音工作台！请继续导入背景声配音...')
                    audio_extract_frame.check_dub_ready_state()
                except Exception as e:
                    messagebox.showerror('导入失败', f"无法加载视频: {e}")

        btn_gif = ctk.CTkButton(
            btn_frame,
            text='🎥 直接导入视频转 GIF',
            fg_color='#6366F1',
            hover_color='#4F46E5',
            height=36,
            command=go_to_gif
        )
        btn_gif.grid(row=0, column=0, padx=(0, 4), sticky='ew')

        btn_studio = ctk.CTkButton(
            btn_frame,
            text='🎬 导入影音工作室混音',
            fg_color='#06B6D4',
            hover_color='#0891B2',
            height=36,
            command=go_to_studio
        )
        btn_studio.grid(row=0, column=1, padx=(4, 0), sticky='ew')

        btn_action_row = ctk.CTkFrame(container, fg_color='transparent')
        btn_action_row.grid(row=3, column=0, sticky='ew', pady=(12, 0))
        btn_action_row.grid_columnconfigure((0, 1), weight=1)

        def open_folder():
            try:
                import subprocess
                subprocess.Popen(f'explorer /select,"{os.path.normpath(save_path)}"')
            except Exception as e:
                print(f"Error opening folder: {e}")

        btn_folder = ctk.CTkButton(
            btn_action_row,
            text='📂 打开文件位置',
            fg_color='#475569',
            hover_color='#64748B',
            height=32,
            command=open_folder
        )
        btn_folder.grid(row=0, column=0, padx=(0, 4), sticky='ew')

        btn_close = ctk.CTkButton(
            btn_action_row,
            text='✕ 关闭',
            fg_color='#334155',
            hover_color='#475569',
            height=32,
            command=lambda: redirect_win.destroy()
        )
        btn_close.grid(row=0, column=1, padx=(4, 0), sticky='ew')

        redirect_win.protocol('WM_DELETE_WINDOW', lambda: redirect_win.destroy())

    def on_browser_changed(self, choice):
        if choice != '无 (默认)':
            self.cookie_file_path = None
            self.lbl_cookie_file_status.configure(text='未载入文本', text_color='gray40')

    def import_cookie_file(self):
        """Loads a cookies.txt file manually."""
        path = filedialog.askopenfilename(
            title='选择已导出的 cookies.txt 文件',
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
        )
        if path:
            self.cookie_file_path = path
            filename = os.path.basename(path)
            if len(filename) > 15:
                filename = filename[:12] + '...'
            self.lbl_cookie_file_status.configure(text=f"已载入: {filename}", text_color='#10B981')
            self.option_cookies_browser.set('无 (默认)')
            self.lbl_status.configure(
                text=f"已成功加载本地 Cookie 文件: {filename}。开始解析吧！",
                text_color='#10B981'
            )
        else:
            self.cookie_file_path = None
            self.lbl_cookie_file_status.configure(text='未载入文本', text_color='gray40')
