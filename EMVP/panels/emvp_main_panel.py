"""
Main Panel of the add-on
"""

from bpy.types import Panel as BpyPanel
from ..operators.reset_vertex_color_layers import ResetVertexColorLayers
from ..operators.paint_vertex_colors import PaintVertexColors
from ..operators.add_pbr_material import AddPBRMaterial
from ..operators.select_faces_with_same_data import SelectFacesWithSameData
from ..operators.copy_vertex_color_data import CopyVertexColorData
from ..operators.tweak_vertex_color_data import TweakVertexColorData
from ..addon_preferences import AddonPrefs
from ..data.maps import map_is_color
from ..data.color_layers import are_all_layers_created


class EMVPPanel(BpyPanel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Paint Vertex Colors"
    bl_idname = "OBJECT_PT_PVC"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EMVP'

    def draw(self, context):
        layout = self.layout

        ao = context.active_object

        if not ao or ao.type != 'MESH' or len(context.selected_objects) != 1:
            layout.label(
                text="Select a single mesh object", icon='ERROR')
            return

        if not are_all_layers_created(ao.data):
            if context.mode != 'OBJECT':
                layout.label(text="Press TAB for OBJECT mode", icon='ERROR')
            else:
                op = layout.operator(
                    ResetVertexColorLayers.bl_idname, text="Set Vertex Color Layers    ")
                op.reset_all_maps = True
                op.only_selected_faces = False
                op.force_reset = False
        else:
            prefs = AddonPrefs.get_preferences(context)
            layout.prop(prefs, "map")
            use_color = map_is_color(prefs.map)
            if use_color:
                layout.prop(prefs, "color")
            else:
                layout.prop(prefs, "strength", slider=True)

            self.draw_paint_ops(context, prefs)
            self.draw_tweak_ops(context, prefs)
            self.draw_copy_ops(context, use_color)
            self.draw_select_ops(context, prefs)
            self.draw_reset_ops(context, prefs)

            layout.operator(AddPBRMaterial.bl_idname)

    def draw_paint_ops(self, context, prefs):
        box = self.layout.box()
        row = box.row()
        # row.label(text="Paint")
        sub_row = row.row()

        op_only_selected = sub_row.operator(
            PaintVertexColors.bl_idname, text="Paint Selected")
        op_only_selected.only_selected = True
        sub_row.enabled = context.mode == "EDIT_MESH"

        op_all_faces = row.operator(
            PaintVertexColors.bl_idname, text="Paint All")
        op_all_faces.only_selected = False

        for op in (op_only_selected, op_all_faces):
            op.color = prefs.color
            op.map = prefs.map
            op.strength = prefs.strength

    def draw_tweak_ops(self, context, prefs):
        box = self.layout.box()

        row = box.row()
        sub_row = row.row()
        add_data_to_selected = sub_row.operator(
            TweakVertexColorData.bl_idname, text="Add to Selected")
        add_data_to_selected.add = True
        add_data_to_selected.only_selected_faces = True
        sub_row.enabled = context.mode == 'EDIT_MESH'
        add_data_to_all = row.operator(
            TweakVertexColorData.bl_idname, text="Add to All")
        add_data_to_all.add = True
        add_data_to_all.only_selected_faces = False

        row = box.row()
        sub_row = row.row()
        rem_data_to_selected = sub_row.operator(
            TweakVertexColorData.bl_idname, text="Remove from Selected")
        rem_data_to_selected.add = False
        rem_data_to_selected.only_selected_faces = True
        sub_row.enabled = context.mode == 'EDIT_MESH'
        rem_data_to_all = row.operator(
            TweakVertexColorData.bl_idname, text="Remove from All")
        rem_data_to_all.add = False
        rem_data_to_all.only_selected_faces = False

        for op in (add_data_to_all, add_data_to_selected, rem_data_to_all, rem_data_to_selected):
            op.color = prefs.color
            op.strength = prefs.strength
            op.map = prefs.map

    def draw_copy_ops(self, context, use_color):
        box = self.layout.box()
        row = box.row()
        # row.label(text="Copy Data")
        sub_row = row.row()

        sub_row.operator(CopyVertexColorData.bl_idname,
                         text="Copy " + ("Color" if use_color else "Data"))

    def draw_select_ops(self, context, prefs):
        box = self.layout.box()
        row = box.row()
        # row.label(text="Select")
        select_same = row.operator(
            SelectFacesWithSameData.bl_idname, text="Select Same")
        select_same.invert = False
        select_invert = row.operator(
            SelectFacesWithSameData.bl_idname, text="Select Inverse")
        select_invert.invert = True

        for op in (select_same, select_invert):
            op.map = prefs.map

    def draw_reset_ops(self, context, prefs):
        box = self.layout.box()
        row = box.row()
        # row.label(text="Reset")
        sub_row = row.row()

        op_only_selected = sub_row.operator(
            ResetVertexColorLayers.bl_idname, text="Reset Selected")
        sub_row.enabled = context.mode == "EDIT_MESH"
        op_only_selected.only_selected_faces = True

        op_all_faces = row.operator(
            ResetVertexColorLayers.bl_idname, text="Reset All")
        op_all_faces.only_selected_faces = False

        row = box.row()
        row.label(text="")
        row.prop(prefs, "reset_all_maps", text="Apply to All Maps")

        for op in (op_only_selected, op_all_faces):
            op.reset_all_maps = prefs.reset_all_maps
            op.selected_map = prefs.map
            op.force_reset = True
