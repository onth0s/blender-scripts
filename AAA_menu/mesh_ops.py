import bpy  # type: ignore
from bpy.types import Menu  # type: ignore
from AAA_utils import MHE, OBJ, MHS

class VIEW3D_MT_STD_TOOLS(Menu):
    bl_label = "Standard Tools"

    def draw(self, context):
        LYT = self.layout
        M = context.mode

        BRUSH = "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\"

        if M in (MHE):
            LYT.operator_context = "INVOKE_DEFAULT"

            LYT.operator("mesh.duplicate_move", text="Q - Duplicate")
            LYT.operator("mesh.inset", text="W - Inset")
            LYT.operator("mesh.vert_connect_path", text="E - Connect Path")
            LYT.operator("mesh.split", text="R - Split")

            LYT.separator()
            LYT.operator("mesh.extrude_region_move", text="S - Extrude")
            LYT.operator("mesh.bevel", text="D - Bevel")

            # custom built-in operator call to make sure the active tool
            # switches from the selection ones to the spin tool
            LYT.operator("aaa.std_tools", text="F - Spin").name = "SPIN_TOOL"

            LYT.separator()
            LYT.operator("mesh.remove_doubles", text="Z - Remove Doubles")
            LYT.operator(
                "wm.call_menu", text="C - Merge"
            ).name = "VIEW3D_MT_edit_mesh_merge"
            LYT.operator("mesh.subdivide", text="V - Subdivide")

        elif M in (OBJ):
            LYT.operator("object.parent_set", text="E - Parent Object").type = "OBJECT"
            LYT.operator("object.parent_clear", text="Q - Clear Parent").type = "CLEAR"

        elif M in (MHS):
            OP = LYT.operator("brush.asset_activate", text="R - Smooth")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Smooth"

            OP = LYT.operator("brush.asset_activate", text="S - Clay Strips")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Clay Strips"

            OP = LYT.operator("brush.asset_activate", text="C - Crease Sharp")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Crease Sharp"

            OP = LYT.operator("brush.asset_activate", text="F - Crease Polish")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Crease Polish"

            OP = LYT.operator("brush.asset_activate", text="D - Grab")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Grab"

            OP = LYT.operator("brush.asset_activate", text="G - Grab 2D")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Grab 2D"

            OP = LYT.operator("brush.asset_activate", text="B - Blob")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Blob"

            OP = LYT.operator("brush.asset_activate", text="Q - Inflate")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Inflate/Deflate"

            OP = LYT.operator("brush.asset_activate", text="W - Pinch")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Pinch/Magnify"

            OP = LYT.operator("brush.asset_activate", text="T - Fill")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Fill/Deepen"

            OP = LYT.operator("brush.asset_activate", text="E - Flatten")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Flatten/Contrast"

            OP = LYT.operator("brush.asset_activate", text="V - Draw Sharp")
            OP.asset_library_type = "ESSENTIALS"
            OP.relative_asset_identifier = BRUSH + "Draw Sharp"

            LYT.separator()
            LYT.operator(
                "wm.tool_set_by_id", text="Z - Mask"
            ).name = "builtin_brush.mask"

            LYT.separator()
            LYT.operator(
                "wm.tool_set_by_id", text="H - Lasso Hide"
            ).name = "builtin.lasso_hide"

            LYT.separator()
            LYT.operator(
                "wm.tool_set_by_id", text="X - Line Trim"
            ).name = "builtin.line_trim"

            LYT.operator(
                "wm.tool_set_by_id", text="A - Lasso Trim"
            ).name = "builtin.lasso_trim"


class VIEW3D_MT_MODIFIERS(Menu):
    bl_label = "Modifiers"

    def draw(self, context):
        LYT = self.layout

        LYT.operator(
            "wm.call_panel", text="D - Manage"
        ).name = "VIEW3D_PT_manage_modifiers"
        LYT.separator()

        LYT.operator("object.modifier_add", text="S - Subsurf").type = "SUBSURF"

        LYT.operator("object.modifier_add", text="T - Mirror").type = "MIRROR"

        LYT.operator("object.modifier_add", text="V - Solidify").type = "SOLIDIFY"


class VIEW3D_MT_APPLY_CLEAR(Menu):
    bl_label = "Apply or Clear"

    def draw(self, context):
        LYT = self.layout
        MN = "wm.call_menu"

        LYT.operator(MN, text="A - Apply").name = "VIEW3D_MT_APPLY"
        LYT.operator(MN, text="D - Clear").name = "VIEW3D_MT_CLEAR"


class VIEW3D_MT_APPLY(Menu):
    bl_label = "Apply"

    def draw(self, context):
        LYT = self.layout

        props = LYT.operator("object.transform_apply", text="Q - All")
        props.location = True
        props.scale = True
        props.rotation = True
        props = LYT.operator("object.transform_apply", text="W - Except Location")
        props.location = False
        props.scale = True
        props.rotation = True

        LYT.separator()
        props = LYT.operator("object.transform_apply", text="A - Location")
        props.location = True
        props.scale = False
        props.rotation = False

        props = LYT.operator("object.transform_apply", text="S - Scale")
        props.location = False
        props.scale = True
        props.rotation = False

        props = LYT.operator("object.transform_apply", text="D - Rotation")
        props.location = False
        props.scale = False
        props.rotation = True


class VIEW3D_MT_CLEAR(Menu):
    bl_label = "Clear"

    def draw(self, context):
        LYT = self.layout
        OB = "object"

        LYT.operator("aaa.clear_all_transforms", text="Q - Clear All")
        LYT.separator()

        props = LYT.operator(OB + ".location_clear", text="A - Location")
        props.clear_delta = False

        props = LYT.operator(OB + ".scale_clear", text="S - Scale")
        props.clear_delta = False

        props = LYT.operator(OB + ".rotation_clear", text="D - Rotation")
        props.clear_delta = False

        LYT.operator("aaa.clear_except_location", text="W - Except Location")

        LYT.separator()
        props = LYT.operator(OB + ".origin_clear", text="E - Origin to Parent")
