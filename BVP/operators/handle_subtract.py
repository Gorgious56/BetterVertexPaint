"""
Operator to handle subtraction with SHIFT key pressed/released
"""

import bpy
from ..addon_preferences import get_preferences


class HandleSubtract(bpy.types.Operator):
    """
    Operator to handle subtraction with SHIFT key pressed/released"""
    bl_idname = "paint.bvp_toggle_subtract"
    bl_label = "BVP : Toggle Paint Subtract"
    bl_options = {'UNDO'}

    subtract: bpy.props.BoolProperty(
        default=False
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.mode == 'PAINT_VERTEX'

    def execute(self, context):
        prefs = get_preferences(context)

        prefs.subtract = self.subtract
        return {'FINISHED'}
