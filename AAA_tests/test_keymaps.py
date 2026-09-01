import unittest
import AAA_keymap

class TestKeymapDeclarations(unittest.TestCase):
    def _check_keymap_list(self, lst, list_name):
        self.assertIsInstance(lst, (list, tuple), f"{list_name} is not a list or tuple")
        for i, entry in enumerate(lst):
            with self.subTest(list=list_name, index=i):
                self.assertIsInstance(
                    entry,
                    (tuple, list),
                    f"Entry {i} in {list_name} is not a tuple/list",
                )
                self.assertGreaterEqual(
                    len(entry), 3, f"Entry {i} in {list_name} has fewer than 3 elements"
                )

    def test_window_keys_exists(self):
        self.assertTrue(hasattr(AAA_keymap, "WINDOW_KEYS"))

    def test_view3d_keys_exists(self):
        self.assertTrue(hasattr(AAA_keymap, "VIEW_3D_KEYS"))

    def test_image_keys_exists(self):
        self.assertTrue(hasattr(AAA_keymap, "IMAGE_KEYS"))

    def test_image_paint_keys_exists(self):
        self.assertTrue(hasattr(AAA_keymap, "IMAGE_PAINT_KEYS"))

    def test_vertex_paint_keys_exists(self):
        self.assertTrue(hasattr(AAA_keymap, "VERTEX_PAINT_KEYS"))

    def test_sculpt_keys_exists(self):
        self.assertTrue(hasattr(AAA_keymap, "SCULPT_KEYS"))

    def test_window_keys_well_formed(self):
        self._check_keymap_list(AAA_keymap.WINDOW_KEYS, "WINDOW_KEYS")

    def test_view3d_keys_well_formed(self):
        self._check_keymap_list(AAA_keymap.VIEW_3D_KEYS, "VIEW_3D_KEYS")

    def test_image_keys_well_formed(self):
        self._check_keymap_list(AAA_keymap.IMAGE_KEYS, "IMAGE_KEYS")

    def test_image_paint_keys_well_formed(self):
        self._check_keymap_list(AAA_keymap.IMAGE_PAINT_KEYS, "IMAGE_PAINT_KEYS")

    def test_vertex_paint_keys_well_formed(self):
        self._check_keymap_list(AAA_keymap.VERTEX_PAINT_KEYS, "VERTEX_PAINT_KEYS")

    def test_sculpt_keys_well_formed(self):
        self._check_keymap_list(AAA_keymap.SCULPT_KEYS, "SCULPT_KEYS")

    def test_addon_keymaps_is_list(self):
        self.assertIsInstance(AAA_keymap.addon_keymaps, list)
