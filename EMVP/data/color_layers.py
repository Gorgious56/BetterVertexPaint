"""
Stores references to color layers information
"""

prefix = "EMVP"

layer_color_alpha = prefix + "_" + "COLOR_ALPHA"
# Metallic Specular Roughness Transmission
layer_msrt = prefix + "_" + "M_S_R_T"
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


def reset_vertex_colors(mesh, color_layer, only_selected=False):
    default_color = default_values[color_layer.name]
    if only_selected:  # Reset only selected faces
        for poly in mesh.polygons:
            if not poly.select:
                continue
            for idx in poly.loop_indices:
                color_layer.data[idx].color = default_color
    else:  # Reset all faces
        for poly in mesh.polygons:
            for idx in poly.loop_indices:
                color_layer.data[idx].color = default_color


def set_layers_to_default(mesh, force_reset, only_selected=False):
    for color_layer_name in all_layers:
        set_layer_to_default(mesh, force_reset, color_layer_name, [
                             vc.name for vc in mesh.vertex_colors], only_selected)


def set_layer_to_default(mesh, force_reset, color_layer_name, color_layer_names=None, only_selected=False):
    if color_layer_names is None:
        color_layer_names = [vc.name for vc in mesh.vertex_colors]
    if color_layer_name not in color_layer_names:
        reset_vertex_colors(mesh, mesh.vertex_colors.new(
            name=color_layer_name), only_selected)
    elif force_reset:  # The color layer already exists. Overwrite if force_reset
        reset_vertex_colors(
            mesh, mesh.vertex_colors[color_layer_name], only_selected)


def are_all_layers_created(mesh):
    vertex_color_names = \
        [
            vc.name for vc in mesh.vertex_colors
        ]
    if not mesh.vertex_colors or len(vertex_color_names) == 0:
        return False
    for color_layer_name in all_layers:
        if color_layer_name not in vertex_color_names:
            return False
    return True
