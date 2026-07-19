import unittest
import bpy  # type: ignore
import AAA_utils
from .helpers import _make_mesh_object, _clean_scene, silence_warnings

class TestSwitchWorkspaceExecution(unittest.TestCase):
    """SwitchWorkspace operator switches to a named workspace."""

    def test_workspaces_exist(self):
        self.assertGreater(len(bpy.data.workspaces), 0)

    def test_switch_to_first_workspace(self):
        ws = bpy.data.workspaces[0].name
        res = bpy.ops.aaa.switch_workspace(name=ws)
        self.assertEqual(res, {"FINISHED"})

    def test_switch_to_each_workspace(self):
        for ws in bpy.data.workspaces:
            with self.subTest(workspace=ws.name):
                res = bpy.ops.aaa.switch_workspace(name=ws.name)
                self.assertEqual(res, {"FINISHED"})

    def test_switch_to_nonexistent_workspace_returns_cancelled(self):
        with silence_warnings():
            res = bpy.ops.aaa.switch_workspace(name="NON_EXISTENT_WORKSPACE_NAME_123")
        self.assertEqual(res, {"CANCELLED"})


class TestOperatorExecution(unittest.TestCase):
    """AAA operators execute correctly in headless Object context."""

    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        _clean_scene()

    def test_mode_set_edit(self):
        res = bpy.ops.aaa.mode_set(mode="EDIT")
        self.assertIn("FINISHED", res)
        self.assertEqual(bpy.context.mode, "EDIT_MESH")

    def test_mode_set_returns_to_object(self):
        bpy.ops.aaa.mode_set(mode="EDIT")
        res = bpy.ops.aaa.mode_set(mode="OBJECT")
        self.assertIn("FINISHED", res)
        self.assertEqual(bpy.context.mode, "OBJECT")

    def test_reorder_modifiers_down(self):
        self.obj.modifiers.new("SubsurfMod", "SUBSURF")
        self.obj.modifiers.new("MirrorMod", "MIRROR")
        res = bpy.ops.aaa.reorder_modifiers(name="SubsurfMod", where="DOWN", index=0)
        self.assertEqual(res, {"FINISHED"})
        self.assertEqual(self.obj.modifiers[1].name, "SubsurfMod")

    def test_reorder_modifiers_up(self):
        self.obj.modifiers.new("SubsurfMod", "SUBSURF")
        self.obj.modifiers.new("MirrorMod", "MIRROR")
        res = bpy.ops.aaa.reorder_modifiers(name="MirrorMod", where="UP", index=1)
        self.assertEqual(res, {"FINISHED"})
        self.assertEqual(self.obj.modifiers[0].name, "MirrorMod")

    def test_add_material_new(self):
        res = bpy.ops.aaa.add_material(mode="NEW")
        self.assertEqual(res, {"FINISHED"})
        self.assertEqual(len(self.obj.data.materials), 1)

    def test_add_material_last(self):
        bpy.ops.aaa.add_material(mode="NEW")
        bpy.ops.mesh.primitive_cube_add(
            size=1, enter_editmode=False, location=(5, 0, 0)
        )
        self.obj2 = bpy.context.active_object
        res = bpy.ops.aaa.add_material(mode="LAST")
        self.assertEqual(res, {"FINISHED"})
        self.assertEqual(len(self.obj2.data.materials), 1)

    def test_roll_axis_x(self):
        res = bpy.ops.aaa.roll_axis(axis="X")
        self.assertEqual(res, {"FINISHED"})
        self.assertEqual(bpy.context.scene.axis_roll, "X")

    def test_roll_axis_y(self):
        bpy.ops.aaa.roll_axis(axis="Y")
        self.assertEqual(bpy.context.scene.axis_roll, "Y")

    def test_roll_axis_z(self):
        bpy.ops.aaa.roll_axis(axis="Z")
        self.assertEqual(bpy.context.scene.axis_roll, "Z")

    def test_std_tools(self):
        with silence_warnings():
            res = bpy.ops.aaa.std_tools(name="SPIN_TOOL")
        self.assertEqual(res, {"FINISHED"})

    def test_context_debugger(self):
        res = bpy.ops.aaa.test_context_debugger()
        self.assertEqual(res, {"FINISHED"})


