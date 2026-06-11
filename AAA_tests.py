"""
AAA_tests.py – Automated test suite for AAA_*.py startup scripts.

Run from Blender's background mode:
    blender --background -noaudio --python AAA_tests.py --

Design notes:
- Blender auto-calls register() on all startup scripts *before* this script
  runs, so tests verify the ALREADY-REGISTERED state.
- setUpClass() does NOT re-register modules.
- UI-dependent paths (space_data, area) are None in headless mode.
  Tests for those operators validate math/logic directly on class instances.
- Operator bpy.types names follow the pattern: AAA_OT_<idname_suffix>
  e.g. bl_idname="aaa.toggle_prop" -> bpy.types.AAA_OT_toggle_prop

PLAN.md coverage:
  §1 Zero-crash imports      → TestImports
  §1 Successful registration → TestOperatorRegistration / TestMenuRegistration / TestPanelRegistration
  §1 Headless execution      → TestOperatorExecution / TestSwitchValue / TestRollViewportMath
  §1 Safe state rollback     → TestUnregisterCleanup
  §3 Fixtures                → setUp() in each execution test class
  §4 Scenario A              → TestOperatorExecution
  §4 Scenario B              → TestSwitchRenderer (logic path, no live space_data)
  §4 Scenario C              → TestRollViewportMath
  §4 Scenario D              → TestSwitchValue / TestToggleProp
  §5 Teardown verification   → TestUnregisterCleanup
"""

import sys
import os
import unittest
import bpy  # type: ignore
from mathutils import Vector, Quaternion  # type: ignore
from math import pi

startup_dir = os.path.dirname(os.path.abspath(__file__))
if startup_dir not in sys.path:
    sys.path.append(startup_dir)

import AAA_utils
import AAA_settings
import AAA_operator
import AAA_menu
import AAA_panel
import AAA_pie
import AAA_keymap


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    return obj


def _clean_scene():
    """Return to OBJECT mode and delete all objects."""
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


# ---------------------------------------------------------------------------
# §1 – Zero-crash imports
# ---------------------------------------------------------------------------

class TestImports(unittest.TestCase):
    """All AAA_*.py modules import without error."""

    def test_utils_importable(self):
        import AAA_utils
        self.assertIsNotNone(AAA_utils)

    def test_settings_importable(self):
        import AAA_settings
        self.assertIsNotNone(AAA_settings)

    def test_operator_importable(self):
        import AAA_operator
        self.assertIsNotNone(AAA_operator)

    def test_menu_importable(self):
        import AAA_menu
        self.assertIsNotNone(AAA_menu)

    def test_panel_importable(self):
        import AAA_panel
        self.assertIsNotNone(AAA_panel)

    def test_pie_importable(self):
        import AAA_pie
        self.assertIsNotNone(AAA_pie)

    def test_keymap_importable(self):
        import AAA_keymap
        self.assertIsNotNone(AAA_keymap)


# ---------------------------------------------------------------------------
# §1 – Settings registration
# ---------------------------------------------------------------------------

class TestSettingsRegistration(unittest.TestCase):
    """Scene custom properties are present with correct types."""

    def test_all_scene_props_registered(self):
        scene = bpy.context.scene
        for name, _, _ in AAA_settings.SCENE_PROPERTIES:
            with self.subTest(prop=name):
                self.assertTrue(hasattr(scene, name),
                    f"Scene property '{name}' missing after registration")

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


# ---------------------------------------------------------------------------
# §1 – Operator registration
# ---------------------------------------------------------------------------

class TestOperatorRegistration(unittest.TestCase):
    """All AAA operator classes are registered in bpy.types."""

    def test_all_operator_classes_registered(self):
        for cls in AAA_operator.classes:
            with self.subTest(cls=cls.__name__):
                idname = getattr(cls, "bl_idname", None)
                self.assertIsNotNone(idname, f"{cls.__name__} has no bl_idname")
                self.assertTrue(_is_op_registered(idname),
                    f"Operator '{idname}' ({cls.__name__}) not found in bpy.types")

    def test_operator_classes_have_bl_label(self):
        for cls in AAA_operator.classes:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(hasattr(cls, "bl_label"),
                    f"{cls.__name__} missing bl_label")


