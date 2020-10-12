"""
Store enum values to access in layout properties
"""

from . import color_layers as layers

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
    ("Emission Strength",) * 3,
    # 8 :
    ("Emission Color",) * 3,
    # 9 :
    ("Alpha",) * 3,
    # 10 :
    ("Bump",) * 3,
]


color_map_name = all_maps[0][0]
subsurface_color_map_name = all_maps[1][0]
subsurface_strength_map_name = all_maps[2][0]
metallic_map_name = all_maps[3][0]
specular_map_name = all_maps[4][0]
roughness_map_name = all_maps[5][0]
transmission_map_name = all_maps[6][0]
emi_str_map_name = all_maps[7][0]
emission_color_map_name = all_maps[8][0]
alpha_map_name = all_maps[9][0]
bump_map_name = all_maps[10][0]


map_channels = \
    {
        color_map_name: -1,
        subsurface_color_map_name: -1,
        emission_color_map_name: -1,
        metallic_map_name: 0,
        subsurface_strength_map_name: 3,
        specular_map_name: 1,
        roughness_map_name: 2,
        transmission_map_name: 3,
        emi_str_map_name: 3,
        alpha_map_name: 3,
        bump_map_name: 0
    }

map_color_layer = \
    {
        color_map_name: layers.layer_color_alpha,
        alpha_map_name: layers.layer_color_alpha,
        subsurface_color_map_name: layers.layer_sc_s,
        subsurface_strength_map_name: layers.layer_sc_s,
        metallic_map_name: layers.layer_msrt,
        specular_map_name: layers.layer_msrt,
        roughness_map_name: layers.layer_msrt,
        transmission_map_name: layers.layer_msrt,
        emission_color_map_name: layers.layer_emi_emistr,
        emi_str_map_name: layers.layer_emi_emistr,
        bump_map_name: layers.layer_b
    }


def map_is_color(map_value):
    return "color" in str(map_value).lower()
