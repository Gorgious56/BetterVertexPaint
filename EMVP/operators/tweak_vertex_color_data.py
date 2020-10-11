"""
This operator is used to add or retract values to the data of a given vertex color layer
"""

import bpy
from ..paint_logic.color_layers import add_to_data
from ..paint_logic.maps import map_color_layer, all_maps, map_is_color, map_channels


class TweakVertexColorData(bpy.types.Operator):
    """Tweak Vertex Colors Data"""
    bl_idname = "object.tweak_vertex_color_data"
    bl_label = "Tweak Vertex Colors Data"
    bl_options = {'REGISTER', 'UNDO'}

    add: bpy.props.BoolProperty(
        name="Add Values",
        default=True,
    )

    only_selected_faces: bpy.props.BoolProperty(
        name="Apply to All Faces",
        default=False,
    )

    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=[1, 1, 1, 1],
        size=4,
        min=0,
        max=1,)

    map: bpy.props.EnumProperty(
        name="Map",
        items=all_maps,
    )

    strength: bpy.props.FloatProperty(
        name="Strength",
        default=1,
        min=0,
        soft_max=2,
        max=4.875,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def execute(self, context):
        mesh = context.active_object.data

        prev_mode = None
        if context.mode != 'OBJECT':
            prev_mode = context.mode

        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.paint.vertex_paint_toggle()
        channel = map_channels[self.map] if map_channels[self.map] > -1 else None
        add_value = (self.color if map_is_color(self.map) else self.strength)
        if not self.add:
            if channel is None:
                add_value = [-v for v in add_value]
            else:
                add_value *= -1
        add_to_data(
            mesh,
            map_color_layer[self.map],
            self.only_selected_faces,
            add_value,
            channel)

        if prev_mode:
            if prev_mode == 'EDIT_MESH':
                bpy.ops.object.mode_set(mode='EDIT')
            else:
                bpy.ops.object.mode_set(mode=prev_mode)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "add",
                    text="Add" if self.add else "Remove")
        layout.prop(self, "only_selected_faces",
                    text="Only Selected Faces")
        layout.prop(self, "map")
        if map_is_color(self.map):
            layout.prop(self, "color", text="Color")
        else:
            layout.prop(self, "strength", text="Strength")

        layout = self.layout
