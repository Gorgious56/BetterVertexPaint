"""import bpy
import bmesh




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
"""