class TestSaveOperations(unittest.TestCase):
    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        _clean_scene()

    def test_save_incremental_cancelled_no_filepath(self):
        with silence_warnings():
            res = bpy.ops.aaa.save_incremental()
        self.assertIn(res, [{"FINISHED"}, {"CANCELLED"}])

    def test_save_file_cancelled_no_filepath(self):
        with silence_warnings():
            res = bpy.ops.aaa.save_file()
        self.assertEqual(res, {"CANCELLED"})

    def test_resolve_incremented_path_basic(self):
        result = AAA_utils.resolve_incremented_path(r"C:\tmp\file_000.blend")
        self.assertEqual(result, r"C:\tmp\file_001.blend")

    def test_resolve_incremented_path_no_number(self):
        result = AAA_utils.resolve_incremented_path(r"C:\tmp\file.blend")
        self.assertEqual(result, r"C:\tmp\file_001.blend")


class TestToggleProp(unittest.TestCase):
    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        _clean_scene()

    def test_toggle_flips_false_to_true(self):
        bpy.context.scene.loop_frames = False
        res = bpy.ops.aaa.toggle_prop(prop="context.scene.loop_frames")
        self.assertEqual(res, {"FINISHED"})
        self.assertTrue(bpy.context.scene.loop_frames)
        bpy.context.scene.loop_frames = False

    def test_toggle_flips_true_to_false(self):
        bpy.context.scene.loop_frames = True
        bpy.ops.aaa.toggle_prop(prop="context.scene.loop_frames")
        self.assertFalse(bpy.context.scene.loop_frames)

    def test_double_toggle_is_identity(self):
        original = bpy.context.scene.loop_frames
        bpy.ops.aaa.toggle_prop(prop="context.scene.loop_frames")
        bpy.ops.aaa.toggle_prop(prop="context.scene.loop_frames")
        self.assertEqual(bpy.context.scene.loop_frames, original)

    def test_toggle_show_overlays(self):
        bpy.context.scene.show_overlays = False
        bpy.ops.aaa.toggle_prop(prop="context.scene.show_overlays")
        self.assertTrue(bpy.context.scene.show_overlays)
        bpy.context.scene.show_overlays = False


class TestSwitchCondition(unittest.TestCase):
    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        bpy.ops.aaa.switch_condition(cond="TRANSFORM")
        _clean_scene()

    def test_switch_to_sculpt(self):
        bpy.ops.aaa.switch_condition(cond="SCULPT")
        self.assertEqual(bpy.context.scene.conditions, "SCULPT")

    def test_switch_to_timeline(self):
        bpy.ops.aaa.switch_condition(cond="TIMELINE")
        self.assertEqual(bpy.context.scene.conditions, "TIMELINE")

    def test_switch_restores_transform(self):
        bpy.ops.aaa.switch_condition(cond="SCULPT")
        bpy.ops.aaa.switch_condition(cond="TRANSFORM")
        self.assertEqual(bpy.context.scene.conditions, "TRANSFORM")


class TestSwitchValue(unittest.TestCase):
    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        bpy.context.scene.conditions = "TRANSFORM"
        _clean_scene()

    def test_switch_value_sets_string_property(self):
        res = bpy.ops.aaa.switch_value(
            val_a="bpy.context.scene.conditions", val_b="TIMELINE"
        )
        self.assertEqual(res, {"FINISHED"})
        self.assertIsInstance(bpy.context.scene.conditions, str)


class TestReloadScripts(unittest.TestCase):
    def test_reload_scripts_execution(self):
        res = bpy.ops.aaa.reload_scripts()
        self.assertEqual(res, {"FINISHED"})

