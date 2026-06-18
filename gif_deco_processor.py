import os
import colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageSequence


class DecoLayer:
    """DecoLayer"""

    def __init__(self, layer_id, layer_type, content):
        self.id = layer_id
        self.type = layer_type
        self.content = content
        self.group_id = 0
        self.x_pct = 0.5
        self.y_pct = 0.5
        self.scale = 1.0
        self.rotation = 0.0
        self.opacity = 1.0
        self.start_frame = 0
        self.end_frame = -1
        self.always_show = True
        self.motion_type = 'Static'
        self.motion_speed = 1.0
        self.motion_intensity = 1.0
        self.color = '#FFFFFF'
        self.font_family = 'Microsoft YaHei'
        self.stroke_width = 0
        self.stroke_color = '#000000'
        self.shadow_dx = 0
        self.shadow_dy = 0
        self.shadow_color = '#000000'
        self.glow_enabled = False
        self.glow_color = '#818CF8'
        self.gradient_enabled = False
        self.gradient_end_color = '#FFFF00'
        self._sticker_cache = None
        self._sticker_is_gif = False
        self._last_loaded_path = ''

    def get_display_name(self):
        """Returns a friendly display label for the layer list."""
        if self.type == 'Text':
            if len(self.content) > 8:
                snippet = self.content[:8] + '...'
            else:
                snippet = self.content
            return f"💬 文字: '{snippet}'"
        elif self.type == 'Emoji':
            return f"😂 表情: {self.content}"
        elif self.type == 'Sticker':
            filename = os.path.basename(self.content)
            if len(filename) > 12:
                snippet = filename[:12] + '...'
            else:
                snippet = filename
            return f"🖼️ 贴图: {snippet}"
        return 'Layer'

    def load_sticker(self):
        """Loads and caches static or animated sticker frames."""
        if self.type != 'Sticker' or not self.content or not os.path.exists(self.content):
            self._sticker_cache = None
            return None
        if self._last_loaded_path == self.content and self._sticker_cache is not None:
            return None
        self._last_loaded_path = self.content
        self._sticker_cache = []
        self._sticker_is_gif = False
        try:
            with Image.open(self.content) as img:
                n_frames = getattr(img, 'n_frames', 1)
                if n_frames > 1 and self.content.lower().endswith('.gif'):
                    self._sticker_is_gif = True
                    for frame in ImageSequence.Iterator(img):
                        self._sticker_cache.append(frame.copy().convert('RGBA'))
                else:
                    self._sticker_cache.append(img.copy().convert('RGBA'))
        except Exception as e:
            print(f'Error loading sticker {self.content}: {str(e)}')
            self._sticker_cache = None
            return None


