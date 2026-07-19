import unittest
import bpy  # type: ignore
import AAA_settings
import AAA_operator
import AAA_menu
import AAA_panel
import AAA_pie
from .helpers import _is_op_registered, _is_class_registered

class TestSettingsRegistration(unittest.TestCase):
    """Scene custom properties are present with correct types."""

    def test_all_scene_props_registered(self):
        scene = bpy.context.scene
        for name, _, _ in AAA_settings.SCENE_PROPERTIES:
            with self.subTest(prop=name):
                self.assertTrue(
                    hasattr(scene, name),
                    f"Scene property '{name}' missing after registration",
                )

    def test_conditions_is_string(self):
        self.assertIsInstance(bpy.context.scene.conditions, str)

    def test_show_overlays_is_bool(self):
        self.assertIsInstance(bpy.context.scene.show_overlays, bool)

    def test_loop_frames_is_bool(self):
        self.assertIsInstance(bpy.context.scene.loop_frames, bool)

    def test_axis_roll_is_string(self):
        self.assertIsInstance(bpy.context.scene.axis_roll, str)

    def test_already_saved_counter_is_int(self):
        self.assertIsInstance(bpy.context.scene.already_saved_counter, int)


class TestOperatorRegistration(unittest.TestCase):
    """All AAA operator classes are registered in bpy.types."""

    def test_all_operator_classes_registered(self):
        for cls in AAA_operator.classes:
            with self.subTest(cls=cls.__name__):
                idname = getattr(cls, "bl_idname", None)
                self.assertIsNotNone(idname, f"{cls.__name__} has no bl_idname")
                self.assertTrue(
                    _is_op_registered(idname),
                    f"Operator '{idname}' ({cls.__name__}) not found in bpy.types",
                )

    def test_operator_classes_have_bl_label(self):
        for cls in AAA_operator.classes:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(
                    hasattr(cls, "bl_label"), f"{cls.__name__} missing bl_label"
                )


class TestMenuRegistration(unittest.TestCase):
    """All AAA menu classes are registered in bpy.types."""

    def test_all_menu_classes_registered(self):
        for cls in AAA_menu.classes:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(
                    _is_class_registered(cls),
                    f"Menu '{cls.__name__}' is not registered",
                )


class TestPanelRegistration(unittest.TestCase):
    """All AAA panel classes are registered in bpy.types."""

    def test_all_panel_classes_registered(self):
        for cls in AAA_panel.classes:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(
                    _is_class_registered(cls),
                    f"Panel '{cls.__name__}' is not registered",
                )

    def test_panels_have_required_attributes(self):
        for cls in AAA_panel.classes:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(
                    hasattr(cls, "bl_space_type"),
                    f"Panel '{cls.__name__}' missing bl_space_type",
                )
                self.assertTrue(
                    hasattr(cls, "bl_region_type"),
                    f"Panel '{cls.__name__}' missing bl_region_type",
                )
                self.assertTrue(
                    hasattr(cls, "bl_label"), f"Panel '{cls.__name__}' missing bl_label"
                )


class TestPieMenuRegistration(unittest.TestCase):
    """All AAA pie menu classes are registered in bpy.types."""

    def test_all_pie_classes_registered(self):
        for cls in AAA_pie.classes:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(
                    _is_class_registered(cls), f"Pie '{cls.__name__}' is not registered"
                )
