import sys
import os
import unittest
import io
import contextlib
import bpy  # type: ignore
from mathutils import Vector, Quaternion  # type: ignore

@contextlib.contextmanager
def silence_warnings():
    """Silence stdout warning messages printed during Blender operator executions."""
    with contextlib.redirect_stdout(io.StringIO()):
        yield


def _idname_to_bpy_types_key(bl_idname: str) -> str:
    """
    Convert 'aaa.toggle_prop' -> 'AAA_OT_toggle_prop'.
    Blender convention: <PREFIX>_OT_<suffix> (prefix uppercased)
    """
    prefix, suffix = bl_idname.split(".", 1)
    return f"{prefix.upper()}_OT_{suffix}"


def _is_op_registered(bl_idname: str) -> bool:
    return hasattr(bpy.types, _idname_to_bpy_types_key(bl_idname))


def _is_class_registered(cls) -> bool:
    """Check if a menu/panel class is registered (uses class __name__ directly)."""
    return hasattr(bpy.types, cls.__name__)


def _make_mesh_object(name="TestCube"):
    """Add a cube to the scene and return the active object."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    return obj


def _clean_scene():
    """Return to OBJECT mode and delete all objects."""
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
