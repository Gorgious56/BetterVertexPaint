"""
Define the add-on preferences
"""

import bpy
from bpy.types import AddonPreferences
from .data.maps import all_maps


class AddonPrefs(AddonPreferences):
    """
    Add-on Preferences
    """
    bl_idname = __package__

    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=[1, 1, 1, 1],
        size=4,
        min=0,
        max=1,
    )

    map: bpy.props.EnumProperty(
        name="Map",
        items=all_maps,
    )
    strength: bpy.props.FloatProperty(
        name="Strength",
        default=1,
        min=0,
        soft_max=1,
        max=4.875,
    )
    reset_all_maps: bpy.props.BoolProperty(
        name="Reset All Maps",
        default=False
    )

    @staticmethod
    def get_preferences(context):
        return context.preferences.addons.get(
            AddonPrefs.bl_idname).preferences
    """
    def draw(self, context):
        layout = self.layout
    """
