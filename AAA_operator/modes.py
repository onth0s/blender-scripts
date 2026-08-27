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
            if self.mode == "OBJECT" or self.mode == OBJ:
                context.space_data.shading.cavity_type = "BOTH"
            else:
                context.space_data.shading.cavity_type = "WORLD"

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


class AAA_OT_sculpt_brush_activate(Operator):
    bl_idname = "aaa.sculpt_brush_activate"
    bl_label = "Sculpt Brush Activate"
    bl_options = {"REGISTER", "UNDO"}

    asset_identifier: bpy.props.StringProperty(name="Asset Identifier", default="")  # type: ignore
    asset_library_type: bpy.props.StringProperty(name="Asset Library Type", default="ESSENTIALS")  # type: ignore
    tool_id: bpy.props.StringProperty(name="Tool ID", default="")  # type: ignore
    brush_type: bpy.props.EnumProperty(  # type: ignore
        name="Brush Type",
        items=[
            ("STANDARD", "Standard", "Standard sculpt brush"),
            ("DENSITY", "Density", "Density sculpt brush"),
            ("MOVE", "Move", "Move sculpt brush"),
        ],
        default="STANDARD",
    )

    def execute(self, context):
        obj = context.sculpt_object or context.active_object
        scene = context.scene

        # 1. Wireframe display (only active for Density brush)
        if obj and hasattr(obj, "show_wire"):
            obj.show_wire = self.brush_type == "DENSITY"

        # 2. Dyntopo state tracking and restoration
        if obj and hasattr(obj, "use_dynamic_topology_sculpting"):
            cur_dyntopo = obj.use_dynamic_topology_sculpting

            if self.brush_type == "DENSITY":
                if not scene.dyntopo_override_density and not scene.dyntopo_override_move:
                    scene.dyntopo_prev_state = cur_dyntopo
                scene.dyntopo_override_density = True
                scene.dyntopo_override_move = False

                if not cur_dyntopo:
                    bpy.ops.sculpt.dynamic_topology_toggle()

            elif self.brush_type == "MOVE":
                if not scene.dyntopo_override_density and not scene.dyntopo_override_move:
                    scene.dyntopo_prev_state = cur_dyntopo
                scene.dyntopo_override_move = True
                scene.dyntopo_override_density = False

                if cur_dyntopo:
                    bpy.ops.sculpt.dynamic_topology_toggle()

            else:  # STANDARD
                if scene.dyntopo_override_density or scene.dyntopo_override_move:
                    target_dyntopo = scene.dyntopo_prev_state
                    if cur_dyntopo != target_dyntopo:
                        bpy.ops.sculpt.dynamic_topology_toggle()
                    scene.dyntopo_override_density = False
                    scene.dyntopo_override_move = False

        # 3. Brush asset or tool activation
        if self.asset_identifier:
            bpy.ops.brush.asset_activate(
                asset_library_type=self.asset_library_type,
                relative_asset_identifier=self.asset_identifier,
            )
        elif self.tool_id:
            bpy.ops.wm.tool_set_by_id(name=self.tool_id)

        return {"FINISHED"}


