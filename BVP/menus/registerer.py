"""
Surrogate Class to register other menu items
"""

import bpy.types
from . import bvp_main


class VIEW3D_MT_registerer(bpy.types.Menu):
    """
    Surrogate Class to register other menu items
    Do not use externally
    """
    bl_label = "surrogate menu registerer"

    menus = (
        bvp_main.pbr_material_submenu,
        bvp_main.draw_brush_reminder,
        bvp_main.draw_vertex_colors_reminder,
        bvp_main.draw_material_reminder,
        bvp_main.set_vertex_colors_menu,
        bvp_main.vertex_map_submenu,
        bvp_main.vertex_color_strength_submenu,
    )

    def draw(self, context):
        return

    def register():
        for menu in VIEW3D_MT_registerer.menus:
            bpy.types.VIEW3D_MT_editor_menus.append(menu)

    def unregister():
        for menu in reversed(VIEW3D_MT_registerer.menus):
            bpy.types.VIEW3D_MT_editor_menus.remove(menu)
