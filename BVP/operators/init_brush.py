"""
This operator initializes the custom brush used in the add-on.
"""
import bpy
from ..paint_logic import brush_handler

class InitBrush(bpy.types.Operator):
    """
    This operator initializes the custom brush used in the add-on.
    """
    bl_idname = "paint.bvp_init_brush"
    bl_label = "Set Custom Brush"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.tool_settings.vertex_paint.brush = brush_handler.get_or_create_brush()
        return {'FINISHED'}
