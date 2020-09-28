"""
Operator to paint selected vertex color onto the selected face(s)
"""

import bpy
from ..data_structures.color_layers import *


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

    map_enum_color = ("Color", "Color", "Color")
    map_enum_alpha = ("Alpha", "Alpha", "Alpha")
    map_enum_metallic = ("Metallic", "Metallic", "Metallic")
    map_enum_specular = ("Specular", "Specular", "Specular")
    map_enum_roughness = ("Roughness", "Roughness", "Roughness")
    map_enum_transmission = ("Transmission", "Transmission", "Transmission")

    map: bpy.props.EnumProperty(
        name="Map",
        items=[
            map_enum_color,
            map_enum_alpha,
            map_enum_metallic,
            map_enum_specular,
            map_enum_roughness,
            map_enum_transmission,
        ],
    )

    strength: bpy.props.FloatProperty(
        name="Strength",
        default=1,
        min=0,
        soft_max=1,
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
        color_layer = self.get_vertex_color_layer(mesh)
#        if self.map in (
#            PaintVertexColors.map_enum_color[0],
#            PaintVertexColors.map_enum_alpha[0]):
#            color_layer = mesh.vertex_colors.get(AddVertexColorLayer.color_alpha_layer)
#        elif self.map in (
#            PaintVertexColors.map_enum_metallic[0],
#            PaintVertexColors.map_enum_specular[0],
#            PaintVertexColors.map_enum_roughness[0],
#            PaintVertexColors.map_enum_transmission[0],
#            ):
#            color_layer = mesh.vertex_colors.get(AddVertexColorLayer.msrt_layer)
        if not color_layer:
            return {'FINISHED'}
        only_selected = self.only_selected

        if self.map == PaintVertexColors.map_enum_color[0]:
            r, g, b = self.color[0:3]
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    color_layer.data[idx].color = [
                        r, g, b, color_layer.data[idx].color[3]]
        elif self.map == PaintVertexColors.map_enum_alpha[0]:
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    r, g, b = color_layer.data[idx].color[0:3]
                    color_layer.data[idx].color = [r, g, b, self.strength]
        elif self.map == PaintVertexColors.map_enum_metallic[0]:
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    r, g, b, a = color_layer.data[idx].color
                    color_layer.data[idx].color = [self.strength, g, b, a]
        elif self.map == PaintVertexColors.map_enum_specular[0]:
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    r, g, b, a = color_layer.data[idx].color
                    color_layer.data[idx].color = [r, self.strength, b, a]
        elif self.map == PaintVertexColors.map_enum_roughness[0]:
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    r, g, b, a = color_layer.data[idx].color
                    color_layer.data[idx].color = [r, g, self.strength, a]
        elif self.map == PaintVertexColors.map_enum_transmission[0]:
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
        if self.map == PaintVertexColors.map_enum_color[0]:
            layout.prop(self, "color")
        else:
            layout.prop(self, "strength", slider=True)
        layout.prop(self, "map")

    def get_vertex_color_layer(self, mesh):
        color_map = self.map
        if color_map in (
                PaintVertexColors.map_enum_color[0],
                PaintVertexColors.map_enum_alpha[0]):
            return mesh.vertex_colors.get(color_alpha_layer)
        if color_map in (
                PaintVertexColors.map_enum_metallic[0],
                PaintVertexColors.map_enum_specular[0],
                PaintVertexColors.map_enum_roughness[0],
                PaintVertexColors.map_enum_transmission[0],
        ):
            return mesh.vertex_colors.get(msrt_layer)
        return None
