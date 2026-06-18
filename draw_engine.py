# ============================================================
# Module: draw_engine.py
# Reconstructed from Python 3.14 bytecode
# NOTE: Function bodies need manual reconstruction
#       Class/function structure is accurate
# ============================================================

from __future__ import annotations
import sys
import math
import tkinter
from typing import Union, TYPE_CHECKING
from core_rendering import CTkCanvas


class DrawEngine:
    """DrawEngine"""

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'canvas'", "'CTkCanvas'"]
        pass  # TODO: reconstruct body from bytecode

    def __init__(self, canvas):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['True']
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'round_width_to_even_numbers'", "'bool'", "'round_height_to_even_numbers'"]
        pass  # TODO: reconstruct body from bytecode

    def set_round_to_even_numbers(self, round_width_to_even_numbers, round_height_to_even_numbers):
        # --- Auto-reconstructed from bytecode ---
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'user_corner_radius'", "'Union[float, int]'", "'return'"]
        pass  # TODO: reconstruct body from bytecode

    def __calc_optimal_corner_radius(self, user_corner_radius):
        """polygon_shapes"""
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'polygon_shapes'", "'darwin'", "'font_shapes'", "'circle_shapes'", '0.5']
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'Union[float, int]'", "'height'"]
        pass  # TODO: reconstruct body from bytecode

    def draw_background_corners(self, width, height):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'background_corner_top_left'", "'background_parts'", "('tags', 'width')", 'True', "'background_corner_top_right'", "'background_corner_bottom_right'", "'background_corner_bottom_left'"]
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'Union[float, int]'", "'height'", "'corner_radius'", "'border_width'", "'overwrite_preferred_drawing_method'", "'str'"]
        pass  # TODO: reconstruct body from bytecode

    def draw_rounded_rect_with_border(self, width, height, corner_radius, border_width, overwrite_preferred_drawing_method):
        """Draws a rounded rectangle with a corner_radius and border_width on the canvas. The border elements have a 'border_parts' tag,
the main foreground elements have an 'inner_parts' tag to color the elements accordingly.

returns bool if recoloring is necessary """
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['"Draws a rounded rectangle with a corner_radius and border_w', "'polygon_shapes'", "'font_shapes'", "'circle_shapes'", '()']
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'border_width'", "'inner_corner_radius'", "'return'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_rect_with_border_polygon_shapes(self, width, height, corner_radius, border_width, inner_corner_radius):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'border_parts'", "'border_line_1'", "('tags',)", 'True', "('joinstyle', 'width')", "'inner_parts'", "'inner_line_1'", "('tags', 'joinstyle')"]
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'border_width'", "'inner_corner_radius'", "'exclude_parts'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_rect_with_border_font_shapes(self, width, height, corner_radius, border_width, inner_corner_radius, exclude_parts):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'border_oval_1_a'", "'border_oval_1'", "'border_corner_part'", "'border_parts'", "('tags', 'anchor')", "'border_oval_1_b'", "('tags', 'anchor', 'angle')", 'True']
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'border_width'", "'inner_corner_radius'", "'return'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_rect_with_border_circle_shapes(self, width, height, corner_radius, border_width, inner_corner_radius):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'border_oval_1'", "'border_corner_part'", "'border_parts'", "('tags', 'width')", "'border_oval_2'", "'border_oval_3'", "'border_oval_4'", 'True']
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'Union[float, int]'", "'height'", "'corner_radius'", "'border_width'", "'left_section_width'", "'return'"]
        pass  # TODO: reconstruct body from bytecode

    def draw_rounded_rect_with_border_vertical_split(self, width, height, corner_radius, border_width, left_section_width):
        """Draws a rounded rectangle with a corner_radius and border_width on the canvas which is split at left_section_width.
The border elements have the tags 'border_parts_left', 'border_parts_lright',
the main foreground elements have an 'inner_parts_left' and inner_parts_right' tag,
to color the elements accordingly.

returns bool if recoloring is necessary """
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['"Draws a rounded rectangle with a corner_radius and border_w', "'polygon_shapes'", "'circle_shapes'", "'font_shapes'", '()']
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'border_width'", "'inner_corner_radius'", "'left_section_width'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_rect_with_border_vertical_split_polygon_shapes(self, width, height, corner_radius, border_width, inner_corner_radius, left_section_width):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'border_parts'", "'border_line_left_1'", "('tags',)", "'border_line_right_1'", "'border_rect_left_1'", "('tags', 'width')", "'border_rect_right_1'", 'True']
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'border_width'", "'inner_corner_radius'", "'left_section_width'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_rect_with_border_vertical_split_font_shapes(self, width, height, corner_radius, border_width, inner_corner_radius, left_section_width, exclude_parts):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'border_oval_1_a'", "'border_oval_1'", "'border_corner_part'", "'border_parts'", "('tags', 'anchor')", "'border_oval_1_b'", "('tags', 'anchor', 'angle')", 'True']
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'Union[float, int]'", "'height'", "'corner_radius'", "'border_width'", "'progress_value_1'", "'float'"]
        pass  # TODO: reconstruct body from bytecode

    def draw_rounded_progress_bar_with_border(self, width, height, corner_radius, border_width, progress_value_1, progress_value_2, orientation):
        """Draws a rounded bar on the canvas, and onntop sits a progress bar from value 1 to value 2 (range 0-1, left to right, bottom to top).
The border elements get the 'border_parts' tag", the main elements get the 'inner_parts' tag and
the progress elements get the 'progress_parts' tag. The 'orientation' argument defines from which direction the progress starts (n, w, s, e).

returns bool if recoloring is necessary """
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'Draws a rounded bar on the canvas, and onntop sits a progre", "'polygon_shapes'", "'circle_shapes'", "'font_shapes'"]
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'border_width'", "'inner_corner_radius'", "'progress_value_1'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_progress_bar_with_border_polygon_shapes(self, width, height, corner_radius, border_width, inner_corner_radius, progress_value_1, progress_value_2, orientation):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'progress_parts'", "'progress_line_1'", "('tags', 'joinstyle')", "'inner_parts'", 'True', "'w'", "'s'", "('width',)"]
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'border_width'", "'inner_corner_radius'", "'progress_value_1'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_progress_bar_with_border_font_shapes(self, width, height, corner_radius, border_width, inner_corner_radius, progress_value_1, progress_value_2, orientation):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'progress_oval_1_a'", "('tags', 'anchor')", "'progress_oval_1_b'", "('tags', 'anchor', 'angle')", "'progress_oval_2_a'", "'progress_oval_2_b'", 'True', "'progress_oval_3_a'"]
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'Union[float, int]'", "'height'", "'corner_radius'", "'border_width'", "'button_length'", "'button_corner_radius'"]
        pass  # TODO: reconstruct body from bytecode

    def draw_rounded_slider_with_border_and_button(self, width, height, corner_radius, border_width, button_length, button_corner_radius, slider_value, orientation):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'polygon_shapes'", "'circle_shapes'", "'font_shapes'"]
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'border_width'", "'inner_corner_radius'", "'button_length'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_slider_with_border_and_button_polygon_shapes(self, width, height, corner_radius, border_width, inner_corner_radius, button_length, button_corner_radius, slider_value, orientation):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'slider_parts'", "'slider_line_1'", "('tags', 'joinstyle')", 'True', "'w'", "('width',)", "'s'", '(0, 0, 0, 0)']
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'border_width'", "'inner_corner_radius'", "'button_length'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_slider_with_border_and_button_font_shapes(self, width, height, corner_radius, border_width, inner_corner_radius, button_length, button_corner_radius, slider_value, orientation):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'slider_oval_1_a'", "'slider_parts'", "('tags', 'anchor')", "'slider_oval_1_b'", "('tags', 'anchor', 'angle')", 'True', "'slider_oval_2_a'", "'slider_oval_2_b'"]
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'Union[float, int]'", "'height'", "'corner_radius'", "'border_spacing'", "'start_value'", "'float'"]
        pass  # TODO: reconstruct body from bytecode

    def draw_rounded_scrollbar(self, width, height, corner_radius, border_spacing, start_value, end_value, orientation):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'polygon_shapes'", "'circle_shapes'", "'font_shapes'"]
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'inner_corner_radius'", "'start_value'", "'float'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_scrollbar_polygon_shapes(self, width, height, corner_radius, inner_corner_radius, start_value, end_value, orientation):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'border_parts'", "'border_rectangle_1'", "('tags', 'width')", 'True', "'scrollbar_parts'", "'scrollbar_polygon_1'", "('tags', 'joinstyle')", "'vertical'"]
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'int'", "'height'", "'corner_radius'", "'inner_corner_radius'", "'start_value'", "'float'"]
        pass  # TODO: reconstruct body from bytecode

    def __draw_rounded_scrollbar_font_shapes(self, width, height, corner_radius, inner_corner_radius, start_value, end_value, orientation):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'border_parts'", "'border_rectangle_1'", "('tags', 'width')", 'True', "'scrollbar_oval_1_a'", "'scrollbar_corner_part'", "('tags', 'anchor')", "'scrollbar_oval_1_b'"]
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'width'", "'Union[float, int]'", "'height'", "'size'", "'Union[int, float]'", "'return'", "'bool'"]
        pass  # TODO: reconstruct body from bytecode

    def draw_checkmark(self, width, height, size):
        """Draws a rounded rectangle with a corner_radius and border_width on the canvas. The border elements have a 'border_parts' tag,
the main foreground elements have an 'inner_parts' tag to color the elements accordingly.

returns bool if recoloring is necessary """
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['"Draws a rounded rectangle with a corner_radius and border_w', "'polygon_shapes'", "'circle_shapes'", '2.8', "'checkmark'", "('tags', 'width', 'joinstyle', 'capstyle')", 'True', '0.8']
        pass  # TODO: reconstruct body from bytecode

    def __annotate__(format):
        # --- Auto-reconstructed from bytecode ---
        # constants used: ['2', "'x_position'", "'Union[int, float]'", "'y_position'", "'size'", "'return'", "'bool'"]
        pass  # TODO: reconstruct body from bytecode

    def draw_dropdown_arrow(self, x_position, y_position, size):
        """Draws a dropdown bottom facing arrow at (x_position, y_position) in a given size

returns bool if recoloring is necessary """
        # --- Auto-reconstructed from bytecode ---
        # constants used: ["'Draws a dropdown bottom facing arrow at (x_position, y_posi", "'polygon_shapes'", "'circle_shapes'", "'dropdown_arrow'", "('tags', 'width', 'joinstyle', 'capstyle')", 'True', "'font_shapes'", "'Y'"]
        pass  # TODO: reconstruct body from bytecode
