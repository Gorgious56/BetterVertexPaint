import bpy
import bmesh


class AddVertexColorPreviewMaterial(bpy.types.Operator):
    """Set a PBR Material using the custom maps"""
    bl_idname = "object.add_vertex_color_preview_mat"
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
        output = nodes.new(type='ShaderNodeOutputMaterial')
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (-300, 0)
        vc_color = nodes.new(type='ShaderNodeVertexColor')
        vc_color.location = (-700, 0)
        vc_msrt = nodes.new(type='ShaderNodeVertexColor')
        vc_msrt.location = (-700, -200)
        vc_msr_sep = nodes.new(type='ShaderNodeSeparateRGB')
        vc_msr_sep.location = (-500, -170)

        vc_color.layer_name = AddVertexColorLayer.color_alpha_layer
        links = vc_preview_mat.node_tree.links

        links.new(vc_color.outputs[0], bsdf.inputs[0])  # Color
        links.new(vc_color.outputs[1], bsdf.inputs[18])  # Alpha
        links.new(bsdf.outputs[0], output.inputs[0])  # Main output

        vc_msrt.layer_name = AddVertexColorLayer.msrt_layer
        # Separate Metallic, Specular, Roughness
        links.new(vc_msrt.outputs[0], vc_msr_sep.inputs[0])
        links.new(vc_msr_sep.outputs[0], bsdf.inputs[4])  # Metallic
        links.new(vc_msr_sep.outputs[1], bsdf.inputs[5])  # Specular
        links.new(vc_msr_sep.outputs[2], bsdf.inputs[7])  # Roughness
        links.new(vc_msrt.outputs[1], bsdf.inputs[15])  # Transmission

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


class SelectFacesWithSameColor(bpy.types.Operator):
    """Select Faces with the same vertex colors information"""
    bl_idname = "object.select_same_vertex_colors"
    bl_label = "Select Faces With Same Data"
    bl_options = {'REGISTER', 'UNDO'}

    selected_face_idx = None

    @classmethod
    def poll(cls, context):
        if not PaintVertexColors.poll(context) or context.mode != 'EDIT_MESH':
            return False
        bm = bmesh.from_edit_mesh(context.active_object.data)
        cls.selected_face_idx = None
        for f in bm.faces:
            if not f.select:
                continue
            if f.select:
                if cls.selected_face_idx is not None:
                    cls.selected_face_idx = None
                    bm.free()
                    return False
                cls.selected_face = f.index
        bm.free()
        return True

    def execute(self, context):
        mesh = context.active_object.data
        sfi = self.selected_face_idx

        color_layer = get_vertex_color_layer(mesh)

        if not color_layer:
            return {'FINISHED'}

        def get_mean_value(face_index):
            for idx in mesh.polygons[face_index].loop_indices:
                print(idx)

        map = get_color_map()
        if map == PaintVertexColors.map_enum_color[0]:
            get_mean_value(sfi)
            return {'FINISHED'}
            r, g, b = self.color[0:3]
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    color_layer.data[idx].color = [
                        r, g, b, color_layer.data[idx].color[3]]
        elif map == PaintVertexColors.map_enum_alpha[0]:
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    r, g, b = color_layer.data[idx].color[0:3]
                    color_layer.data[idx].color = [r, g, b, self.strength]
        elif map == PaintVertexColors.map_enum_metallic[0]:
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    r, g, b, a = color_layer.data[idx].color
                    color_layer.data[idx].color = [self.strength, g, b, a]
        elif map == PaintVertexColors.map_enum_specular[0]:
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    r, g, b, a = color_layer.data[idx].color
                    color_layer.data[idx].color = [r, self.strength, b, a]
        elif map == PaintVertexColors.map_enum_roughness[0]:
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    r, g, b, a = color_layer.data[idx].color
                    color_layer.data[idx].color = [r, g, self.strength, a]
        elif map == PaintVertexColors.map_enum_transmission[0]:
            for poly in mesh.polygons:
                if only_selected and not poly.select:
                    continue
                for idx in poly.loop_indices:
                    r, g, b, a = color_layer.data[idx].color
                    color_layer.data[idx].color = [r, g, b, self.strength]

        return {'FINISHED'}


def get_vertex_color_layer(mesh):
    color_map = get_color_map()
    if color_map in (
            PaintVertexColors.map_enum_color[0],
            PaintVertexColors.map_enum_alpha[0]):
        return mesh.vertex_colors.get(AddVertexColorLayer.color_alpha_layer)
    elif color_map in (
        PaintVertexColors.map_enum_metallic[0],
        PaintVertexColors.map_enum_specular[0],
        PaintVertexColors.map_enum_roughness[0],
        PaintVertexColors.map_enum_transmission[0],
    ):
        return mesh.vertex_colors.get(AddVertexColorLayer.msrt_layer)


def get_color_map():
    return kmi.properties.map

# def register():
#     bpy.utils.register_class(AddVertexColorLayer)
#     bpy.utils.register_class(SelectFacesWithSameColor)
#     bpy.utils.register_class(PaintVertexColors)
#     bpy.utils.register_class(AddVertexColorPreviewMaterial)
#     bpy.utils.register_class(EMVPPanel)


# def unregister():
#     bpy.utils.unregister_class(EMVPPanel)
#     bpy.utils.unregister_class(AddVertexColorPreviewMaterial)
#     bpy.utils.unregister_class(PaintVertexColors)
#     bpy.utils.register_class(SelectFacesWithSameColor)
#     bpy.utils.unregister_class(AddVertexColorLayer)


# if __name__ == "__main__":
#     register()
#     keymap_items = bpy.context.window_manager.keyconfigs.addon.keymaps['3D View Generic'].keymap_items
#     while PaintVertexColors.bl_idname in keymap_items.keys():
#         keymap_items.remove(keymap_items.get(PaintVertexColors.bl_idname))
#     kmi = keymap_items.new(PaintVertexColors.bl_idname, "NONE", "ANY")
#     kmi.type = 'NDOF_BUTTON_10'
