import os
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

try:
    import imageio_ffmpeg
except ImportError:
    imageio_ffmpeg = None


def _get_startupinfo():
    """Returns Windows STARTUPINFO to suppress console windows, or None on other OS."""
    if os.name == 'nt':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return si
    return None


class VideoProcessor:
    """VideoProcessor"""

    def __init__(self, file_path=None):
        self.file_path = file_path
        self.cap = None
        self.metadata = {}
        if file_path:
            self.load_video(file_path)

    def load_video(self, file_path):
        """Loads video file and extracts general metadata."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Video file not found: {file_path}')
        self.file_path = file_path
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            raise ValueError(f'Failed to open video file: {file_path}')

        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if fps <= 0:
            fps = 24.0
        duration = total_frames / fps

        self.metadata = {
            'path': file_path,
            'filename': os.path.basename(file_path),
            'width': width,
            'height': height,
            'fps': fps,
            'total_frames': total_frames,
            'duration': duration,
        }
        return self.metadata

    def get_frame_at_time(self, seconds, target_width=None):
        """
        Retrieves a single frame at a specific timestamp (in seconds) for timeline scrubbing.
        Returns a PIL Image.
        """
        if not self.cap:
            return None
        fps = self.metadata.get('fps', 24.0)
        total_frames = self.metadata.get('total_frames', 0)
        frame_idx = int(seconds * fps)
        frame_idx = max(0, min(frame_idx, total_frames - 1))

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = self.cap.read()
        if not ret or frame is None:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                return None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)

        if target_width:
            aspect = img.height / img.width
            target_height = int(target_width * aspect)
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return img

    def apply_filters_and_adjustments(self, pil_img, adjustments=None, filter_name=None):
        """
        Applies brightness, contrast, saturation, and artistic filters to a PIL Image.
        """
        if adjustments:
            brightness = adjustments.get('brightness', 1.0)
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(pil_img)
                pil_img = enhancer.enhance(brightness)
            contrast = adjustments.get('contrast', 1.0)
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(pil_img)
                pil_img = enhancer.enhance(contrast)
            saturation = adjustments.get('saturation', 1.0)
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(pil_img)
                pil_img = enhancer.enhance(saturation)

        if filter_name and filter_name != 'None':
            if filter_name == 'Grayscale':
                pil_img = pil_img.convert('L').convert('RGB')
                return pil_img
            elif filter_name == 'Invert':
                arr = np.array(pil_img)
                arr = 255 - arr
                pil_img = Image.fromarray(arr)
                return pil_img
            elif filter_name == 'Sepia':
                arr = np.array(pil_img)
                sepia_matrix = np.array([
                    [0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]
                ])
                sepia_arr = arr.dot(sepia_matrix.T)
                sepia_arr = np.clip(sepia_arr, 0, 255).astype(np.uint8)
                pil_img = Image.fromarray(sepia_arr)
                return pil_img
            elif filter_name == 'Vintage':
                arr = np.array(pil_img).astype(float)
                arr[:, :, 0] = arr[:, :, 0] * 0.95 + 10
                arr[:, :, 1] = arr[:, :, 1] * 0.9 + 5
                arr[:, :, 2] = arr[:, :, 2] * 0.8
                arr = np.clip(arr, 0, 255).astype(np.uint8)
                pil_img = Image.fromarray(arr)
                return pil_img
            elif filter_name == 'High Contrast':
                enhancer = ImageEnhance.Contrast(pil_img)
                pil_img = enhancer.enhance(1.8)
        return pil_img

    def apply_text_overlay(self, pil_img, text_config):
        """
        Draws custom text overlay (meme captions, watermarks) on a PIL Image.
        """
        if not text_config or not text_config.get('text'):
            return pil_img
        text = text_config['text']
        position_type = text_config.get('position', 'Bottom')
        font_size = text_config.get('font_size', 24)
        color = text_config.get('color', '#FFFFFF')

        font = None
        font_paths = ['C:\\Windows\\Fonts\\msyh.ttc', 'C:\\Windows\\Fonts\\arial.ttf', 'C:\\Windows\\Fonts\\simhei.ttf']
        for path in font_paths:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, font_size)
                    break
                except Exception:
                    continue
        if font is None:
            font = ImageFont.load_default()

        if pil_img.mode != 'RGB':
            pil_img = pil_img.convert('RGB')
        draw = ImageDraw.Draw(pil_img)
        w, h = pil_img.size

        try:
            left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
            text_w = right - left
            text_h = bottom - top
        except AttributeError:
            text_w, text_h = draw.textsize(text, font=font)

        margin = 15
        if position_type == 'Top':
            x = (w - text_w) // 2
            y = margin
        elif position_type == 'Bottom':
            x = (w - text_w) // 2
            y = h - text_h - margin - 10
        elif position_type == 'Center':
            x = (w - text_w) // 2
            y = (h - text_h) // 2
        else:
            x = (w - text_w) // 2
            y = h - text_h - margin - 10

        outline_range = 2
        for ox in range(-outline_range, outline_range + 1):
            for oy in range(-outline_range, outline_range + 1):
                if ox != 0 or oy != 0:
                    draw.text((x + ox, y + oy), text, font=font, fill='#000000')
        draw.text((x, y), text, font=font, fill=color)
        return pil_img

    def extract_frames_range(self, start_time, end_time, options, progress_callback):
        """
        Extracts and processes frames between start_time and end_time based on configurations.
        Returns a list of PIL Images.
        """
        if not self.file_path:
            return []
        cap = cv2.VideoCapture(self.file_path)
        fps = self.metadata.get('fps', 24.0)
        total_frames = self.metadata.get('total_frames', 0)

        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        start_frame = max(0, min(start_frame, total_frames - 1))
        end_frame = max(start_frame, min(end_frame, total_frames - 1))

        target_fps = options.get('fps', 12.0)
        scale = options.get('scale', 1.0)
        speed = options.get('speed', 1.0)
        loop_style = options.get('loop', 'Normal')
        crop_rect = options.get('crop', None)
        adjustments = options.get('adjustments', None)
        filter_name = options.get('filter', 'None')
        text_config = options.get('text_config', None)
        cancel_event = options.get('_cancel_event')

        frame_step = (fps / target_fps) * speed
        frame_step = max(1.0, frame_step)

        frames = []
        current_frame = float(start_frame)
        total_steps = int((end_frame - start_frame) / frame_step)
        total_steps = max(1, total_steps)
        processed_count = 0

        while current_frame <= end_frame:
            if cancel_event is not None and cancel_event.is_set():
                cap.release()
                raise InterruptedError('操作已由用户取消')
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(current_frame))
            ret, frame = cap.read()
            if not ret or frame is None:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)

            if crop_rect:
                x, y, w, h = crop_rect
                img_w, img_h = img.size
                x = max(0, min(x, img_w - 1))
                y = max(0, min(y, img_h - 1))
                w = max(10, min(w, img_w - x))
                h = max(10, min(h, img_h - y))
                img = img.crop((x, y, x + w, y + h))

            if scale != 1.0:
                new_w = int(img.width * scale)
                new_h = int(img.height * scale)
                new_w = max(16, new_w - new_w % 2)
                new_h = max(16, new_h - new_h % 2)
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

            img = self.apply_filters_and_adjustments(img, adjustments, filter_name)
            img = self.apply_text_overlay(img, text_config)
            frames.append(img)
            current_frame += frame_step
            processed_count += 1

            if progress_callback:
                progress = min(0.9, processed_count / total_steps)
                progress_callback(progress, f'正在处理视频帧... ({processed_count}/{total_steps})')

        cap.release()
        if not frames:
            return []

        if loop_style == 'Reverse':
            frames.reverse()
            return frames
        elif loop_style == 'Ping-Pong':
            reverse_frames = frames[::-1][1:-1]
            frames.extend(reverse_frames)

        return frames

    def release(self):
        """Release the capture device."""
        if self.cap:
            self.cap.release()
            self.cap = None

    def extract_audio(self, output_audio_path, start_time, end_time, audio_format, bitrate, progress_callback):
        """
        Extracts audio from the video file using FFmpeg, supporting multiple formats and high-fidelity controls.
        """
        if not self.file_path:
            raise ValueError('No video loaded.')
        if imageio_ffmpeg is None:
            raise ImportError('imageio-ffmpeg is required for audio extraction.')
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [ffmpeg_exe, '-y']

        if start_time is not None:
            cmd.extend(['-ss', str(start_time)])
        if end_time is not None:
            cmd.extend(['-to', str(end_time)])

        cmd.extend(['-i', self.file_path, '-vn'])

        fmt = audio_format.lower().strip()
        if fmt == 'mp3':
            cmd.extend(['-acodec', 'libmp3lame', '-b:a', bitrate])
        elif fmt == 'wav':
            cmd.extend(['-acodec', 'pcm_s16le'])
        elif fmt == 'flac':
            cmd.extend(['-acodec', 'flac'])
        elif fmt == 'aac':
            cmd.extend(['-acodec', 'aac', '-b:a', bitrate])
        elif fmt == 'm4a':
            cmd.extend(['-acodec', 'aac', '-b:a', bitrate])
        else:
            cmd.extend(['-acodec', 'aac', '-b:a', bitrate])

        cmd.append(output_audio_path)

        if progress_callback:
            progress_callback(0.2, '正在解析音频流并进行高保真重编码...')

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=_get_startupinfo()
            )
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise RuntimeError(f'FFmpeg error: {stderr.decode("utf-8", errors="ignore")}')
            if progress_callback:
                progress_callback(1.0, '高保真音频提取成功！')
            return True
        except Exception as e:
            if progress_callback:
                progress_callback(0.0, f'提取失败: {str(e)}')
            raise e

    def merge_video_audio(self, video_path, audio_path, output_path, options, progress_callback):
        """
        Combines a video and an audio file into a single video, with independent volume controls,
        clipping/trimming ranges, and loop/truncation alignment strategies.
        """
        if imageio_ffmpeg is None:
            raise ImportError('imageio-ffmpeg is required for video-audio merging.')
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        v_volume = options.get('v_volume', 1.0)
        a_volume = options.get('a_volume', 1.0)
        align_mode = options.get('align_mode', 'video')
        v_start = options.get('v_start', None)
        v_end = options.get('v_end', None)
        a_start = options.get('a_start', None)
        a_end = options.get('a_end', None)

        has_audio = True
        try:
            chk_cmd = [ffmpeg_exe, '-i', video_path]
            process = subprocess.Popen(
                chk_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=_get_startupinfo()
            )
            stdout, stderr = process.communicate()
            output = stderr.decode('utf-8', errors='ignore') + stdout.decode('utf-8', errors='ignore')
            has_audio = 'Audio:' in output
        except Exception as e:
            print(f'Error checking audio stream: {str(e)}')
            has_audio = True

        cmd = [ffmpeg_exe, '-y']
        v_inputs = []
        if align_mode == 'audio':
            v_inputs.extend(['-stream_loop', '-1'])
        if v_start is not None:
            v_inputs.extend(['-ss', str(v_start)])
        if v_end is not None:
            v_inputs.extend(['-to', str(v_end)])

        cmd.extend(v_inputs)
        cmd.extend(['-i', video_path])

        a_inputs = []
        if align_mode == 'loop_audio':
            a_inputs.extend(['-stream_loop', '-1'])
        if a_start is not None:
            a_inputs.extend(['-ss', str(a_start)])
        if a_end is not None:
            a_inputs.extend(['-to', str(a_end)])

        cmd.extend(a_inputs)
        cmd.extend(['-i', audio_path])

        if has_audio and v_volume > 0.01:
            filter_str = f'[0:a]volume={v_volume}[a0];[1:a]volume={a_volume}[a1];[a0][a1]amix=inputs=2:duration=first[out_a]'
        else:
            filter_str = f'[1:a]volume={a_volume}[out_a]'

        cmd.extend(['-filter_complex', filter_str, '-map', '0:v', '-map', '[out_a]'])
        cmd.extend(['-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k'])

        if align_mode in ('shortest', 'loop_audio', 'video'):
            cmd.append('-shortest')

        cmd.append(output_path)

        if progress_callback:
            progress_callback(0.4, '正在融合多轨声道，进行 FFmpeg 极速混音...')

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=_get_startupinfo()
            )
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise RuntimeError(f'FFmpeg error: {stderr.decode("utf-8", errors="ignore")}')
            if progress_callback:
                progress_callback(1.0, '影音配音与多轨混音合成成功！')
            return True
        except Exception as e:
            if progress_callback:
                progress_callback(0.0, f'配音合成失败: {str(e)}')
            raise e
