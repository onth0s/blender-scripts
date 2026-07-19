import unittest
import bpy  # type: ignore
import AAA_operator
from .helpers import _make_mesh_object, _clean_scene

class TestKeyConditionsRouting(unittest.TestCase):
    def setUp(self):
        self.original_condition = bpy.context.scene.conditions
        self.original_frame = bpy.context.scene.frame_current
        self.original_loop = bpy.context.scene.loop_frames
        self.original_start = bpy.context.scene.frame_start
        self.original_end = bpy.context.scene.frame_end

        bpy.context.scene.conditions = "TIMELINE"
        bpy.context.scene.loop_frames = True
        bpy.context.scene.frame_start = 10
        bpy.context.scene.frame_end = 250

    def tearDown(self):
        bpy.context.scene.conditions = self.original_condition
        bpy.context.scene.frame_current = self.original_frame
        bpy.context.scene.loop_frames = self.original_loop
        bpy.context.scene.frame_start = self.original_start
        bpy.context.scene.frame_end = self.original_end
        _clean_scene()

    def test_key_q_timeline_wraparound(self):
        bpy.context.scene.frame_current = 10
        res = bpy.ops.aaa.key_q()
        self.assertEqual(res, {"FINISHED"})
        self.assertEqual(bpy.context.scene.frame_current, 250)

    def test_key_w_timeline_sets_start(self):
        bpy.context.scene.frame_current = 100
        res = bpy.ops.aaa.key_w()
        self.assertEqual(res, {"FINISHED"})
        self.assertEqual(bpy.context.scene.frame_current, 10)

    def test_key_e_timeline_wraparound(self):
        bpy.context.scene.frame_current = 250
        res = bpy.ops.aaa.key_e()
        self.assertEqual(res, {"FINISHED"})
        self.assertEqual(bpy.context.scene.frame_current, 10)


class TestConditionsRouter(unittest.TestCase):
    def test_router_exists(self):
        self.assertTrue(hasattr(AAA_operator, "CONDITIONS_ROUTER"))

    def test_router_has_transform(self):
        self.assertIn("TRANSFORM", AAA_operator.CONDITIONS_ROUTER)

    def test_router_has_timeline(self):
        self.assertIn("TIMELINE", AAA_operator.CONDITIONS_ROUTER)

    def test_router_values_are_dicts_with_callables(self):
        for cond, key_map in AAA_operator.CONDITIONS_ROUTER.items():
            with self.subTest(cond=cond):
                self.assertIsInstance(
                    key_map, dict, f"CONDITIONS_ROUTER['{cond}'] is not a dict"
                )
                for key, handler in key_map.items():
                    with self.subTest(key=key):
                        self.assertTrue(
                            callable(handler),
                            f"CONDITIONS_ROUTER['{cond}']['{key}'] is not callable",
                        )
