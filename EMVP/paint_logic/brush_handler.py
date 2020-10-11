"""
This module handles the logic of the custom brush used in the add-on
"""

import bpy


BVP_BRUSH_NAME = "BVP_BRUSH"
PALETTE_NAME = "BVP_PALETTE"


def get_or_create_palette(context):
    palette = bpy.data.palettes.get(PALETTE_NAME)
    if not palette:
        palette = bpy.data.palettes.new(PALETTE_NAME)
        context.tool_settings.vertex_paint.palette = palette
    return palette


def get_or_create_brush():
    brush = bpy.data.brushes.get(BVP_BRUSH_NAME)
    if not brush and 'Draw' in bpy.data.brushes:
        brush = bpy.data.brushes['Draw'].copy()
    brush.name = BVP_BRUSH_NAME
    # brush.curve_preset = 'CONSTANT'
    brush.use_alpha = False
    brush.blend = 'MIX'
    brush.use_frontface = False
    brush.use_alpha = False
    return brush


def get_brush():
    return bpy.data.brushes.get(BVP_BRUSH_NAME)
