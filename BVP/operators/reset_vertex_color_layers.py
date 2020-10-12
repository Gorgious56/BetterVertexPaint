"""
This operator makes sure the vertex color layers are present on the active object
It is also used to reset the layers to their default values

It can be used to reset a sepcific map or all maps
It can be used on all faces or only selected faces
"""

import bpy
from ..paint_logic.color_layers import set_layers_to_default, set_layer_to_default
from ..paint_logic.maps import map_color_layer, all_maps
from .context_manager import init_prev_mode, reset_previous_mode
from ..paint_logic import on_setting_change

class BVP_ResetVertexColorLayers(bpy.types.Operator):
    """Reset Custom Vertex Colors Layers"""
    bl_idname = "paint.reset_vertex_color_layer"
    bl_label = "Reset Vertex Colors Layers"
    bl_options = {'REGISTER', 'UNDO'}

    reset_all_maps: bpy.props.BoolProperty(
        name="Reset All Maps",
        default=False,
    )

    only_selected_faces: bpy.props.BoolProperty(
        name="Reset All Faces",
        default=False,
    )

    force_reset: bpy.props.BoolProperty(
        name="Force Reset",
        default=True,
    )

    selected_map: bpy.props.EnumProperty(
        name="Map",
        items=all_maps,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def execute(self, context):
        mesh = context.active_object.data

        if self.only_selected_faces:
            if self.reset_all_maps:
                set_layers_to_default(
                    mesh,
                    self.force_reset,
                    only_selected=self.only_selected_faces)
            else:
                set_layer_to_default(
                    mesh,
                    self.force_reset,
                    map_color_layer[self.selected_map],
                    only_selected=self.only_selected_faces)

        else:
            if self.reset_all_maps:
                set_layers_to_default(mesh, self.force_reset)
            else:
                set_layer_to_default(mesh, self.force_reset,
                                     map_color_layer[self.selected_map])

        on_setting_change.update_prefs(self, context)


        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "only_selected_faces",
                    text="Reset Only Selected Faces")
        layout.prop(self, "reset_all_maps", text="Reset All Maps")
        if not self.reset_all_maps:
            layout.prop(self, "selected_map", text="Map")
