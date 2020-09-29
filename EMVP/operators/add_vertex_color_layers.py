"""
This operator makes sure the vertex color layers are present on the active object
"""

import bpy
from ..data.color_layers import all_layers, default_values


class AddVertexColorLayers(bpy.types.Operator):
    """Add Custom Vertex Colors Layers"""
    bl_idname = "object.add_vertex_color_layer"
    bl_label = "Set Vertex Colors Layers"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.active_object or context.active_object.type != 'MESH':
            return False
        vertex_color_names = \
            [
                vc.name for vc in context.active_object.data.vertex_colors
            ]
        if not context.active_object.data.vertex_colors or len(vertex_color_names) == 0:
            return True
        for color_layer_name in all_layers:
            if color_layer_name not in vertex_color_names:
                return True
        return False

    def execute(self, context):
        mesh = context.active_object.data
        vertex_color_names = [vc.name for vc in mesh.vertex_colors]
        for color_layer_name in all_layers:
            if color_layer_name not in vertex_color_names:
                color_layer = mesh.vertex_colors.new(name=color_layer_name)
                default_color = default_values[color_layer_name]
                for poly in mesh.polygons:
                    for idx in poly.loop_indices:
                        color_layer.data[idx].color = default_color

        prev_mode = None
        if context.mode != 'OBJECT':
            prev_mode = context.mode

        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.paint.vertex_paint_toggle()

        if prev_mode:
            if prev_mode == 'EDIT_MESH':
                bpy.ops.object.mode_set(mode='EDIT')
            else:
                bpy.ops.object.mode_set(mode=prev_mode)

        return {'FINISHED'}
