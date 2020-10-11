"""
This operator will select the faces which contain
the same data in the same channel as the one selected
"""

import bpy
from ..paint_logic.color_layers import get_data_from_face
from ..paint_logic.maps import all_maps, map_color_layer, map_is_color, map_channels


class SelectFacesWithSameData(bpy.types.Operator):
    """Select Faces with the same vertex colors data.
    Assumes all loops in a face share the same data
    and all selected faces share the same data"""
    bl_idname = "object.select_same_vertex_color_data"
    bl_label = "Select Faces With Same Data"
    bl_options = {'REGISTER', 'UNDO'}

    invert: bpy.props.BoolProperty(
        name="invert",
        default=False,
    )

    map: bpy.props.EnumProperty(
        name="Map",
        items=all_maps,
    )

    threshold: bpy.props.FloatProperty(
        name="Threshold",
        min=0,
        soft_max=1,
        max=5,
    )

    @classmethod
    def poll(cls, context):
        # TODO Find a way to poll when exactly one face is selected (bmesh ?) without crashing
        return context.active_object \
            and context.active_object.type == 'MESH' \
            and len(context.active_object.data.polygons) > 0 \
            and context.mode == 'EDIT_MESH'

    def execute(self, context):
        mesh = context.active_object.data
        sf = None
        # I don't know why but edit mesh bmesh is constantly crashing :
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        for i, f in enumerate(mesh.polygons):
            if f.select:
                sf = i
                break

        if sf is None:
            print("No face selected")
            return {'FINISHED'}

        # bpy.ops.paint.vertex_paint_toggle()
        # bpy.ops.paint.vertex_paint_toggle()
        color_layer = mesh.vertex_colors.get(map_color_layer[self.map])
        if not color_layer:
            print(
                f"No vertex color layer named {color_layer.name} on selected object")
            return {'FINISHED'}

        channel = map_channels[self.map]
        if map_is_color(self.map):
            color = get_data_from_face(color_layer, mesh.polygons[sf])
            # TODO : Unselect edges and vertices.
            for f in mesh.polygons:
                same_color = True
                color_data = get_data_from_face(color_layer, f)
                for i, channel in enumerate(color):
                    if abs(channel - color_data[i]) > self.threshold:
                        same_color = False
                        break
                f.select = not self.invert if same_color else self.invert
        else:
            data = get_data_from_face(color_layer, mesh.polygons[sf], channel)
            # TODO : Unselect edges and vertices.
            for f in mesh.polygons:
                f.select = self.invert if abs(get_data_from_face(
                    color_layer, f, channel) - data) > self.threshold else not self.invert
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "invert")
        layout.prop(self, "map")
        layout.prop(self, "threshold", slider=True)
