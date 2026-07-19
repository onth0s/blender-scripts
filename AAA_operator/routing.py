import bpy  # type: ignore
from bpy.types import Operator  # type: ignore

def execute_transform_q(context):
    AT = context.area.type
    if AT in ("VIEW_3D", "GRAPH_EDITOR"):
        bpy.ops.transform.translate("INVOKE_DEFAULT")
    elif AT == "SEQUENCE_EDITOR":
        bpy.ops.transform.seq_slide("INVOKE_DEFAULT", view2d_edge_pan=True)
    else:
        print("something's wrong with the GLOBAL_Q operator under TRANSFORM")


def execute_transform_w(context):
    AT = context.area.type
    if AT in ("VIEW_3D", "GRAPH_EDITOR"):
        bpy.ops.transform.resize("INVOKE_DEFAULT")
    elif AT == "DOPESHEET_EDITOR":
        bpy.ops.transform.transform("INVOKE_DEFAULT", mode="TIME_SCALE")


def execute_transform_e(context):
    AT = context.area.type
    if AT in ("VIEW_3D", "GRAPH_EDITOR"):
        bpy.ops.transform.rotate("INVOKE_DEFAULT")


def execute_timeline_q(context):
    SN = context.scene
    if SN.loop_frames:
        if SN.use_preview_range:
            if SN.frame_current == SN.frame_preview_start:
                SN.frame_current = SN.frame_preview_end
            else:
                bpy.ops.screen.frame_offset(delta=-1)
        else:
            if SN.frame_current == SN.frame_start:
                SN.frame_current = SN.frame_end
            else:
                bpy.ops.screen.frame_offset(delta=-1)
    else:
        bpy.ops.screen.frame_offset(delta=-1)


def execute_timeline_w(context):
    if context.scene.use_preview_range:
        context.scene.frame_current = context.scene.frame_preview_start
    else:
        context.scene.frame_current = context.scene.frame_start


def execute_timeline_e(context):
    SN = context.scene
    if SN.loop_frames:
        if SN.use_preview_range:
            if SN.frame_current == SN.frame_preview_end:
                SN.frame_current = SN.frame_preview_start
            else:
                bpy.ops.screen.frame_offset(delta=1)
        else:
            if SN.frame_current == SN.frame_end:
                SN.frame_current = SN.frame_start
            else:
                bpy.ops.screen.frame_offset(delta=1)
    else:
        bpy.ops.screen.frame_offset(delta=1)


# Router registry mapping scene conditions to key functions
CONDITIONS_ROUTER = {
    "TRANSFORM": {
        "Q": execute_transform_q,
        "W": execute_transform_w,
        "E": execute_transform_e,
    },
    "TIMELINE": {
        "Q": execute_timeline_q,
        "W": execute_timeline_w,
        "E": execute_timeline_e,
    },
}


class GlobalQ(Operator):
    bl_idname = "aaa.key_q"
    bl_label = "GLOBAL_Q"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        CN = context.scene.conditions
        if CN in CONDITIONS_ROUTER and "Q" in CONDITIONS_ROUTER[CN]:
            CONDITIONS_ROUTER[CN]["Q"](context)
        else:
            self.report(
                {"WARNING"}, f"No mapping found for key Q under condition '{CN}'"
            )
        return {"FINISHED"}


class GlobalW(Operator):
    bl_idname = "aaa.key_w"
    bl_label = "GLOBAL_W"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        CN = context.scene.conditions
        if CN in CONDITIONS_ROUTER and "W" in CONDITIONS_ROUTER[CN]:
            CONDITIONS_ROUTER[CN]["W"](context)
        else:
            self.report(
                {"WARNING"}, f"No mapping found for key W under condition '{CN}'"
            )
        return {"FINISHED"}


class GlobalE(Operator):
    bl_idname = "aaa.key_e"
    bl_label = "GLOBAL_E"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        CN = context.scene.conditions
        if CN in CONDITIONS_ROUTER and "E" in CONDITIONS_ROUTER[CN]:
            CONDITIONS_ROUTER[CN]["E"](context)
        else:
            self.report(
                {"WARNING"}, f"No mapping found for key E under condition '{CN}'"
            )
        return {"FINISHED"}
