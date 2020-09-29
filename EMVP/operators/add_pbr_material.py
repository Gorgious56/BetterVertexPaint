"""
Operator to add a PBR based material using the right vertex color maps
"""

import bpy
from ..data.color_layers import layer_color_alpha, layer_msrt, layer_emi_ior, layer_sc_s


class AddPBRMaterial(bpy.types.Operator):
    """Set a PBR Material using the custom maps"""
    bl_idname = "object.add_pbr_material"
    bl_label = "Set PBR Material"
    bl_options = {'REGISTER', 'UNDO'}

    mat_name = "VC_PREVIEW"

    @classmethod
    def poll(cls, context):
        ao = context.active_object
        return ao and context.active_object.type == "MESH"

    def execute(self, context):
        vc_preview_mat = bpy.data.materials.get(self.mat_name)
        if vc_preview_mat is None:
            vc_preview_mat = bpy.data.materials.new(self.mat_name)
        vc_preview_mat.use_nodes = True
        nodes = vc_preview_mat.node_tree.nodes
        nodes.clear()
        links = vc_preview_mat.node_tree.links

        output = nodes.new(type='ShaderNodeOutputMaterial')
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (-300, 0)

        vc_color = nodes.new(type='ShaderNodeVertexColor')
        vc_color.location = (-700, 0)

        vc_msrt = nodes.new(type='ShaderNodeVertexColor')
        vc_msrt.location = (-700, -200)
        vc_msr_sep = nodes.new(type='ShaderNodeSeparateRGB')
        vc_msr_sep.location = (-500, -170)

        vc_subsurface = nodes.new(type='ShaderNodeVertexColor')
        vc_subsurface.location = (-700, -100)

        vc_emi_ior = nodes.new(type='ShaderNodeVertexColor')
        vc_emi_ior.location = (-700, -300)

        vc_color.layer_name = layer_color_alpha
        links.new(vc_color.outputs[0], bsdf.inputs[0])  # Color
        links.new(vc_color.outputs[1], bsdf.inputs[18])  # Alpha

        vc_msrt.layer_name = layer_msrt
        # Separate Metallic, Specular, Roughness
        links.new(vc_msrt.outputs[0], vc_msr_sep.inputs[0])
        links.new(vc_msr_sep.outputs[0], bsdf.inputs[4])  # Metallic
        links.new(vc_msr_sep.outputs[1], bsdf.inputs[5])  # Specular
        links.new(vc_msr_sep.outputs[2], bsdf.inputs[7])  # Roughness
        links.new(vc_msrt.outputs[1], bsdf.inputs[15])  # Transmission

        vc_subsurface.layer_name = layer_sc_s
        links.new(vc_subsurface.outputs[0], bsdf.inputs[3])  # Subsurface color
        links.new(vc_subsurface.outputs[1], bsdf.inputs[1])  # Subsurface strength

        vc_emi_ior.layer_name = layer_emi_ior
        links.new(vc_emi_ior.outputs[0], bsdf.inputs[17])  # Emission
        # links.new(vc_emi_ior.outputs[1], bsdf.inputs[14])  # IOR


        links.new(bsdf.outputs[0], output.inputs[0])  # Main output

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
