import bpy  # type: ignore
from bpy.props import *  # type: ignore
from bpy.types import (Menu, Operator)  # type: ignore

from AAA_utils import *

# TODO
# flow.prop(context.preferences.inputs, "drag_threshold_tablet")

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


class VIEW3D_MT_MODE(Menu):
    bl_label = "Mode"

    def draw(self, context):
        OBT = context.object.type
        MS = "aaa.mode_set"

        LYT = self.layout

        if OBT == TMH:
            LYT.operator(MS, text="A - Object Mode").mode = 'OBJECT'
            LYT.operator(MS, text="S - Edit Mode").mode = 'EDIT'
            LYT.operator(MS, text="D - Sculpt Mode").mode = 'SCULPT'
        else: 
            LYT.label(text="No valid object selected")


class VIEW3D_MT_VIEWPORT_DISPLAY(Menu):
    bl_label = "Viewport Display"

    def draw(self, context):
        LYT = self.layout

        LYT.operator("aaa.toggle_overlays", text="Q - Header").header = True
        LYT.operator("aaa.toggle_overlays", text="A - Overlays").header = False

        LYT.separator()
        LYT.operator("aaa.toggle_prop", text="Z - Face Orientation") \
            .prop = "context.space_data.overlay.show_face_orientation"


class VIEW3D_MT_SHADING_OPTIONS(Menu):
    bl_label = "Shading Options"

    def draw(self, context):
        LYT = self.layout
        OBT = None if context.object is None else context.object.type

        if OBT == TMH and OBT != None:
            LYT.operator("object.shade_flat", text="A - Flat")
            LYT.operator("object.shade_smooth", text="S - Smooth")
            LYT.operator("object.shade_auto_smooth", text="D - Autosmooth")

        LYT.separator()
        LYT.operator("wm.call_menu", text="C - Cavity Type") \
            .name = "VIEW3D_MT_SHADING_OPTIONS_CAVITY"


class VIEW3D_MT_SHADING_OPTIONS_CAVITY(Menu):
    bl_label = "Cavity Options"

    def draw(self, context):
        global cavity_state
        LYT = self.layout

        cavity_state = "Disable" if context.space_data.shading.show_cavity \
            else "Enable"

        LYT.operator("aaa.toggle_prop", text="W - " + cavity_state) \
            .prop = "context.space_data.shading.show_cavity"

        TEMP = "context.space_data.shading.cavity_type"
        LYT.separator()
        OP = LYT.operator("aaa.switch_value", text="A - World")
        OP.val_a = TEMP
        OP.val_b = "WORLD"

        OP = LYT.operator("aaa.switch_value", text="S - Screen")
        OP.val_a = TEMP
        OP.val_b = "SCREEN"
        
        OP = LYT.operator("aaa.switch_value", text="D - Both")
        OP.val_a = TEMP
        OP.val_b = "BOTH"


class VIEW3D_MT_RENDERER(Menu):
    bl_label = ""

    def draw(self, context):
        OP = "aaa.switch_renderer"
        LYT = self.layout

        LYT.operator(OP, text="W - LookDev").mode = "MATERIAL"
        LYT.operator(OP, text="A - EEVEE").mode = "BLENDER_EEVEE_NEXT"
        LYT.operator(OP, text="S - Workbench").mode = "BLENDER_WORKBENCH"
        LYT.operator(OP, text="D - Cycles").mode = "CYCLES"
        LYT.operator(OP, text="Z - Solid").mode = "SOLID"


class VIEW3D_MT_VIEW(Menu):
    bl_label = "Views"

    def draw(self, context):
        LYT = self.layout
        MN = "wm.call_menu"

        LYT.operator(MN, text="Q - Align Normal").name = "VIEW3D_MT_VIEW_ALIGN"
        LYT.operator(MN, text="W - Views").name = "VIEW3D_MT_VIEW_VIEW"

        LYT.separator()
        LYT.operator("view3d.view_persportho", text="E - Persp/Ortho")

        LYT.separator()
        LYT.operator(
            "aaa.toggle_prop", text="R - Lock Orbit") \
            .prop = "context.space_data.region_3d.lock_rotation"

        LYT.operator(MN, text="X - Axis Roll")\
            .name = "VIEW3D_MT_VIEW_AXIS_ROLL"

        LYT.separator()
        LYT.operator_context = 'INVOKE_DEFAULT'
        LYT.operator("view3d.walk", text="F - Walk Navigation")
        LYT.operator("view3d.localview", text="Z - Local View")


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


