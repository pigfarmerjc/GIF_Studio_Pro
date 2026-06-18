import os
import numpy as np
from PIL import Image


class GifEncoder:
    """
    Core GIF compilation engine. Features:
    - Global Palette Quantization (generates a unified palette to prevent color flickering)
    - Custom color depth controls (16 to 256 colors)
    - Floyd-Steinberg Dithering toggle
    - Frame difference optimization (LZW)
    """

    def __init__(self):
        pass

    def _generate_global_palette(self, pil_images, color_count=256, sample_limit=30):
        if not pil_images:
            return None

        num_frames = len(pil_images)
        step = max(1, num_frames // sample_limit)
        sampled_frames = pil_images[::step]

        widths = [f.width for f in sampled_frames]
        heights = [f.height for f in sampled_frames]

        tile_w = min(400, widths[0])
        tile_h = min(300, heights[0])

        composite_w = tile_w * len(sampled_frames)
        composite_h = tile_h

        composite = Image.new('RGB', (composite_w, composite_h))

        for idx, frame in enumerate(sampled_frames):
            tile = frame.resize((tile_w, tile_h), Image.Resampling.NEAREST)
            composite.paste(tile, (idx * tile_w, 0))

        global_palette_img = composite.quantize(
            colors=color_count,
            method=Image.Quantize.MAXCOVERAGE
        )
        composite.close()

        return global_palette_img

    def save_gif(self, pil_images, output_path, fps=12.0, options=None, progress_callback=None):
        if not pil_images:
            raise ValueError('No frames to encode into GIF.')

        if options is None:
            options = {}

        color_count = options.get('colors', 256)
        use_dither = options.get('dither', True)
        use_global_palette = options.get('global_palette', True)
        delays = options.get('delays', None)
        loop = options.get('loop', 0)
        cancel_event = options.get('_cancel_event')

        if delays is None:
            delay_per_frame = int(1000.0 / fps)
            delay_per_frame = max(20, delay_per_frame)
            delays = [delay_per_frame] * len(pil_images)

        total_frames = len(pil_images)
        quantized_frames = []

        if use_global_palette and total_frames > 1:
            if progress_callback:
                progress_callback(0.91, '生成全局最佳调色板...')

            global_palette_img = self._generate_global_palette(pil_images, color_count)

            if progress_callback:
                progress_callback(0.93, '正在以全局调色板映射全部帧...')

            for idx, frame in enumerate(pil_images):
                if cancel_event is not None and cancel_event.is_set():
                    raise InterruptedError('操作已由用户取消')
                rgb_frame = frame.convert('RGB')
                dither_val = Image.Dither.FLOYDSTEINBERG if use_dither else Image.Dither.NONE
                mapped = rgb_frame.quantize(palette=global_palette_img, dither=dither_val)
                quantized_frames.append(mapped)
        else:
            for idx, frame in enumerate(pil_images):
                if cancel_event is not None and cancel_event.is_set():
                    raise InterruptedError('操作已由用户取消')
                rgb_frame = frame.convert('RGB')
                mapped = rgb_frame.quantize(
                    colors=color_count,
                    method=Image.Quantize.MAXCOVERAGE
                )
                quantized_frames.append(mapped)

        if progress_callback:
            progress_callback(0.96, '进行 LZW 深度编码与文件写入...')

        first_frame = quantized_frames[0]
        subsequent_frames = quantized_frames[1:]

        first_frame.save(
            output_path,
            save_all=True,
            append_images=subsequent_frames,
            duration=delays,
            loop=loop,
            optimize=True
        )

        if progress_callback:
            progress_callback(1.0, 'GIF 保存成功！')

        file_size = os.path.getsize(output_path)
        return {
            'path': output_path,
            'filename': os.path.basename(output_path),
            'size_bytes': file_size,
            'size_mb': file_size / 1048576,
            'width': first_frame.width,
            'height': first_frame.height,
            'total_frames': total_frames,
        }