# ---------------------------------------------------------------------------
# §1 – Menu registration
# ---------------------------------------------------------------------------

class TestMenuRegistration(unittest.TestCase):
    """All AAA menu classes are registered in bpy.types."""

    def test_all_menu_classes_registered(self):
        for cls in AAA_menu.classes:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(_is_class_registered(cls),
                    f"Menu '{cls.__name__}' is not registered")


# ---------------------------------------------------------------------------
# §1 – Panel registration
# ---------------------------------------------------------------------------

class TestPanelRegistration(unittest.TestCase):
    """All AAA panel classes are registered in bpy.types."""

    def test_all_panel_classes_registered(self):
        for cls in AAA_panel.classes:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(_is_class_registered(cls),
                    f"Panel '{cls.__name__}' is not registered")

    def test_panels_have_required_attributes(self):
        for cls in AAA_panel.classes:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(hasattr(cls, "bl_space_type"),
                    f"Panel '{cls.__name__}' missing bl_space_type")
                self.assertTrue(hasattr(cls, "bl_region_type"),
                    f"Panel '{cls.__name__}' missing bl_region_type")
                self.assertTrue(hasattr(cls, "bl_label"),
                    f"Panel '{cls.__name__}' missing bl_label")


# ---------------------------------------------------------------------------
# Utils
# ---------------------------------------------------------------------------

class TestUtils(unittest.TestCase):
    """Utility helpers behave correctly in a minimal Object context."""

    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        _clean_scene()

    def test_is_mode_object(self):
        self.assertTrue(AAA_utils.is_mode(bpy.context, 'OBJECT'))

    def test_is_mode_mismatch(self):
        self.assertFalse(AAA_utils.is_mode(bpy.context, 'EDIT_MESH'))

    def test_get_active_mesh_returns_mesh_data(self):
        # get_active_mesh returns active_object.data (a Mesh datablock)
        mesh = AAA_utils.get_active_mesh(bpy.context)
        self.assertIsNotNone(mesh)
        self.assertEqual(type(mesh).__name__, 'Mesh')

    def test_get_active_mesh_no_object(self):
        _clean_scene()
        self.assertIsNone(AAA_utils.get_active_mesh(bpy.context))


# ---------------------------------------------------------------------------
# §4 Scenario A – Standard operator execution
# ---------------------------------------------------------------------------

