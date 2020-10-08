"""
This operator copies the vertex color data of the currently selected face

"""

import bpy
from ..data.color_layers import get_data_from_face
from ..data.maps import map_color_layer, map_is_color, map_channels
from ..addon_preferences import AddonPrefs


class CopyVertexColorData(bpy.types.Operator):
    """Copy Vertex Color Data

    Assumes only one face is selected."""
    bl_idname = "object.copy_vertex_color_data"
    bl_label = "Copy Vertex Colors Layers"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # TODO Find a way to poll when exactly one face is selected (bmesh ?) without crashing
        return context.active_object and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH'

    def execute(self, context):
        mesh = context.active_object.data

        prev_mode = None
        if context.mode != 'OBJECT':
            prev_mode = context.mode

        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.paint.vertex_paint_toggle()

        prefs = AddonPrefs.get_preferences(context)
        _map = prefs.map
        color_layer = mesh.vertex_colors.get(map_color_layer[_map])
        if not color_layer:
            print(
                f"No vertex color layer named {color_layer.name} on selected object")
            return {'FINISHED'}

        selected_face = None
        for f in mesh.polygons:
            if f.select:
                selected_face = f
                break
        if not selected_face:
            return {'FINISHED'}
        if map_is_color(_map):
            data = get_data_from_face(color_layer, selected_face)
            prefs.color = data
        else:
            data = get_data_from_face(
                color_layer, selected_face, map_channels[_map])
            prefs.strength = data

        if prev_mode:
            if prev_mode == 'EDIT_MESH':
                bpy.ops.object.mode_set(mode='EDIT')
            else:
                bpy.ops.object.mode_set(mode=prev_mode)

        return {'FINISHED'}
