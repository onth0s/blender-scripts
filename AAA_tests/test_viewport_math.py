import unittest
import bpy  # type: ignore
from mathutils import Vector, Quaternion  # type: ignore
from math import pi

class _RollOperator:
    def __init__(self):
        self.initial_angle = 0
        self.angle_now = 0
        self.initial_rotation = Vector((0, 0, 0))
        self.camNormal = Vector((0, 0, -1))
        self.temp_degree = 0

    def execute(self, rv3d):
        angle_diff = self.angle_now - self.initial_angle
        quat = Quaternion(self.camNormal, angle_diff)
        rv3d.view_rotation = self.initial_rotation @ quat
        if angle_diff > 0:
            self.temp_degree = angle_diff
        else:
            self.temp_degree = -1 * angle_diff
        return {"FINISHED"}


class TestRollViewportMath(unittest.TestCase):
    def _run_roll(self, initial_angle, angle_now, cam_normal, initial_rotation):
        op = _RollOperator()
        op.initial_angle = initial_angle
        op.angle_now = angle_now
        op.camNormal = cam_normal
        op.initial_rotation = initial_rotation.copy()

        class MockRV3D:
            def __init__(self):
                self.view_rotation = initial_rotation.copy()

        rv3d = MockRV3D()
        op.execute(rv3d)
        return rv3d.view_rotation

    def test_zero_angle_diff_produces_identity_rotation(self):
        identity = Quaternion()
        result = self._run_roll(
            initial_angle=1.0,
            angle_now=1.0,
            cam_normal=Vector((0, 0, -1)),
            initial_rotation=identity,
        )
        self.assertAlmostEqual(result.w, 1.0, places=5)
        self.assertAlmostEqual(result.x, 0.0, places=5)
        self.assertAlmostEqual(result.y, 0.0, places=5)
        self.assertAlmostEqual(result.z, 0.0, places=5)

    def test_quarter_turn_around_z_axis(self):
        identity = Quaternion()
        result = self._run_roll(
            initial_angle=0.0,
            angle_now=pi / 2,
            cam_normal=Vector((0, 0, 1)),
            initial_rotation=identity,
        )
        expected = Quaternion((0, 0, 1), pi / 2)
        self.assertAlmostEqual(result.w, expected.w, places=5)
        self.assertAlmostEqual(result.z, expected.z, places=5)

    def test_negative_angle_diff(self):
        identity = Quaternion()
        result_pos = self._run_roll(0.0, pi / 4, Vector((0, 0, 1)), identity)
        result_neg = self._run_roll(0.0, -pi / 4, Vector((0, 0, 1)), identity)
        self.assertAlmostEqual(result_pos.z, -result_neg.z, places=5)

    def test_non_identity_initial_rotation_composes(self):
        start_rot = Quaternion((0, 0, 1), pi / 4)
        result = self._run_roll(
            initial_angle=0.0,
            angle_now=pi / 4,
            cam_normal=Vector((0, 0, 1)),
            initial_rotation=start_rot,
        )
        expected = start_rot @ Quaternion((0, 0, 1), pi / 4)
        self.assertAlmostEqual(result.w, expected.w, places=5)
        self.assertAlmostEqual(result.z, expected.z, places=5)


class TestSwitchRendererLogic(unittest.TestCase):
    def test_engine_enum_items_accessible(self):
        props = bpy.types.RenderSettings.bl_rna.properties
        self.assertIn("engine", props)
        items = props["engine"].enum_items
        self.assertGreater(len(items), 0)

    def test_eevee_engine_present(self):
        items = bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items
        eevee_engines = [
            i.identifier
            for i in items
            if "EEVEE" in i.identifier or "BLENDER_EEVEE" in i.identifier
        ]
        self.assertGreater(len(eevee_engines), 0)

    def test_workbench_or_eevee_engine_present(self):
        items = bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items
        identifiers = [i.identifier for i in items]
        self.assertGreater(len(identifiers), 0)
        self.assertIn("BLENDER_EEVEE", identifiers)

    def test_scene_render_engine_assignable(self):
        items = bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items
        identifiers = [i.identifier for i in items]
        available = [i for i in identifiers if i != "BLENDER_WORKBENCH"]
        engine = available[0] if available else "BLENDER_EEVEE"
        original = bpy.context.scene.render.engine
        bpy.context.scene.render.engine = engine
        self.assertEqual(bpy.context.scene.render.engine, engine)
        bpy.context.scene.render.engine = original
