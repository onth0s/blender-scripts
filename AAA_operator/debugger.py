import bpy  # type: ignore
from bpy.types import Operator  # type: ignore
from datetime import datetime

class TestOperator(Operator):
    """Test Operator Docstring"""

    bl_idname = "aaa.test_operator"
    bl_label = "Test Operator"
    bl_options = {"REGISTER", "UNDO"}

    testVal: bpy.props.IntProperty()  # type: ignore

    def execute(self, context):
        time = str(datetime.time(datetime.now()))
        print("{}: {}".format(self.testVal, time[:-7]))

        return {"FINISHED"}


class TestContextDebugger(Operator):
    bl_idname = "aaa.test_context_debugger"
    bl_label = "Test Context Debugger"
    bl_options = {"REGISTER"}

    def execute(self, context):
        print("\n=============== FULL CONTEXT DUMP ===============\n")

        if context.area is not None:
            print(
                """  >>> context.area.type:
    Active Area:""",
                context.area.type,
            )

            print(
                """\n  >>> context.area.ui_type:
    UI Type:""",
                context.area.ui_type,
            )
        else:
            print("  >>> context.area: None")

        print(
            """\n  >>> context.active_object:
    Active Object:""",
            context.active_object,
        )

        print(
            f"""\n  >>> context.selected_objects:
    Selected Objects ({len(context.selected_objects)}):""",
            context.selected_objects,
        )

        print(
            """\n  >>> context.mode:
    Mode:""",
            context.mode,
        )

        if context.screen is not None:
            print(
                """\n  >>> context.screen.name:
    Screen:""",
                context.screen.name,
            )
        else:
            print("\n  >>> context.screen: None")

        if context.region is not None:
            print(
                """\n  >>> context.region.type:
    Region:""",
                context.region.type,
            )
        else:
            print("\n  >>> context.region: None")

        return {"FINISHED"}
