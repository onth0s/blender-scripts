import bpy  # type: ignore
from bpy.types import Menu  # type: ignore


class VIEW3D_MT_FACE_SETS(Menu):
    bl_label = "Face Sets"

    def draw(self, context):
        LYT = self.layout

        LYT.operator("sculpt.face_sets_create",
                     text="A - From Masked").mode = "MASKED"
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
        op = self.layout.operator(
            "sculpt.mesh_filter", text="T - Surface Smooth")
        op.type = 'SURFACE_SMOOTH'


class VIEW3D_MT_SCULPT_HIDE(Menu):
    bl_label = "Sculpt Hide"

    def draw(self, context):
        LYT = self.layout

        op = LYT.operator("paint.hide_show_masked", text="F - Hide Masked")
        op.action = "HIDE"

        op = LYT.operator("paint.hide_show_all", text="G - Show All")
        op.action = "SHOW"

        LYT.separator()
        LYT.operator(
            "wm.tool_set_by_id", text="H - Lasso Hide"
        ).name = "builtin.lasso_hide"
        LYT.operator(
            "wm.tool_set_by_id", text="B - Box Hide"
        ).name = "builtin.box_hide"


# Backwards compatibility alias
VIEW3D_MT_SCULPT_OPS = VIEW3D_MT_SCULPT_HIDE


class VIEW3D_MT_SCULPT_MASK(Menu):
    bl_label = "Sculpt Mask"

    def draw(self, context):
        LYT = self.layout

        LYT.operator(
            "wm.tool_set_by_id", text="Z - Mask"
        ).name = "builtin_brush.mask"
        LYT.operator(
            "wm.tool_set_by_id", text="B - Box Mask"
        ).name = "builtin.box_mask"
        LYT.operator(
            "wm.tool_set_by_id", text="L - Lasso Mask"
        ).name = "builtin.lasso_mask"

        LYT.separator()
        op = LYT.operator("paint.mask_flood_fill", text="S - Clear")
        op.mode = "VALUE"
        op.value = 0

        op = LYT.operator("paint.mask_flood_fill", text="D - Invert")
        op.mode = "INVERT"


class VIEW3D_MT_SCULPT_PAINT(Menu):
    bl_label = "Sculpt Paint"

    def draw(self, context):
        LYT = self.layout
        BRUSH = "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\"

        OP = LYT.operator("aaa.sculpt_brush_activate", text="S - Paint Hard")
        OP.asset_identifier = BRUSH + "Paint Hard"
        OP.brush_type = "STANDARD"
