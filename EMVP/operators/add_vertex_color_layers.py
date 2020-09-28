"""
This operator makes sure the vertex color layers are present on the active object
"""

import bpy
from ..data_structures.color_layers import color_alpha_layer, msrt_layer


class AddVertexColorLayer(bpy.types.Operator):
    """Add Custom Vertex Colors Layers"""
    bl_idname = "object.add_vertex_color_layer"
    bl_label = "Add Vertex Colors Layers"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.active_object or context.active_object.type != 'MESH':
            return False
        vertex_color_names = [
            vc.name for vc in context.active_object.data.vertex_colors]
        return not context.active_object.data.vertex_colors \
            or color_alpha_layer not in vertex_color_names \
            or msrt_layer not in vertex_color_names

    def execute(self, context):
        mesh = context.active_object.data
        vertex_color_names = [vc.name for vc in mesh.vertex_colors]
        if color_alpha_layer not in vertex_color_names:
            color_layer = mesh.vertex_colors.new(name=color_alpha_layer)

        prev_mode = None
        if context.mode != 'OBJECT':
            prev_mode = context.mode

        if msrt_layer not in vertex_color_names:
            color_layer = mesh.vertex_colors.new(name=msrt_layer)
            for poly in mesh.polygons:
                for idx in poly.loop_indices:
                    color_layer.data[idx].color = [0, .5, .5, 0]

        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.paint.vertex_paint_toggle()

        if prev_mode:
            if prev_mode == 'EDIT_MESH':
                bpy.ops.object.mode_set(mode='EDIT')
            else:
                bpy.ops.object.mode_set(mode=prev_mode)

        return {'FINISHED'}
