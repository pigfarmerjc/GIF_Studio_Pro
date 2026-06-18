import os
import yt_dlp
import imageio_ffmpeg


class YtDownloader:
    """YtDownloader"""

    def __init__(self):
        try:
            self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            self.ffmpeg_dir = os.path.dirname(self.ffmpeg_exe)
        except Exception as e:
            print(f'Error locating FFmpeg for yt-dlp: {str(e)}')
            self.ffmpeg_dir = None

    def get_video_info(self, url, browser_name, cookie_file):
        """
        Parses video page URL and extracts title, thumbnail, duration, 
        author/uploader, and available high-quality video/audio stream resolutions.
        Supports loading browser cookies or manual cookies.txt to download protected/Instagram media.
        """
        ydl_opts_list = []
        if cookie_file and os.path.exists(cookie_file):
            ydl_opts_list = [{'cookiefile': cookie_file}]
        elif browser_name and browser_name != '无 (默认)' and browser_name != 'None' and '自动' not in browser_name:
            ydl_opts_list = [{'cookiesfrombrowser': (browser_name.lower(),)}]
        else:
            ydl_opts_list = []
            candidates = ['chrome', 'edge', 'firefox', 'opera', 'vivaldi']
            import sys
            if sys.platform != 'win32':
                candidates.append('safari')
            for c in candidates:
                ydl_opts_list.append({'cookiesfrombrowser': (c,)})

        base_opts = {
            'skip_download': True,
            'quiet': True,
            'no_warnings': True
        }
        import shutil
        node_path = shutil.which('node')
        if node_path:
            base_opts['js_runtimes'] = {'node': {'path': node_path}}

        last_error = None
        info = None
        successful_config = {}
        has_auth_error = False

        for opt in ydl_opts_list:
            ydl_opts = base_opts.copy()
            ydl_opts.update(opt)
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    successful_config = opt
                    break
            except Exception as e:
                last_error = e
                err_str = str(e).lower()
                if 'unsupported url' in err_str or 'not a valid url' in err_str:
                    break
                if ("confirm you're not a bot" in err_str or 
                    'sign in' in err_str or 
                    'login' in err_str or 
                    '403' in err_str or 
                    'copy chrome cookie database' in err_str):
                    has_auth_error = True

        if info is None:
            friendly_err = ''
            if has_auth_error:
                friendly_err = (
                    '【🔒 人机验证与登录限制拦截】\n\n目标网页要求登录，或触发了安全人机验证拦截。\n'
                    '虽然软件尝试自动从您电脑的 Chrome/Edge 等浏览器提取 Cookie 登录凭证，但均未成功。这通常是由于：\n'
                    ' 1. 您的 Chrome/Edge 浏览器正处于开启状态，其 Cookie 数据库已被系统进程锁定；\n'
                    ' 2. 您未在浏览器中登录该目标网站的账号，或 Cookie 已过期。\n\n'
                    '💡 极客推荐解决方案（100% 成功破译防爬）：\n'
                    ' 1. 在浏览器安装 Cookie 导出插件（如 Get cookies.txt LOCALLY）；\n'
                    ' 2. 登录该目标网站（如 YouTube 或 Instagram）；\n'
                    ' 3. 点击浏览器插件图标，将 Cookie 导出为 `cookies.txt` 文本文件；\n'
                    ' 4. 点击本软件顶部的【📂 导入 cookies.txt】按钮载入该文件，即可成功破译并极速抓取！'
                )
            else:
                friendly_err = f'解析失败：{str(last_error)}\n\n提示：请确认您的链接正确无误，且网络可以正常访问该网站。如果该内容需要登录才能观看，请点击上方【导入 cookies.txt】载入登录凭证。'
            return {'success': False, 'error': friendly_err}

        try:
            title = info.get('title') or info.get('description') or '未知视频/帖子标题'
            if len(title) > 80:
                title = title[:80] + '...'
            thumbnail = info.get('thumbnail', '')
            duration = info.get('duration', 0) or 0
            uploader = info.get('uploader') or info.get('uploader_id') or '未知创作者'

            entries = info.get('entries')
            if entries is not None or info.get('_type') == 'playlist':
                entries_list = list(entries) if entries is not None else []
                num_entries = len(entries_list)
                if not thumbnail and num_entries > 0:
                    thumbnail = entries_list[0].get('thumbnail', '')

                resolutions = [('playlist', f'📥 下载帖子中的全部多媒体 (共 {num_entries} 张图片/视频)')]
                resolutions.append(('audio', '仅下载第一轨高保真音频 (MP3 格式)'))

                return {
                    'success': True,
                    'title': title,
                    'thumbnail': thumbnail,
                    'duration': duration,
                    'uploader': uploader,
                    'resolutions': resolutions,
                    'is_playlist': True,
                    'num_entries': num_entries,
                    'cookie_config': successful_config
                }

            formats = info.get('formats', [])
            heights = set()
            for f in formats:
                h = f.get('height')
                if h and isinstance(h, int):
                    heights.add(h)

            resolutions = []
            standard_heights = {
                2160: '2160p (4K 极清)',
                1080: '1080p (高清 H.264/推荐)',
                720: '720p (高清)',
                480: '480p (标清)',
                360: '360p (流畅)'
            }
            sorted_heights = sorted(list(heights), reverse=True)
            for h in sorted_heights:
                if h in standard_heights:
                    resolutions.append((h, standard_heights[h]))
                    del standard_heights[h]

            if not resolutions:
                resolutions = [(1080, '1080p (默认高画质)'), (720, '720p (标清)'), (360, '360p (低画质)')]

            resolutions.append(('audio', '仅下载高保真音频 (MP3 格式)'))

            return {
                'success': True,
                'title': title,
                'thumbnail': thumbnail,
                'duration': duration,
                'uploader': uploader,
                'resolutions': resolutions,
                'is_playlist': False,
                'num_entries': 0,
                'cookie_config': successful_config
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def download_video(self, url, resolution_choice, save_path, progress_callback, browser_name, cookie_file, cookie_config):
        """
        Executes a video or audio download in a background thread, using the local
        FFmpeg to merge tracks instantly and posting real-time progress.
        Supports loading browser cookies or manual cookies.txt for protected media.
        """
        out_dir = os.path.dirname(save_path)
        out_file = os.path.basename(save_path)
        name_no_ext = os.path.splitext(out_file)[0]

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'outtmpl': os.path.join(out_dir, f'{name_no_ext}.%(ext)s')
        }

        import shutil
        node_path = shutil.which('node')
        if node_path:
            ydl_opts['js_runtimes'] = {'node': {'path': node_path}}

        if self.ffmpeg_exe:
            ydl_opts['ffmpeg_location'] = self.ffmpeg_exe

        if cookie_config:
            ydl_opts.update(cookie_config)
        elif cookie_file and os.path.exists(cookie_file):
            ydl_opts['cookiefile'] = cookie_file
        elif browser_name and browser_name != '无 (默认)' and browser_name != 'None' and '自动' not in browser_name:
            ydl_opts['cookiesfrombrowser'] = browser_name.lower()

        if resolution_choice == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320'
            }]
        elif resolution_choice == 'playlist':
            ydl_opts['format'] = 'best'
            ydl_opts['outtmpl'] = os.path.join(out_dir, f'{name_no_ext}_%(playlist_index)s.%(ext)s')
        else:
            try:
                h = int(resolution_choice)
                ydl_opts['format'] = f'bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={h}]+bestaudio/best[height<={h}]'
            except ValueError:
                ydl_opts['format'] = 'best'
            ydl_opts['merge_output_format'] = 'mp4'

        def ydl_hook(d):
            if not progress_callback:
                return None
            status = d['status']
            if status == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                percent = downloaded / total if total > 0 else 0.0
                speed = d.get('speed', 0)
                speed_mb = speed / 1048576 if speed else 0.0
                progress_callback(percent, speed_mb, '正在极速下载中...')
                return None
            elif status == 'finished':
                progress_callback(0.95, 0.0, '下载完成，正在处理/合并媒体轨...')
                return None
            return None

        ydl_opts['progress_hooks'] = [ydl_hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if resolution_choice != 'playlist':
            expected_ext = '.mp3' if resolution_choice == 'audio' else '.mp4'
            actual_file = os.path.normpath(os.path.join(out_dir, f'{name_no_ext}{expected_ext}'))
            norm_save_path = os.path.normpath(save_path)
            if os.path.exists(actual_file) and actual_file != norm_save_path:
                if os.path.exists(norm_save_path):
                    os.remove(norm_save_path)
                os.rename(actual_file, norm_save_path)

        if progress_callback:
            progress_callback(1.0, 0.0, '下载与保存成功！')

        return True
