"""
Utilities method to deal with context subtelties
"""

import bpy


def init_prev_mode(context):
    if context.mode != 'OBJECT':
        return context.mode
    return None


def reset_previous_mode(prev_mode):
    if prev_mode:
        if prev_mode == 'EDIT_MESH':
            bpy.ops.object.mode_set(mode='EDIT')  # wtf ?
        elif prev_mode == 'PAINT_VERTEX':
            bpy.ops.object.mode_set(mode='VERTEX_PAINT')  # WTF ????
        else:
            bpy.ops.object.mode_set(mode=prev_mode)
