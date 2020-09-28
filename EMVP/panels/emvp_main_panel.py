"""
Main Panel of the add-on
"""

from bpy.types import Panel as BpyPanel
from ..operators.add_vertex_color_layers import AddVertexColorLayer
from ..operators.paint_vertex_colors import PaintVertexColors


class EMVPPanel(BpyPanel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Paint Vertex Colors"
    bl_idname = "OBJECT_PT_PVC"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EMVP'

    # @classmethod
    # def poll(cls, context):
    #     ao = context.active_object
    #     return ao and context.active_object.type == 'MESH'

    def draw(self, context):
        layout = self.layout

        ao = context.active_object

        if not ao or ao.type != 'MESH' or len(context.selected_objects) != 1:
            layout.label(
                text="Please select a single mesh object", icon='ERROR')
            return

        if AddVertexColorLayer.poll(context):
            layout.operator(AddVertexColorLayer.bl_idname)
        else:
            # layout.prop(kmi.properties, "map")
            # if (get_color_map() == PaintVertexColors.map_enum_color[0]):
            #     layout.prop(kmi.properties, "color")
            # else:
            #     layout.prop(kmi.properties, "strength", slider=True)

            row = layout.row()
            row.label(text="Paint")
            sub_row = row.row()
            op_only_selected = sub_row.operator(PaintVertexColors.bl_idname, text="Selected")
            op_only_selected.only_selected = True
            op.color =  [1, 0, 0, 1]
            op.map = PaintVertexColors.map_enum_color[0]
            op.strength = 1
            sub_row.enabled = context.mode == "EDIT_MESH"

            # op_all_faces = row.operator(PaintVertexColors.bl_idname, text="All")
            # op_all_faces.only_selected = False

            # layout.operator(SelectFacesWithSameColor.bl_idname)
            # layout.operator(AddVertexColorPreviewMaterial.bl_idname)

            # for op in (op_only_selected, op_all_faces):
            #     op.color =  kmi.properties.color
            #     op.map = kmi.properties.map
            #     op.strength = kmi.properties.strength
