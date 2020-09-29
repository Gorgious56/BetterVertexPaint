"""
Stores references to color layers information
"""

prefix = "EMVP"

layer_color_alpha = prefix + "_" + "COLOR_ALPHA"
layer_msrt = prefix + "_" + "M_S_R_T"  # Metallic Specular Roughness Transmission
layer_sc_s = prefix + "_" + "S_SC"  # Subsurface Color, Subsurface
layer_emi_ior = prefix + "_" + "EMI_IOR"  # Emission Color, IOR

all_layers = \
    [
        layer_color_alpha,
        layer_msrt,
        layer_sc_s,
        layer_emi_ior
    ]

default_values = \
    {
        layer_color_alpha: (1, 1, 1, 1),
        layer_msrt: (0, .5, .5, 0),
        layer_sc_s: (.8, .8, .8, 0),
        layer_emi_ior: (0, 0, 0, 1.45),
    }
