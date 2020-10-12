"""
Mudle designed to create and handle addon keymaps
"""

import bpy
from ..operators.handle_subtract import HandleSubtract
from ..operators.set_vertex_colors import BVP_SetVertexColors


def create_keymap():
    remove_keymap()
    keymap_items = bpy.context.window_manager.keyconfigs.addon.keymaps[
        '3D View Generic'].keymap_items
    kmi_sub = keymap_items.new(HandleSubtract.bl_idname, 'LEFT_CTRL', 'PRESS')
    kmi_sub.properties.subtract = True

    kmi_add = keymap_items.new(
        HandleSubtract.bl_idname, 'LEFT_CTRL', 'RELEASE')
    kmi_add.properties.subtract = False

    kmi_set_vertex_colors = keymap_items.new(
        BVP_SetVertexColors.bl_idname, 'P', 'PRESS', ctrl=True)


def remove_keymap():
    keymap_items = bpy.context.window_manager.keyconfigs.addon.keymaps[
        '3D View Generic'].keymap_items
    for km in keymap_items:
        if km.name in (HandleSubtract.bl_label, BVP_SetVertexColors.bl_label):
            keymap_items.remove(km)
