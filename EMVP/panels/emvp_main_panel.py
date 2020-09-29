"""
Main Panel of the add-on
"""

from bpy.types import Panel as BpyPanel
from ..operators.add_vertex_color_layers import AddVertexColorLayers
from ..operators.paint_vertex_colors import PaintVertexColors
from ..operators.add_pbr_material import AddPBRMaterial
from ..addon_preferences import AddonPrefs
from ..data.maps import map_is_color


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

        if AddVertexColorLayers.poll(context):
            if context.mode != 'OBJECT':
                layout.label(text="Press TAB for OBJECT mode", icon='ERROR')
            else:
                layout.operator(AddVertexColorLayers.bl_idname)
        else:
            prefs = context.preferences.addons.get(AddonPrefs.bl_idname).preferences
            layout.prop(prefs, "map")
            if map_is_color(prefs.map):
                layout.prop(prefs, "color")
            else:
                layout.prop(prefs, "strength", slider=True)

            row = layout.row()
            row.label(text="Paint")
            sub_row = row.row()

            op_only_selected = sub_row.operator(PaintVertexColors.bl_idname, text="Selected")
            op_only_selected.only_selected = True
            sub_row.enabled = context.mode == "EDIT_MESH"

            op_all_faces = row.operator(PaintVertexColors.bl_idname, text="All")
            op_all_faces.only_selected = False

            # layout.operator(SelectFacesWithSameColor.bl_idname)
            layout.operator(AddPBRMaterial.bl_idname)

            for op in (op_only_selected, op_all_faces):
                op.color = prefs.color
                op.map = prefs.map
                op.strength = prefs.strength
