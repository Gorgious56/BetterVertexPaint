"""
Operator to paint selected vertex color onto the selected face(s)
"""

import bpy
from ..data.maps import all_maps, map_color_layer, map_channels, map_is_color


class PaintVertexColors(bpy.types.Operator):
    """Paint faces (Go into Edit Mode to paint selected faces)"""
    bl_idname = "object.paint_vertex_colors"
    bl_label = "Paint Faces"
    bl_options = {'REGISTER', 'UNDO'}

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

    only_selected: bpy.props.BoolProperty(
        name="Only Selected",
        description="Paint only selected faces",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object \
            and context.active_object.type == 'MESH' \
            and len(context.active_object.data.polygons) > 0

    def execute(self, context):
        mesh = context.active_object.data

        prev_mode = None
        if context.mode != 'OBJECT':
            prev_mode = context.mode

        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.paint.vertex_paint_toggle()

        color_layer = mesh.vertex_colors.get(map_color_layer[self.map])

        if not color_layer:
            print(
                f"No vertex color layer named {color_layer.name} on selected object")
            return {'FINISHED'}

        only_selected = self.only_selected

        if map_is_color(self.map):
            r, g, b = self.color[0:3]
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    color_layer.data[idx].color = [
                        r, g, b, color_layer.data[idx].color[3]]
        else:
            channel = map_channels[self.map]
            if channel == 0:
                for poly in mesh.polygons:
                    if only_selected and not poly.select:
                        continue
                    for idx in poly.loop_indices:
                        r, g, b, a = color_layer.data[idx].color
                        color_layer.data[idx].color = [self.strength, g, b, a]
            elif channel == 1:
                for poly in mesh.polygons:
                    if only_selected and not poly.select:
                        continue
                    for idx in poly.loop_indices:
                        r, g, b, a = color_layer.data[idx].color
                        color_layer.data[idx].color = [r, self.strength, b, a]
            elif channel == 2:
                for poly in mesh.polygons:
                    if only_selected and not poly.select:
                        continue
                    for idx in poly.loop_indices:
                        r, g, b, a = color_layer.data[idx].color
                        color_layer.data[idx].color = [r, g, self.strength, a]
            else:
                for poly in mesh.polygons:
                    if only_selected and not poly.select:
                        continue
                    for idx in poly.loop_indices:
                        r, g, b, a = color_layer.data[idx].color
                        color_layer.data[idx].color = [r, g, b, self.strength]

        if prev_mode:
            if prev_mode == 'EDIT_MESH':
                bpy.ops.object.mode_set(mode='EDIT')
            else:
                bpy.ops.object.mode_set(mode=prev_mode)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        if map_is_color(self.map):
            layout.prop(self, "color")
        else:
            layout.prop(self, "strength", slider=True)
        layout.prop(self, "map")
