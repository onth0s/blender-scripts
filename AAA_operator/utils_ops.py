import bpy  # type: ignore
from bpy.types import Operator  # type: ignore

class SwitchCondition(Operator):
    bl_idname = "aaa.switch_condition"
    bl_label = "SWITCH_CONDITION"
    bl_options = {"REGISTER"}

    cond: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        context.scene.conditions = self.cond

        return {"FINISHED"}


class SwitchValue(Operator):
    bl_idname = "aaa.switch_value"
    bl_label = "SWITCH_VALUE"
    bl_options = {"REGISTER"}

    val_a: bpy.props.StringProperty()  # type: ignore
    val_b: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        # this is a workaround to set a property from the outside
        # it's not a good practice, but it works
        # TODO find a better way to do this
        exec(f"{self.val_a} = '{self.val_b}'")

        return {"FINISHED"}


class ToggleProp(Operator):
    bl_idname = "aaa.toggle_prop"
    bl_label = "Toggle Property"
    bl_options = {"UNDO"}

    prop: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        exec(self.prop + " = not " + self.prop)

        return {"FINISHED"}
