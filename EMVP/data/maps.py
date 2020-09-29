"""
Store enum values to access in layout properties
"""

from .color_layers import layer_color_alpha, layer_emi_ior, layer_msrt, layer_sc_s

all_maps = [
    # 0 :
    ("Color",) * 3,
    # 1 :
    ("Subsurface Color",) * 3,
    # 2 :
    ("Subsurface Strength",) * 3,
    # 3 :
    ("Metallic",) * 3,
    # 4 :
    ("Specular",) * 3,
    # 5 :
    ("Roughness",) * 3,
    # 6 :
    ("Transmission",) * 3,
    # 7 :
    ("---Placeholder---",) * 3,
    # 8 :
    ("Emission Color",) * 3,
    # 9 :
    ("Alpha",) * 3,
]


color_map_name = all_maps[0][0]
subsurface_color_map_name = all_maps[1][0]
subsurface_strength_map_name = all_maps[2][0]
metallic_map_name = all_maps[3][0]
specular_map_name = all_maps[4][0]
roughness_map_name = all_maps[5][0]
transmission_map_name = all_maps[6][0]
ior_map_name = all_maps[7][0]
emission_color_map_name = all_maps[8][0]
alpha_map_name = all_maps[9][0]


map_channels = \
    {
        color_map_name: -1,
        subsurface_color_map_name: -1,
        subsurface_strength_map_name: 3,
        metallic_map_name: 0,
        specular_map_name: 1,
        roughness_map_name: 2,
        transmission_map_name: 3,
        ior_map_name: 3,
        emission_color_map_name: -1,
        alpha_map_name: 3,
    }

map_color_layer = \
    {
        color_map_name: layer_color_alpha,
        subsurface_color_map_name: layer_sc_s,
        subsurface_strength_map_name: layer_sc_s,
        metallic_map_name: layer_msrt,
        specular_map_name: layer_msrt,
        roughness_map_name: layer_msrt,
        transmission_map_name: layer_msrt,
        ior_map_name: layer_emi_ior,
        emission_color_map_name: layer_emi_ior,
        alpha_map_name: layer_color_alpha,
    }


def map_is_color(map_value):
    return "color" in map_value.lower()
