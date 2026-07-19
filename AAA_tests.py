"""
AAA_tests.py – Automated test suite runner for AAA_*.py startup scripts.

Run from Blender's background mode:
    blender --background -noaudio --python AAA_tests.py --
"""

import sys
import os
import unittest

# Ensure the startup directory is in the path
startup_dir = os.path.dirname(os.path.abspath(__file__))
if startup_dir not in sys.path:
    sys.path.append(startup_dir)

import AAA_tests  # Import the package containing all tests

# Blender startup script stubs (required for --background loading)
def register():
    pass


def unregister():
    pass


if __name__ == "__main__":
    args = sys.argv
    unittest_args = args[args.index("--") + 1 :] if "--" in args else []

    # Load tests from the AAA_tests package
    suite = unittest.defaultTestLoader.loadTestsFromModule(AAA_tests)
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
