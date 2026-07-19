import unittest
import bpy  # type: ignore
import AAA_settings
import AAA_operator
import AAA_keymap
import AAA_menu
import AAA_panel
import AAA_pie
from .helpers import _is_op_registered

class TestUnregisterCleanup(unittest.TestCase):
    """
    Plan §5: verify that unregister() fully cleans up scene properties,
    operator bindings, and keymaps — then re-registers for subsequent tests.

    WARNING: This test class runs LAST and re-registers everything after.
    It must stay last alphabetically or be explicitly ordered.
    """

    def test_settings_unregister_removes_scene_props(self):
        prop_names = [name for name, _, _ in AAA_settings.SCENE_PROPERTIES]
        AAA_settings.unregister()
        try:
            for name in prop_names:
                with self.subTest(prop=name):
                    self.assertFalse(
                        hasattr(bpy.types.Scene, name),
                        f"bpy.types.Scene.{name} still present after unregister()",
                    )
        finally:
            AAA_settings.register()

    def test_operator_unregister_removes_from_bpy_types(self):
        idnames = [
            cls.bl_idname for cls in AAA_operator.classes if hasattr(cls, "bl_idname")
        ]
        AAA_operator.unregister()
        try:
            for idname in idnames:
                with self.subTest(idname=idname):
                    self.assertFalse(
                        _is_op_registered(idname),
                        f"'{idname}' still in bpy.types after unregister()",
                    )
        finally:
            AAA_operator.register()

    def test_keymap_unregister_clears_addon_keymaps(self):
        AAA_keymap.unregister()
        self.assertEqual(
            len(AAA_keymap.addon_keymaps),
            0,
            "addon_keymaps not empty after unregister()",
        )
        AAA_keymap.register()

    def test_menu_unregister_removes_from_bpy_types(self):
        class_names = [cls.__name__ for cls in AAA_menu.classes]
        AAA_menu.unregister()
        try:
            for name in class_names:
                with self.subTest(cls=name):
                    self.assertFalse(
                        hasattr(bpy.types, name),
                        f"Menu '{name}' still in bpy.types after unregister()",
                    )
        finally:
            AAA_menu.register()

    def test_panel_unregister_removes_from_bpy_types(self):
        class_names = [cls.__name__ for cls in AAA_panel.classes]
        AAA_panel.unregister()
        try:
            for name in class_names:
                with self.subTest(cls=name):
                    self.assertFalse(
                        hasattr(bpy.types, name),
                        f"Panel '{name}' still in bpy.types after unregister()",
                    )
        finally:
            AAA_panel.register()

    def test_pie_unregister_removes_from_bpy_types(self):
        class_names = [cls.__name__ for cls in AAA_pie.classes]
        AAA_pie.unregister()
        try:
            for name in class_names:
                with self.subTest(cls=name):
                    self.assertFalse(
                        hasattr(bpy.types, name),
                        f"Pie '{name}' still in bpy.types after unregister()",
                    )
        finally:
            AAA_pie.register()
