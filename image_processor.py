import os
from PIL import Image


class ImageProcessor:
    """ImageProcessor"""

    def __init__(self):
        self.image_paths = []
        self.images_metadata = []

    def clear(self):
        self.image_paths = []
        self.images_metadata = []

    def add_images(self, paths):
        """Adds a list of image paths and reads their metadata."""
        added_count = 0
        for path in paths:
            if not os.path.exists(path):
                continue
            try:
                with Image.open(path) as img:
                    width, height = img.size
                    fmt = img.format
                    size_bytes = os.path.getsize(path)

                    self.image_paths.append(path)
                    self.images_metadata.append({
                        'path': path,
                        'filename': os.path.basename(path),
                        'width': width,
                        'height': height,
                        'format': fmt,
                        'size': size_bytes,
                    })
                    added_count += 1
            except Exception as e:
                print(f'Error loading image {path}: {str(e)}')
        return added_count

    def remove_image_at(self, index):
        """Removes an image from the list by index."""
        if 0 <= index < len(self.image_paths):
            self.image_paths.pop(index)
            self.images_metadata.pop(index)
            return True
        return False

    def move_image(self, index, direction):
        """
        Moves an image up or down in the sequence.
        direction: -1 for Up, 1 for Down
        """
        new_index = index + direction
        if not (0 <= index < len(self.image_paths)):
            return False
        if not (0 <= new_index < len(self.image_paths)):
            return False
        
        # Swap
        self.image_paths[index], self.image_paths[new_index] = self.image_paths[new_index], self.image_paths[index]
        self.images_metadata[index], self.images_metadata[new_index] = self.images_metadata[new_index], self.images_metadata[index]
        return True

    def get_images_list(self):
        """Returns the list of metadata dictionaries."""
        return self.images_metadata

    def process_frames(self, options, progress_callback=None):
        """
        Loads all added images, applies resizing, scaling, and generates frame sequences
        along with transition crossfades if specified.
        Returns a tuple: (list of PIL Images, list of delays in ms)
        """
        if not self.image_paths:
            return [], []

        resize_mode = options.get('resize_mode', 'Match First')
        scale = options.get('scale', 1.0)
        custom_w = options.get('custom_width', 400)
        custom_h = options.get('custom_height', 300)
        default_delay = options.get('delay', 500)
        transition_type = options.get('transition_type', 'None')
        transition_duration = options.get('transition_duration', 200)
        fps = options.get('fps', 12.0)

        raw_images = []
        total_imgs = len(self.image_paths)

        for i, path in enumerate(self.image_paths):
            if progress_callback:
                p = min(0.3, 0.3 * (i + 1) / total_imgs)
                progress_callback(p, f'正在载入图片... ({i + 1}/{total_imgs})')
            img = Image.open(path).convert('RGB')
            raw_images.append(img)

        if not raw_images:
            return [], []

        target_w, target_h = raw_images[0].size
        if resize_mode == 'Custom':
            target_w = custom_w
            target_h = custom_h

        resized_images = []
        for i, img in enumerate(raw_images):
            if resize_mode == 'Original':
                w = int(img.width * scale)
                h = int(img.height * scale)
            else:
                w = int(target_w * scale)
                h = int(target_h * scale)

            w = max(16, w - w % 2)
            h = max(16, h - h % 2)

            if img.width != w or img.height != h:
                resized_img = img.resize((w, h), Image.Resampling.LANCZOS)
            else:
                resized_img = img.copy()
            resized_images.append(resized_img)

        compiled_frames = []
        delays = []
        num_images = len(resized_images)

        for i in range(num_images):
            current_img = resized_images[i]
            if transition_type == 'None' or num_images < 2:
                compiled_frames.append(current_img)
                delays.append(default_delay)
            else:
                static_duration = max(50, default_delay - transition_duration)
                compiled_frames.append(current_img)
                delays.append(static_duration)

                next_idx = (i + 1) % num_images
                next_img = resized_images[next_idx]

                if current_img.size != next_img.size:
                    next_img_res = next_img.resize(current_img.size, Image.Resampling.LANCZOS)
                else:
                    next_img_res = next_img

                trans_frames_count = int((transition_duration / 1000.0) * fps)
                trans_frames_count = max(1, trans_frames_count)
                trans_delay = int(transition_duration / trans_frames_count)

                for f in range(trans_frames_count):
                    alpha = (f + 1) / (trans_frames_count + 1)
                    blended = Image.blend(current_img, next_img_res, alpha)
                    compiled_frames.append(blended)
                    delays.append(trans_delay)

            if progress_callback:
                p = 0.3 + 0.6 * (i + 1) / num_images
                progress_callback(p, f'正在生成过场动画... ({i + 1}/{num_images})')

        return compiled_frames, delays