class GifDecoProcessor:
    """GifDecoProcessor"""

    def __init__(self):
        pass

    def hex_to_rgb(self, hex_str):
        """Converts hex color string to RGB tuple."""
        hex_str = hex_str.lstrip('#')
        if len(hex_str) != 6:
            return (255, 255, 255)
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

    def get_font_path(self, font_name):
        """Maps friendly font names to actual Windows TTF/TTC paths."""
        fonts = {
            'Microsoft YaHei': 'C:\\Windows\\Fonts\\msyh.ttc',
            'SimHei': 'C:\\Windows\\Fonts\\simhei.ttf',
            'Arial': 'C:\\Windows\\Fonts\\arial.ttf',
            'Courier New': 'C:\\Windows\\Fonts\\cour.ttf',
            'Comic Sans MS': 'C:\\Windows\\Fonts\\comic.ttf',
            'Segoe UI Emoji': 'C:\\Windows\\Fonts\\seguiemj.ttf'
        }
        path = fonts.get(font_name, 'C:\\Windows\\Fonts\\msyh.ttc')
        if os.path.exists(path):
            return path

        for fb in ('C:\\Windows\\Fonts\\msyh.ttc', 'C:\\Windows\\Fonts\\simhei.ttf', 'C:\\Windows\\Fonts\\arial.ttf'):
            if os.path.exists(fb):
                return fb
        return None

    def draw_gradient_text(self, draw, frame_img, position, text, font, start_color_hex, end_color_hex, stroke_width, stroke_color_hex):
        """
        Renders elegant text filled with a dual-color linear vertical gradient using transparency masks.
        """
        stroke_w = int(stroke_width)
        stroke_c = self.hex_to_rgb(stroke_color_hex) if stroke_color_hex else (0, 0, 0)

        try:
            left, top, right, bottom = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
            text_w = right - left
            text_h = bottom - top
        except AttributeError:
            text_w, text_h = draw.textsize(text, font=font, stroke_width=stroke_w)
            left, top = 0, 0

        if text_w <= 0 or text_h <= 0:
            return None

        padding = 10
        mask_w = text_w + padding * 2
        mask_h = text_h + padding * 2

        mask = Image.new('L', (mask_w, mask_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.text((padding - left, padding - top), text, font=font, fill=255, stroke_width=stroke_w, stroke_fill=255)

        gradient = Image.new('RGB', (mask_w, mask_h))
        c1 = self.hex_to_rgb(start_color_hex)
        c2 = self.hex_to_rgb(end_color_hex)

        for y in range(mask_h):
            ratio = y / max(1, mask_h - 1)
            r = int(c1[0] + (c2[0] - c1[0]) * ratio)
            g = int(c1[1] + (c2[1] - c1[1]) * ratio)
            b = int(c1[2] + (c2[2] - c1[2]) * ratio)
            gradient.paste((r, g, b), (0, y, mask_w, y + 1))

        paste_x = int(position[0] + left - padding)
        paste_y = int(position[1] + top - padding)

        frame_img.paste(gradient, (paste_x, paste_y), mask=mask)
        return None

    def draw_glow_text(self, draw, position, text, font, main_color_hex, glow_color_hex, base_stroke_width, base_stroke_color_hex):
        """
        Creates a soft glowing drop shadow/halo effect by drawing concentric
        semi-transparent outlines behind the text.
        """
        glow_color = self.hex_to_rgb(glow_color_hex)
        x, y = position

        glow_steps = [(8, 0.05), (6, 0.1), (4, 0.2), (2, 0.35)]

        for width, opacity in glow_steps:
            stroke_w = int(base_stroke_width + width)
            fill_color = (*glow_color, int(255 * opacity))
            draw.text((x, y), text, font=font, fill=fill_color, stroke_width=stroke_w, stroke_fill=fill_color)

        if base_stroke_width > 0 and base_stroke_color_hex:
            draw.text((x, y), text, font=font, fill=main_color_hex, stroke_width=int(base_stroke_width), stroke_fill=base_stroke_color_hex)
            return None

        draw.text((x, y), text, font=font, fill=main_color_hex)
        return None

    def render_frame(self, base_frame, frame_idx, total_frames, layers):
        """
        Renders all visible decoration layers on a single RGB PIL Image frame.
        Computes dynamic positions, rotations, opacities, and renders custom typography.
        """
        frame = base_frame.copy().convert('RGBA')
        W, H = frame.size

        for layer in layers:
            if not layer.always_show:
                start = layer.start_frame
                end = layer.end_frame if layer.end_frame >= 0 else total_frames - 1
                if not (start <= frame_idx <= end):
                    continue

            if layer.type == 'Sticker':
                layer.load_sticker()
                if not layer._sticker_cache:
                    continue

            x_base = layer.x_pct * W
            y_base = layer.y_pct * H
            scale_factor = layer.scale
            opacity = layer.opacity
            rotation = layer.rotation
            display_text = layer.content
            color = layer.color

            t = frame_idx / max(1, total_frames - 1)
            motion = layer.motion_type
            speed = layer.motion_speed
            intensity = layer.motion_intensity

            item_width = 100
            item_height = 30
            font = None

            if layer.type in ('Text', 'Emoji'):
                font_fam = 'Segoe UI Emoji' if layer.type == 'Emoji' else layer.font_family
                font_path = self.get_font_path(font_fam)
                font_size = max(10, int(30 * scale_factor))
                if font_path:
                    try:
                        font = ImageFont.truetype(font_path, font_size)
                    except Exception:
                        font = ImageFont.load_default()
                else:
                    font = ImageFont.load_default()

                temp_draw = ImageDraw.Draw(frame)
                try:
                    left, top, right, bottom = temp_draw.textbbox((0, 0), display_text, font=font)
                    item_width = right - left
                    item_height = bottom - top
                except AttributeError:
                    item_width, item_height = temp_draw.textsize(display_text, font=font)
                    left, top = 0, 0

            elif layer.type == 'Sticker' and layer._sticker_cache:
                sticker_list = layer._sticker_cache
                if layer._sticker_is_gif:
                    st_frame_idx = frame_idx % len(sticker_list)
                    sticker_img = sticker_list[st_frame_idx]
                else:
                    sticker_img = sticker_list[0]
                item_width = int(sticker_img.width * scale_factor)
                item_height = int(sticker_img.height * scale_factor)

            if motion == 'Scroll Left':
                prog = (t * speed) % 1.0
                x = W - (W + item_width) * prog
                y = y_base - item_height / 2
            elif motion == 'Scroll Right':
                prog = (t * speed) % 1.0
                x = -item_width + (W + item_width) * prog
                y = y_base - item_height / 2
            elif motion == 'Bounce Y':
                cycle = t * speed * 2.0 * np.pi
                bounce_offset = abs(np.sin(cycle)) * intensity * 60
                x = x_base - item_width / 2
                y = y_base - item_height / 2 - bounce_offset
            elif motion == 'Float':
                cycle_x = t * speed * 2.0 * np.pi
                cycle_y = t * speed * 1.5 * np.pi
                offset_x = np.sin(cycle_x) * intensity * 25
                offset_y = np.cos(cycle_y) * intensity * 15
                x = x_base - item_width / 2 + offset_x
                y = y_base - item_height / 2 + offset_y
            elif motion == 'Pulse':
                cycle = t * speed * 2.0 * np.pi
                pulse_scale = 1.0 + np.sin(cycle) * intensity * 0.35
                scale_factor = layer.scale * pulse_scale

                if layer.type in ('Text', 'Emoji'):
                    font_size = max(10, int(30 * scale_factor))
                    if font_path:
                        try:
                            font = ImageFont.truetype(font_path, font_size)
                        except Exception:
                            font = ImageFont.load_default()
                    temp_draw = ImageDraw.Draw(frame)
                    try:
                        left, top, right, bottom = temp_draw.textbbox((0, 0), display_text, font=font)
                        item_width = right - left
                        item_height = bottom - top
                    except AttributeError:
                        item_width, item_height = temp_draw.textsize(display_text, font=font)
                elif layer.type == 'Sticker':
                    item_width = int(sticker_img.width * scale_factor)
                    item_height = int(sticker_img.height * scale_factor)
                x = x_base - item_width / 2
                y = y_base - item_height / 2
            elif motion == 'Typewriter' and layer.type in ('Text', 'Emoji'):
                prog = min(1.0, t * speed)
                char_len = int(len(layer.content) * prog)
                display_text = layer.content[:char_len]
                temp_draw = ImageDraw.Draw(frame)
                try:
                    left, top, right, bottom = temp_draw.textbbox((0, 0), display_text, font=font)
                    item_width = right - left
                    item_height = bottom - top
                except AttributeError:
                    item_width, item_height = temp_draw.textsize(display_text, font=font)
                x = x_base - item_width / 2
                y = y_base - item_height / 2
            elif motion == 'Rainbow' and layer.type in ('Text', 'Emoji'):
                h_val = (t * speed) % 1.0
                rgb = colorsys.hsv_to_rgb(h_val, 0.8, 1.0)
                color = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
                x = x_base - item_width / 2
                y = y_base - item_height / 2
            elif motion == 'Fade':
                if t < 0.2:
                    alpha = t / 0.2
                elif t > 0.8:
                    alpha = (1.0 - t) / 0.2
                else:
                    alpha = 1.0
                opacity = layer.opacity * alpha
                x = x_base - item_width / 2
                y = y_base - item_height / 2
            else:
                x = x_base - item_width / 2
                y = y_base - item_height / 2

            pos_x = int(x)
            pos_y = int(y)

            layer_canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            layer_draw = ImageDraw.Draw(layer_canvas)

            if layer.type in ('Text', 'Emoji'):
                if abs(rotation) > 0.5:
                    text_pad = 20
                    thumb_w = item_width + text_pad * 2
                    thumb_h = item_height + text_pad * 2
                    text_thumb = Image.new('RGBA', (thumb_w, thumb_h), (0, 0, 0, 0))
                    thumb_draw = ImageDraw.Draw(text_thumb)
                    draw_pos = (text_pad, text_pad)

                    if layer.gradient_enabled and layer.type != 'Emoji':
                        self.draw_gradient_text(thumb_draw, text_thumb, draw_pos, display_text, font, color, layer.gradient_end_color, layer.stroke_width, layer.stroke_color)
                    elif layer.glow_enabled:
                        self.draw_glow_text(thumb_draw, draw_pos, display_text, font, color, layer.glow_color, layer.stroke_width, layer.stroke_color)
                    else:
                        if layer.shadow_dx != 0 or layer.shadow_dy != 0:
                            s_pos = (draw_pos[0] + layer.shadow_dx, draw_pos[1] + layer.shadow_dy)
                            thumb_draw.text(s_pos, display_text, font=font, fill=layer.shadow_color, stroke_width=int(layer.stroke_width), stroke_fill=layer.stroke_color)
                        thumb_draw.text(draw_pos, display_text, font=font, fill=color, stroke_width=int(layer.stroke_width), stroke_fill=layer.stroke_color)

                    rotated_thumb = text_thumb.rotate(-rotation, resample=Image.Resampling.BICUBIC, expand=True)
                    paste_x = pos_x - (rotated_thumb.width - item_width) // 2
                    paste_y = pos_y - (rotated_thumb.height - item_height) // 2
                    layer_canvas.paste(rotated_thumb, (paste_x, paste_y), mask=rotated_thumb)
                else:
                    if layer.gradient_enabled and layer.type != 'Emoji':
                        self.draw_gradient_text(layer_draw, layer_canvas, (pos_x, pos_y), display_text, font, color, layer.gradient_end_color, layer.stroke_width, layer.stroke_color)
                    elif layer.glow_enabled:
                        self.draw_glow_text(layer_draw, (pos_x, pos_y), display_text, font, color, layer.glow_color, layer.stroke_width, layer.stroke_color)
                    else:
                        if layer.shadow_dx != 0 or layer.shadow_dy != 0:
                            s_pos = (pos_x + layer.shadow_dx, pos_y + layer.shadow_dy)
                            layer_draw.text(s_pos, display_text, font=font, fill=layer.shadow_color, stroke_width=int(layer.stroke_width), stroke_fill=layer.stroke_color)
                        layer_draw.text((pos_x, pos_y), display_text, font=font, fill=color, stroke_width=int(layer.stroke_width), stroke_fill=layer.stroke_color)
            elif layer.type == 'Sticker' and layer._sticker_cache:
                proc_sticker = sticker_img.resize((item_width, item_height), Image.Resampling.LANCZOS)
                if abs(rotation) > 0.5:
                    proc_sticker = proc_sticker.rotate(-rotation, resample=Image.Resampling.BICUBIC, expand=True)
                    paste_x = pos_x - (proc_sticker.width - item_width) // 2
                    paste_y = pos_y - (proc_sticker.height - item_height) // 2
                else:
                    paste_x = pos_x
                    paste_y = pos_y
                layer_canvas.paste(proc_sticker, (paste_x, paste_y), mask=proc_sticker)

            if opacity < 1.0:
                r_c, g_c, b_c, a_c = layer_canvas.split()
                a_c = a_c.point(lambda p: int(p * opacity))
                layer_canvas = Image.merge('RGBA', (r_c, g_c, b_c, a_c))

            frame = Image.alpha_composite(frame, layer_canvas)

        return frame.convert('RGB')
