"""
Logic executed when the addon settings are changed
"""

from .. import addon_preferences
from ..paint_logic.maps import map_color_layer, map_is_color, map_channels
from ..paint_logic.brush_handler import get_or_create_brush, get_or_create_palette


def update_prefs(self, context):
    ao = context.active_object
    if not ao:
        return
    mesh = ao.data
    if not mesh:
        return
    prefs = addon_preferences.get_preferences(context)
    _map = prefs.map

    map_name = map_color_layer[_map]
    for i, vc in enumerate(mesh.vertex_colors):
        if vc.name == map_name:
            mesh.vertex_colors.active_index = i
            break
    vertex_color_layer = mesh.vertex_colors.get(map_name)
    if vertex_color_layer:
        vertex_color_layer.active_render = True

    brush = get_or_create_brush()
    get_or_create_palette(context)

    if map_is_color(_map):
        brush.blend = 'MIX'
    else:
        channel = map_channels[_map]
        if channel == 3:
            brush.blend = 'ERASE_ALPHA' if prefs.subtract else 'ADD_ALPHA'
        else:
            brush.blend = 'SUB' if prefs.subtract else 'ADD'
        brush.color = [(c == channel) * prefs.strength for c in range(3)]
        prefs.last_was_color = False
        brush.secondary_color = brush.color