class VIEW3D_MT_VIEW_VIEW(Menu):
    bl_label = "Views"

    def draw(self, context):
        LYT = self.layout
        LYT.operator("view3d.view_axis", text="Q - Top").type = 'TOP'
        LYT.operator("view3d.view_axis", text="A - Bottom").type = 'BOTTOM'

        LYT.separator()
        LYT.operator("view3d.view_axis", text="W - Front").type = 'FRONT'
        LYT.operator("view3d.view_axis", text="S - Back").type = 'BACK'

        LYT.separator()
        LYT.operator("view3d.view_axis", text="E - Right").type = 'RIGHT'
        LYT.operator("view3d.view_axis", text="D - Left").type = 'LEFT'


class VIEW3D_MT_VIEW_AXIS_ROLL(Menu):
    bl_label = "Axis Roll"

    def draw(self, context):
        layout = self.layout
        layout.operator("aaa.roll_axis", text="A - X Axis").axis = 'X'
        layout.operator("aaa.roll_axis", text="S - Y Axis").axis = 'Y'
        layout.operator("aaa.roll_axis", text="D - Z Axis").axis = 'Z'


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


class VIEW3D_MT_SELECT(Menu):
    bl_label = "Select"

    def draw(self, context):
        AT = context.area.type
        M = context.mode

        layout = self.layout

        if AT == 'VIEW_3D':
            if M in OBJ:
                layout.operator("object.select_all", text="A - All") \
                    .action = 'SELECT'
                layout.operator("object.select_all", text="S - None") \
                    .action = 'DESELECT'
                layout.operator("object.select_all", text="D - Invert") \
                    .action = 'INVERT'
                layout.operator("object.select_grouped",
                                text="Q - Select Grouped").type = 'PARENT'
            if M in MHE:
                layout.operator("mesh.select_all", text="A - All") \
                    .action = 'SELECT'
                layout.operator("mesh.select_all", text="S - None") \
                    .action = 'DESELECT'
                layout.operator("mesh.select_all", text="D - Invert") \
                    .action = 'INVERT'

                layout.separator()
                layout.operator("mesh.select_linked", text="Q - Linked")

                layout.separator()
                layout.operator("mesh.loop_to_region", text="E - Inner Region")
                layout.operator("mesh.region_to_loop", text="F - Boundary")


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
            layout.operator("view3d.snap_cursor_to_center",
                            text="A - Cursor to Center")
            layout.operator("view3d.snap_cursor_to_selected",
                            text="D - Cursor to Selection")
            layout.operator("view3d.snap_cursor_to_active",
                            text="W - Cursor to Active")
            layout.operator("view3d.snap_selected_to_cursor",
                            text="S - Selection with Offset").use_offset = True


class VIEW3D_MT_PIVOT_POINT(Menu):
    bl_label = "Pivot Point test"

    def draw(self, context):
        LYT = self.layout
        TPV = "bpy.context.scene.tool_settings.transform_pivot_point"

        OP = LYT.operator("aaa.switch_value", text="Q - Bounding Box")
        OP.val_a = TPV
        OP.val_b = "BOUNDING_BOX_CENTER"

        OP = LYT.operator("aaa.switch_value", text="W - Active Element")
        OP.val_a = TPV
        OP.val_b = "ACTIVE_ELEMENT"

        OP = LYT.operator("aaa.switch_value", text="A - Individual Origins")
        OP.val_a = TPV
        OP.val_b = "INDIVIDUAL_ORIGINS"

        OP = LYT.operator("aaa.switch_value", text="S - Median Point")
        OP.val_a = TPV
        OP.val_b = "MEDIAN_POINT"

        OP = LYT.operator("aaa.switch_value", text="D - 3D Cursor")
        OP.val_a = TPV
        OP.val_b = "CURSOR"

        if context.mode == OBJ:
            TS = context.scene.tool_settings
            TS2 = "context.scene.tool_settings"
            LYT.separator()

            STATE = " [ON]" if TS.use_transform_data_origin else " [OFF]"
            LYT.operator("aaa.toggle_prop", text="Z - Only Origins" + STATE) \
                .prop = TS2 + ".use_transform_data_origin"

            STATE = " [ON]" if TS.use_transform_skip_children else " [OFF]"
            LYT.operator("aaa.toggle_prop", text="X - Only Parents" + STATE) \
                .prop = TS2 + ".use_transform_skip_children"

            STATE = " [ON]" if TS.use_transform_pivot_point_align else " [OFF]"
            LYT.operator("aaa.toggle_prop", text="C - Only Locations" + STATE)\
                .prop = TS2 + ".use_transform_pivot_point_align"


class VIEW3D_MT_MHE_MODE(Menu):
    bl_label = "Select Mode"

    def draw(self, context):
        LYT = self.layout

        LYT.operator("mesh.select_mode", text="A - Vertex Select") \
            .type = 'VERT'
        LYT.operator("mesh.select_mode", text="S - Edge Select") \
            .type = 'EDGE'
        LYT.operator("mesh.select_mode", text="D - Face Select")\
            .type = 'FACE'


