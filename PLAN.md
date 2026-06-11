# AAA Addon — Full Refactoring Strategy

## Scope

Only files matching `AAA_*.py` are in scope. There are 7 files totaling ~2050 lines:

| File | Lines | Purpose |
|------|-------|---------|
| `AAA_utils.py` | 65 | Constants for modes & object types |
| `AAA_settings.py` | 40 | Scene-level custom properties |
| `AAA_operator.py` | 645 | 21 operator classes |
| `AAA_panel.py` | 329 | 7 panel classes |
| `AAA_menu.py` | 635 | 24 menu classes |
| `AAA_pie.py` | 261 | 6 pie menu classes |
| `AAA_keymap.py` | 80 | Keymap registration |

---

## Cross-Cutting Issues Identified

1. **Star-import pollution** — `from AAA_utils import *`, `from mathutils import *`, `from math import *`, `from bpy.props import *` used in 5 of 7 files, making dependencies invisible.
2. **Monolithic files** — `AAA_operator.py` (21 classes), `AAA_menu.py` (24 classes), `AAA_panel.py` (7 panels) each mix unrelated concerns.
3. **Custom Scene properties scattered** — 10 properties directly monkey-patched onto `bpy.types.Scene` without a PropertyGroup.
4. **`exec()` calls** — `SWITCH_VALUE` and `ToggleProp` use `exec()`. **Per `AGENTS.md`: do NOT refactor or remove these.**
5. **Dead / commented code** — large blocks in `AAA_panel.py:49-71`, `AAA_panel.py:292-301`, `AAA_operator.py:25-33`, commented-out method call `SaveIncremental:72`.
6. **`print()` debugging** — `ReorderModifiers:349-350`, `TestContextDebugger:575+`. Should be `self.report()` or removed.
7. **Missing docstrings / empty labels** — `SWITCH_CONDITION`, `SWITCH_VALUE`, `RollAxis`, `PIE_MT_ANIMATION` placeholder entries, `VIEW3D_PT_FRAME_RATE.bl_label = ""`.
8. **Global mutable state** — `addon_keymaps` list in `AAA_keymap.py`, `cavity_state` string in `VIEW3D_MT_SHADING_OPTIONS_CAVITY`.
9. **Empty stubs** — `AAA_utils.register/unregister` are `pass`.
10. **Duplicated patterns** — `MN = "wm.call_menu"`, `PT = "wm.call_panel"` re-assigned in every pie/menu `draw()`.
11. **Inconsistent naming** — `SWITCH_CONDITION` vs `SaveFile` vs `GLOBAL_Q`.
12. **Missing error handling** — operators assume `context.active_object`, `context.object`, etc. are never `None`.
13. **`bpy.context` vs `context`** — `AAA_panel.py:26` uses `bpy.context.active_object` instead of the passed `context`.
14. **No Python type annotations** anywhere.
15. **Near-duplicate menus** — `VIEW3D_MT_VIEW_ALIGN` and `VIEW3D_MT_VIEW_VIEW` differ only by `align_active=True`.

---

## Phases (execute sequentially)

### Phase 1 — Foundation: Constants, Property Groups & Common Utilities

**Goal**: Establish shared infrastructure that all other phases depend on.

1.1 **Replace `AAA_utils.py` star-imports with explicit named imports.**  
  - Convert `from AAA_utils import *` → `from AAA_utils import OBJ, MHE, MHS, ...` in every file.
  - Better: create a namespaced constants class or enum (e.g., `Mode.OBJECT`, `Mode.EDIT_MESH`).

1.2 **Create `AAA_properties.py` with a `class AAA_SceneProperties(PropertyGroup)`.**  
  - Move all 10 properties from `AAA_settings.py` into the group.
  - Assign via `bpy.types.Scene.aaa = PointerProperty(type=AAA_SceneProperties)`.
  - Update all references from `context.scene.conditions` → `context.scene.aaa.conditions`, etc.
  - Keep `AAA_settings.py` as a thin re-export shim for backward compatibility during transition.

1.3 **Extract shared UI-string constants.**  
  - Define `WM_CALL_MENU = "wm.call_menu"`, `WM_CALL_PANEL = "wm.call_panel"` in one place.

1.4 **Stub cleanup.**  
  - Remove empty `register/unregister` from `AAA_utils.py`.

