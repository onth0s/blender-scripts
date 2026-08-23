# Reference

- [Blender Python API Documentation](https://docs.blender.org/api/current/index.html) — Always refer to this for the most up-to-date API reference when writing or modifying scripts in this project.

# Intent

These scripts are ad hoc automations and shortcuts tailored to the specific workflow of a single user. They are not intended to be shipped, packaged, or comply with arbitrary conventions. Pragmatism over purity.

# Exceptions

- **Do not refactor or remove** the `exec()` calls in `SWITCH_VALUE` (`AAA_operator.py`) and `ToggleProp` (`AAA_operator.py`) — they are known and accepted (even if not ideal).

- **Do not remove or change** empty operators or empty menu calls (e.g. `.name = ""` or empty arguments) in `AAA_pie.py` — they are deliberate layout placeholders/anchors to maintain pie menu direction balance.

# Namespace Rules

- **Use the `AAA_` prefix** (e.g. `AAA_PT_` for panels, `AAA_OT_` for operators, `AAA_MT_` for menus) on custom classes and registered types where there is a likelihood of namespace conflicts with Blender's built-in types.

# Keymap Rules

- **Check for conflicts**: When adding new keymap items or changing key bindings, always inspect existing keymaps across Blender's default, addon, and user key configurations to ensure the new shortcut does not conflict with existing workflows or built-in tools.


