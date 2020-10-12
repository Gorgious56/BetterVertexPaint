"""
Operator to paint selected vertex color onto the selected face(s)
"""

import bpy
from ..paint_logic.maps import map_color_layer, map_channels
from ..paint_logic.brush_handler import get_brush
from .. import addon_preferences


class BVP_SetVertexColors(bpy.types.Operator):
    """Paint faces"""
    bl_idname = "paint.bvp_set_vertex_colors"
    bl_label = "BVP : Set Vertex Colors"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object \
            and context.active_object.type == 'MESH' \
            and len(context.active_object.data.polygons) > 0

    def execute(self, context):
        mesh = context.active_object.data

        prefs = addon_preferences.get_preferences(context)
        _map = prefs.map

        color_layer = mesh.vertex_colors.get(map_color_layer[_map])

        if not color_layer:
            print(
                f"No vertex color layer named {color_layer.name} on selected object")
            return {'FINISHED'}

        only_selected = mesh.use_paint_mask or mesh.use_paint_mask_vertex

        channel = map_channels[_map]

        brush = get_brush()
        r, g, b, a = (brush.color[0], brush.color[1], brush.color[2], prefs.strength)
        new_r = channel in (-1, 0)
        new_g = channel in (-1, 1)
        new_b = channel in (-1, 2)
        new_a = channel == 3
        a = prefs.strength
        r = brush.color[0] * (1 if channel == -1 else a)
        g = brush.color[1] * (1 if channel == -1 else a)
        b = brush.color[2] * (1 if channel == -1 else a)

        for poly in mesh.polygons:
            if only_selected and not poly.select:
                continue
            for idx in poly.loop_indices:
                prev_r, prev_g, prev_b, prev_a = color_layer.data[idx].color
                color_layer.data[idx].color = \
                [
                    r if new_r else prev_r,
                    g if new_g else prev_g,
                    b if new_b else prev_b,
                    a if new_a else prev_a
                ]

        return {'FINISHED'}