class VIEW3D_MT_STD_TOOLS(Menu):
    bl_label = "Standard Tools"

    def draw(self, context):
        LYT = self.layout
        M = context.mode

        if M in (MHE):
            LYT.operator_context = 'INVOKE_DEFAULT'

            LYT.operator("mesh.duplicate_move", text="Q - Duplicate")
            LYT.operator("mesh.inset", text="W - Inset")
            LYT.operator("mesh.vert_connect_path", text="E - Connect Path")
            LYT.operator("mesh.split", text="R - Split")

            LYT.separator()
            LYT.operator("mesh.extrude_region_move", text="S - Extrude")
            LYT.operator("mesh.bevel", text="D - Bevel")

            # custom built-in operator call to make sure the active tool switches
            # from the selection ones to the spin tool
            LYT.operator("aaa.std_tools", text="F - Spin") \
                .name = "SPIN_TOOL"

            LYT.separator()
            LYT.operator("mesh.remove_doubles", text="Z - Remove Doubles")
            LYT.operator("wm.call_menu", text="C - Merge") \
                .name = "VIEW3D_MT_edit_mesh_merge"
            LYT.operator("mesh.subdivide", text="v - Subdivide")
        elif M in (OBJ):
            LYT.operator("object.parent_set", text="E - Parent Object") \
                .type = 'OBJECT'
            LYT.operator("object.parent_clear", text="Q - Clear Parent") \
                .type = 'CLEAR'
        elif M in (MHS):
            LYT.label(text="Here will go some sculpting brushes.")
            # LYT.operator("object.parent_clear", text="Q - Clear Parent") \
            #     .type = 'CLEAR'
            
            LYT.operator_context = 'INVOKE_DEFAULT'

            # OP = LYT.operator("brush.asset_activate", text="C - Crease")
            # OP.asset_library_type = "ESSENTIALS"
            # OP.asset_library_identifier = "Crease Sharp"
            # OP.relative_asset_identifier = "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Crease"


            # bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="")

            OP = LYT.operator("brush.asset_activate", text="S - Clay Strips")
            OP.asset_library_type = "ESSENTIALS"
            OP.asset_library_identifier = "Clay Strips"
            OP.relative_asset_identifier = "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Clay Strips"


            

            # bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Crease Sharp")

class VIEW3D_MT_APPLY_CLEAR(Menu):
    bl_label = "Apply or Clear"

    def draw(self, context):
        LYT = self.layout
        MN = "wm.call_menu"

        LYT.operator(MN, text="A - Apply").name = 'VIEW3D_MT_APPLY'
        LYT.operator(MN, text="D - Clear").name = 'VIEW3D_MT_CLEAR'


class VIEW3D_MT_APPLY(Menu):
    bl_label = "Apply"

    def draw(self, context):
        LYT = self.layout

        props = LYT.operator("object.transform_apply", text="Q - All")
        props.location = True
        props.scale = True
        props.rotation = True
        props = LYT.operator("object.transform_apply",
                             text="W - Except Location")
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
        OB = 'object'

        props = LYT.operator(OB+".location_clear", text="A - Location")
        props.clear_delta = False

        props = LYT.operator(OB+".scale_clear", text="S - Scale")
        props.clear_delta = False

        props = LYT.operator(OB+".rotation_clear", text="D - Rotation")
        props.clear_delta = False

        LYT.separator()
        props = LYT.operator(OB+".origin_clear", text="W - Origin to Parent")


classes = (
    VIEW3D_MT_WORKSPACE,
    VIEW3D_MT_MODE,

    VIEW3D_MT_VIEWPORT_DISPLAY,
    VIEW3D_MT_SHADING_OPTIONS,
    VIEW3D_MT_SHADING_OPTIONS_CAVITY,
    VIEW3D_MT_RENDERER,

    VIEW3D_MT_VIEW,
    VIEW3D_MT_VIEW_ALIGN,
    VIEW3D_MT_VIEW_VIEW,
    VIEW3D_MT_VIEW_AXIS_ROLL,

    VIEW3D_MT_TRANSFORM_GIZMO,

    VIEW3D_MT_SELECT,
    VIEW3D_MT_SELECT_MODE,

    VIEW3D_MT_CURSOR_POSITION,

    VIEW3D_MT_PIVOT_POINT,

    VIEW3D_MT_MHE_MODE,
    VIEW3D_MT_STD_TOOLS,

    VIEW3D_MT_APPLY_CLEAR,
    VIEW3D_MT_APPLY,
    VIEW3D_MT_CLEAR,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
