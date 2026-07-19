import sys
import os
import unittest

# Ensure the startup directory is in the path
startup_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if startup_dir not in sys.path:
    sys.path.append(startup_dir)

from AAA_tests.test_imports import TestImports
from AAA_tests.test_registration import (
    TestSettingsRegistration,
    TestOperatorRegistration,
    TestMenuRegistration,
    TestPanelRegistration,
    TestPieMenuRegistration,
)
from AAA_tests.test_utils import TestUtils
from AAA_tests.test_operator_exec import (
    TestSwitchWorkspaceExecution,
    TestOperatorExecution,
    TestSaveOperations,
    TestToggleProp,
    TestSwitchCondition,
    TestSwitchValue,
)
from AAA_tests.test_viewport_math import TestRollViewportMath, TestSwitchRendererLogic
from AAA_tests.test_routing import TestKeyConditionsRouting, TestConditionsRouter
from AAA_tests.test_keymaps import TestKeymapDeclarations
from AAA_tests.test_unregister import TestUnregisterCleanup


def register():
    pass


def unregister():
    pass


if __name__ == "__main__":
    args = sys.argv
    unittest_args = args[args.index("--") + 1 :] if "--" in args else []

    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print()
        print(" ╔══════════════════════════╗")
        print(" ║  BANZAI! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧  ║")
        print(" ║  All tests passed!       ║")
        print(" ╚══════════════════════════╝")
        print()

    sys.exit(not result.wasSuccessful())
