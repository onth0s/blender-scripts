import unittest

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