**Files touched**: `AAA_utils.py`, `AAA_settings.py`, new `AAA_properties.py`, all files that import from `AAA_utils`.

---

### Phase 2 — Operator Decoupling

**Goal**: Split `AAA_operator.py` (21 classes) into domain-specific modules.

2.1 **Create `AAA_op_file.py`** — file operations: `SaveFile`, `SaveIncremental`.

2.2 **Create `AAA_op_viewport.py`** — viewport controls: `RollViewport`, `RollAxis`, `ToggleOverlays`, `SwitchRenderer`, `ModeSet`, `SwitchWorkspace`, `STDTools`.

2.3 **Create `AAA_op_edit.py`** — editing utilities: `ReorderModifiers`, `AddMaterial`.

2.4 **Create `AAA_op_global.py`** — global condition/key operators: `SWITCH_CONDITION`, `SWITCH_VALUE`, `GLOBAL_Q`, `GLOBAL_W`, `GLOBAL_E`, `ToggleProp`.

2.5 **Create `AAA_op_debug.py`** — debugging: `TestOperator`, `TestContextDebugger`.

2.6 **Shim `AAA_operator.py`** — re-export all classes from submodules so existing cross-references (`aaa.switch_workspace`, etc.) continue to work.

**Files touched**: `AAA_operator.py` (becomes shim), 5 new files.

---

### Phase 3 — UI Decoupling (Menus & Panels)

**Goal**: Split monolithic UI files into domain modules.

3.1 **Split `AAA_menu.py` → domain files:**
  - `AAA_menu_workspace.py` — `VIEW3D_MT_WORKSPACE`, `VIEW3D_MT_MODE`
  - `AAA_menu_view.py` — `VIEW3D_MT_VIEW`, `VIEW3D_MT_VIEW_ALIGN`, `VIEW3D_MT_VIEW_VIEW`, `VIEW3D_MT_VIEW_AXIS_ROLL`
  - `AAA_menu_display.py` — `VIEW3D_MT_VIEWPORT_DISPLAY`, `VIEW3D_MT_SHADING_OPTIONS`, `VIEW3D_MT_SHADING_OPTIONS_CAVITY`, `VIEW3D_MT_RENDERER`, `VIEW3D_MT_SHADING_PIE` (moved from `AAA_pie.py`)
  - `AAA_menu_select.py` — `VIEW3D_MT_SELECT`, `VIEW3D_MT_SELECT_MODE`
  - `AAA_menu_tools.py` — `VIEW3D_MT_TRANSFORM_GIZMO`, `VIEW3D_MT_CURSOR_POSITION`, `VIEW3D_MT_PIVOT_POINT`, `VIEW3D_MT_STD_TOOLS`, `VIEW3D_MT_MHE_MODE`
  - `AAA_menu_edit.py` — `VIEW3D_MT_MODIFIERS`, `VIEW3D_MT_APPLY_CLEAR`, `VIEW3D_MT_APPLY`, `VIEW3D_MT_CLEAR`, `VIEW3D_MT_FACE_SETS`
  - `AAA_menu_animation.py` — `VIEW3D_MT_ANIMATION_PLAYBACK`, `VIEW3D_MT_ABOUT_FRAMES`

3.2 **Fix the `VIEW3D_MT_VIEW_ALIGN` / `VIEW3D_MT_VIEW_VIEW` duplication.**  
  - Both are nearly identical; make one accept a `use_align_active` parameter or merge into a single menu.

3.3 **Split `AAA_panel.py` → domain files:**
  - `AAA_panel_modifiers.py` — `VIEW3D_PT_manage_modifiers`
  - `AAA_panel_viewport.py` — `VIEW3D_PT_proportional_edit_2`, `VIEW3D_PT_frame_range`, `VIEW3D_PT_object_color`, `VIEW3D_PT_lighting`, `VIEW3D_PT_background_color`, `VIEW3D_PT_FRAME_RATE`

3.4 **Shim both `AAA_menu.py` and `AAA_panel.py`** to re-export from submodules.

**Files touched**: `AAA_menu.py`, `AAA_panel.py`, `AAA_pie.py` (shading pie moves), ~10 new files.

---

### Phase 4 — Keymap & Pie Menu Refinement

**Goal**: Clean up keymap registration and pie menus.

