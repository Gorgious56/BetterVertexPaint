"""
BVP Menus
"""

from bpy.types import Menu
import bpy.types
from ..operators.add_pbr_material import BVP_AddPBRMaterial
from ..operators.reset_vertex_color_layers import BVP_ResetVertexColorLayers
from ..operators.set_vertex_colors import BVP_SetVertexColors
from ..operators.init_brush import InitBrush
from ..paint_logic.maps import map_is_color, map_channels
from ..paint_logic.color_layers import are_all_layers_created
from ..paint_logic.brush_handler import get_brush, BVP_BRUSH_NAME, get_or_create_palette
from ..addon_preferences import get_preferences


paint_mode = 'PAINT_VERTEX'


def pbr_material_submenu(self, context):
    if context.mode != paint_mode:
        return
    self.layout.menu(VIEW3D_MT_bvp_settings.__name__)


def draw_brush_reminder(self, context):
    if context.mode != paint_mode:
        return
    if not is_brush_ok(context):
        VIEW3D_MT_bvp_settings.draw_custom_brush(context, self.layout)


def is_brush_ok(context):
    return context.tool_settings.vertex_paint.brush.name == \
        BVP_BRUSH_NAME


def draw_vertex_colors_reminder(self, context):
    if context.mode != paint_mode:
        return
    if not are_vertex_colors_ok(context):
        VIEW3D_MT_bvp_settings.draw_vertex_colors(context, self.layout)


def are_vertex_colors_ok(context):
    ao = context.active_object
    return ao and are_all_layers_created(ao.data)


def draw_material_reminder(self, context):
    if context.mode != paint_mode:
        return
    if not is_material_ok(context):
        VIEW3D_MT_bvp_settings.draw_pbr_material(context, self.layout)


def is_material_ok(context):
    ao = context.active_object
    mat = bpy.data.materials.get(BVP_AddPBRMaterial.mat_name)
    return mat and mat.name in ao.data.materials


def vertex_map_submenu(self, context):
    if context.mode != paint_mode:
        return
    if not get_brush() \
            or not is_material_ok(context) \
            or not are_vertex_colors_ok(context) \
            or not is_brush_ok(context):
        return
    prefs = get_preferences(context)
    self.layout.prop(prefs, "map")


def vertex_color_strength_submenu(self, context):
    if context.mode != paint_mode:
        return
    prefs = get_preferences(context)
    brush = get_brush()
    if not brush \
            or not is_material_ok(context) \
            or not are_vertex_colors_ok(context) \
            or not is_brush_ok(context):
        return
    layout = self.layout
    if not map_is_color(prefs.map):
        channel = map_channels[prefs.map]
        if channel != 3:
            layout.prop(prefs, "strength", slider=True, text='Value')
    else:
        layout.prop(brush, "color", text="")

        row = layout.row(align=True)
        row.label(text="Palette")
        row.operator("palette.color_add", icon='ADD', text="")
        palette = get_or_create_palette(context)
        row = layout.row(align=True)
        row.scale_x = 0.3
        for c in palette.colors:
            row.prop(c, "color", text="")



class VIEW3D_MT_bvp_settings(Menu):
    """
    Menu used to tweak the object's material in Vertex Paint Mode
    """
    bl_label = "BVP"
    bl_category = "BVP"

    @staticmethod
    def draw_custom_brush(context, layout):
        layout.operator(InitBrush.bl_idname, icon="FILE_REFRESH" if
                        is_brush_ok(context) else "ERROR")

    @staticmethod
    def draw_vertex_colors(context, layout):
        ao = context.active_object
        if not ao:
            return
        refresh = are_vertex_colors_ok(context)
        op = layout.operator(
            BVP_ResetVertexColorLayers.bl_idname, text=(
                "Refresh" if refresh else "Create") + " Vertex Color Layers",
            icon="FILE_REFRESH" if refresh else "ERROR")
        op.reset_all_maps = True
        op.only_selected_faces = False
        op.force_reset = False

    @staticmethod
    def draw_pbr_material(context, layout):
        mat = bpy.data.materials.get(BVP_AddPBRMaterial.mat_name)
        layout.operator(BVP_AddPBRMaterial.bl_idname, text=(
                        "Reset" if mat else "Create") + " PBR Material",
                        icon="FILE_REFRESH" if is_material_ok(context) else "ERROR")

        return mat

    def draw(self, context):

        layout = self.layout
        layout.operator(
            BVP_SetVertexColors.bl_idname, text="Set Vertex Colors")

        self.draw_custom_brush(context, layout)
        self.draw_vertex_colors(context, layout)

        # mat = self.draw_pbr_material(context, layout)
        # if mat:
        #     node = mat.node_tree.nodes.get(BVP_AddPBRMaterial.dirt_mix_name)
        #     if node:
        #         layout.prop(node.inputs[0], "default_value",
        #                     text="Dirt Factor", slider=True)

        
        prefs = get_preferences(context)
        _map = prefs.map
        mesh = context.active_object.data

        op = layout.operator(
            BVP_ResetVertexColorLayers.bl_idname,
            text=f"Discard '{_map}' Layer Data",
            icon='TRASH')
        op.selected_map = _map
        op.reset_all_maps = False
        op.only_selected_faces = mesh.use_paint_mask or mesh.use_paint_mask_vertex
        op.force_reset = True

        op = layout.operator(
            BVP_ResetVertexColorLayers.bl_idname,
            text=f"Discard ~ALL~ Layers Data",
            icon='TRASH')
        op.reset_all_maps = True
        op.only_selected_faces = mesh.use_paint_mask or mesh.use_paint_mask_vertex
        op.force_reset = True
