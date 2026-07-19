import bpy  # type: ignore
from bpy.types import Menu  # type: ignore
from AAA_utils import OBJ, MHE, MHS

class VIEW3D_MT_SELECT(Menu):
    bl_label = "Select"

    def draw(self, context):
        AT = context.area.type
        M = context.mode

        LYT = self.layout

        if AT == "VIEW_3D":
            if M in OBJ:
                LYT.operator("object.select_all", text="A - All").action = "SELECT"
                LYT.operator("object.select_all", text="S - None").action = "DESELECT"
                LYT.operator("object.select_all", text="D - Invert").action = "INVERT"
                LYT.operator(
                    "object.select_grouped", text="Q - Select Grouped"
                ).type = "PARENT"
            elif M in MHE:
                LYT.operator("mesh.select_all", text="A - All").action = "SELECT"
                LYT.operator("mesh.select_all", text="S - None").action = "DESELECT"
                LYT.operator("mesh.select_all", text="D - Invert").action = "INVERT"

                LYT.separator()
                LYT.operator("mesh.select_linked", text="Q - Linked")

                LYT.separator()
                LYT.operator("mesh.loop_to_region", text="E - Inner Region")
                LYT.operator("mesh.region_to_loop", text="F - Boundary")
            elif M in MHS:
                OP = LYT.operator("paint.mask_flood_fill", text="S - Clear")
                OP.mode = "VALUE"
                OP.value = 0

                OP = LYT.operator("paint.mask_flood_fill", text="D - Invert")
                OP.mode = "INVERT"

        elif AT == "SEQUENCE_EDITOR":
            LYT.operator("sequencer.select_all", text="A - All").action = "SELECT"
            LYT.operator("sequencer.select_all", text="S - None").action = "DESELECT"
            LYT.operator("sequencer.select_all", text="D - Invert").action = "INVERT"


class VIEW3D_MT_SELECT_MODE(Menu):
    bl_label = "Select"

    def draw(self, context):
        TL = "wm.tool_set_by_id"
        LYT = self.layout

        LYT.operator(TL, text="W - Default").name = "builtin.select"

        LYT.separator()
        LYT.operator(TL, text="A - Lasso").name = "builtin.select_lasso"
        LYT.operator(TL, text="S - Box").name = "builtin.select_box"
        LYT.operator(TL, text="D - Circle").name = "builtin.select_circle"

        LYT.separator()
        LYT.operator(TL, text="E - Cursor").name = "builtin.cursor"


class VIEW3D_MT_CURSOR_POSITION(Menu):
    bl_label = "Cursor Position"

    def draw(self, context):
        M = context.mode
        layout = self.layout

        if M in (OBJ, MHE):
            layout.operator("view3d.snap_cursor_to_center", text="A - Cursor to Center")
            layout.operator(
                "view3d.snap_cursor_to_selected", text="D - Cursor to Selection"
            )
            layout.operator("view3d.snap_cursor_to_active", text="W - Cursor to Active")
            layout.operator(
                "view3d.snap_selected_to_cursor", text="S - Selection with Offset"
            ).use_offset = True


class VIEW3D_MT_MHE_MODE(Menu):
    bl_label = "Select Mode"

    def draw(self, context):
        LYT = self.layout

        LYT.operator("mesh.select_mode", text="A - Vertex Select").type = "VERT"
        LYT.operator("mesh.select_mode", text="S - Edge Select").type = "EDGE"
        LYT.operator("mesh.select_mode", text="D - Face Select").type = "FACE"