4.1 **Refactor `AAA_keymap.py`:**
  - Replace global `addon_keymaps` list with a `KeymapManager` class that encapsulates add/remove logic.
  - Split `global_keymap()` into named registration methods: `register_global()`, `register_3dview()`, `register_overrides()`, `register_image_editor()`.
  - Add error handling in `unregister()` so one failure doesn't leak subsequent keymaps.

4.2 **Refactor `AAA_pie.py`:**
  - Remove empty placeholder operators in `PIE_MT_ANIMATION` (operators with `text=""` and `name=""`).
  - Replace global `cavity_state` variable in `VIEW3D_MT_SHADING_OPTIONS_CAVITY` with a local or inline expression.
  - Move `VIEW3D_MT_SHADING_PIE` to the display-menu domain module (Phase 3).

**Files touched**: `AAA_keymap.py`, `AAA_pie.py`.

---

### Phase 5 — Naming Convention & API Consistency Pass

**Goal**: Consistent naming, type annotations, docstrings, dead-code removal.

5.1 **Rename inconsistent classes:**
  - `SWITCH_CONDITION` → `SwitchCondition`
  - `SWITCH_VALUE` → `SwitchValue` (but keep `exec()` per AGENTS.md)
  - `GLOBAL_Q` → `GlobalQ`, `GLOBAL_W` → `GlobalW`, `GLOBAL_E` → `GlobalE`

5.2 **Add Python type annotations** to all method signatures and class attributes.

5.3 **Add concise docstrings** to all operators, panels, and menus (1-2 lines).

5.4 **Remove dead code:**
  - Commented-out blocks in `AAA_panel.py:49-71`, `AAA_panel.py:292-301`, `AAA_operator.py:25-33`
  - `SaveIncremental.add_path_to_recent_files` (dead, never called)
  - `RollViewport.toDegrees` / `RollViewport.to360Degrees` (dead methods with bugs)
  - Commented-out lines in `VIEW3D_PT_FRAME_RATE.draw()`

5.5 **Remove `print()` debugging statements** in `ReorderModifiers` and `TestContextDebugger` or convert to `self.report()`.

5.6 **Fix `AAA_panel.py:26`** — use `context.active_object` instead of `bpy.context.active_object`.

5.7 **Remove the stale API enum comment block** at the top of `AAA_pie.py:6-22`.

**Files touched**: All 7+ files.

---

### Phase 6 — Error Handling & Edge Cases

**Goal**: Make operators robust against missing context, None objects, and other edge cases.

6.1 **Add `None` guards** for `context.active_object`, `context.object`, `context.space_data`, etc. in:
  - All panels (especially `VIEW3D_PT_manage_modifiers`, `VIEW3D_PT_object_color`)
  - Operators: `ModeSet`, `ReorderModifiers`, `AddMaterial`, `ToggleOverlays`

6.2 **Add poll() classmethods** where missing:
  - `ModeSet.poll()` — check for mesh objects
  - `ReorderModifiers.poll()` — check for active object with modifiers
  - `AddMaterial.poll()` — check for object with material slots

6.3 **Review all `context.area.type` checks** in `GLOBAL_Q`, `GLOBAL_W`, `GLOBAL_E` for unhandled area types (add fallback or silent skip).

6.4 **`SaveIncremental` path edge case:** Ensure `currentblend` has a valid `.blend` extension before regex matching.

**Files touched**: `AAA_operator.py` (and split files), `AAA_panel.py` (and split files).

---

### Phase 7 — Verification & Testing

**Goal**: Ensure nothing is broken after the refactor.

7.1 **Manual verification checklist:**
  - All operators register without errors (`bpy.utils.register_all` works).
  - Keymap items are correctly registered and removable.
  - All Scene properties are accessible through the PropertyGroup path.
  - UI panels render without AttributeError.
  - Pie menus show correctly.
  - All `aaa.*` operator `bl_idname` references resolve correctly.

7.2 **Automation:**
  - Create a minimal `.blend` test script that iterates all registered classes, calls `execute()` on each operator with a mock context where feasible.
  - Test keymap unregister does not leave stale entries.

7.3 **Rollback plan:** Keep shim files in each phase so the addon never enters a broken state. Only remove shims after Phase 7 is complete.

**Files touched**: New test script(s).
