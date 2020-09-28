"""
Base module to enter Blender
"""

from . import auto_load

bl_info = {
    "name": "EMVP",
    "author": "Gorgious",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}

al = auto_load.AutoLoad()


def register():
    al.register()


def unregister():
    al.unregister()