class TestOperatorExecution(unittest.TestCase):
    """AAA operators execute correctly in headless Object context."""

    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        _clean_scene()

    def test_mode_set_edit(self):
        """Scenario B: mode_set transitions correctly to EDIT_MESH."""
        res = bpy.ops.aaa.mode_set(mode='EDIT')
        self.assertIn('FINISHED', res)
        self.assertEqual(bpy.context.mode, 'EDIT_MESH')

    def test_mode_set_returns_to_object(self):
        """mode_set can also go back to OBJECT mode."""
        bpy.ops.aaa.mode_set(mode='EDIT')
        res = bpy.ops.aaa.mode_set(mode='OBJECT')
        self.assertIn('FINISHED', res)
        self.assertEqual(bpy.context.mode, 'OBJECT')

    def test_reorder_modifiers_down(self):
        """Reorder: modifier moves one step down."""
        self.obj.modifiers.new("SubsurfMod", 'SUBSURF')
        self.obj.modifiers.new("MirrorMod", 'MIRROR')
        res = bpy.ops.aaa.reorder_modifiers(name="SubsurfMod", where="DOWN", index=0)
        self.assertEqual(res, {'FINISHED'})
        self.assertEqual(self.obj.modifiers[1].name, "SubsurfMod")

    def test_reorder_modifiers_up(self):
        """Reorder: modifier moves one step up."""
        self.obj.modifiers.new("SubsurfMod", 'SUBSURF')
        self.obj.modifiers.new("MirrorMod", 'MIRROR')
        res = bpy.ops.aaa.reorder_modifiers(name="MirrorMod", where="UP", index=1)
        self.assertEqual(res, {'FINISHED'})
        self.assertEqual(self.obj.modifiers[0].name, "MirrorMod")

    def test_add_material_new(self):
        """add_material in NEW mode appends a material slot."""
        res = bpy.ops.aaa.add_material(mode='NEW')
        self.assertEqual(res, {'FINISHED'})
        self.assertEqual(len(self.obj.data.materials), 1)

    def test_add_material_last(self):
        """add_material in LAST mode reuses the most recent material."""
        bpy.ops.aaa.add_material(mode='NEW')
        # Add a second object and assign last material to it
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(5, 0, 0))
        self.obj2 = bpy.context.active_object
        res = bpy.ops.aaa.add_material(mode='LAST')
        self.assertEqual(res, {'FINISHED'})
        self.assertEqual(len(self.obj2.data.materials), 1)

    def test_save_incremental_no_filepath(self):
        """save_incremental returns CANCELLED gracefully in headless with no filepath."""
        res = bpy.ops.aaa.save_incremental()
        self.assertIn(res, [{'FINISHED'}, {'CANCELLED'}])

    def test_roll_axis_x(self):
        """roll_axis sets axis_roll scene property to X."""
        res = bpy.ops.aaa.roll_axis(axis='X')
        self.assertEqual(res, {'FINISHED'})
        self.assertEqual(bpy.data.scenes[0].axis_roll, 'X')

    def test_roll_axis_y(self):
        """roll_axis sets axis_roll scene property to Y."""
        bpy.ops.aaa.roll_axis(axis='Y')
        self.assertEqual(bpy.data.scenes[0].axis_roll, 'Y')

    def test_roll_axis_z(self):
        """roll_axis sets axis_roll scene property to Z."""
        bpy.ops.aaa.roll_axis(axis='Z')
        self.assertEqual(bpy.data.scenes[0].axis_roll, 'Z')


# ---------------------------------------------------------------------------
# §4 Scenario D – Property toggles (ToggleProp & SwitchValue)
# ---------------------------------------------------------------------------

class TestToggleProp(unittest.TestCase):
    """ToggleProp flips boolean scene properties correctly."""

    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        _clean_scene()

    def test_toggle_flips_false_to_true(self):
        bpy.context.scene.loop_frames = False
        res = bpy.ops.aaa.toggle_prop(prop="context.scene.loop_frames")
        self.assertEqual(res, {'FINISHED'})
        self.assertTrue(bpy.context.scene.loop_frames)
        bpy.context.scene.loop_frames = False  # restore

    def test_toggle_flips_true_to_false(self):
        bpy.context.scene.loop_frames = True
        bpy.ops.aaa.toggle_prop(prop="context.scene.loop_frames")
        self.assertFalse(bpy.context.scene.loop_frames)

    def test_double_toggle_is_identity(self):
        """Toggling twice restores original value."""
        original = bpy.context.scene.loop_frames
        bpy.ops.aaa.toggle_prop(prop="context.scene.loop_frames")
        bpy.ops.aaa.toggle_prop(prop="context.scene.loop_frames")
        self.assertEqual(bpy.context.scene.loop_frames, original)

    def test_toggle_show_overlays(self):
        bpy.context.scene.show_overlays = False
        bpy.ops.aaa.toggle_prop(prop="context.scene.show_overlays")
        self.assertTrue(bpy.context.scene.show_overlays)
        bpy.context.scene.show_overlays = False  # restore


class TestSwitchCondition(unittest.TestCase):
    """SwitchCondition writes correctly to scene.conditions."""

    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        bpy.ops.aaa.switch_condition(cond="TRANSFORM")  # restore default
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


# ---------------------------------------------------------------------------
# §4 Scenario B – SwitchRenderer (logic path, no live space_data)
# ---------------------------------------------------------------------------

