import bpy  # type: ignore
from bpy.types import Menu  # type: ignore
from AAA_utils import TMH, OBJ, MHE, MHS, is_active_type, get_active_mesh

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
            LYT.operator(MS, text="A - Object Mode").mode = "OBJECT"
            LYT.operator(MS, text="S - Edit Mode").mode = "EDIT"
            LYT.operator(MS, text="D - Sculpt Mode").mode = "SCULPT"
            LYT.operator(MS, text="E - Vertex Paint").mode = "VERTEX_PAINT"
            LYT.operator(MS, text="F - Texture Paint").mode = "TEXTURE_PAINT"
        else:
            LYT.label(text="No valid object selected")


class VIEW3D_MT_VIEWPORT_DISPLAY(Menu):
    bl_label = "Viewport Display"

    def draw(self, context):
        LYT = self.layout

        LYT.operator("aaa.toggle_overlays", text="Q - Header").header = "HEADER"
        LYT.operator("aaa.toggle_overlays", text="A - Overlays").header = "OVERLAYS"
        LYT.operator("aaa.toggle_overlays", text="F - Floor").header = "FLOOR"

        LYT.separator()
        LYT.operator(
            "aaa.toggle_prop", text="Z - Face Orientation"
        ).prop = "context.space_data.overlay.show_face_orientation"
        LYT.operator(
            "aaa.toggle_prop", text="W - Wireframes"
        ).prop = "bpy.context.space_data.overlay.show_wireframes"


class VIEW3D_MT_SHADING_OPTIONS(Menu):
    bl_label = "Shading Options"

    def draw(self, context):
        LYT = self.layout

        if is_active_type(context, TMH):
            LYT.operator("object.shade_flat", text="A - Flat")
            LYT.operator("object.shade_smooth", text="S - Smooth")
            if hasattr(bpy.ops.object, "shade_auto_smooth"):
                LYT.operator("object.shade_auto_smooth", text="D - Autosmooth")
            else:
                # Fallback for newer Blender versions where auto-smooth is done via modifiers or attributes
                if get_active_mesh(context):
                    # In 4.1+, auto smooth is driven by modifiers or mesh attributes, but we can display the label or call the modern equivalent if needed
                    # Let's add a toggle for the classic custom split normals or a toggle prop
                    LYT.operator(
                        "object.shade_smooth", text="D - Smooth (Auto)"
                    ).use_auto_smooth = True

        LYT.separator()
        LYT.operator(
            "wm.call_menu", text="C - Cavity Type"
        ).name = "VIEW3D_MT_SHADING_OPTIONS_CAVITY"


class VIEW3D_MT_SHADING_OPTIONS_CAVITY(Menu):
    bl_label = "Cavity Options"

    def draw(self, context):
        LYT = self.layout

        cavity_state = "Disable" if context.space_data.shading.show_cavity else "Enable"

        LYT.operator(
            "aaa.toggle_prop", text="W - " + cavity_state
        ).prop = "context.space_data.shading.show_cavity"

        TEMP = "context.space_data.shading.space_data.shading.cavity_type"  # wait, is it show_cavity or cavity_type? Ah, the original code: TEMP = "context.space_data.shading.cavity_type"
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

        engine_eevee = "BLENDER_EEVEE_NEXT"
        if (
            engine_eevee
            not in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items
        ):
            engine_eevee = "BLENDER_EEVEE"

        LYT.operator(OP, text="W - LookDev").mode = "MATERIAL"
        LYT.operator(OP, text="A - EEVEE").mode = engine_eevee
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
            "aaa.toggle_prop", text="R - Lock Orbit"
        ).prop = "context.space_data.region_3d.lock_rotation"

        LYT.operator(MN, text="X - Axis Roll").name = "VIEW3D_MT_VIEW_AXIS_ROLL"

        LYT.separator()
        LYT.operator_context = "INVOKE_DEFAULT"
        LYT.operator("view3d.walk", text="F - Walk Navigation")
        LYT.operator("view3d.localview", text="Z - Local View")


class VIEW3D_MT_VIEW_ALIGN(Menu):
    bl_label = "Align Normal"

    def draw(self, context):
        LYT = self.layout

        props = LYT.operator("view3d.view_axis", text="Q - Top")
        props.align_active = True
        props.type = "TOP"
        props = LYT.operator("view3d.view_axis", text="A - Bottom")
        props.align_active = True
        props.type = "BOTTOM"

        LYT.separator()
        props = LYT.operator("view3d.view_axis", text="W - Front")
        props.align_active = True
        props.type = "FRONT"
        props = LYT.operator("view3d.view_axis", text="S - Back")
        props.align_active = True
        props.type = "BACK"

        LYT.separator()
        props = LYT.operator("view3d.view_axis", text="E - Right")
        props.align_active = True
        props.type = "RIGHT"
        props = LYT.operator("view3d.view_axis", text="D - Left")
        props.align_active = True
        props.type = "LEFT"


class VIEW3D_MT_VIEW_VIEW(Menu):
    bl_label = "Views"

    def draw(self, context):
        LYT = self.layout
        LYT.operator("view3d.view_axis", text="Q - Top").type = "TOP"
        LYT.operator("view3d.view_axis", text="A - Bottom").type = "BOTTOM"

        LYT.separator()
        LYT.operator("view3d.view_axis", text="W - Front").type = "FRONT"
        LYT.operator("view3d.view_axis", text="S - Back").type = "BACK"

        LYT.separator()
        LYT.operator("view3d.view_axis", text="E - Right").type = "RIGHT"
        LYT.operator("view3d.view_axis", text="D - Left").type = "LEFT"


class VIEW3D_MT_VIEW_AXIS_ROLL(Menu):
    bl_label = "Axis Roll"

    def draw(self, context):
        layout = self.layout
        layout.operator("aaa.roll_axis", text="A - X Axis").axis = "X"
        layout.operator("aaa.roll_axis", text="S - Y Axis").axis = "Y"
        layout.operator("aaa.roll_axis", text="D - Z Axis").axis = "Z"


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
            LYT.operator("aaa.toggle_prop", text="Z - Only Origins" + STATE).prop = (
                TS2 + ".use_transform_data_origin"
            )

            STATE = " [ON]" if TS.use_transform_skip_children else " [OFF]"
            LYT.operator("aaa.toggle_prop", text="X - Only Parents" + STATE).prop = (
                TS2 + ".use_transform_skip_children"
            )

            STATE = " [ON]" if TS.use_transform_pivot_point_align else " [OFF]"
            LYT.operator("aaa.toggle_prop", text="C - Only Locations" + STATE).prop = (
                TS2 + ".use_transform_pivot_point_align"
            )
