import bpy  # type: ignore
from bpy.types import Operator  # type: ignore
from bpy.props import StringProperty  # type: ignore
from AAA_utils import MHE, MHS, MHV, OBJ


class ModeSet(Operator):
    bl_idname = "aaa.mode_set"
    bl_label = ""

    mode: StringProperty()  # type: ignore

    def execute(self, context):
        # space_data is None in headless/background mode; guard before accessing shading
        if context.space_data is not None:
            if self.mode in (MHE, MHS.MHV):
                context.space_data.shading.cavity_type = "WORLD"
                context.space_data.shading.cavity_type = "WORLD"
                context.space_data.shading.cavity_type = "WORLD"
            elif self.mode == OBJ:
                context.space_data.shading.cavity_type = "BOTH"

        bpy.ops.object.mode_set(mode=self.mode)
        return {"FINISHED"}


class STDTools(Operator):
    bl_idname = "aaa.std_tools"
    bl_label = "Standard Tools"
    bl_options = {"REGISTER"}

    name: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        if self.name == "SPIN_TOOL":
            bpy.ops.wm.tool_set_by_id(name="builtin.spin")
            context.scene.tool_settings.workspace_tool_type = "DEFAULT"

        return {"FINISHED"}
