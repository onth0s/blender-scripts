# AAA — Personal Blender Workflow Scripts

A collection of startup scripts for Blender that provide custom pie menus,
operators, panels, keymaps, and scene settings — tailored to a single-user
sculpting/retopology workflow.

> **Pragmatism over purity.** These are ad hoc automations, not a polished
> addon. No `bl_info`, no `__init__.py`. They live in Blender's startup
> directory and auto-register on launch.

---

## Files

| File | Purpose |
|---|---|
| `AAA_settings.py` | Declares custom `Scene` properties (`conditions`, `show_overlays`, `axis_roll`, `loop_frames`, …) |
| `AAA_operator.py` | ~20 operators: save, mode switching, modifier reorder, viewport roll, global key routing, property toggles, debug tools |
| `AAA_menu.py` | Custom `VIEW3D_MT_*` menus (workspace, mode, viewport display, shading, renderer, select, tools, modifiers, pivot, apply/clear, …) |
| `AAA_pie.py` | Pie menus: **SPACE** (general), **S** (tools), **A** (animation), **Z** (shading), **C** (key conditions), **Ctrl+S** (save) |
| `AAA_panel.py` | Popover panels (modifier manager, proportional edit, frame range, object color, lighting, background, frame rate) |
| `AAA_keymap.py` | Global keymap registration — ties pie menus & operators to keyboard shortcuts |
| `AAA_utils.py` | Shared constants (`OBJ`, `MHE`, `MHS`, `ALL`, …), mode/type helpers, incremental save path resolver |
| `AAA_tests.py` | Headless test suite (`unittest`), runnable via `blender --background -noaudio --python AAA_tests.py --` |

---

## Pie Menu Overview

| Key | Pie | Contents |
|---|---|---|
| **SPACE** | `PIE_MT_SPACE` | Workspace, View, Select, Select Mode, Apply/Clear, Object Ops / Edit Mode / Face Sets |
| **S** | `PIE_MT_S` | Orientation, Tools, Pivot Point, Snapping, Proportional Edit, Modifiers, Cursor |
| **A** | `PIE_MT_ANIMATION` | Timeline playback, frame range |
| **Z** | `VIEW3D_MT_SHADING_PIE` | Object Color, Display, Renderer, Lighting, Background, Shading Options |
| **C** | `PIE_MT_KEY_CONDITIONS` | Switch between Transform / Timeline key routing modes |
| **Ctrl+S** | `PIE_MT_SAVE_N_STUFF` | Save, Save Incremental, Open, New, Append, Import OBJ, Override Startup, Run Script |

---

## Global Key Routing (`Q` / `W` / `E`)

The `scene.conditions` property controls what **Q**, **W**, and **E** do:

- **TRANSFORM** (default): Q → Translate, W → Scale/Time Scale, E → Rotate
- **TIMELINE**: Q → step back / wrap, W → jump to start, E → step forward / wrap

Switch via `PIE_MT_KEY_CONDITIONS` (pie bound to **C**).

---

## Key Operators

| Operator | ID | Action |
|---|---|---|
| `SaveFile` | `aaa.save_file` | Save current blend; warns if no changes |
| `SaveIncremental` | `aaa.save_incremental` | Save with incremented filename (`file_001.blend` → `file_002.blend`) |
| `ModeSet` | `aaa.mode_set` | Switch object mode (also sets cavity type) |
| `ToggleOverlays` | `aaa.toggle_overlays` | Toggle header / floor / all overlays |
| `RollViewport` | `aaa.roll_viewport` | Drag-rotate viewport around chosen axis (**Alt+MMB**) |
| `RollAxis` | `aaa.roll_axis` | Set the roll axis (X/Y/Z) |
| `ReorderModifiers` | `aaa.reorder_modifiers` | Move modifier up/down/top/bottom |
| `AddMaterial` | `aaa.add_material` | Add new or most-recent material to active object |
| `SwitchRenderer` | `aaa.switch_renderer` | Swap between Solid / Material / EEVEE / Cycles / Workbench |
| `SwitchCondition` | `aaa.switch_condition` | Set `scene.conditions` |
| `SwitchValue` / `ToggleProp` | `aaa.switch_value` / `aaa.toggle_prop` | Generic exec-based value assignment / toggle |
| `GlobalQ/W/E` | `aaa.key_q/w/e` | Routed by `CONDITIONS_ROUTER` |
| `TestOperator` / `TestContextDebugger` | `aaa.test_operator` / `aaa.test_context_debugger` | Debug utilities |

---

## Panels

- **Manage Modifiers** (`VIEW3D_PT_manage_modifiers`) — reorder list with up/down/top/bottom buttons
- **Proportional Editing** (`VIEW3D_PT_proportional_edit_2`) — distance, connected, falloff
- **Frame Range** (`VIEW3D_PT_frame_range`) — start/end, preview range, loop toggle
- **Object Color** (`VIEW3D_PT_object_color`) — color type, single/object/material
- **Lighting** (`VIEW3D_PT_lighting`) — studio light, matcap, scene lights/world
- **Background Color** (`VIEW3D_PT_background_color`) — viewport/world background
- **Frame Rate** (`VIEW3D_PT_FRAME_RATE`) — FPS display

---

## Keymap Reference

| Shortcut | Action |
|---|---|
| **SPACE** | `PIE_MT_SPACE` |
| **S** | `PIE_MT_S` |
| **A** | `PIE_MT_ANIMATION` |
| **Z** | `VIEW3D_MT_SHADING_PIE` |
| **C** | `PIE_MT_KEY_CONDITIONS` |
| **Ctrl+S** | `PIE_MT_SAVE_N_STUFF` |
| **Q** / **W** / **E** | Global key routing (Transform or Timeline) |
| **Ctrl+Shift+Alt+P** | `TestContextDebugger` |
| **Alt+MMB drag** | `RollViewport` |
| **Shift+Ctrl+MMB** | `view3d.view_selected` |
| **Ctrl+Alt+MMB** | `view3d.view_center_pick` |
| **Shift+Ctrl+MMB** (Image Editor) | Zoom to 1:1 |

---

## Running Tests

```bash
blender --background -noaudio --python AAA_tests.py --
```

Covers: import sanity, registration/unregistration, operator execution (headless-compatible), filename increment logic, quaternion rotation math, conditions routing, keymap declarations.

---

## Notes

- **Empty operators/menus** in pie menus are deliberate — they maintain directional balance.
- The `exec()` calls in `SwitchValue` and `ToggleProp` are known and accepted workarounds.
- These scripts assume a personal workflow and are not designed for general distribution.
