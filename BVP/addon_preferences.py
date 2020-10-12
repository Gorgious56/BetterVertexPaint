"""
Define the add-on preferences
"""

import bpy
from bpy.types import AddonPreferences
from .paint_logic.maps import all_maps
from .paint_logic import on_setting_change


class BVPAddonPrefs(AddonPreferences):
    """
    Add-on Preferences
    """
    bl_idname = __package__

    map: bpy.props.EnumProperty(
        name="Map",
        items=all_maps,
        update=on_setting_change.update_prefs,
    )

    strength: bpy.props.FloatProperty(
        name="Strength",
        default=0,
        min=0,
        soft_max=1,
        max=1,
        update=on_setting_change.update_prefs,
    )

    subtract: bpy.props.BoolProperty(
        default=False,
        update=on_setting_change.update_prefs,
    )


addon_name = BVPAddonPrefs.bl_idname


def get_preferences(context):
    return context.preferences.addons.get(addon_name).preferences
