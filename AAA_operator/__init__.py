import bpy  # type: ignore

from .file_ops import SaveFile, SaveIncremental
from .viewport import (
    SwitchWorkspace,
    ToggleOverlays,
    RollViewport,
    RollAxis,
    SwitchRenderer,
)
from .modes import ModeSet, STDTools
from .objects import (
    ReorderModifiers,
    AddMaterial,
    AAA_OT_clear_all_transforms,
    AAA_OT_clear_except_location,
)
from .routing import GlobalQ, GlobalW, GlobalE, CONDITIONS_ROUTER
from .utils_ops import SwitchCondition, SwitchValue, ToggleProp
from .debugger import TestOperator, TestContextDebugger

classes = (
    AAA_OT_clear_all_transforms,
    AAA_OT_clear_except_location,
    SaveFile,
    SaveIncremental,
    SwitchWorkspace,
    ModeSet,
    ToggleOverlays,
    RollViewport,
    RollAxis,
    STDTools,
    ReorderModifiers,
    AddMaterial,
    SwitchRenderer,
    SwitchCondition,
    SwitchValue,
    GlobalQ,
    GlobalW,
    GlobalE,
    ToggleProp,
    TestOperator,
    TestContextDebugger,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
