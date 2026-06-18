# ============================================================
# Module: gif_deco_tab.py
# Reconstructed from Python 3.14 bytecode
# NOTE: Function bodies need manual reconstruction
#       Class/function structure is accurate
# ============================================================

import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import customtkinter as ctk
from PIL import Image, ImageSequence, ImageTk
from gif_deco_processor import DecoLayer, GifDecoProcessor


class GifDecoTab(ctk.CTkFrame):
    """GifDecoTab"""

    def __init__(self, master, app):
        """transparent"""
        super().__init__(master, fg_color='transparent')
        self.app = app
        self.processor = GifDecoProcessor()
        self.source_gif_path = ''
        self.source_frames = []
        self.source_delays = []
        self.gif_loaded = False
        self.layers = []
        self.selected_layer = None
        self.current_frame_idx = 0
        self.is_playing = False
        self.play_after_id = None
        self.temp_deco_path = os.path.join(
            os.path.expanduser('~'),
            'AppData',
            'Local',
            'Temp',
            'gif_studio_decorated.gif'
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=4)
        self.create_left_panel()
        self.create_right_panel()
        self.create_bottom_progress()

    def on_show(self):
        """Called when this tab is selected in navigation."""
        pass

    def create_left_panel(self):
        """Builds the visual canvas preview and timeline scrubber."""
        self.left_frame = ctk.CTkFrame(self, fg_color='#1E293B', corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky='nsew')
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.header_left = ctk.CTkFrame(self.left_frame, fg_color='transparent')
        self.header_left.grid(row=0, column=0, padx=15, pady=(15, 5), sticky='ew')
        self.header_left.grid_columnconfigure(1, weight=1)
        self.btn_import_gif = ctk.CTkButton(
            self.header_left,
            text='📂 导入要装饰的 GIF',
            fg_color='#6366F1',
            hover_color='#4F46E5',
            font=ctk.CTkFont(family='Microsoft YaHei', weight='bold'),
            command=self.import_source_gif
        )
        self.btn_import_gif.grid(row=0, column=0, sticky='w')
        self.lbl_gif_info = ctk.CTkLabel(
            self.header_left,
            text='当前未载入 GIF 图片',
            text_color='gray50',
            anchor='w'
        )
        self.lbl_gif_info.grid(row=0, column=1, padx=15, sticky='ew')
        self.canvas_container = ctk.CTkFrame(self.left_frame, fg_color='#0F172A', corner_radius=8)
        self.canvas_container.grid(row=1, column=0, padx=15, pady=5, sticky='nsew')
        self.canvas_container.grid_rowconfigure(0, weight=1)
        self.canvas_container.grid_columnconfigure(0, weight=1)
        self.preview_canvas = tk.Canvas(
            self.canvas_container,
            bg='#0F172A',
            highlightthickness=0,
            cursor='arrow'
        )
        self.preview_canvas.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.preview_canvas.bind('<ButtonPress-1>', self._on_canvas_click)
        self.preview_canvas.bind('<B1-Motion>', self._on_canvas_drag)
        self.preview_canvas.bind('<ButtonRelease-1>', self._on_canvas_release)
        self.preview_canvas.bind('<ButtonPress-3>', self._on_canvas_right_click)
        self.preview_canvas.bind('<B3-Motion>', self._on_canvas_right_drag)
        self.timeline_frame = ctk.CTkFrame(self.left_frame, fg_color='transparent')
        self.timeline_frame.grid(row=2, column=0, padx=15, pady=(5, 15), sticky='ew')
        self.timeline_frame.grid_columnconfigure(1, weight=1)
        self.btn_play = ctk.CTkButton(
            self.timeline_frame,
            text='▶ 播放预览',
            width=95,
            height=28,
            fg_color='#10B981',
            hover_color='#059669',
            font=ctk.CTkFont(family='Microsoft YaHei', size=12, weight='bold'),
            command=self.toggle_play
        )
        self.btn_play.grid(row=0, column=0, padx=(0, 10))
        self.btn_play.configure(state='disabled')
        self.slider_timeline = ctk.CTkSlider(
            self.timeline_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self.on_scrub
        )
        self.slider_timeline.grid(row=0, column=1, sticky='ew')
        self.slider_timeline.set(0)
        self.slider_timeline.configure(state='disabled')
        self.lbl_frame_info = ctk.CTkLabel(
            self.timeline_frame,
            text='帧: 0 / 0',
            text_color='gray70',
            font=ctk.CTkFont(size=12)
        )
        self.lbl_frame_info.grid(row=0, column=2, padx=(10, 0))

    def create_right_panel(self):
        """Builds the Layers Manager and Collapsible Layer Attributes panels."""
        self.right_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='#1E293B',
            corner_radius=10,
            label_text='🛠️ 涂鸦图层属性与效果编辑器'
        )
        self.right_frame.grid(
            row=0,
            column=1,
            padx=(10, 0),
            pady=(0, 10),
            sticky='nsew'
        )
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.section_layers = ctk.CTkFrame(
            self.right_frame,
            fg_color='#0F172A',
            corner_radius=8
        )
        self.section_layers.grid(
            row=0,
            column=0,
            padx=5,
            pady=8,
            sticky='ew'
        )
        self.section_layers.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.section_layers,
            text='Layers 图层管理器',
            font=ctk.CTkFont(size=14, weight='bold'),
            text_color='#818CF8'
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=10,
            pady=(10, 8),
            sticky='w'
        )

        self.add_btn_frame = ctk.CTkFrame(
            self.section_layers,
            fg_color='transparent'
        )
        self.add_btn_frame.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky='ew'
        )
        self.add_btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_add_text = ctk.CTkButton(
            self.add_btn_frame,
            text='➕ 动态文字',
            fg_color='#6366F1',
            hover_color='#4F46E5',
            height=28,
            command=lambda: self.add_layer('Text')
        )
        self.btn_add_text.grid(
            row=0,
            column=0,
            padx=2,
            sticky='ew'
        )

        self.btn_add_emoji = ctk.CTkButton(
            self.add_btn_frame,
            text='➕ Emoji 表情',
            fg_color='#818CF8',
            hover_color='#6366F1',
            height=28,
            command=lambda: self.add_layer('Emoji')
        )
        self.btn_add_emoji.grid(
            row=0,
            column=1,
            padx=2,
            sticky='ew'
        )

        self.btn_add_sticker = ctk.CTkButton(
            self.add_btn_frame,
            text='➕ 贴图动图',
            fg_color='#06B6D4',
            hover_color='#0891B2',
            height=28,
            command=lambda: self.add_layer('Sticker')
        )
        self.btn_add_sticker.grid(
            row=0,
            column=2,
            padx=2,
            sticky='ew'
        )

        self.btn_add_text.configure(state='disabled')
        self.btn_add_emoji.configure(state='disabled')
        self.btn_add_sticker.configure(state='disabled')

        self.group_btn_frame = ctk.CTkFrame(
            self.section_layers,
            fg_color='transparent'
        )
        self.group_btn_frame.grid(
            row=2,
            column=0,
            padx=10,
            pady=(0, 5),
            sticky='ew'
        )
        self.group_btn_frame.grid_columnconfigure((0, 1), weight=1)

        self.btn_group_layers = ctk.CTkButton(
            self.group_btn_frame,
            text='🔗 组合所选',
            fg_color='#F59E0B',
            hover_color='#D97706',
            height=28,
            font=ctk.CTkFont(family='Microsoft YaHei', size=12, weight='bold'),
            command=self.group_selected_layers
        )
        self.btn_group_layers.grid(
            row=0,
            column=0,
            padx=2,
            sticky='ew'
        )

        self.btn_ungroup_layers = ctk.CTkButton(
            self.group_btn_frame,
            text='🔓 取消组合',
            fg_color='#475569',
            hover_color='#64748B',
            height=28,
            font=ctk.CTkFont(family='Microsoft YaHei', size=12, weight='bold'),
            command=self.ungroup_selected_layers
        )
        self.btn_ungroup_layers.grid(
            row=0,
            column=1,
            padx=2,
            sticky='ew'
        )

        self.btn_group_layers.configure(state='disabled')
        self.btn_ungroup_layers.configure(state='disabled')

        self.layers_list_container = ctk.CTkScrollableFrame(
            self.section_layers,
            fg_color='#1E293B',
            height=130,
            label_text='涂鸦层叠加顺序 (最上层优先渲染)'
        )
        self.layers_list_container.grid(
            row=3,
            column=0,
            padx=10,
            pady=(5, 15),
            sticky='ew'
        )
        self.layers_list_container.grid_columnconfigure(0, weight=1)

        self.lbl_layers_empty = ctk.CTkLabel(
            self.layers_list_container,
            text='暂无图层，请导入后点击上方按钮添加',
            text_color='gray50'
        )
        self.lbl_layers_empty.grid(
            row=0,
            column=0,
            padx=10,
            pady=25
        )

        self.list_item_widgets = []

        self.attrs_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color='transparent'
        )
        self.attrs_frame.grid(
            row=1,
            column=0,
            padx=0,
            pady=0,
            sticky='ew'
        )
        self.attrs_frame.grid_columnconfigure(0, weight=1)

        self.sub_content = ctk.CTkFrame(
            self.attrs_frame,
            fg_color='#0F172A',
            corner_radius=8
        )
        self.sub_content.grid(
            row=0,
            column=0,
            padx=5,
            pady=6,
            sticky='ew'
        )
        self.sub_content.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.sub_content,
            text='✏️ 涂鸦内容与字体设置',
            font=ctk.CTkFont(size=13, weight='bold'),
            text_color='#818CF8'
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=10,
            pady=(8, 5),
            sticky='w'
        )

        self.lbl_content_desc = ctk.CTkLabel(
            self.sub_content,
            text='文字/Emoji内容:'
        )
        self.lbl_content_desc.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky='w'
        )

        self.entry_content = ctk.CTkEntry(
            self.sub_content,
            placeholder_text='输入文本或粘贴表情...'
        )
        self.entry_content.grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
            sticky='ew'
        )
        self.entry_content.bind('<KeyRelease>', self.on_attr_change)

        self.sticker_file_frame = ctk.CTkFrame(
            self.sub_content,
            fg_color='transparent'
        )
        self.sticker_file_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=5,
            sticky='ew'
        )
        self.sticker_file_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.sticker_file_frame,
            text='贴图路径:'
        ).grid(
            row=0,
            column=0,
            padx=(0, 10)
        )

        self.entry_sticker_path = ctk.CTkEntry(
            self.sticker_file_frame,
            state='readonly',
            placeholder_text='选择本地PNG/JPG/GIF...'
        )
        self.entry_sticker_path.grid(
            row=0,
            column=1,
            padx=(0, 8),
            sticky='ew'
        )

        self.btn_change_sticker = ctk.CTkButton(
            self.sticker_file_frame,
            text='🔍 更换贴图',
            width=70,
            height=26,
            fg_color='#475569',
            hover_color='#64748B',
            command=self.change_sticker_file
        )
        self.btn_change_sticker.grid(
            row=0,
            column=2
        )
        self.sticker_file_frame.grid_remove()

        self.lbl_font_desc = ctk.CTkLabel(
            self.sub_content,
            text='字体家族:'
        )
        self.lbl_font_desc.grid(
            row=3,
            column=0,
            padx=10,
            pady=5,
            sticky='w'
        )

        self.val_font = ctk.CTkOptionMenu(
            self.sub_content,
            values=['Microsoft YaHei', 'SimHei', 'Arial', 'Courier New', 'Comic Sans MS'],
            command=self.on_attr_change
        )
        self.val_font.grid(
            row=3,
            column=1,
            padx=10,
            pady=5,
            sticky='ew'
        )

        self.sub_position = ctk.CTkFrame(
            self.attrs_frame,
            fg_color='#0F172A',
            corner_radius=8
        )
        self.sub_position.grid(
            row=1,
            column=0,
            padx=5,
            pady=6,
            sticky='ew'
        )
        self.sub_position.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.sub_position,
            text='📐 空间定位与尺寸旋转',
            font=ctk.CTkFont(size=13, weight='bold'),
            text_color='#818CF8'
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            padx=10,
            pady=(8, 5),
            sticky='w'
        )

        ctk.CTkLabel(
            self.sub_position,
            text='水平位置 (X):'
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.val_x = ctk.CTkSlider(
            self.sub_position,
            from_=0.0,
            to=1.0,
            number_of_steps=200,
            command=self.on_attr_change
        )
        self.val_x.grid(
            row=1,
            column=1,
            padx=10,
            pady=4,
            sticky='ew'
        )

        self.lbl_x_disp = ctk.CTkLabel(
            self.sub_position,
            text='50%',
            text_color='gray60',
            width=40
        )
        self.lbl_x_disp.grid(
            row=1,
            column=2,
            padx=(0, 15)
        )

        ctk.CTkLabel(
            self.sub_position,
            text='垂直位置 (Y):'
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.val_y = ctk.CTkSlider(
            self.sub_position,
            from_=0.0,
            to=1.0,
            number_of_steps=200,
            command=self.on_attr_change
        )
        self.val_y.grid(
            row=2,
            column=1,
            padx=10,
            pady=4,
            sticky='ew'
        )

        self.lbl_y_disp = ctk.CTkLabel(
            self.sub_position,
            text='50%',
            text_color='gray60',
            width=40
        )
        self.lbl_y_disp.grid(
            row=2,
            column=2,
            padx=(0, 15)
        )

        self.lbl_scale_title = ctk.CTkLabel(
            self.sub_position,
            text='缩放比例/字号:'
        )
        self.lbl_scale_title.grid(
            row=3,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.val_scale = ctk.CTkSlider(
            self.sub_position,
            from_=0.1,
            to=4.0,
            number_of_steps=390,
            command=self.on_attr_change
        )
        self.val_scale.grid(
            row=3,
            column=1,
            padx=10,
            pady=4,
            sticky='ew'
        )

        self.lbl_scale_disp = ctk.CTkLabel(
            self.sub_position,
            text='1.0x',
            text_color='gray60',
            width=40
        )
        self.lbl_scale_disp.grid(
            row=3,
            column=2,
            padx=(0, 15)
        )

        ctk.CTkLabel(
            self.sub_position,
            text='旋转角度 (°):'
        ).grid(
            row=4,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.val_rotation = ctk.CTkSlider(
            self.sub_position,
            from_=0,
            to=360,
            number_of_steps=360,
            command=self.on_attr_change
        )
        self.val_rotation.grid(
            row=4,
            column=1,
            padx=10,
            pady=4,
            sticky='ew'
        )

        self.lbl_rotation_disp = ctk.CTkLabel(
            self.sub_position,
            text='0°',
            text_color='gray60',
            width=40
        )
        self.lbl_rotation_disp.grid(
            row=4,
            column=2,
            padx=(0, 15)
        )

        ctk.CTkLabel(
            self.sub_position,
            text='不透明度 (α):'
        ).grid(
            row=5,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.val_opacity = ctk.CTkSlider(
            self.sub_position,
            from_=0.0,
            to=1.0,
            number_of_steps=100,
            command=self.on_attr_change
        )
        self.val_opacity.grid(
            row=5,
            column=1,
            padx=10,
            pady=4,
            sticky='ew'
        )

        self.lbl_opacity_disp = ctk.CTkLabel(
            self.sub_position,
            text='100%',
            text_color='gray60',
            width=40
        )
        self.lbl_opacity_disp.grid(
            row=5,
            column=2,
            padx=(0, 15)
        )

        self.sub_motion = ctk.CTkFrame(
            self.attrs_frame,
            fg_color='#0F172A',
            corner_radius=8
        )
        self.sub_motion.grid(
            row=2,
            column=0,
            padx=5,
            pady=6,
            sticky='ew'
        )
        self.sub_motion.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.sub_motion,
            text='🌀 物理动态特效动画',
            font=ctk.CTkFont(size=13, weight='bold'),
            text_color='#818CF8'
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            padx=10,
            pady=(8, 5),
            sticky='w'
        )

        ctk.CTkLabel(
            self.sub_motion,
            text='动画特效轨迹:'
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky='w'
        )

        self.val_motion_type = ctk.CTkOptionMenu(
            self.sub_motion,
            values=['Static', 'Scroll Left', 'Scroll Right', 'Bounce Y', 'Float', 'Pulse', 'Typewriter', 'Rainbow', 'Fade'],
            command=self.on_attr_change
        )
        self.val_motion_type.grid(
            row=1,
            column=1,
            columnspan=2,
            padx=10,
            pady=5,
            sticky='ew'
        )

        ctk.CTkLabel(
            self.sub_motion,
            text='动效运行速度:'
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.val_motion_speed = ctk.CTkSlider(
            self.sub_motion,
            from_=0.1,
            to=5.0,
            number_of_steps=49,
            command=self.on_attr_change
        )
        self.val_motion_speed.grid(
            row=2,
            column=1,
            padx=10,
            pady=4,
            sticky='ew'
        )

        self.lbl_speed_disp = ctk.CTkLabel(
            self.sub_motion,
            text='1.0x',
            text_color='gray60',
            width=40
        )
        self.lbl_speed_disp.grid(
            row=2,
            column=2,
            padx=(0, 15)
        )

        ctk.CTkLabel(
            self.sub_motion,
            text='物理摆幅强度:'
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.val_motion_intensity = ctk.CTkSlider(
            self.sub_motion,
            from_=0.1,
            to=3.0,
            number_of_steps=29,
            command=self.on_attr_change
        )
        self.val_motion_intensity.grid(
            row=3,
            column=1,
            padx=10,
            pady=4,
            sticky='ew'
        )

        self.lbl_intensity_disp = ctk.CTkLabel(
            self.sub_motion,
            text='1.0x',
            text_color='gray60',
            width=40
        )
        self.lbl_intensity_disp.grid(
            row=3,
            column=2,
            padx=(0, 15)
        )

        self.sub_art = ctk.CTkFrame(
            self.attrs_frame,
            fg_color='#0F172A',
            corner_radius=8
        )
        self.sub_art.grid(
            row=3,
            column=0,
            padx=5,
            pady=6,
            sticky='ew'
        )
        self.sub_art.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(
            self.sub_art,
            text='🎨 高级艺术字排版样式',
            font=ctk.CTkFont(size=13, weight='bold'),
            text_color='#818CF8'
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            padx=10,
            pady=(8, 5),
            sticky='w'
        )

        ctk.CTkLabel(
            self.sub_art,
            text='核心填充:'
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.btn_main_color = ctk.CTkButton(
            self.sub_art,
            text='#FFFFFF',
            fg_color='#FFFFFF',
            text_color='#000000',
            hover_color='#E2E8F0',
            width=80,
            height=24,
            command=lambda: self.choose_color('main')
        )
        self.btn_main_color.grid(
            row=1,
            column=1,
            padx=5,
            pady=4,
            sticky='ew'
        )

        ctk.CTkLabel(
            self.sub_art,
            text='描边粗细:'
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.val_stroke_width = ctk.CTkSlider(
            self.sub_art,
            from_=0,
            to=8,
            number_of_steps=8,
            command=self.on_attr_change
        )
        self.val_stroke_width.grid(
            row=2,
            column=1,
            padx=5,
            pady=4,
            sticky='ew'
        )

        ctk.CTkLabel(
            self.sub_art,
            text='描边颜色:'
        ).grid(
            row=2,
            column=2,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.btn_stroke_color = ctk.CTkButton(
            self.sub_art,
            text='#000000',
            fg_color='#000000',
            text_color='#FFFFFF',
            hover_color='#1E293B',
            width=80,
            height=24,
            command=lambda: self.choose_color('stroke')
        )
        self.btn_stroke_color.grid(
            row=2,
            column=3,
            padx=(5, 15),
            pady=4,
            sticky='ew'
        )

        ctk.CTkLabel(
            self.sub_art,
            text='投影偏移 X:'
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.val_shadow_dx = ctk.CTkSlider(
            self.sub_art,
            from_=-15,
            to=15,
            number_of_steps=30,
            command=self.on_attr_change
        )
        self.val_shadow_dx.grid(
            row=3,
            column=1,
            padx=5,
            pady=4,
            sticky='ew'
        )

        ctk.CTkLabel(
            self.sub_art,
            text='投影偏移 Y:'
        ).grid(
            row=4,
            column=0,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.val_shadow_dy = ctk.CTkSlider(
            self.sub_art,
            from_=-15,
            to=15,
            number_of_steps=30,
            command=self.on_attr_change
        )
        self.val_shadow_dy.grid(
            row=4,
            column=1,
            padx=5,
            pady=4,
            sticky='ew'
        )

        ctk.CTkLabel(
            self.sub_art,
            text='阴影颜色:'
        ).grid(
            row=3,
            column=2,
            padx=10,
            pady=4,
            sticky='w'
        )

        self.btn_shadow_color = ctk.CTkButton(
            self.sub_art,
            text='#000000',
            fg_color='#000000',
            text_color='#FFFFFF',
            hover_color='#1E293B',
            width=80,
            height=24,
            command=lambda: self.choose_color('shadow')
        )
        self.btn_shadow_color.grid(
            row=3,
            column=3,
            padx=(5, 15),
            pady=4,
            sticky='ew'
        )

        self.val_glow_enabled = ctk.CTkCheckBox(
            self.sub_art,
            text='启用发光halo',
            text_color='gray90',
            font=ctk.CTkFont(size=12),
            command=self.on_attr_change
        )
        self.val_glow_enabled.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=10,
            pady=6,
            sticky='w'
        )

        self.btn_glow_color = ctk.CTkButton(
            self.sub_art,
            text='发光色',
            fg_color='#818CF8',
            hover_color='#6366F1',
            width=80,
            height=24,
            command=lambda: self.choose_color('glow')
        )
        self.btn_glow_color.grid(
            row=5,
            column=3,
            padx=(5, 15),
            pady=6,
            sticky='ew'
        )

        self.val_gradient_enabled = ctk.CTkCheckBox(
            self.sub_art,
            text='渐变色填充',
            text_color='gray90',
            font=ctk.CTkFont(size=12),
            command=self.on_attr_change
        )
        self.val_gradient_enabled.grid(
            row=6,
            column=0,
            columnspan=2,
            padx=10,
            pady=6,
            sticky='w'
        )

        self.btn_gradient_end = ctk.CTkButton(
            self.sub_art,
            text='渐变终色',
            fg_color='#FFFF00',
            text_color='#000000',
            hover_color='#E2E8F0',
            width=80,
            height=24,
            command=lambda: self.choose_color('gradient')
        )
        self.btn_gradient_end.grid(
            row=6,
            column=3,
            padx=(5, 15),
            pady=6,
            sticky='ew'
        )

        self.sub_timing = ctk.CTkFrame(
            self.attrs_frame,
            fg_color='#0F172A',
            corner_radius=8
        )
        self.sub_timing.grid(
            row=4,
            column=0,
            padx=5,
            pady=6,
            sticky='ew'
        )
        self.sub_timing.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(
            self.sub_timing,
            text='⏱️ 涂鸦显现帧区间微调',
            font=ctk.CTkFont(size=13, weight='bold'),
            text_color='#818CF8'
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            padx=10,
            pady=(8, 5),
            sticky='w'
        )

        self.val_always_show = ctk.CTkCheckBox(
            self.sub_timing,
            text='全程持续显示 (忽略区间)',
            text_color='gray90',
            command=self.toggle_timing_mode
        )
        self.val_always_show.select()
        self.val_always_show.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=10,
            pady=5,
            sticky='w'
        )

        self.timing_bounds_frame = ctk.CTkFrame(
            self.sub_timing,
            fg_color='transparent'
        )
        self.timing_bounds_frame.grid(
            row=2,
            column=0,
            columnspan=4,
            padx=10,
            pady=5,
            sticky='ew'
        )
        self.timing_bounds_frame.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(
            self.timing_bounds_frame,
            text='起始帧:'
        ).grid(
            row=0,
            column=0,
            padx=(0, 5)
        )

        self.val_start_frame = ctk.CTkSlider(
            self.timing_bounds_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self.on_attr_change
        )
        self.val_start_frame.grid(
            row=0,
            column=1,
            padx=5,
            sticky='ew'
        )

        self.lbl_start_frame_disp = ctk.CTkLabel(
            self.timing_bounds_frame,
            text='0',
            text_color='gray60',
            width=25
        )
        self.lbl_start_frame_disp.grid(
            row=0,
            column=2
        )

        ctk.CTkLabel(
            self.timing_bounds_frame,
            text='结束帧:'
        ).grid(
            row=0,
            column=3,
            padx=(10, 5)
        )

        self.val_end_frame = ctk.CTkSlider(
            self.timing_bounds_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self.on_attr_change
        )
        self.val_end_frame.grid(
            row=0,
            column=4,
            padx=5,
            sticky='ew'
        )

        self.lbl_end_frame_disp = ctk.CTkLabel(
            self.timing_bounds_frame,
            text='0',
            text_color='gray60',
            width=25
        )
        self.lbl_end_frame_disp.grid(
            row=0,
            column=5
        )

        self.timing_bounds_frame.grid_remove()
        self.attrs_frame.grid_remove()

    def create_bottom_progress(self):
        """Action panel at the bottom."""
        self.bottom_frame = ctk.CTkFrame(self, fg_color='#1E293B', corner_radius=10)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=(10, 0), sticky='ew')
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.action_layout = ctk.CTkFrame(self.bottom_frame, fg_color='transparent')
        self.action_layout.grid(row=0, column=0, padx=20, pady=(15, 10), sticky='ew')
        self.action_layout.grid_columnconfigure(0, weight=1)
        self.btn_compile = ctk.CTkButton(
            self.action_layout,
            text='🚀 一键急速渲染 —— 保存涂鸦装饰后的新 GIF',
            height=45,
            fg_color='#6366F1',
            hover_color='#4F46E5',
            font=ctk.CTkFont(size=15, weight='bold', family='Microsoft YaHei'),
            command=self.start_deco_rendering
        )
        self.btn_compile.grid(row=0, column=0, sticky='ew', padx=(0, 10))
        self.btn_compile.configure(state='disabled')
        self.btn_save_gif = ctk.CTkButton(
            self.action_layout,
            text='💾 导出另存为...',
            height=45,
            fg_color='#10B981',
            hover_color='#059669',
            font=ctk.CTkFont(size=15, weight='bold', family='Microsoft YaHei'),
            command=self.save_decorated_gif
        )
        self.btn_save_gif.grid(row=0, column=1, sticky='e')
        self.btn_save_gif.configure(state='disabled')
        self.lbl_status = ctk.CTkLabel(
            self.bottom_frame,
            text='等待载入目标 GIF 文件...',
            text_color='gray60',
            anchor='w'
        )
        self.lbl_status.grid(row=1, column=0, padx=20, pady=(0, 2), sticky='ew')
        self.progress_bar = ctk.CTkProgressBar(
            self.bottom_frame,
            fg_color='#0F172A',
            progress_color='#818CF8'
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, padx=20, pady=(0, 15), sticky='ew')

    def import_source_gif(self):
        """Selects and loads local GIF frames."""
        path = filedialog.askopenfilename(
            title='选择要进行涂鸦装饰的 GIF 动图',
            filetypes=[('GIF 图片', '*.gif')]
        )
        if not path:
            return
        self.load_gif_from_path(path)

    def load_gif_from_path(self, path):
        """Loads and extracts a GIF file into frames cache."""
        self.stop_play()
        self.lbl_status.configure(text='正在读取并提取 GIF 序列帧...')
        self.progress_bar.set(0.1)
        self.update()
        try:
            with Image.open(path) as img:
                w, h = img.size
                total = getattr(img, 'n_frames', 1)
                self.source_frames = []
                self.source_delays = []
                for idx, frame in enumerate(ImageSequence.Iterator(img)):
                    self.source_frames.append(frame.copy().convert('RGB'))
                    dur = frame.info.get('duration', 100)
                    self.source_delays.append(dur if dur > 10 else 100)
            self.source_gif_path = path
            self.gif_loaded = True
            self.current_frame_idx = 0
            filename = os.path.basename(path)
            self.lbl_gif_info.configure(
                text=f"{filename} | {w}x{h} | {total} 帧",
                text_color='#10B981'
            )
            self.slider_timeline.configure(
                state='normal',
                from_=0,
                to=total - 1,
                number_of_steps=total - 1
            )
            self.slider_timeline.set(0)
            self.lbl_frame_info.configure(text=f"帧: 1 / {total}")
            self.val_start_frame.configure(
                from_=0,
                to=total - 1,
                number_of_steps=total - 1
            )
            self.val_end_frame.configure(
                from_=0,
                to=total - 1,
                number_of_steps=total - 1
            )
            self.val_start_frame.set(0)
            self.val_end_frame.set(total - 1)
            
            self.btn_play.configure(state='normal')
            self.btn_add_text.configure(state='normal')
            self.btn_add_emoji.configure(state='normal')
            self.btn_add_sticker.configure(state='normal')
            self.btn_group_layers.configure(state='normal')
            self.btn_ungroup_layers.configure(state='normal')
            self.btn_compile.configure(state='normal')
            
            self.lbl_status.configure(text='GIF 载入成功！点击右侧按钮添加文字或贴图')
            self.progress_bar.set(0)
            self.refresh_preview()
        except Exception as e:
            self.lbl_status.configure(
                text=f"读取失败: {str(e)}",
                text_color='#EF4444'
            )
            self.progress_bar.set(0)
            messagebox.showerror('载入失败', f"无法解析该 GIF 文件:\n{str(e)}")

    def refresh_preview(self):
        """Renders current frame with active layers and paints onto canvas."""
        if not self.gif_loaded or not self.source_frames:
            return
        idx = self.current_frame_idx
        total = len(self.source_frames)
        base_frame = self.source_frames[idx]
        rendered_frame = self.processor.render_frame(base_frame, idx, total, self.layers)
        w, h = rendered_frame.size
        self.update_idletasks()
        cw = max(1, self.preview_canvas.winfo_width())
        ch = max(1, self.preview_canvas.winfo_height())
        max_w = max(400, cw - 30)
        scale = min(1.0, max_w / w)
        self.display_scale = scale
        preview_w = int(w * scale)
        preview_h = int(h * scale)
        ox = max(0, (cw - preview_w) // 2)
        oy = max(0, (ch - preview_h) // 2)
        self.img_ox = ox
        self.img_oy = oy
        resized = rendered_frame.resize((preview_w, preview_h), Image.Resampling.NEAREST)
        self.preview_image_tk = ImageTk.PhotoImage(resized)
        self.preview_canvas.delete('all')
        self.preview_canvas.create_image(
            ox,
            oy,
            anchor='nw',
            image=self.preview_image_tk,
            tags='bg_image'
        )
        self.lbl_frame_info.configure(text=f"帧: {idx + 1} / {total}")
        self._draw_canvas_selection_overlays()

    def on_scrub(self, value):
        """Scrub slider timeline updates frame preview instantly."""
        self.current_frame_idx = int(value)
        self.refresh_preview()

    def toggle_play(self):
        """Starts/stops the real-time playback loop."""
        if not self.gif_loaded:
            return
        if self.is_playing:
            self.stop_play()
            return
        self.is_playing = True
        self.btn_play.configure(
            text='⏸ 暂停预览',
            fg_color='#E11D48',
            hover_color='#BE123C'
        )
        self.play_loop()

    def play_loop(self):
        """Sequential loop playback using Tkinter after hooks."""
        if not self.is_playing or not self.source_frames:
            return
        total = len(self.source_frames)
        self.current_frame_idx = (self.current_frame_idx + 1) % total
        self.slider_timeline.set(self.current_frame_idx)
        self.refresh_preview()
        delay = self.source_delays[self.current_frame_idx]
        self.play_after_id = self.after(delay, self.play_loop)

    def stop_play(self):
        """Halts looping thread safely."""
        self.is_playing = False
        if self.play_after_id:
            self.after_cancel(self.play_after_id)
            self.play_after_id = None
        self.btn_play.configure(
            text='▶ 播放预览',
            fg_color='#10B981',
            hover_color='#059669'
        )

    def add_layer(self, layer_type):
        """Spawns a new DecoLayer overlay."""
        if not self.gif_loaded:
            return
        layer_id = len(self.layers) + 1
        if layer_type == 'Text':
            new_layer = DecoLayer(layer_id, 'Text', '新建文字')
        elif layer_type == 'Emoji':
            new_layer = DecoLayer(layer_id, 'Emoji', '🌟')
            new_layer.scale = 1.2
        elif layer_type == 'Sticker':
            path = filedialog.askopenfilename(
                title='选择导入要作为贴图的图片或动图',
                filetypes=[
                    ('支持格式', '*.png *.jpg *.jpeg *.gif'),
                    ('全部文件', '*.*')
                ]
            )
            if not path:
                return
            new_layer = DecoLayer(layer_id, 'Sticker', path)
            new_layer.load_sticker()
        
        self.layers.append(new_layer)
        self.selected_layer = new_layer
        self.refresh_layers_list()
        self.select_layer_by_widget(new_layer)
        self.refresh_preview()

    def delete_layer(self, layer):
        """Removes the target layer overlay."""
        if layer in self.layers:
            self.layers.remove(layer)
            if self.selected_layer == layer:
                self.selected_layer = None
                self.attrs_frame.grid_remove()
            self.refresh_layers_list()
            self.refresh_preview()

    def move_layer(self, layer, direction):
        """Swaps Z-index sorting layer position (direction: -1 = Up, 1 = Down)."""
        idx = self.layers.index(layer)
        new_idx = idx + direction
        if 0 <= new_idx < len(self.layers):
            self.layers[idx], self.layers[new_idx] = self.layers[new_idx], self.layers[idx]
            self.refresh_layers_list()
            self.refresh_preview()

    def refresh_layers_list(self):
        """Re-draws scroll list panel."""
        for w in self.list_item_widgets:
            w.destroy()
        self.list_item_widgets = []
        if not self.layers:
            self.lbl_layers_empty.grid()
            return
        self.lbl_layers_empty.grid_remove()
        for idx, layer in enumerate(reversed(self.layers)):
            real_idx = len(self.layers) - 1 - idx
            item = ctk.CTkFrame(
                self.layers_list_container,
                fg_color='#334155' if self.selected_layer == layer else '#1E293B',
                height=38
            )
            item.grid(row=idx, column=0, padx=5, pady=3, sticky='ew')
            item.grid_columnconfigure(1, weight=1)
            lbl_name = ctk.CTkLabel(
                item,
                text=layer.get_display_name(),
                anchor='w',
                text_color='white',
                font=ctk.CTkFont(size=12)
            )
            lbl_name.grid(row=0, column=0, columnspan=2, padx=10, sticky='ew')
            lbl_name.bind('<Button-1>', lambda event, l=layer: self.select_layer_by_widget(l))
            item.bind('<Button-1>', lambda event, l=layer: self.select_layer_by_widget(l))
            
            ctrl_box = ctk.CTkFrame(item, fg_color='transparent')
            ctrl_box.grid(row=0, column=2, padx=5)
            
            btn_up = ctk.CTkButton(
                ctrl_box,
                text='▲',
                width=22,
                height=22,
                fg_color='#475569',
                hover_color='#64748B',
                command=lambda l=layer: self.move_layer(l, 1)
            )
            btn_up.grid(row=0, column=0, padx=1)
            
            btn_down = ctk.CTkButton(
                ctrl_box,
                text='▼',
                width=22,
                height=22,
                fg_color='#475569',
                hover_color='#64748B',
                command=lambda l=layer: self.move_layer(l, -1)
            )
            btn_down.grid(row=0, column=1, padx=1)
            
            btn_del = ctk.CTkButton(
                ctrl_box,
                text='✕',
                width=22,
                height=22,
                fg_color='#E11D48',
                hover_color='#BE123C',
                command=lambda l=layer: self.delete_layer(l)
            )
            btn_del.grid(row=0, column=2, padx=1)
            
            if real_idx == len(self.layers) - 1:
                btn_up.configure(state='disabled')
            if real_idx == 0:
                btn_down.configure(state='disabled')
                
            self.list_item_widgets.append(item)

    def select_layer_by_widget(self, layer):
        """Switches currently edited layer and populates property sliders."""
        self.selected_layer = layer
        self.refresh_layers_list()
        self.attrs_frame.grid()
        self.block_trigger = True
        
        if layer.type == 'Sticker':
            self.lbl_content_desc.grid_remove()
            self.entry_content.grid_remove()
            self.lbl_font_desc.grid_remove()
            self.val_font.grid_remove()
            self.sub_art.grid_remove()
            
            self.sticker_file_frame.grid()
            self.entry_sticker_path.configure(state='normal')
            self.entry_sticker_path.delete(0, tk.END)
            self.entry_sticker_path.insert(0, layer.content)
            self.entry_sticker_path.configure(state='readonly')
            self.lbl_scale_title.configure(text='贴图尺寸缩放:')
        else:
            self.sticker_file_frame.grid_remove()
            self.lbl_content_desc.grid()
            self.entry_content.grid()
            self.entry_content.delete(0, tk.END)
            self.entry_content.insert(0, layer.content)
            self.lbl_scale_title.configure(text='文字字体大小:')
            
            if layer.type == 'Emoji':
                self.lbl_font_desc.grid_remove()
                self.val_font.grid_remove()
                self.sub_art.grid_remove()
            else:
                self.lbl_font_desc.grid()
                self.val_font.grid()
                self.val_font.set(layer.font_family)
                self.sub_art.grid()
                
                self.btn_main_color.configure(
                    fg_color=layer.color,
                    text=layer.color,
                    text_color='#000000' if self.is_light_color(layer.color) else '#FFFFFF'
                )
                self.val_stroke_width.set(layer.stroke_width)
                self.btn_stroke_color.configure(
                    fg_color=layer.stroke_color,
                    text=layer.stroke_color,
                    text_color='#000000' if self.is_light_color(layer.stroke_color) else '#FFFFFF'
                )
                self.val_shadow_dx.set(layer.shadow_dx)
                self.val_shadow_dy.set(layer.shadow_dy)
                self.btn_shadow_color.configure(
                    fg_color=layer.shadow_color,
                    text=layer.shadow_color,
                    text_color='#000000' if self.is_light_color(layer.shadow_color) else '#FFFFFF'
                )
                if layer.glow_enabled:
                    self.val_glow_enabled.select()
                else:
                    self.val_glow_enabled.deselect()
                    
                self.btn_glow_color.configure(
                    fg_color=layer.glow_color,
                    text=layer.glow_color,
                    text_color='#000000' if self.is_light_color(layer.glow_color) else '#FFFFFF'
                )
                if layer.gradient_enabled:
                    self.val_gradient_enabled.select()
                else:
                    self.val_gradient_enabled.deselect()
                    
                self.btn_gradient_end.configure(
                    fg_color=layer.gradient_end_color,
                    text=layer.gradient_end_color,
                    text_color='#000000' if self.is_light_color(layer.gradient_end_color) else '#FFFFFF'
                )
        
        self.val_x.set(layer.x_pct)
        self.val_y.set(layer.y_pct)
        self.val_scale.set(layer.scale)
        self.val_rotation.set(layer.rotation)
        self.val_opacity.set(layer.opacity)
        
        self.lbl_x_disp.configure(text=f"{int(layer.x_pct * 100)}%")
        self.lbl_y_disp.configure(text=f"{int(layer.y_pct * 100)}%")
        self.lbl_scale_disp.configure(text=f"{layer.scale:.2f}x")
        self.lbl_rotation_disp.configure(text=f"{int(layer.rotation)}°")
        self.lbl_opacity_disp.configure(text=f"{int(layer.opacity * 100)}%")
        
        self.val_motion_type.set(layer.motion_type)
        self.val_motion_speed.set(layer.motion_speed)
        self.val_motion_intensity.set(layer.motion_intensity)
        self.lbl_speed_disp.configure(text=f"{layer.motion_speed:.1f}x")
        self.lbl_intensity_disp.configure(text=f"{layer.motion_intensity:.1f}x")
        
        if layer.always_show:
            self.val_always_show.select()
            self.timing_bounds_frame.grid_remove()
        else:
            self.val_always_show.deselect()
            self.timing_bounds_frame.grid()
            
        self.val_start_frame.set(layer.start_frame)
        self.val_end_frame.set(layer.end_frame if layer.end_frame >= 0 else len(self.source_frames) - 1)
        self.lbl_start_frame_disp.configure(text=str(layer.start_frame))
        self.lbl_end_frame_disp.configure(
            text=str(layer.end_frame if layer.end_frame >= 0 else len(self.source_frames) - 1)
        )
        self.block_trigger = False

    def on_attr_change(self, value):
        """Fires when sliders move or text box is typed. Syncs settings back to target layer."""
        if hasattr(self, 'block_trigger') and self.block_trigger:
            return
        if not self.selected_layer:
            return
        layer = self.selected_layer
        if layer.type != 'Sticker':
            layer.content = self.entry_content.get()
            layer.font_family = self.val_font.get()
        layer.x_pct = self.val_x.get()
        layer.y_pct = self.val_y.get()
        layer.scale = self.val_scale.get()
        layer.rotation = self.val_rotation.get()
        layer.opacity = self.val_opacity.get()
        
        self.lbl_x_disp.configure(text=f"{int(layer.x_pct * 100)}%")
        self.lbl_y_disp.configure(text=f"{int(layer.y_pct * 100)}%")
        self.lbl_scale_disp.configure(text=f"{layer.scale:.2f}x")
        self.lbl_rotation_disp.configure(text=f"{int(layer.rotation)}°")
        self.lbl_opacity_disp.configure(text=f"{int(layer.opacity * 100)}%")
        
        layer.motion_type = self.val_motion_type.get()
        layer.motion_speed = self.val_motion_speed.get()
        layer.motion_intensity = self.val_motion_intensity.get()
        self.lbl_speed_disp.configure(text=f"{layer.motion_speed:.1f}x")
        self.lbl_intensity_disp.configure(text=f"{layer.motion_intensity:.1f}x")
        
        layer.always_show = self.val_always_show.get()
        layer.start_frame = int(self.val_start_frame.get())
        layer.end_frame = int(self.val_end_frame.get())
        
        self.lbl_start_frame_disp.configure(text=str(layer.start_frame))
        self.lbl_end_frame_disp.configure(text=str(layer.end_frame))
        
        if layer.start_frame > layer.end_frame:
            layer.end_frame = layer.start_frame
            self.block_trigger = True
            self.val_end_frame.set(layer.end_frame)
            self.lbl_end_frame_disp.configure(text=str(layer.end_frame))
            self.block_trigger = False
            
        if layer.type == 'Text':
            layer.stroke_width = int(self.val_stroke_width.get())
            layer.shadow_dx = int(self.val_shadow_dx.get())
            layer.shadow_dy = int(self.val_shadow_dy.get())
            layer.glow_enabled = self.val_glow_enabled.get()
            layer.gradient_enabled = self.val_gradient_enabled.get()
            
        self.refresh_preview()

    def toggle_timing_mode(self):
        """Collapses or expands frame ranges depending on always_show checkbox."""
        if self.val_always_show.get():
            self.timing_bounds_frame.grid_remove()
        else:
            self.timing_bounds_frame.grid()
        self.on_attr_change(None)

    def change_sticker_file(self):
        """Allows replacing the image source file of a sticker layer."""
        if not self.selected_layer or self.selected_layer.type != 'Sticker':
            return
        path = filedialog.askopenfilename(
            title='更换贴图图片/动图',
            filetypes=[
                ('图像文件', '*.png *.jpg *.jpeg *.gif'),
                ('全部文件', '*.*')
            ]
        )
        if not path:
            return
        self.selected_layer.content = path
        self.selected_layer.load_sticker()
        self.block_trigger = True
        self.entry_sticker_path.configure(state='normal')
        self.entry_sticker_path.delete(0, tk.END)
        self.entry_sticker_path.insert(0, path)
        self.entry_sticker_path.configure(state='readonly')
        self.block_trigger = False
        self.refresh_layers_list()
        self.refresh_preview()

    def choose_color(self, target):
        """Triggers standard colorpicker for text art attributes."""
        if not self.selected_layer or self.selected_layer.type != 'Text':
            return
        layer = self.selected_layer
        init_color = '#FFFFFF'
        if target == 'main':
            init_color = layer.color
        elif target == 'stroke':
            init_color = layer.stroke_color
        elif target == 'shadow':
            init_color = layer.shadow_color
        elif target == 'glow':
            init_color = layer.glow_color
        elif target == 'gradient':
            init_color = layer.gradient_end_color
            
        color = colorchooser.askcolor(initialcolor=init_color, title='选择文字效果色彩')
        if not color[1]:
            return
        val = color[1]
        is_light = self.is_light_color(val)
        txt_c = '#000000' if is_light else '#FFFFFF'
        
        if target == 'main':
            layer.color = val
            self.btn_main_color.configure(fg_color=val, text=val, text_color=txt_c)
        elif target == 'stroke':
            layer.stroke_color = val
            self.btn_stroke_color.configure(fg_color=val, text=val, text_color=txt_c)
        elif target == 'shadow':
            layer.shadow_color = val
            self.btn_shadow_color.configure(fg_color=val, text=val, text_color=txt_c)
        elif target == 'glow':
            layer.glow_color = val
            self.btn_glow_color.configure(fg_color=val, text=val, text_color=txt_c)
        elif target == 'gradient':
            layer.gradient_end_color = val
            self.btn_gradient_end.configure(fg_color=val, text=val, text_color=txt_c)
            
        self.on_attr_change(None)

    def is_light_color(self, hex_color):
        """Determines if hex color is light or dark (for button text contrasts)."""
        rgb = self.processor.hex_to_rgb(hex_color)
        luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
        return luminance > 160

    def start_deco_rendering(self):
        """Launches threaded background compiler."""
        if not self.gif_loaded or not self.source_frames:
            return
        self.stop_play()
        self.btn_compile.configure(state='disabled')
        self.btn_save_gif.configure(state='disabled')
        self.progress_bar.set(0)
        self.lbl_status.configure(text='正在初始化涂鸦贴图编译引擎...')
        t = threading.Thread(target=self._threaded_render_compile, daemon=True)
        t.start()

    def _threaded_render_compile(self):
        def update_progress(val, status_text):
            self.after(0, lambda: self.progress_bar.set(val))
            self.after(0, lambda: self.lbl_status.configure(text=status_text))
            
        try:
            total_frames = len(self.source_frames)
            decorated_frames = []
            for idx in range(total_frames):
                update_progress(
                    0.85 * (idx + 1) / total_frames,
                    f"正在将图层装饰合成到帧... ({idx + 1}/{total_frames})"
                )
                base_frame = self.source_frames[idx]
                rendered = self.processor.render_frame(base_frame, idx, total_frames, self.layers)
                decorated_frames.append(rendered)
                
            update_progress(0.9, '帧图层合成完毕，启动高精调色板 GIF 编码压缩...')
            
            enc_opt = {
                'colors': 256,
                'dither': True,
                'global_palette': True,
                'delays': self.source_delays.copy()
            }
            
            result = self.app.gif_encoder.save_gif(
                decorated_frames,
                self.temp_deco_path,
                options=enc_opt,
                progress_callback=update_progress
            )
            
            self.after(0, lambda: self.show_render_success(result))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror('涂鸦生成失败', f'编译合成中出错:\n{str(e)}'))
            self.after(0, lambda: self.lbl_status.configure(text=f"生成失败: {str(e)}", text_color='#EF4444'))
            self.after(0, lambda: self.progress_bar.set(0))
            self.after(0, lambda: self.btn_compile.configure(state='normal'))

    def show_render_success(self, result):
        """Displays preview play modal on compilation completion."""
        self.lbl_status.configure(
            text=f"图层装饰成功！生成大小: {result['size_mb']:.2f} MB | {result['total_frames']} 帧",
            text_color='#10B981'
        )
        self.progress_bar.set(1.0)
        self.btn_compile.configure(state='normal')
        self.btn_save_gif.configure(state='normal')
        
        preview_win = ctk.CTkToplevel(self)
        preview_win.title('🎉 涂鸦装饰 GIF 生成预览')
        preview_win.geometry('520x540')
        preview_win.minsize(450, 480)
        preview_win.lift()
        preview_win.grab_set()
        
        preview_win.grid_rowconfigure(1, weight=1)
        preview_win.grid_columnconfigure(0, weight=1)
        
        info_text = f"🎉 涂鸦装饰成功！生成新 GIF 大小: {result['size_mb']:.2f} MB\n请在下方确认最终动效，满意后点击另存导出保存文件"
        lbl_info = ctk.CTkLabel(
            preview_win,
            text=info_text,
            justify='center',
            font=ctk.CTkFont(family='Microsoft YaHei', size=13)
        )
        lbl_info.grid(row=0, column=0, padx=20, pady=15, sticky='ew')
        
        try:
            from PIL import Image, ImageTk
            import tkinter as tk
            
            preview_frame = ctk.CTkFrame(preview_win, fg_color='#0F172A', corner_radius=10)
            preview_frame.grid(row=1, column=0, padx=20, pady=5, sticky='nsew')
            preview_frame.grid_rowconfigure(0, weight=1)
            preview_frame.grid_columnconfigure(0, weight=1)
            
            _canvas = tk.Canvas(preview_frame, bg='#0A0F1E', highlightthickness=0)
            _canvas.grid(row=0, column=0, sticky='nsew')
            
            _frames = []
            _delays = []
            _after_id = [None]
            _idx = [0]
            
            with Image.open(self.temp_deco_path) as _img:
                _w, _h = _img.size
                _scale = min(1.0, 440 / _w)
                _pw, _ph = int(_w * _scale), int(_h * _scale)
                for _i in range(getattr(_img, 'n_frames', 1)):
                    _img.seek(_i)
                    _f = _img.copy().convert('RGBA').resize((_pw, _ph), Image.Resampling.LANCZOS)
                    _frames.append(ImageTk.PhotoImage(_f))
                    _d = _img.info.get('duration', 100)
                    _delays.append(max(20, _d))
                    
            _canvas.config(width=_pw, height=_ph)
            
            def _play():
                if not _frames:
                    return
                _canvas.delete('all')
                _canvas.create_image(0, 0, anchor='nw', image=_frames[_idx[0]])
                _after_id[0] = preview_win.after(_delays[_idx[0]], _play)
                _idx[0] = (_idx[0] + 1) % len(_frames)
                
            _play()
            
            def _on_close():
                if _after_id[0]:
                    preview_win.after_cancel(_after_id[0])
                preview_win.grab_release()
                preview_win.destroy()
                
            preview_win.protocol('WM_DELETE_WINDOW', _on_close)
        except Exception as _e:
            ctk.CTkLabel(
                preview_win,
                text=f"预览加载失败: {str(_e)}"
            ).grid(row=1, column=0)
            
        btn_frame = ctk.CTkFrame(preview_win, fg_color='transparent')
        btn_frame.grid(row=2, column=0, padx=20, pady=15, sticky='ew')
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        
        def save_and_close():
            preview_win.grab_release()
            preview_win.destroy()
            self.save_decorated_gif()
            
        btn_save = ctk.CTkButton(
            btn_frame,
            text='💾 另存导出新 GIF',
            fg_color='#10B981',
            hover_color='#059669',
            height=38,
            command=save_and_close
        )
        btn_save.grid(row=0, column=0, padx=(0, 5), sticky='ew')
        
        btn_close = ctk.CTkButton(
            btn_frame,
            text='❌ 关闭预览',
            fg_color='#334155',
            hover_color='#475569',
            height=38,
            command=lambda: [preview_win.grab_release(), preview_win.destroy()]
        )
        btn_close.grid(row=0, column=1, padx=(5, 0), sticky='ew')
        
        preview_win.protocol('WM_DELETE_WINDOW', lambda: [preview_win.grab_release(), preview_win.destroy()])

    def save_decorated_gif(self):
        """Copies compiled temporary GIF to user destination."""
        if not os.path.exists(self.temp_deco_path):
            return
        save_path = filedialog.asksaveasfilename(
            title='导出涂鸦装饰后的 GIF 动图',
            defaultextension='.gif',
            filetypes=[('GIF Image', '*.gif')]
        )
        if not save_path:
            return
        try:
            shutil.copy(self.temp_deco_path, save_path)
            if hasattr(self.app, 'workspace_dir') and os.path.exists(self.app.workspace_dir):
                ws_dest = os.path.join(self.app.workspace_dir, os.path.basename(save_path))
                shutil.copy(self.temp_deco_path, ws_dest)
            self.lbl_status.configure(text=f"导出成功！已保存至 {os.path.basename(save_path)}")
            messagebox.showinfo('导出成功', f"恭喜！涂鸦贴图 GIF 已经成功导出并保存到:\n{save_path}")
        except Exception as e:
            messagebox.showerror('导出失败', f"无法写入目标文件:\n{str(e)}")

    def _get_layer_canvas_coords(self, layer):
        """Returns (disp_x, disp_y, disp_w, disp_h) for a layer projected onto canvas space."""
        if not self.gif_loaded or not self.source_frames:
            return
        base_frame = self.source_frames[self.current_frame_idx]
        W, H = base_frame.size
        cw = max(1, self.preview_canvas.winfo_width())
        ch = max(1, self.preview_canvas.winfo_height())
        scale = getattr(self, 'display_scale', 1.0)
        preview_w = int(W * scale)
        preview_h = int(H * scale)
        ox = max(0, (cw - preview_w) // 2)
        oy = max(0, (ch - preview_h) // 2)
        x_base = layer.x_pct * W
        y_base = layer.y_pct * H
        base_w = 80
        base_h = 30
        
        if layer.type == 'Text':
            base_w = len(layer.content) * 15 * layer.scale
            base_h = 24 * layer.scale
        elif layer.type == 'Emoji':
            base_w = 32 * layer.scale
            base_h = 32 * layer.scale
        elif layer.type == 'Sticker' and layer._sticker_cache:
            base_w = layer._sticker_cache[0].width * layer.scale
            base_h = layer._sticker_cache[0].height * layer.scale
            
        disp_w = base_w * scale
        disp_h = base_h * scale
        disp_x = ox + x_base * scale
        disp_y = oy + y_base * scale
        return disp_x, disp_y, disp_w, disp_h

    def _draw_canvas_selection_overlays(self):
        """Draws bounding boxes and corner resize handles for selected layers."""
        self.preview_canvas.delete('overlay')
        if not hasattr(self, 'selected_layers'):
            self.selected_layers = []
        if self.selected_layer and self.selected_layer not in self.selected_layers:
            self.selected_layers = [self.selected_layer]
        for layer in self.selected_layers:
            coords = self._get_layer_canvas_coords(layer)
            if not coords:
                continue
            disp_x, disp_y, disp_w, disp_h = coords
            x1 = disp_x - disp_w / 2
            y1 = disp_y - disp_h / 2
            x2 = disp_x + disp_w / 2
            y2 = disp_y + disp_h / 2
            self.preview_canvas.create_rectangle(
                x1, y1, x2, y2,
                outline='#F59E0B',
                width=1,
                dash=(5, 3),
                tags='overlay'
            )
            sz = 4
            self.preview_canvas.create_rectangle(
                x2 - sz, y2 - sz, x2 + sz, y2 + sz,
                fill='#F59E0B',
                outline='#FFFFFF',
                width=1,
                tags=('overlay', 'resize_handle')
            )

    def _on_canvas_click(self, event):
        if not self.gif_loaded or not self.layers:
            return
        mx, my = event.x, event.y
        if not hasattr(self, 'selected_layers'):
            self.selected_layers = []
        for layer in self.selected_layers:
            coords = self._get_layer_canvas_coords(layer)
            if not coords:
                continue
            disp_x, disp_y, disp_w, disp_h = coords
            x2 = disp_x + disp_w / 2
            y2 = disp_y + disp_h / 2
            if abs(mx - x2) <= 10 and abs(my - y2) <= 10:
                self._drag_mode = 'resize'
                self._resize_layer = layer
                self._drag_start = (mx, my)
                self._layer_start_scale = layer.scale
                return
        clicked_layer = None
        for layer in reversed(self.layers):
            coords = self._get_layer_canvas_coords(layer)
            if not coords:
                continue
            disp_x, disp_y, disp_w, disp_h = coords
            x1 = disp_x - disp_w / 2
            y1 = disp_y - disp_h / 2
            x2 = disp_x + disp_w / 2
            y2 = disp_y + disp_h / 2
            if x1 <= mx <= x2 and y1 <= my <= y2:
                clicked_layer = layer
                break
        is_multi = bool(event.state & 1) or bool(event.state & 4)
        if clicked_layer:
            if hasattr(clicked_layer, 'group_id') and clicked_layer.group_id:
                group_layers = [l for l in self.layers if getattr(l, 'group_id', 0) == clicked_layer.group_id]
            else:
                group_layers = [clicked_layer]
                
            if is_multi:
                for l in group_layers:
                    if l in self.selected_layers:
                        self.selected_layers.remove(l)
                    else:
                        self.selected_layers.append(l)
            else:
                self.selected_layers = group_layers
                
            self.selected_layer = self.selected_layers[-1] if self.selected_layers else None
            if self.selected_layer:
                self.select_layer_by_widget(self.selected_layer)
                
            self._drag_mode = 'move'
            self._drag_start = (mx, my)
            self._layer_start_positions = {l: (l.x_pct, l.y_pct) for l in self.selected_layers}
        else:
            if not is_multi:
                self.selected_layers.clear()
                self.selected_layer = None
                self.attrs_frame.grid_remove()
                
        self.refresh_layers_list()
        self.refresh_preview()

    def _on_canvas_drag(self, event):
        """_drag_mode"""
        if not self.gif_loaded or not getattr(self, '_drag_mode', None) or not self.selected_layers:
            return
        mx, my = event.x, event.y
        start_x, start_y = self._drag_start
        dx = mx - start_x
        dy = my - start_y
        base_frame = self.source_frames[self.current_frame_idx]
        W, H = base_frame.size
        scale = getattr(self, 'display_scale', 1.0)
        
        if self._drag_mode == 'move':
            delta_x_pct = dx / max(1, W * scale)
            delta_y_pct = dy / max(1, H * scale)
            self.block_trigger = True
            for layer in self.selected_layers:
                start_x_pct, start_y_pct = self._layer_start_positions.get(layer, (layer.x_pct, layer.y_pct))
                layer.x_pct = max(0.0, min(start_x_pct + delta_x_pct, 1.0))
                layer.y_pct = max(0.0, min(start_y_pct + delta_y_pct, 1.0))
            self.block_trigger = False
            if self.selected_layer:
                self.val_x.set(self.selected_layer.x_pct)
                self.val_y.set(self.selected_layer.y_pct)
                self.lbl_x_disp.configure(text=f"{int(self.selected_layer.x_pct * 100)}%")
                self.lbl_y_disp.configure(text=f"{int(self.selected_layer.y_pct * 100)}%")
            self.refresh_preview()
        elif self._drag_mode == 'resize':
            layer = self._resize_layer
            coords = self._get_layer_canvas_coords(layer)
            if not coords:
                return
            disp_x, disp_y, _, _ = coords
            current_dist = ((mx - disp_x) ** 2 + (my - disp_y) ** 2) ** 0.5
            original_dist = ((start_x - disp_x) ** 2 + (start_y - disp_y) ** 2) ** 0.5
            if original_dist > 5:
                ratio = current_dist / original_dist
                self.block_trigger = True
                layer.scale = max(0.1, min(self._layer_start_scale * ratio, 4.0))
                self.block_trigger = False
                self.val_scale.set(layer.scale)
                self.lbl_scale_disp.configure(text=f"{layer.scale:.2f}x")
                self.refresh_preview()

    def _on_canvas_right_click(self, event):
        if not self.gif_loaded or not self.layers:
            return
        mx, my = event.x, event.y
        clicked_layer = None
        for layer in reversed(self.layers):
            coords = self._get_layer_canvas_coords(layer)
            if not coords:
                continue
            disp_x, disp_y, disp_w, disp_h = coords
            x1 = disp_x - disp_w / 2
            y1 = disp_y - disp_h / 2
            x2 = disp_x + disp_w / 2
            y2 = disp_y + disp_h / 2
            if x1 <= mx <= x2 and y1 <= my <= y2:
                clicked_layer = layer
                break
        if clicked_layer:
            self.selected_layer = clicked_layer
            self.selected_layers = [clicked_layer]
            self.select_layer_by_widget(clicked_layer)
            self._drag_mode = 'rotate'
            self._drag_start = (mx, my)
            self._layer_start_rotation = clicked_layer.rotation
            coords = self._get_layer_canvas_coords(clicked_layer)
            disp_x, disp_y, _, _ = coords
            import math
            self._start_angle = math.atan2(my - disp_y, mx - disp_x)
            self.refresh_layers_list()
            self.refresh_preview()

    def _on_canvas_right_drag(self, event):
        """_drag_mode"""
        if not self.gif_loaded or not getattr(self, '_drag_mode', None) or self._drag_mode != 'rotate' or not self.selected_layer:
            return
        mx, my = event.x, event.y
        layer = self.selected_layer
        coords = self._get_layer_canvas_coords(layer)
        if not coords:
            return
        disp_x, disp_y, _, _ = coords
        import math
        current_angle = math.atan2(my - disp_y, mx - disp_x)
        delta_angle = current_angle - self._start_angle
        delta_deg = math.degrees(delta_angle)
        self.block_trigger = True
        new_rot = (self._layer_start_rotation + delta_deg) % 360
        layer.rotation = round(new_rot)
        self.block_trigger = False
        self.val_rotation.set(layer.rotation)
        self.lbl_rotation_disp.configure(text=f"{int(layer.rotation)}°")
        self.refresh_preview()

    def _on_canvas_release(self, event):
        self._drag_mode = None

    def group_selected_layers(self):
        """Combines all currently selected layers into a single group."""
        if not hasattr(self, 'selected_layers') or len(self.selected_layers) < 2:
            messagebox.showinfo('无法组合', '请按住 Shift / Ctrl 键点击图层多选，至少选择 2 个图层以进行组合。')
            return
        import time
        new_group_id = int(time.time())
        for l in self.selected_layers:
            l.group_id = new_group_id
        self.refresh_layers_list()
        messagebox.showinfo('组合成功', f"已成功将 {len(self.selected_layers)} 个图层组合！\n拖动其中任意一个，组合内的所有图层将同步移动。")

    def ungroup_selected_layers(self):
        """Breaks the grouping of currently selected layers."""
        if not hasattr(self, 'selected_layers') or not self.selected_layers:
            return
        count = 0
        for l in self.selected_layers:
            if hasattr(l, 'group_id') and l.group_id:
                l.group_id = 0
                count += 1
        self.refresh_layers_list()
        if count > 0:
            messagebox.showinfo('拆分成功', f"已成功拆分 {count} 个图层的组合关系。")
