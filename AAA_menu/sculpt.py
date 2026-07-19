import bpy  # type: ignore
from bpy.types import Menu  # type: ignore

class VIEW3D_MT_FACE_SETS(Menu):
    bl_label = "Face Sets"

    def draw(self, context):
        LYT = self.layout

        LYT.operator("sculpt.face_sets_create", text="A - From Masked").mode = "MASKED"
        LYT.operator(
            "sculpt.face_sets_create", text="S - From Visible"
        ).mode = "VISIBLE"
        LYT.operator(
            "sculpt.face_sets_create", text="D - From Selection"
        ).mode = "SELECTION"


class VIEW3D_MT_SCULPT_FILTERS(Menu):
    bl_label = "Sculpt Filters"

    def draw(self, context):
        self.layout.operator_context = 'INVOKE_DEFAULT'
        op = self.layout.operator("sculpt.mesh_filter", text="R - Smooth")
        op.type = 'SMOOTH'
        op = self.layout.operator("sculpt.mesh_filter", text="T - Surface Smooth")
        op.type = 'SURFACE_SMOOTH'


class VIEW3D_MT_SCULPT_OPS(Menu):
    bl_label = "Sculpt Operators"

    def draw(self, context):
        LYT = self.layout
        op = LYT.operator("paint.hide_show_masked", text="F - Hide Masked")
        op.action = "HIDE"

        op = LYT.operator("paint.hide_show_all", text="G - Show All")
        op.action = "SHOW"
