import unittest
import bpy  # type: ignore
import AAA_utils
from .helpers import _make_mesh_object, _clean_scene

class TestUtils(unittest.TestCase):
    """Utility helpers behave correctly in a minimal Object context."""

    def setUp(self):
        self.obj = _make_mesh_object()

    def tearDown(self):
        _clean_scene()

    def test_is_mode_object(self):
        self.assertTrue(AAA_utils.is_mode(bpy.context, "OBJECT"))

    def test_is_mode_mismatch(self):
        self.assertFalse(AAA_utils.is_mode(bpy.context, "EDIT_MESH"))

    def test_get_active_mesh_returns_mesh_data(self):
        mesh = AAA_utils.get_active_mesh(bpy.context)
        self.assertIsNotNone(mesh)
        self.assertEqual(type(mesh).__name__, "Mesh")

    def test_get_active_mesh_no_object(self):
        _clean_scene()
        self.assertIsNone(AAA_utils.get_active_mesh(bpy.context))
