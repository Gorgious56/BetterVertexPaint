# '''
# Copyright (C) 2017 pitiwazou, kilbee


# Created by pitiwazou, kilbee

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
# '''


# import rna_keymap_ui
# from bpy.types import Menu
# import bpy
# bl_info = {
#     "name": "Addon Keymap Template",
#     "description": "",
#     "author": "pitiwazou, kilbee",
#     "version": (0, 0, 1),
#     "blender": (2, 78, 0),
#     "location": "View3D",
#     "warning": "This addon is still in development.",
#     "wiki_url": "",
#     "category": "Object"}


# # -----------------------------------------------------------------------------
# #    UI - Pie menu
# # -----------------------------------------------------------------------------

# # Pie Menu

# class Test_Pie_Menu(Menu):
#     bl_idname = "pie.test_pie_menu"
#     bl_label = "Test Pie Menu"

#     @classmethod
#     def poll(cls, context):
#         return context.object is not None and context.selected_objects

#     def draw(self, context):
#         layout = self.layout
#         pie = layout.menu_pie()

#         #4 - LEFT
#         pie.operator_enum("mesh.select_mode", "type")
#         #6 - RIGHT

#         #2 - BOTTOM

#         #8 - TOP

#         #7 - TOP - LEFT

#         #9 - TOP - RIGHT

#         #1 - BOTTOM - LEFT

#         #3 - BOTTOM - RIGHT

# # -----------------------------------------------------------------------------
# #    Preferences
# # -----------------------------------------------------------------------------

# # Preferences


# class AddonPreferences(bpy.types.AddonPreferences):
#     bl_idname = __name__

#     def draw(self, context):
#         layout = self.layout
#         wm = bpy.context.window_manager
#         box = layout.box()
#         split = box.split()
#         col = split.column()
#         col.label('Setup Pie menu Hotkey')
#         col.separator()
#         wm = bpy.context.window_manager
#         kc = wm.keyconfigs.user
#         km = kc.keymaps['3D View Generic']
#         kmi = get_hotkey_entry_item(
#             km, 'wm.call_menu_pie', 'pie.test_pie_menu')
#         if kmi:
#             col.context_pointer_set("keymap", km)
#             rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
#         else:
#             col.label("No hotkey entry found")
#             col.operator(Template_Add_Hotkey.bl_idname,
#                          text="Add hotkey entry", icon='ZOOMIN')


# # -----------------------------------------------------------------------------
# #    Keymap
# # -----------------------------------------------------------------------------
# addon_keymaps = []


# def get_addon_preferences():
#     ''' quick wrapper for referencing addon preferences '''
#     addon_preferences = bpy.context.user_preferences.addons[__name__].preferences
#     return addon_preferences


# def get_hotkey_entry_item(km, kmi_name, kmi_value):
#     '''
#     returns hotkey of specific type, with specific properties.name (keymap is not a dict, so referencing by keys is not enough
#     if there are multiple hotkeys!)
#     '''
#     for i, km_item in enumerate(km.keymap_items):
#         if km.keymap_items.keys()[i] == kmi_name:
#             if km.keymap_items[i].properties.name == kmi_value:
#                 return km_item
#     return None


# def add_hotkey():
#     user_preferences = bpy.context.user_preferences
#     addon_prefs = user_preferences.addons[__name__].preferences

#     wm = bpy.context.window_manager
#     kc = wm.keyconfigs.addon
#     km = kc.keymaps.new(name="3D View Generic",
#                         space_type='VIEW_3D', region_type='WINDOW')
#     kmi = km.keymap_items.new(
#         "wm.call_menu_pie", 'RIGHTMOUSE', 'PRESS', shift=True, ctrl=True, alt=True)
#     kmi.properties.name = "pie.test_pie_menu"
#     kmi.active = True
#     addon_keymaps.append((km, kmi))


# class Template_Add_Hotkey(bpy.types.Operator):
#     ''' Add hotkey entry '''
#     bl_idname = "template.add_hotkey"
#     bl_label = "Addon Preferences Example"
#     bl_options = {'REGISTER', 'INTERNAL'}

#     def execute(self, context):
#         add_hotkey()

#         self.report(
#             {'INFO'}, "Hotkey added in User Preferences -> Input -> Screen -> Screen (Global)")
#         return {'FINISHED'}


# def remove_hotkey():
#     ''' clears all addon level keymap hotkeys stored in addon_keymaps '''
#     wm = bpy.context.window_manager
#     kc = wm.keyconfigs.addon
#     km = kc.keymaps['3D View Generic']

#     for km, kmi in addon_keymaps:
#         km.keymap_items.remove(kmi)
#         wm.keyconfigs.addon.keymaps.remove(km)
#     addon_keymaps.clear()


# # -----------------------------------------------------------------------------
# #    Register
# # -----------------------------------------------------------------------------
# def register():
#     bpy.utils.register_module(__name__)

#     # hotkey setup
#     add_hotkey()


# def unregister():
#     bpy.utils.unregister_module(__name__)

#     # hotkey cleanup
#     remove_hotkey()


# if __name__ == "__main__":
#     register()