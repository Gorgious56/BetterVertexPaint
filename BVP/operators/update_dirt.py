"""
This operator is used to create a dirt map used in the pbr shader
"""

from math import pi
import bpy
from ..paint_logic.color_layers import layer_dirt, set_layer_to_default
from .context_manager import init_prev_mode, reset_previous_mode


class UpdateDirt(bpy.types.Operator):
    """Update Dirt Data"""
    bl_idname = "paint.update_dirt"
    bl_label = "Update Dirt Data"
    bl_options = {'REGISTER', 'UNDO'}

    # add: bpy.props.BoolProperty(
    #     name="Add Values",
    #     default=True,
    # )

    dirt_only: bpy.props.BoolProperty(
        name="Dirt Only",
        default=False,
    )
    dirt: bpy.props.FloatProperty(
        name="Dirt",
        default=0,
        min=0,
        max=1,
    )
    # color: bpy.props.FloatVectorProperty(
    #     name="Color",
    #     subtype='COLOR',
    #     default=[1, 1, 1, 1],
    #     size=4,
    #     min=0,
    #     max=1,)

    # map: bpy.props.EnumProperty(
    #     name="Map",
    #     items=all_maps,
    # )

    # strength: bpy.props.FloatProperty(
    #     name="Strength",
    #     default=1,
    #     min=0,
    #     soft_max=2,
    #     max=4.875,
    # )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def execute(self, context):
        mesh = context.active_object.data

        prev_mode = init_prev_mode(context)

        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.paint.vertex_paint_toggle()

        mesh.vertex_colors[layer_dirt].active_render = True
        set_layer_to_default(mesh, True, layer_dirt)
        bpy.ops.paint.vertex_color_dirt(
            dirt_angle=self.dirt*pi*0.6,
            dirt_only=self.dirt_only)

        # channel = map_channels[self.map] if map_channels[self.map] > -1 else None
        # add_value = (self.color if map_is_color(self.map) else self.strength)
        # if not self.add:
        #     if channel is None:
        #         add_value = [-v for v in add_value]
        #     else:
        #         add_value *= -1
        # add_to_data(
        #     mesh,
        #     map_color_layer[self.map],
        #     self.only_selected_faces,
        #     add_value,
        #     channel)

        reset_previous_mode(prev_mode)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "dirt_only")
        layout.prop(self, "dirt", slider=True)
        layout.prop(self, "highlight", slider=True)
