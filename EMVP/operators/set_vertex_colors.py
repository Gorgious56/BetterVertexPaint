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
        for poly in mesh.polygons:
            if only_selected and not poly.select:
                continue
            for idx in poly.loop_indices:
                prev_color = color_layer.data[idx].color
                color_layer.data[idx].color = \
                [
                    r if channel == -1 else (r * a if channel == 0 else prev_color[0]),
                    g if channel == -1 else (g * a if channel == 1 else prev_color[1]),
                    b if channel == -1 else (b * a if channel == 2 else prev_color[2]),
                    a if channel == 3 else prev_color[3]
                ]

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "color")
        layout.prop(self, "map")