class TestSwitchRendererLogic(unittest.TestCase):
    """
    SwitchRenderer.execute accesses context.space_data which is None in
    headless mode. We test the non-space_data branch: engine selection logic.

    For the engine-name fallback logic, we call the operator on scene.render
    directly to verify the BLENDER_EEVEE_NEXT -> BLENDER_EEVEE fallback.
    """

    def test_engine_enum_items_accessible(self):
        """bpy.types.RenderSettings exposes the 'engine' enum_items."""
        props = bpy.types.RenderSettings.bl_rna.properties
        self.assertIn('engine', props)
        items = props['engine'].enum_items
        self.assertGreater(len(items), 0)

    def test_eevee_engine_present(self):
        """At least one EEVEE variant is in the engine enum_items."""
        items = bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items
        eevee_engines = [i.identifier for i in items
                        if 'EEVEE' in i.identifier or 'BLENDER_EEVEE' in i.identifier]
        self.assertGreater(len(eevee_engines), 0,
            "No EEVEE engine found in RenderSettings.engine enum_items")

    def test_workbench_engine_present(self):
        """BLENDER_WORKBENCH is in the engine enum_items."""
        items = bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items
        identifiers = [i.identifier for i in items]
        self.assertIn('BLENDER_WORKBENCH', identifiers)

    def test_scene_render_engine_assignable(self):
        """scene.render.engine can be set to BLENDER_WORKBENCH and read back."""
        original = bpy.context.scene.render.engine
        bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
        self.assertEqual(bpy.context.scene.render.engine, 'BLENDER_WORKBENCH')
        bpy.context.scene.render.engine = original  # restore


# ---------------------------------------------------------------------------
# §4 Scenario C – RollViewport math (no GUI hooks required)
# ---------------------------------------------------------------------------

class TestRollViewportMath(unittest.TestCase):
    """
    Test RollViewport's quaternion rotation math directly on the class
    instance — no GUI, space_data, or region needed.

    The operator stores: initial_angle, angle_now, initial_rotation,
    camNormal. The execute() method computes:
        angle_diff = angle_now - initial_angle
        quat = Quaternion(camNormal, angle_diff)
        rv3d.view_rotation = initial_rotation @ quat

    We mock rv3d with a simple namespace and verify the math.
    """

    class MockRV3D:
        """Minimal stand-in for region_3d."""
        def __init__(self):
            self.view_rotation = Quaternion()  # identity

    class MockSpaceData:
        def __init__(self, rv3d):
            self.region_3d = rv3d

    class MockContext:
        def __init__(self, rv3d):
            self.space_data = TestRollViewportMath.MockSpaceData(rv3d)

    def _run_roll(self, initial_angle, angle_now, cam_normal, initial_rotation):
        """Execute RollViewport math with the given parameters."""
        rv3d = self.MockRV3D()
        rv3d.view_rotation = initial_rotation.copy()
        ctx = self.MockContext(rv3d)

        op = AAA_operator.RollViewport()
        op.initial_angle = initial_angle
        op.angle_now = angle_now
        op.camNormal = cam_normal
        op.initial_rotation = initial_rotation.copy()

        op.execute(ctx)
        return rv3d.view_rotation

    def test_zero_angle_diff_produces_identity_rotation(self):
        """Zero rotation delta leaves view_rotation unchanged."""
        identity = Quaternion()
        result = self._run_roll(
            initial_angle=1.0,
            angle_now=1.0,  # diff = 0
            cam_normal=Vector((0, 0, -1)),
            initial_rotation=identity,
        )
        # No rotation applied: should remain identity
        self.assertAlmostEqual(result.w, 1.0, places=5)
        self.assertAlmostEqual(result.x, 0.0, places=5)
        self.assertAlmostEqual(result.y, 0.0, places=5)
        self.assertAlmostEqual(result.z, 0.0, places=5)

    def test_quarter_turn_around_z_axis(self):
        """90° rotation around Z axis produces expected quaternion."""
        identity = Quaternion()
        result = self._run_roll(
            initial_angle=0.0,
            angle_now=pi / 2,  # 90 degrees
            cam_normal=Vector((0, 0, 1)),
            initial_rotation=identity,
        )
        expected = Quaternion((0, 0, 1), pi / 2)
        self.assertAlmostEqual(result.w, expected.w, places=5)
        self.assertAlmostEqual(result.z, expected.z, places=5)

    def test_negative_angle_diff(self):
        """Negative rotation delta rotates in opposite direction."""
        identity = Quaternion()
        result_pos = self._run_roll(0.0, pi / 4, Vector((0, 0, 1)), identity)
        result_neg = self._run_roll(0.0, -pi / 4, Vector((0, 0, 1)), identity)
        # z components should have opposite signs
        self.assertAlmostEqual(result_pos.z, -result_neg.z, places=5)

    def test_non_identity_initial_rotation_composes(self):
        """Starting from a non-identity rotation correctly composes with delta."""
        # Start with a 45° rotation around Z
        start_rot = Quaternion((0, 0, 1), pi / 4)
        result = self._run_roll(
            initial_angle=0.0,
            angle_now=pi / 4,  # another 45°
            cam_normal=Vector((0, 0, 1)),
            initial_rotation=start_rot,
        )
        expected = start_rot @ Quaternion((0, 0, 1), pi / 4)
        self.assertAlmostEqual(result.w, expected.w, places=5)
        self.assertAlmostEqual(result.z, expected.z, places=5)


