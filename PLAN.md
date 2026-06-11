# Automated Headless Testing Strategy for `AAA_*.py` Codebase

This document defines the strategy for executing a fully automated, headless test suite to verify the registration, execution, and stability of the `AAA_*.py` startup automation scripts.

## 1. Objectives
- **Zero-Crash Imports**: Ensure importing any script under `startup/` doesn't trigger unexpected `NameError`, `SyntaxError`, or initialization crashes.
- **Successful Registration**: Verify all custom menus, panels, and operators register without raising metadata collisions.
- **Headless Operator Execution**: Test that operators run without crashes under simulated context states.
- **Safe State Rollback**: Verify that unregistering cleanups Scene properties, keymaps, and operator bindings without memory leaks or state pollution.

---

## 2. Test Architecture

The tests will be executed via a dedicated runner script (`AAA_tests.py`) invoked via Blender's background mode:
```powershell
& "c:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --background -noaudio --python AAA_tests.py
```

### Module Loading & Setup
1. **Mock Environment Initialization**: Set `bpy.data.filepath` to a temporary directory path (e.g. `/tmp/test.blend`) to satisfy `SaveFile` and `SaveIncremental` checks. *Note: `bpy.data.filepath` is read-only in the Python API, so this is not feasible. `resolve_incremented_path()` is tested as a standalone utility instead.*
2. **Context Overrides**: Use `context.temp_override()` to mock active areas (e.g., `VIEW_3D`, `IMAGE_EDITOR`, `SEQUENCE_EDITOR`) and dummy window/screen objects so context-sensitive inspectors do not throw `NoneType` errors. *Note: `temp_override()` accepts only actual bpy structs, not arbitrary Python mocks. Operators that require `context.area`, `context.space_data`, or `context.region` cannot execute in headless mode.*

---

## 3. Test Fixture Setup

To execute operators safely, the test runner must bootstrap the scene state before invoking execution blocks:

| Operator / Module | Required Scene State Fixtures |
| :--- | :--- |
| `ReorderModifiers` | Creates a mesh object, adds two modifiers, set active. |
| `AddMaterial` | Creates a mesh object with empty material slots. |
| `ModeSet` | Instantiates a mesh object to allow transitions to `EDIT_MESH`, `SCULPT`, etc. |
| `SwitchWorkspace` | Ensures the targeted workspace names exist in `bpy.data.workspaces`. |

---

## 4. Operator Testing Scenarios

Each operator is wrapped in standard unit testing assertions:

### Scenario A: Standard Execution (`execute`)
Assert that operators (e.g., `SaveIncremental`, `SwitchCondition`) run and return `{'FINISHED'}` under configured context inputs.

### Scenario B: Dynamic Parameter Call
Invoke properties-based operators (e.g. `ModeSet(mode='EDIT')`, `SwitchRenderer(mode='SOLID')`) and verify the resulting viewport changes:
```python
# Assertion Check Example
bpy.ops.aaa.mode_set(mode='EDIT')
assert context.mode == 'EDIT_MESH', "ModeSet operator failed to transition context mode"
```

### Scenario C: Modal Validation (`RollViewport`)
Test the modal operator by manually calling `execute` or mocking mouse movement events using manual calculations to confirm rotation matrices resolve correctly without GUI window hooks.

### Scenario D: Property Toggles (`ToggleProp` & `SwitchValue`)
Invoke toggles on mock Scene or user properties and assert that the target attributes swap Boolean states or change string values correctly.

---

## 5. Teardown & Cleanup
1. Run `unregister()` on all modules.
2. Assert that allScene properties in `SCENE_PROPERTIES` are deleted cleanly.
3. Verify `addon_keymaps` is empty and all addon keymaps are removed from the window manager.

---

## 6. Known Gaps (Remaining)

The following items from this strategy remain not fully implemented in `AAA_tests.py`:

| Ref | Gap | Reason / Status |
| :-- | :--- | :-------------- |
| §2 | **Mock `bpy.data.filepath`** | `bpy.data.filepath` is read-only; cannot be set from Python. `resolve_incremented_path()` is unit-tested in `TestSaveOperations`. `SaveFile` calls `bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')` which crashes in headless with no filepath — the operator itself would need a guard. |
| §2 | **`context.temp_override()`** | Not used. In background mode Blender provides no `area`, `region`, or `space_data`; `temp_override()` cannot accept arbitrary Python objects, so context-sensitive operators (`ToggleOverlays`, `SwitchRenderer` shading/tool branch, `GlobalQ`/`GlobalW`/`GlobalE` area dispatch, `STDTools`) cannot be invoked via `bpy.ops` in headless mode. These operators are tested at the unit/math level where possible (e.g. `RollViewport` via `_RollOperator` stand-in) or via structure/enum validation (`SwitchRenderer` logic). |
| §4 | **`SaveFile`** | Crashes on `bpy.ops.wm.save_mainfile()` when no filepath is set (headless). No workaround without operator modification. |
| §4 | **`GlobalQ` / `GlobalW` / `GlobalE`** | `CONDITIONS_ROUTER` structure is validated in `TestConditionsRouter` but the operators themselves are not executed (they require `context.area` which is `None` in headless). |
| §4 | **`STDTools` / `TestContextDebugger`** | Require active tool system or area/region — inherently GUI-bound. |