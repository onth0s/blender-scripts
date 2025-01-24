import bpy
from bpy.props import *
from bpy.types import (Menu, Operator)

from AAA_var import *


class VIEW3D_MT_WORKSPACE(Menu):
    bl_label = "Workspace"

    def draw(self, context):
        WS = "aaa.switch_workspace"
        layout = self.layout

        layout.operator(WS, text="A - Main").name = "Main"

        layout.separator()
        layout.operator(WS, text="V - Video Editing").name = "Video Editing"

        layout.separator()
        layout.operator(WS, text="F - Full View").name = "Full View"


class VIEW3D_MT_VIEW(Menu):
    bl_label = "Views"

    def draw(self, context):
        LYT = self.layout
        MN = "wm.call_menu"

        LYT.operator(MN, text="Q - Align Normal").name = "VIEW3D_MT_VIEW_ALIGN"
        # LYT.operator(MN, text="W - Views")\
        #     .name = "VIEW3D_MT_VIEW_VIEW"

        # LYT.separator()
        # LYT.operator("view3d.view_persportho", text="E - Persp/Ortho")

        # LYT.separator()
        # LYT.operator(
        #     "aaa.toggle_prop", text="R - Lock Orbit").prop = "context.space_data.region_3d.lock_rotation"

        # LYT.operator(MN, text="X - Axis Roll")\
        #     .name = "VIEW3D_MT_VIEW_AXIS_ROLL"

        # LYT.separator()
        # LYT.operator("aaa.select_reference_image", text="C - Select Image")

        # LYT.separator()
        # LYT.operator_context = 'INVOKE_DEFAULT'
        # LYT.operator("view3d.walk", text="F - Walk Navigation")
        # LYT.operator("view3d.localview", text="Z - Local View")


class VIEW3D_MT_VIEW_ALIGN(Menu):
    bl_label = "Align Normal"

    def draw(self, context):
        LYT = self.layout

        props = LYT.operator("view3d.view_axis", text="Q - Top")
        props.align_active = True
        props.type = 'TOP'
        props = LYT.operator("view3d.view_axis", text="A - Bottom")
        props.align_active = True
        props.type = 'BOTTOM'

        LYT.separator()
        props = LYT.operator("view3d.view_axis", text="W - Front")
        props.align_active = True
        props.type = 'FRONT'
        props = LYT.operator("view3d.view_axis", text="S - Back")
        props.align_active = True
        props.type = 'BACK'

        LYT.separator()
        props = LYT.operator("view3d.view_axis", text="E - Right")
        props.align_active = True
        props.type = 'RIGHT'
        props = LYT.operator("view3d.view_axis", text="D - Left")
        props.align_active = True
        props.type = 'LEFT'


class VIEW3D_MT_TRANSFORM_GIZMO(Menu):
    bl_label = "Gizmo"

    def draw(self, context):
        TL = "wm.tool_set_by_id"

        layout = self.layout

        layout.operator(TL, text="W - Transform").name = "builtin.transform"

        layout.separator()
        layout.operator(TL, text="A - Move").name = "builtin.move"
        layout.operator(TL, text="S - Scale").name = "builtin.scale"
        layout.operator(TL, text="D - Rotate").name = "builtin.rotate"


class VIEW3D_MT_VIEW_AXIS_ROLL(Menu):
    bl_label = "Axis Roll"

    def draw(self, context):
        layout = self.layout
        layout.operator("aaa.roll_axis", text="A - X Axis").axis = 'X'
        layout.operator("aaa.roll_axis", text="S - Y Axis").axis = 'Y'
        layout.operator("aaa.roll_axis", text="D - Z Axis").axis = 'Z'


classes = (
    VIEW3D_MT_WORKSPACE,

    VIEW3D_MT_VIEW,
    VIEW3D_MT_VIEW_ALIGN,

    VIEW3D_MT_TRANSFORM_GIZMO,

    VIEW3D_MT_VIEW_AXIS_ROLL,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