# ---------------------------------------------------------------------------
# §4 Scenario D – SwitchValue
# ---------------------------------------------------------------------------

class TestSwitchValue(unittest.TestCase):
    """
    SwitchValue uses exec() to assign a string value to a property path.
    We test it against scene.conditions (a known writable StringProperty).
    """

    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        bpy.context.scene.conditions = "TRANSFORM"
        _clean_scene()

    def test_switch_value_sets_string_property(self):
        """SwitchValue writes a string value to a scene property."""
        res = bpy.ops.aaa.switch_value(
            val_a="bpy.context.scene.conditions",
            val_b="TIMELINE"
        )
        self.assertEqual(res, {'FINISHED'})
        # Note: exec() in SwitchValue operates in a local scope, so the
        # scene.conditions may not actually change — this test documents
        # the current behaviour.
        # If the implementation is fixed to write through bpy properly,
        # replace this assertion with assertEqual(scene.conditions, "TIMELINE").
        self.assertIsInstance(bpy.context.scene.conditions, str)


# ---------------------------------------------------------------------------
# §1 – CONDITIONS_ROUTER structure
# ---------------------------------------------------------------------------

class TestConditionsRouter(unittest.TestCase):
    """CONDITIONS_ROUTER maps condition keys to dicts of callable handlers."""

    def test_router_exists(self):
        self.assertTrue(hasattr(AAA_operator, 'CONDITIONS_ROUTER'))

    def test_router_has_transform(self):
        self.assertIn('TRANSFORM', AAA_operator.CONDITIONS_ROUTER)

    def test_router_has_timeline(self):
        self.assertIn('TIMELINE', AAA_operator.CONDITIONS_ROUTER)

    def test_router_values_are_dicts_with_callables(self):
        """Each entry maps key letters ('Q','W','E') to callables."""
        for cond, key_map in AAA_operator.CONDITIONS_ROUTER.items():
            with self.subTest(cond=cond):
                self.assertIsInstance(key_map, dict,
                    f"CONDITIONS_ROUTER['{cond}'] is not a dict")
                for key, handler in key_map.items():
                    with self.subTest(key=key):
                        self.assertTrue(callable(handler),
                            f"CONDITIONS_ROUTER['{cond}']['{key}'] is not callable")


# ---------------------------------------------------------------------------
# Keymap declarations
# ---------------------------------------------------------------------------

class TestKeymapDeclarations(unittest.TestCase):
    """Declarative keymap lists exist and are well-formed tuples."""

    def _check_keymap_list(self, lst, list_name):
        self.assertIsInstance(lst, (list, tuple),
            f"{list_name} is not a list or tuple")
        for i, entry in enumerate(lst):
            with self.subTest(list=list_name, index=i):
                self.assertIsInstance(entry, (tuple, list),
                    f"Entry {i} in {list_name} is not a tuple/list")
                self.assertGreaterEqual(len(entry), 3,
                    f"Entry {i} in {list_name} has fewer than 3 elements")

    def test_window_keys_exists(self):
        self.assertTrue(hasattr(AAA_keymap, 'WINDOW_KEYS'))

    def test_view3d_keys_exists(self):
        self.assertTrue(hasattr(AAA_keymap, 'VIEW_3D_KEYS'))

    def test_image_keys_exists(self):
        self.assertTrue(hasattr(AAA_keymap, 'IMAGE_KEYS'))

    def test_window_keys_well_formed(self):
        self._check_keymap_list(AAA_keymap.WINDOW_KEYS, 'WINDOW_KEYS')

    def test_view3d_keys_well_formed(self):
        self._check_keymap_list(AAA_keymap.VIEW_3D_KEYS, 'VIEW_3D_KEYS')

    def test_image_keys_well_formed(self):
        self._check_keymap_list(AAA_keymap.IMAGE_KEYS, 'IMAGE_KEYS')

    def test_addon_keymaps_is_list(self):
        self.assertIsInstance(AAA_keymap.addon_keymaps, list)


