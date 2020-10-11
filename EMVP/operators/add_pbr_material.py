"""
Operator to add a PBR based material using the right vertex color maps
"""

import bpy
from ..paint_logic import color_layers as layers


def create_nodes(material):
    nodes = material.node_tree.nodes
    nodes.clear()
    links = material.node_tree.links
    cols = [-300 - c * 200 for c in range(5)]

    output = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (cols[0], 0)

    vc_color_alpha = nodes.new(type='ShaderNodeVertexColor')
    vc_color_alpha.location = (cols[3], 0)

    vc_subsurface_substrength = nodes.new(type='ShaderNodeVertexColor')
    vc_subsurface_substrength.location = (cols[3], -100)

    vc_msrt = nodes.new(type='ShaderNodeVertexColor')
    vc_msrt.location = (cols[3], -200)
    vc_msr_sep = nodes.new(type='ShaderNodeSeparateRGB')
    vc_msr_sep.location = (cols[1], -170)

    vc_b = nodes.new(type='ShaderNodeVertexColor')
    vc_b.location = (cols[3], -500)
    vc_b_sep = nodes.new(type='ShaderNodeSeparateRGB')
    vc_b_sep.location = (cols[2], -400)
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (cols[1], -370)

    vc_emi_emistr = nodes.new(type='ShaderNodeVertexColor')
    vc_emi_emistr.location = (cols[3], -300)

    vc_dirt = nodes.new(type='ShaderNodeVertexColor')
    vc_dirt.location = (cols[3], -400)

    dirt_mix = nodes.new(type='ShaderNodeMixRGB')
    dirt_mix.location = (cols[2], 50)
    dirt_mix.name = BVP_AddPBRMaterial.dirt_mix_name

    vc_color_alpha.layer_name = layers.layer_color_alpha
    links.new(vc_color_alpha.outputs[0], dirt_mix.inputs[1])  # Color
    links.new(vc_color_alpha.outputs[1], bsdf.inputs[18])  # Alpha

    vc_msrt.layer_name = layers.layer_msrt
    # Separate Metallic, Specular, Roughness
    links.new(vc_msrt.outputs[0], vc_msr_sep.inputs[0])
    links.new(vc_msr_sep.outputs[0], bsdf.inputs[4])  # Metallic
    links.new(vc_msr_sep.outputs[1], bsdf.inputs[5])  # Specular
    links.new(vc_msr_sep.outputs[2], bsdf.inputs[7])  # Roughness
    links.new(vc_msrt.outputs[1], bsdf.inputs[15]) # Transmission

    vc_subsurface_substrength.layer_name = layers.layer_sc_s
    links.new(vc_subsurface_substrength.outputs[0], bsdf.inputs[3])  # Subsurface color
    links.new(vc_subsurface_substrength.outputs[1], bsdf.inputs[1])  # Subsurface Strength

    vc_emi_emistr.layer_name = layers.layer_emi_emistr
    links.new(vc_emi_emistr.outputs[0], bsdf.inputs[17])  # Emission

    vc_b.layer_name = layers.layer_b
    links.new(vc_b.outputs[0], vc_b_sep.inputs[0])
    links.new(vc_b_sep.outputs[0], bump.inputs[2])
    links.new(bump.outputs[0], bsdf.inputs[19])

    vc_dirt.layer_name = layers.layer_dirt
    links.new(vc_dirt.outputs[0], dirt_mix.inputs[2])

    dirt_mix.blend_type = 'MULTIPLY'
    dirt_mix.inputs[0].default_value = 1
    links.new(dirt_mix.outputs[0], bsdf.inputs[0])

    links.new(bsdf.outputs[0], output.inputs[0])  # Main output


class BVP_AddPBRMaterial(bpy.types.Operator):
    """Set a PBR Material using the custom maps"""
    bl_idname = "paint.bvp_set_pbr_material"
    bl_label = "Set PBR Material"
    bl_options = {'REGISTER', 'UNDO'}

    mat_name = "VC_PREVIEW"
    dirt_mix_name = "Dirt_MIX"

    @classmethod
    def poll(cls, context):
        ao = context.active_object
        return ao and context.active_object.type == "MESH"

    def execute(self, context):
        vc_preview_mat = bpy.data.materials.get(self.mat_name)
        if vc_preview_mat is None:
            vc_preview_mat = bpy.data.materials.new(self.mat_name)
        vc_preview_mat.use_nodes = True

        create_nodes(vc_preview_mat)

        vc_preview_mat.blend_method = 'CLIP'
        vc_preview_mat.use_screen_refraction = True

        mats = context.active_object.data.materials
        if mats:
            if mats[0] == vc_preview_mat:
                return {'FINISHED'}
            for i in range(len(mats) - 1, -1, -1):
                if i == len(mats) - 1:
                    mats.append(mats[i])
                else:
                    mats[i + 1] = mats[i]
            mats[0] = vc_preview_mat
        else:
            mats.append(vc_preview_mat)

        return {'FINISHED'}
