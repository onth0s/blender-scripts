import bpy  # type: ignore

from .file_ops import (
    AAA_OT_save_file,
    AAA_OT_save_incremental,
    AAA_OT_reload_scripts,
    SaveFile,
    SaveIncremental,
    ReloadScripts,
)
from .viewport import (
    AAA_OT_switch_workspace,
    AAA_OT_toggle_overlays,
    AAA_OT_roll_viewport,
    AAA_OT_roll_axis,
    AAA_OT_switch_renderer,
    SwitchWorkspace,
    ToggleOverlays,
    RollViewport,
    RollAxis,
    SwitchRenderer,
)
from .modes import (
    AAA_OT_mode_set,
    AAA_OT_std_tools,
    AAA_OT_sculpt_brush_activate,
    ModeSet,
    STDTools,
)
from .objects import (
    AAA_OT_reorder_modifiers,
    AAA_OT_add_material,
    AAA_OT_clear_all_transforms,
    AAA_OT_clear_except_location,
    ReorderModifiers,
    AddMaterial,
)
from .routing import (
    AAA_OT_global_q,
    AAA_OT_global_w,
    AAA_OT_global_e,
    GlobalQ,
    GlobalW,
    GlobalE,
    CONDITIONS_ROUTER,
)
from .utils_ops import (
    AAA_OT_switch_condition,
    AAA_OT_switch_value,
    AAA_OT_toggle_prop,
    SwitchCondition,
    SwitchValue,
    ToggleProp,
)
from .debugger import (
    AAA_OT_test_operator,
    AAA_OT_test_context_debugger,
    TestOperator,
    TestContextDebugger,
)

classes = (
    AAA_OT_clear_all_transforms,
    AAA_OT_clear_except_location,
    AAA_OT_save_file,
    AAA_OT_save_incremental,
    AAA_OT_reload_scripts,
    AAA_OT_switch_workspace,
    AAA_OT_mode_set,
    AAA_OT_toggle_overlays,
    AAA_OT_roll_viewport,
    AAA_OT_roll_axis,
    AAA_OT_std_tools,
    AAA_OT_sculpt_brush_activate,
    AAA_OT_reorder_modifiers,
    AAA_OT_add_material,
    AAA_OT_switch_renderer,
    AAA_OT_switch_condition,
    AAA_OT_switch_value,
    AAA_OT_global_q,
    AAA_OT_global_w,
    AAA_OT_global_e,
    AAA_OT_toggle_prop,
    AAA_OT_test_operator,
    AAA_OT_test_context_debugger,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