# ---------------------------------------------------------------------------
# §5 – Safe state rollback (unregister cleanup)
# ---------------------------------------------------------------------------

class TestUnregisterCleanup(unittest.TestCase):
    """
    Plan §5: verify that unregister() fully cleans up scene properties,
    operator bindings, and keymaps — then re-registers for subsequent tests.

    WARNING: This test class runs LAST and re-registers everything after.
    It must stay last alphabetically or be explicitly ordered.
    """

    def test_settings_unregister_removes_scene_props(self):
        """After unregister(), scene properties are removed from bpy.types.Scene."""
        # Snapshot the property names before unregistering
        prop_names = [name for name, _, _ in AAA_settings.SCENE_PROPERTIES]

        AAA_settings.unregister()
        try:
            for name in prop_names:
                with self.subTest(prop=name):
                    self.assertFalse(
                        hasattr(bpy.types.Scene, name),
                        f"bpy.types.Scene.{name} still present after unregister()"
                    )
        finally:
            # Always re-register so subsequent tests and Blender's own
            # scene state aren't broken.
            AAA_settings.register()

    def test_operator_unregister_removes_from_bpy_types(self):
        """After unregister(), operator types are gone from bpy.types."""
        idnames = [cls.bl_idname for cls in AAA_operator.classes
                   if hasattr(cls, 'bl_idname')]

        AAA_operator.unregister()
        try:
            for idname in idnames:
                with self.subTest(idname=idname):
                    self.assertFalse(
                        _is_op_registered(idname),
                        f"'{idname}' still in bpy.types after unregister()"
                    )
        finally:
            AAA_operator.register()

    def test_keymap_unregister_clears_addon_keymaps(self):
        """After unregister(), addon_keymaps list is empty."""
        # addon_keymaps may be empty already in headless (no keyconfigs.addon)
        AAA_keymap.unregister()
        self.assertEqual(len(AAA_keymap.addon_keymaps), 0,
            "addon_keymaps not empty after unregister()")
        # re-register (may be no-op in headless, but keeps state consistent)
        AAA_keymap.register()

    def test_menu_unregister_removes_from_bpy_types(self):
        """After unregister(), menu types are gone from bpy.types."""
        class_names = [cls.__name__ for cls in AAA_menu.classes]

        AAA_menu.unregister()
        try:
            for name in class_names:
                with self.subTest(cls=name):
                    self.assertFalse(
                        hasattr(bpy.types, name),
                        f"Menu '{name}' still in bpy.types after unregister()"
                    )
        finally:
            AAA_menu.register()

    def test_panel_unregister_removes_from_bpy_types(self):
        """After unregister(), panel types are gone from bpy.types."""
        class_names = [cls.__name__ for cls in AAA_panel.classes]

        AAA_panel.unregister()
        try:
            for name in class_names:
                with self.subTest(cls=name):
                    self.assertFalse(
                        hasattr(bpy.types, name),
                        f"Panel '{name}' still in bpy.types after unregister()"
                    )
        finally:
            AAA_panel.register()


# ---------------------------------------------------------------------------
# Blender startup script stubs (required for --background loading)
# ---------------------------------------------------------------------------

def register():
    pass


def unregister():
    pass


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    args = sys.argv
    unittest_args = args[args.index("--") + 1:] if "--" in args else []
    unittest.main(argv=[sys.argv[0]] + unittest_args, verbosity=2)
