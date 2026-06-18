import os
from PIL import Image, ImageSequence


class GifOptimizer:
    """
    Provides rich options to compress and optimize GIF files:
    - Color palette reduction (quantization)
    - Frame skipping (with delay compensation)
    - Resolution scale-down
    - Delta-frame optimization (Pillow's native LZW difference encoder)
    """

    def __init__(self):
        pass

    def get_gif_metadata(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'GIF file not found: {file_path}')

        try:
            with Image.open(file_path) as img:
                width, height = img.size
                total_frames = getattr(img, 'n_frames', 1)

                delays = []
                for frame in ImageSequence.Iterator(img):
                    d = frame.info.get('duration', 100)
                    delays.append(d)

                file_size = os.path.getsize(file_path)

                avg_delay = sum(delays) / len(delays) if delays else 100
                avg_fps = 1000.0 / avg_delay if avg_delay > 0 else 10.0

                return {
                    'path': file_path,
                    'filename': os.path.basename(file_path),
                    'width': width,
                    'height': height,
                    'total_frames': total_frames,
                    'delays': delays,
                    'avg_delay': avg_delay,
                    'fps': avg_fps,
                    'size_bytes': file_size,
                    'size_mb': file_size / 1048576,
                }
        except Exception as e:
            raise ValueError(f'Failed to parse GIF metadata: {str(e)}')

    def optimize(self, input_path, output_path, options, progress_callback=None):
        metadata = self.get_gif_metadata(input_path)

        color_count = options.get('colors', 256)
        scale = options.get('scale', 1.0)
        skip_step = options.get('skip_step', 1)

        raw_frames = []
        raw_delays = []

        with Image.open(input_path) as img:
            for frame in ImageSequence.Iterator(img):
                raw_frames.append(frame.copy().convert('RGB'))
                raw_delays.append(frame.info.get('duration', 100))

        total_frames = len(raw_frames)
        if total_frames == 0:
            raise ValueError('No frames found in source GIF.')

        # Each retained frame must inherit the durations until the next retained frame.
        skip_step = max(1, int(skip_step))
        kept_indices = list(range(0, total_frames, skip_step))
        if kept_indices[-1] != total_frames - 1:
            kept_indices.append(total_frames - 1)

        skipped_frames = [raw_frames[index] for index in kept_indices]
        skipped_delays = []
        for position, frame_index in enumerate(kept_indices):
            next_index = kept_indices[position + 1] if position + 1 < len(kept_indices) else total_frames
            skipped_delays.append(sum(raw_delays[frame_index:next_index]))

        optimized_frames = []
        num_kept = len(skipped_frames)

        for i, frame in enumerate(skipped_frames):
            if progress_callback:
                progress_callback(
                    min(0.9, 0.9 * (i + 1) / num_kept),
                    f'正在压缩帧... ({i + 1}/{num_kept})'
                )

            # Scale down if needed
            if scale != 1.0:
                w = int(frame.width * scale)
                h = int(frame.height * scale)
                # Align to even numbers to avoid encoding artifacts
                w = max(16, w - w % 2)
                h = max(16, h - h % 2)
                proc_frame = frame.resize((w, h), Image.Resampling.LANCZOS)
            else:
                proc_frame = frame

            # Quantize if color reduction requested
            if color_count < 256:
                quantized = proc_frame.quantize(
                    colors=color_count,
                    method=Image.Quantize.MAXCOVERAGE
                )
                proc_frame = quantized.convert('RGB')

            optimized_frames.append(proc_frame)

        if not optimized_frames:
            raise ValueError('Optimization resulted in 0 frames.')

        if progress_callback:
            progress_callback(0.95, '正在写入并进行 LZW 编码优化...')

        # Convert to palette mode for GIF saving
        first_frame = optimized_frames[0].convert(
            'P', palette=Image.Palette.ADAPTIVE, colors=color_count
        )
        subsequent_frames = []
        for i in range(1, len(optimized_frames)):
            f = optimized_frames[i].convert(
                'P', palette=Image.Palette.ADAPTIVE, colors=color_count
            )
            subsequent_frames.append(f)

        first_frame.save(
            output_path,
            save_all=True,
            append_images=subsequent_frames,
            duration=skipped_delays,
            loop=0,
            optimize=True
        )

        if progress_callback:
            progress_callback(1.0, '优化完成！')

        new_size = os.path.getsize(output_path)
        original_size = metadata['size_bytes']
        ratio = (original_size - new_size) / original_size if original_size > 0 else 0

        return {
            'output_path': output_path,
            'original_size': original_size,
            'new_size': new_size,
            'ratio': ratio,
        }
