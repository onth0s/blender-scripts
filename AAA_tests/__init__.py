from .test_imports import TestImports
from .test_registration import (
    TestSettingsRegistration,
    TestOperatorRegistration,
    TestMenuRegistration,
    TestPanelRegistration,
    TestPieMenuRegistration,
)
from .test_utils import TestUtils
from .test_operator_exec import (
    TestSwitchWorkspaceExecution,
    TestOperatorExecution,
    TestSaveOperations,
    TestToggleProp,
    TestSwitchCondition,
    TestSwitchValue,
)
from .test_viewport_math import TestRollViewportMath, TestSwitchRendererLogic
from .test_routing import TestKeyConditionsRouting, TestConditionsRouter
from .test_keymaps import TestKeymapDeclarations
from .test_unregister import TestUnregisterCleanup

def register():
    pass

def unregister():
    pass
