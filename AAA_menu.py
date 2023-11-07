import bpy
from bpy.props import *
from bpy.types import (Menu, Operator)

from AAA_var import *

# 'VIEW3D_MT_MT_' is not necessary, it just looks cleaner

class VIEW3D_MT_WORKSPACE(Menu):
    bl_label = "Workspace"
    def draw(self, context):
        WS = "aaa.switch_workspace"
        layout = self.layout
        
        layout.operator(WS, text="A - Object")   .name="Object"
        layout.operator(WS, text="D - GPencil")  .name="GPencil"

        layout.separator()
        layout.operator(WS, text="V - Video Editing").name="Video Editing"
        
        layout.separator()
        layout.operator(WS, text="F - Full View").name="Full View"
class VIEW3D_MT_MODE(Menu):
    bl_label = "Mode"
    def draw(self, context):
        OBT = context.object.type

        OM = "object.mode_set"
        MS = "aaa.mode_set"

        layout = self.layout

        if OBT == 'MESH':
            layout.operator(MS, text="A - Object Mode").mode='OBJECT'
            layout.operator(MS, text="S - Edit Mode").mode='EDIT'
            layout.operator(MS, text="D - Sculpt Mode").mode='SCULPT'
            layout.operator(MS, text="Q - Texture Paint").mode='TEXTURE_PAINT'
            layout.operator(MS, text="W - Weight Paint").mode='WEIGHT_PAINT'
            layout.operator(MS, text="E - Vertex Paint").mode='VERTEX_PAINT'
        if OBT == 'GPENCIL':
            layout.operator(OM, text="A - Object Mode").mode='OBJECT'
            layout.operator(OM, text="S - Edit Mode").mode='EDIT_GPENCIL'
            layout.operator(OM, text="E - Draw Mode").mode='PAINT_GPENCIL'
            layout.operator(OM, text="D - Sculpt Mode").mode='SCULPT_GPENCIL'
            layout.operator(OM, text="W - Weight Mode").mode='WEIGHT_GPENCIL'
        if OBT == 'ARMATURE':
            layout.operator(OM, text="D - Pose Mode").mode='POSE'
            layout.operator(OM, text="A - Object Mode").mode='OBJECT'
            layout.operator(OM, text="S - Edit Mode").mode='EDIT'
        if OBT == 'CURVE':
            layout.operator(OM, text="A - Object Mode").mode='OBJECT'
            layout.operator(OM, text="S - Edit Mode").mode='EDIT'
        if OBT == 'LATTICE':
            layout.operator(OM, text="A - Object Mode").mode='OBJECT'
            layout.operator(OM, text="S - Edit Mode").mode='EDIT'

class VIEW3D_MT_SELECT(Menu):
    bl_label = "Select"
    def draw(self, context):
        C = context
        AT = C.area.type
        M = C.mode

        layout = self.layout

        if AT == 'VIEW_3D':
            if M in OBJ:
                layout.operator("object.select_all", text="A - All").action='SELECT'
                layout.operator("object.select_all", text="S - None").action='DESELECT'
                layout.operator("object.select_all", text="D - Invert").action='INVERT'
            if M in MHE:
                layout.operator("mesh.select_all", text="A - All").action='SELECT'
                layout.operator("mesh.select_all", text="S - None").action='DESELECT'
                layout.operator("mesh.select_all", text="D - Invert").action='INVERT'

                layout.separator()
                layout.operator("mesh.select_linked", text="Q - Linked")
                
                layout.separator()
                layout.operator("mesh.loop_to_region", text="E - Inner Region")
                layout.operator("mesh.region_to_loop", text="F - Boundary")
            if M in MHV:
                layout.operator("paint.face_select_all", text="A - All").action='SELECT'
                layout.operator("paint.face_select_all", text="S - None").action='DESELECT'
                layout.operator("paint.face_select_all", text="D - Invert").action='INVERT'
            if M in MHW:
                if context.object.data.use_paint_mask_vertex:
                    layout.operator("paint.vert_select_all", text="A - All").action='SELECT'
                    layout.operator("paint.vert_select_all", text="S - None").action='DESELECT'
                    layout.operator("paint.vert_select_all", text="D - Invert").action='INVERT'
                if context.object.data.use_paint_mask:
                    layout.operator("paint.face_select_all", text="A - All").action='SELECT'
                    layout.operator("paint.face_select_all", text="S - None").action='DESELECT'
                    layout.operator("paint.face_select_all", text="D - Invert").action='INVERT'

            if M in (GPE, GPS):
                layout.operator("gpencil.select_all", text="A - All").action='SELECT'
                layout.operator("gpencil.select_all", text="S - None").action='DESELECT'
                layout.operator("gpencil.select_all", text="D - Invert").action='INVERT'

                layout.separator()
                layout.operator("gpencil.select_linked", text="Q - Linked")
            
            if M in CVE:
                layout.operator("curve.select_all", text="A - All").action='SELECT'
                layout.operator("curve.select_all", text="S - None").action='DESELECT'
                layout.operator("curve.select_all", text="D - Invert").action='INVERT'

                layout.separator()
                layout.operator("curve.select_linked", text="Q - Linked")

            if M in LCE:
                layout.operator("lattice.select_all", text="A - All").action='SELECT'
                layout.operator("lattice.select_all", text="S - None").action='DESELECT'
                layout.operator("lattice.select_all", text="D - Invert").action='INVERT'

        if AT == 'GRAPH_EDITOR':
            layout.operator("graph.select_all", text="A - All").action='SELECT'
            layout.operator("graph.select_all", text="S - None").action='DESELECT'
            layout.operator("graph.select_all", text="D - Invert").action='INVERT'
        if AT == 'DOPESHEET_EDITOR':
            layout.operator("action.select_all", text="A - All").action='SELECT'
            layout.operator("action.select_all", text="S - None").action='DESELECT'
            layout.operator("action.select_all", text="D - Invert").action='INVERT'
        if AT == 'SEQUENCE_EDITOR':
            layout.operator("sequencer.select_all", text="A - All").action='SELECT'
            layout.operator("sequencer.select_all", text="S - None").action='DESELECT'
            layout.operator("sequencer.select_all", text="D - Invert").action='INVERT'
class VIEW3D_MT_SELECT_MODE(Menu):
    bl_label = "Select"
    def draw(self, context):
        TL = "wm.tool_set_by_id"

        layout = self.layout
        
        layout.operator(TL, text="A - Lasso").name="builtin.select_lasso"
        layout.operator(TL, text="S - Box").name="builtin.select_box"
        layout.operator(TL, text="D - Circle").name="builtin.select_circle"
        layout.operator(TL, text="W - Default").name="builtin.select"
        
        layout.separator()
        layout.operator(TL, text="E - Cursor").name="builtin.cursor"

class VIEW3D_MT_VIEW(Menu):
    bl_label = ""
    def draw(self, context):
        layout = self.layout

        layout.operator("wm.call_menu", text="Q - Align Normal")\
            .name="VIEW3D_MT_VIEW_ALIGN"
        layout.operator("wm.call_menu", text="W - Views")\
            .name="VIEW3D_MT_VIEW_VIEW"
    
        layout.separator()
        layout.operator("view3d.view_persportho", text="E - Persp/Ortho")

        layout.separator()
        layout.operator("aaa.toggle_prop", text="R - Lock Orbit").prop="context.space_data.region_3d.lock_rotation"
        
        layout.operator("wm.call_menu", text="X - Axis Roll")\
            .name="VIEW3D_MT_VIEW_AXIS_ROLL"

        layout.separator()
        layout.operator("aaa.select_reference_image", text="C - Select Image")
        

        layout.separator()
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("view3d.walk", text="F - Walk Navigation")
class VIEW3D_MT_VIEW_ALIGN(Menu):
    bl_label = "Align Normal"
    def draw(self, context):
        layout = self.layout
        props = layout.operator("view3d.view_axis", text="Q - Top")
        props.align_active = True
        props.type = 'TOP'

        props = layout.operator("view3d.view_axis", text="A - Bottom")
        props.align_active = True
        props.type = 'BOTTOM'

        layout.separator()
        props = layout.operator("view3d.view_axis", text="W - Front")
        props.align_active = True
        props.type = 'FRONT'

        props = layout.operator("view3d.view_axis", text="S - Back")
        props.align_active = True
        props.type = 'BACK'

        layout.separator()
        props = layout.operator("view3d.view_axis", text="E - Right")
        props.align_active = True
        props.type = 'RIGHT'

        props = layout.operator("view3d.view_axis", text="D - Left")
        props.align_active = True
        props.type = 'LEFT'
class VIEW3D_MT_VIEW_VIEW(Menu):
    bl_label = "Views"
    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.view_axis", text="Q - Top").type = 'TOP'
        layout.operator("view3d.view_axis", text="A - Bottom").type = 'BOTTOM'

        layout.separator()
        layout.operator("view3d.view_axis", text="W - Front").type = 'FRONT'
        layout.operator("view3d.view_axis", text="S - Back").type = 'BACK'

        layout.separator()
        layout.operator("view3d.view_axis", text="E - Right").type = 'RIGHT'
        layout.operator("view3d.view_axis", text="D - Left").type = 'LEFT'
class VIEW3D_MT_VIEW_AXIS_ROLL(Menu):
    bl_label = "Axis Roll"
    def draw(self, context):
        layout = self.layout
        layout.operator("aaa.roll_axis", text="A - X Axis").axis='X'
        layout.operator("aaa.roll_axis", text="S - Y Axis").axis='Y'
        layout.operator("aaa.roll_axis", text="D - Z Axis").axis='Z'

class VIEW3D_MT_TRANSFORM_GIZMO(Menu):
    bl_label = "Gizmo"
    def draw(self, context):
        TL = "wm.tool_set_by_id"

        layout = self.layout

        layout.operator(TL, text="W - Transform").name="builtin.transform"

        layout.separator()
        layout.operator(TL, text="A - Move").name="builtin.move"
        layout.operator(TL, text="S - Scale").name="builtin.scale"
        layout.operator(TL, text="D - Rotate").name="builtin.rotate"

class VIEW3D_MT_SOME_MODES(Menu):
    bl_label = "Select Mode"
    def draw(self, context):
        layout = self.layout
        C = context
        M = C.mode

        if M in (MHE):
            layout.operator("mesh.select_mode", text="A - Vertex Select").type='VERT'
            layout.operator("mesh.select_mode", text="S - Edge Select").type='EDGE'
            layout.operator("mesh.select_mode", text="D - Face Select").type='FACE'
        if M in (MHV, MHW):
            layout.operator("aaa.toggle_prop", text="A - Vertex").prop="context.object.data.use_paint_mask_vertex"
            layout.operator("aaa.toggle_prop", text="D - Face").prop="context.object.data.use_paint_mask" 
        if M in (GPE, GPS):
            if M in GPE:
                layout.operator("aaa.mode_gp_switcher", text="A - Point").mode="POINT"
                layout.operator("aaa.mode_gp_switcher", text="S - Stroke").mode="STROKE"
                layout.operator("aaa.mode_gp_switcher", text="D - Segment").mode="SEGMENT"
            if M in GPS:
                layout.operator("aaa.toggle_prop", text="A - Point").prop="context.scene.tool_settings.use_gpencil_select_mask_point"
                layout.operator("aaa.toggle_prop", text="S - Point").prop="context.scene.tool_settings.use_gpencil_select_mask_stroke"
                layout.operator("aaa.toggle_prop", text="D - Segment").prop="context.scene.tool_settings.use_gpencil_select_mask_segment"

            layout.separator()
            layout.operator("aaa.toggle_prop", text="F - Multi Frame").prop="context.object.data.use_multiedit"
            layout.prop(context.scene.tool_settings.gpencil_sculpt,\
                "use_multiframe_falloff", text="Use Falloff")
        if M in (GPW):
            layout.operator("aaa.toggle_multi_frame_edit", text="F - Multi Frame")
            layout.prop(context.scene.tool_settings.gpencil_sculpt,\
                "use_multiframe_falloff", text="Use Falloff")
        if M in (GPP):
            layout.operator("aaa.toggle_prop", text="A - Draw on Back")\
                .prop="context.scene.tool_settings.use_gpencil_draw_onback"
            layout.operator("aaa.toggle_prop", text="S - Add Weight Data")\
                .prop="context.scene.tool_settings.use_gpencil_weight_data_add"
            layout.operator("aaa.toggle_prop", text="D - Additive Drawing")\
                .prop="context.scene.tool_settings.use_gpencil_draw_additive"

class VIEW3D_MT_SHADING(Menu):
    bl_label = "Shading..."
    def draw(self, context):
        C = context
        M = C.mode

        layout = self.layout

        global solid_wire

        layout.operator("aaa.toggle_overlays", text="Q - Header").header=True
        layout.operator("aaa.toggle_overlays", text="A - Overlays").header=False
        
        layout.separator()
        layout.operator("aaa.toggle_xray", text="S - XRay")

        if C.scene.solidwireframe:
            solid_wire = "Wireframe"
        else:
            solid_wire = "Solid"    
        layout.operator("aaa.toggle_solid_wireframe", text="D - "+solid_wire)
       
        layout.separator()
        layout.operator("aaa.toggle_wireframe_overlay", text="C - Wireframe").mode="ALL_EDGES"
        layout.operator("aaa.toggle_wireframe_overlay", text="V - Optimal Display").mode="CONTROL_EDGES"

        if M in (GPE, GPS, GPW):
            layout.separator()
            layout.operator("aaa.toggle_prop", text="F - GP Wireframe").prop="context.space_data.overlay.use_gpencil_edit_lines"
            layout.operator("aaa.toggle_prop", text="T - GP Stroke Direction").prop="context.object.data.show_stroke_direction"
class VIEW3D_MT_SHADING_OPTIONS(Menu):
    bl_label = "Shading Options"
    def draw(self, context):
        layout = self.layout
        if context.object.type == 'MESH':
            layout.operator("aaa.toggle_prop", text="D - Autosmooth").prop="context.object.data.use_auto_smooth"
            layout.prop(context.object.data, "auto_smooth_angle", text="Angle")
        
            layout.separator()
        layout.operator("wm.call_menu", text="C - Cavity Type").name="VIEW3D_MT_SHADING_OPTIONS_CAVITY"
class VIEW3D_MT_SHADING_OPTIONS_CAVITY(Menu):
    bl_label = "Cavity Options"
    
    def draw(self, context):
        layout = self.layout

        global cavity_state

        if bpy.context.space_data.shading.show_cavity:
            cavity_state = "Disable"
        else:
            cavity_state = "Enable"
        layout.operator("aaa.cavity_type", text="W - "+cavity_state).mode="TOGGLE"

        layout.separator()
        layout.operator("aaa.cavity_type", text="A - World").mode="WORLD"
        layout.operator("aaa.cavity_type", text="S - Screen").mode="SCREEN"
        layout.operator("aaa.cavity_type", text="D - Both").mode="BOTH"

class VIEW3D_MT_COMMON_MODELING_TOOLS(Menu):
    bl_label = "Modeling Tools"
    def draw(self, context):
        layout = self.layout
        layout.operator("aaa.common_tools", text="W - Inset").name="INSET"
        layout.operator("aaa.common_tools", text="D - Bevel").name="BEVEL"
        layout.operator("aaa.common_tools", text="S - Extrude").name="EXTRUDE"
        layout.operator("wm.call_menu", text="C - Merge").name="VIEW3D_MT_MERGE"
        layout.operator("aaa.common_tools", text="E - Connect Path").name="CONNECT_PATH"
        layout.operator("aaa.common_tools", text="Q - Duplicate").name="DUPLICATE"
        layout.operator("aaa.common_tools", text="X - Subdivide").name="SUBDIVIDE"
        layout.operator("aaa.common_tools", text="Z - Remove Doubles").name="REMOVE_DOUBLES"

class VIEW3D_MT_CURSOR_POSITION(Menu):
    bl_label = "Cursor Position"
    def draw(self, context):
        M = context.mode
        layout = self.layout
        
        if M in (OBJ, MHE, CVE):
            layout.operator("view3d.snap_cursor_to_center", text="A - Cursor to Center")
            layout.operator("view3d.snap_cursor_to_selected", text="D - Cursor to Selection")
            layout.operator("view3d.snap_cursor_to_active", text="W - Cursor to Active")
            layout.operator("view3d.snap_selected_to_cursor", text="S - Selection with Offset").use_offset=True
        if M in (GPE, GPS, GPP):
            layout.operator("view3d.snap_cursor_to_center", text="A - Cursor to Center")
            layout.operator("gpencil.snap_cursor_to_selected", text="D - Cursor to Selection")
            layout.operator("gpencil.snap_to_cursor", text="S - Selection to Cursor").use_offset=False
class VIEW3D_MT_MERGE(Menu):
    bl_label = "Merge"
    # TODO Handle properly the edit mode selection 
    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.merge", text="Q - Center").type='CENTER'
        layout.operator("mesh.merge", text="S - Last").type='LAST'
        layout.operator("mesh.merge", text="A - First").type='FIRST'
        layout.operator("mesh.merge", text="E - Cursor").type='CURSOR'
        layout.operator("mesh.merge", text="F - Collapse").type='COLLAPSE'
        
        layout.separator()
        layout.operator("mesh.remove_doubles", text="W - By Distance").type='FIRST'
class VIEW3D_MT_PIVOT(Menu):
    bl_label = "Pivot Point"
    def draw(self, context):
        PS = "aaa.pivot_selector"

        layout = self.layout
        layout.operator(PS, text="A - Individual Origins").name='INDIVIDUAL_ORIGINS'
        layout.operator(PS, text="S - Median Point").name='MEDIAN_POINT'
        layout.operator(PS, text="D - Cursor").name='CURSOR'
        layout.operator(PS, text="W - Active Element").name='ACTIVE_ELEMENT'
        layout.operator(PS, text="Q - Bounding Box").name='BOUNDING_BOX_CENTER'

        layout.separator()
        layout.operator(PS, text="F - Only Origins").name='ONLY_ORIGINS'

class VIEW3D_MT_SOME_BRUSHES(Menu):
    bl_label = ""
    def draw(self, context):
        TL = "wm.tool_set_by_id"
        layout = self.layout

        layout.operator(TL, text="S - Clay").name="builtin_brush.Clay Strips"

        layout.separator()
        layout.operator(TL, text="A - Crease").name="builtin_brush.Crease"
        layout.operator(TL, text="Q - Pinch").name="builtin_brush.Pinch"
        layout.operator(TL, text="D - Grab").name="builtin_brush.Grab"
        layout.operator(TL, text="W - Inflate").name="builtin_brush.Inflate"
        
        layout.separator()
        layout.operator(TL, text="Z - Scrape").name="builtin_brush.Scrape"
        layout.operator(TL, text="X - Fill").name="builtin_brush.Fill"
        layout.operator(TL, text="C - Flatten").name="builtin_brush.Flatten"

        layout.separator()
        layout.operator(TL, text="R - Smooth").name="builtin_brush.Smooth"
        layout.operator(TL, text="V - Simplify").name="builtin_brush.Simplify"
        layout.operator(TL, text="E - Mask").name="builtin_brush.Mask"
        layout.operator(TL, text="F - Box Mask").name="builtin.box_mask"   
        layout.operator(TL, text="T - Box Hide").name="builtin.box_hide"   
class VIEW3D_MT_MASK_N_STUFF(Menu):
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        layout.operator("paint.mask_flood_fill", text="D - Invert").mode='INVERT'
        props = layout.operator("paint.mask_flood_fill", text="S - Clear")
        props.mode='VALUE'
        props.value=0
        props = layout.operator("paint.hide_show", text="A - Hide Masked")
        props.action='HIDE'
        props.area='MASKED'
        props = layout.operator("paint.hide_show", text="C - Show All")
        props.action='SHOW'
        props.area='INSIDE'
class VIEW3D_MT_DYNTOPO_DETAILING(Menu):
    bl_label = ""
    def draw(self, context):
        DD = "aaa.dyntopo_detailing"
        layout = self.layout
        layout.operator(DD, text="W - Sample").mode='SAMPLE'
        layout.separator()
        layout.operator(DD, text="A - Collapse").mode='COLLAPSE'
        layout.operator(DD, text="S - Subdivide Collapse").mode='SUBDIVIDE_COLLAPSE'
        layout.operator(DD, text="D - Subdivide").mode='SUBDIVIDE'
class VIEW3D_MT_SCULPT_POPOVER(Menu):
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        layout.operator("wm.call_panel", text="A - Random Settings").name='VIEW3D_PT_sculpt_popup'
        layout.prop(context.tool_settings.sculpt, "constant_detail_resolution", text="Dynatopo Resolution")

class VIEW3D_MT_EEVEE_OR_CYCLES(Menu):
    bl_label = ""
    def draw(self, context):
        EC = "aaa.eevee_or_cycles"
        layout = self.layout
        layout.operator(EC, text="A - EEVEE").mode="BLENDER_EEVEE"
        layout.operator(EC, text="S - Workbench").mode="BLENDER_WORKBENCH"
        layout.operator(EC, text="D - Cycles").mode="CYCLES"
        layout.operator(EC, text="W - LookDev").mode="MATERIAL"

class VIEW3D_MT_ANIMATION_PLAYBACK(Menu):
    bl_label = "Shading Options"
    def draw(self, context):
        layout = self.layout
        layout.operator("screen.animation_play", text="D - Play")
        layout.operator("screen.frame_jump", text="A - Jump Start").end=False
        layout.operator("screen.frame_jump", text="Q - Jump End").end=True
        layout.operator("screen.animation_play", text="E - Reverse").reverse=True
class VIEW3D_MT_ANIMATION_OPS(Menu):
    bl_label = "Set Frame.."
    def draw(self, context):
        layout = self.layout
        layout.operator("anim.start_frame_set", text="A - Start")
        layout.operator("anim.end_frame_set", text="D - End")
class VIEW3D_MT_TIMELINE_TRANSFORM(Menu):
    bl_label = "Transform"
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("transform.transform", text="S - esScale").mode="TIME_SCALE" 
        layout.operator("transform.transform", text="A - Move").mode="TIME_TRANSLATE" 
class VIEW3D_MT_GRAPH_EDITOR_TRANSFORM(Menu):
    bl_label = "Transformasda"
    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("transform.translate", text="A - Translate")
        layout.operator("transform.resize", text="S - Scale")
        layout.operator("transform.rotate", text="D - Rotate")
class VIEW3D_MT_ABOUT_FRAMES(Menu):
    bl_label = "Frame..."
    def draw(self, context):
        layout = self.layout
        layout.operator("wm.call_panel", text="D - Rate").name="VIEW3D_PT_gp_frame_rate"
        layout.operator("aaa.toggle_prop", text="A - Preview").prop="context.scene.use_preview_range"
        layout.operator("wm.call_panel", text="F - Range").name="VIEW3D_PT_gp_frame_range"
        
        if bpy.context.area.type != 'VIEW_3D':
            layout.separator()
            layout.operator("wm.call_menu", text="S - Bounds").name="VIEW3D_MT_ANIMATION_OPS"

            layout.operator_context = 'INVOKE_DEFAULT'
            layout.operator("anim.previewrange_set", text="W - Set Bounds")

class VIEW3D_MT_STRIP_TOOLS(Menu):
    bl_label = "Strip Tools"
    def draw(self, context):
        lyt = self.layout
        # lyt.operator_context = 'EXEC_DEFAULT'
        lyt.operator_context = 'INVOKE_REGION_WIN'

        props = lyt.operator("sequencer.split", text="E - Split")
        props.type = 'SOFT'
    
        # bpy.ops.sequencer.split(type='SOFT', side='RIGHT')
class VIEW3D_MT_SEQUENCER_CONDITIONS(Menu):
    bl_label = "Strip Tools"
    def draw(self, context):
        lyt = self.layout
        lyt.operator("aaa.conditions_switcher_sequencer", text="Q - Ignore Markers")

class VIEW3D_MT_GP_OPS(Menu):
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("gpencil.interpolate_sequence", text="A - Sequence") 
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("gpencil.interpolate", text="S - Interpolate")

        
        layout.separator()
        layout.operator("aaa.gp_set_strokes_opacity", text="V - Strokes Opacity 1")

class VIEW3D_MT_GP_TOOLS(Menu):
    bl_label = ""
    def draw(self, context):
        M = context.mode
        TL = "wm.tool_set_by_id"
        layout = self.layout
        # if M in (GPE):
        #     layout.operator(TL, text="R - Smooth").name="builtin_brush.Smooth"
        if M in (GPS):
            layout.operator(TL, text="R - Smooth").name="builtin_brush.Smooth"
            layout.operator(TL, text="F - Thickness").name="builtin_brush.Thickness"
            layout.operator(TL, text="R - Strength").name="builtin_brush.Strength"
            layout.operator(TL, text="R - Randomize").name="builtin_brush.Randomize"
            layout.operator(TL, text="E - Grab").name="builtin_brush.Grab"
            layout.operator(TL, text="D - Push").name="builtin_brush.Push"
            layout.operator(TL, text="R - Twist").name="builtin_brush.Twist"
            layout.operator(TL, text="R - Pinch").name="builtin_brush.Pinch"
            layout.operator(TL, text="R - Clone").name="builtin_brush.Clone"
        if M in (GPP):
            layout.operator("wm.call_menu", text="S - Draw").name="VIEW3D_MT_GP_BRUSHES"
            layout.operator(TL, text="D - Erase").name="builtin_brush.Erase"
            layout.operator(TL, text="A - Cutter").name="builtin.cutter"
            layout.operator(TL, text="F - Fill").name="builtin_brush.Fill"
            
            layout.separator()
            layout.operator(TL, text="W - Line").name="builtin.line"
            layout.operator(TL, text="D - Arc").name="builtin.arc"
            layout.operator(TL, text="E - Curve").name="builtin.curve"
            layout.operator(TL, text="C - Box").name="builtin.box"
            layout.operator(TL, text="V - Circle").name="builtin.circle"
        
class VIEW3D_MT_GP_BRUSH_1(Menu):
    bl_label = ""
    def draw(self, context):
        # gpencil_tool = {DRAW, FILL, ERASE}
        layout = self.layout
        for i in range(len(bpy.data.brushes)):
            if bpy.data.brushes[i].gpencil_settings is not None\
                and bpy.data.brushes[i].gpencil_tool == 'DRAW':
                props = layout.operator("aaa.gp_set_tool_1", text=bpy.data.brushes[i].name)
                props.name = bpy.data.brushes[i].name        
class VIEW3D_MT_GP_BRUSH_2(Menu):
    bl_label = ""
    def draw(self, context):
        # gpencil_tool = {DRAW, FILL, ERASE}
        layout = self.layout
        for i in range(len(bpy.data.brushes)):
            if bpy.data.brushes[i].gpencil_settings is not None\
                and bpy.data.brushes[i].gpencil_tool == 'DRAW':
                props = layout.operator("aaa.gp_set_tool_2", text=bpy.data.brushes[i].name)
                props.name = bpy.data.brushes[i].name        
class VIEW3D_MT_GP_BRUSH_3(Menu):
    bl_label = ""
    def draw(self, context):
        # gpencil_tool = {DRAW, FILL, ERASE}
        layout = self.layout
        for i in range(len(bpy.data.brushes)):
            if bpy.data.brushes[i].gpencil_settings is not None\
                and bpy.data.brushes[i].gpencil_tool == 'DRAW':
                props = layout.operator("aaa.gp_set_tool_3", text=bpy.data.brushes[i].name)
                props.name = bpy.data.brushes[i].name        
class VIEW3D_MT_GP_BRUSH_4(Menu):
    bl_label = ""
    def draw(self, context):
        # gpencil_tool = {DRAW, FILL, ERASE}
        layout = self.layout
        for i in range(len(bpy.data.brushes)):
            if bpy.data.brushes[i].gpencil_settings is not None\
                and bpy.data.brushes[i].gpencil_tool == 'DRAW':
                props = layout.operator("aaa.gp_set_tool_4", text=bpy.data.brushes[i].name)
                props.name = bpy.data.brushes[i].name        
class VIEW3D_MT_GP_BRUSH_5(Menu):
    bl_label = ""
    def draw(self, context):
        # gpencil_tool = {DRAW, FILL, ERASE}
        layout = self.layout
        for i in range(len(bpy.data.brushes)):
            if bpy.data.brushes[i].gpencil_settings is not None\
                and bpy.data.brushes[i].gpencil_tool == 'DRAW':
                props = layout.operator("aaa.gp_set_tool_5", text=bpy.data.brushes[i].name)
                props.name = bpy.data.brushes[i].name        
class VIEW3D_MT_GP_BRUSH_6(Menu):
    bl_label = ""
    def draw(self, context):
        # gpencil_tool = {DRAW, FILL, ERASE}
        layout = self.layout
        for i in range(len(bpy.data.brushes)):
            if bpy.data.brushes[i].gpencil_settings is not None\
                and bpy.data.brushes[i].gpencil_tool == 'DRAW':
                props = layout.operator("aaa.gp_set_tool_6", text=bpy.data.brushes[i].name)
                props.name = bpy.data.brushes[i].name
class VIEW3D_MT_GP_BRUSH_7(Menu):
    bl_label = ""
    def draw(self, context):
        # gpencil_tool = {DRAW, FILL, ERASE}
        layout = self.layout
        for i in range(len(bpy.data.brushes)):
            if bpy.data.brushes[i].gpencil_settings is not None\
                and bpy.data.brushes[i].gpencil_tool == 'DRAW':
                props = layout.operator("aaa.gp_set_tool_7", text=bpy.data.brushes[i].name)
                props.name = bpy.data.brushes[i].name
class VIEW3D_MT_GP_BRUSH_8(Menu):
    bl_label = ""
    def draw(self, context):
        # gpencil_tool = {DRAW, FILL, ERASE}
        layout = self.layout
        for i in range(len(bpy.data.brushes)):
            if bpy.data.brushes[i].gpencil_settings is not None\
                and bpy.data.brushes[i].gpencil_tool == 'DRAW':
                props = layout.operator("aaa.gp_set_tool_8", text=bpy.data.brushes[i].name)
                props.name = bpy.data.brushes[i].name

class VIEW3D_MT_GP_MATERIALS(Menu):
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        layout.operator("aaa.gp_switch_material", text="D - Black Flow Stroke").name='Black Flow Stroke'
        layout.operator("aaa.gp_switch_material", text="S - Grey Opacity Stroke").name='Grey Opacity Stroke'
        layout.operator("aaa.gp_switch_material", text="W - Grey Fill").name='Grey Fill'
class VIEW3D_MT_GP_LAYERS_1(Menu):
    bl_label = "Layer..."
    def draw(self, context):
        layout = self.layout

        layout.operator("wm.call_panel", text="D - Opacity").name="VIEW3D_PT_gp_layer_1"
        layout.operator("wm.call_panel", text="R - Rename").name="VIEW3D_PT_rename_gp_layer"
        layout.operator("aaa.gp_layer_separate_selection", text="V - Separate")

        layout.separator()
        layout.operator("gpencil.layer_isolate", text="Z - Lock Isolate").affect_visibility=False
        layout.operator("aaa.toggle_prop", text="    - Lock Layer").prop="context.active_gpencil_layer.lock"
        layout.operator("gpencil.layer_isolate", text="F - Hide Isolate").affect_visibility=True
        layout.operator("aaa.toggle_prop", text="    - Hide").prop="context.active_gpencil_layer.hide"

        layout.separator()
        layout.operator("aaa.gp_layer_unlocked_move", text="G - Move Unlocked")

        layout.separator()
        layout.operator("gpencil.blank_frame_add", text="C - Blank Keyframe")
        layout.operator("aaa.toggle_prop", text="T - Onion Skinning").prop="context.active_gpencil_layer.use_onion_skinning"
class VIEW3D_MT_GP_LAYERS_2(Menu):
    bl_label = "GPencil..."
    def draw(self, context):
        layout = self.layout
        layout.operator("aaa.on_call_gp_layers_panel", text="A - Object")
        layout.operator("wm.call_panel", text="D - Layer").name="VIEW3D_PT_gpencil_layers"
        
class VIEW3D_MT_ADD_MESH(Menu):
    bl_label = "Add Mesh..."
    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.primitive_cube_add", text="D - Cube")
        layout.operator("mesh.primitive_cylinder_add", text="W - Cylinder")
        layout.operator("mesh.primitive_torus_add", text="Z - Torus")
        layout.operator("mesh.primitive_circle_add", text="Z - Circle")
        
        layout.operator("mesh.primitive_uv_sphere_add", text="Z - UV Sphere")
        layout.operator("mesh.primitive_ico_sphere_add", text="E - Icosphere")

        layout.separator()
        layout.operator("mesh.primitive_plane_add", text="F - Plane")
        layout.operator("mesh.primitive_grid_add", text="Z - Grid")
        
        layout.separator()
        layout.operator("mesh.primitive_monkey_add", text="Z - Suzane")
class VIEW3D_MT_ADD_ARMATURE(Menu):
    bl_label = "Add Armature..."
    def draw(self, context):
        layout = self.layout
        layout.operator("object.armature_add", text="D - Single Bone")

        layout.separator()
        layout.operator("object.armature_human_metarig_add", text="W - Human Meta-Rig")
        layout.operator("object.armature_basic_human_metarig_add", text="S - Basic Human Meta-Rig")
class VIEW3D_MT_ADD_CURVE(Menu):
    bl_label = "Add Curve..."
    def draw(self, context):
        layout = self.layout
        layout.operator("curve.primitive_bezier_curve_add", text="D - Bézier Curve")
        layout.operator("curve.primitive_bezier_circle_add", text="S - Bézier Circle")
class VIEW3D_MT_ADD_GPENCIL(Menu):
    bl_label = "Add GPencil..."
    def draw(self, context):
        layout = self.layout
        layout.operator("aaa.on_add_gp_object", text="D - Empty").type1='EMPTY'
        layout.operator("aaa.on_add_gp_object", text="S - Stroke").type1='STROKE'
        layout.operator("aaa.on_add_gp_object", text="A - Suzane").type1='MONKEY'
class VIEW3D_MT_ADD_LIGHT(Menu):
    bl_label = "Add Light..."
    def draw(self, context):
        layout = self.layout
        layout.operator("object.light_add", text="D - Point").type='POINT'
        layout.operator("object.light_add", text="D - Sun").type='SUN'
        layout.operator("object.light_add", text="D - Spot").type='SPOT'
        layout.operator("object.light_add", text="D - Area").type='AREA'

        layout.separator()
        layout.operator("object.lightprobe_add", text="D - Reflection Cubemap").type='CUBEMAP'
        layout.operator("object.lightprobe_add", text="D - Reflection Plane").type='PLANAR'
        layout.operator("object.lightprobe_add", text="D - Irradiance Volume").type='GRID'
class VIEW3D_MT_ADD_MISC(Menu):
    bl_label = "Add Miscellaneous..."
    def draw(self, context):
        layout = self.layout
        layout.operator("object.empty_add", text="D - Empty").type='PLAIN_AXES'

        layout.separator()
        layout.operator("object.add", text="W - Lattice").type='LATTICE'
        
        layout.separator()
        layout.operator_menu_enum("object.effector_add", "type", text="F - Force Field", icon='OUTLINER_OB_FORCE_FIELD')
        
        layout.separator()
        layout.operator("object.speaker_add", text="T - Speaker")

class VIEW3D_MT_PRESETS_BACKGROUND(Menu):
    bl_label = "Background Presets"
    preset_subdir = "scene/background"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset
class VIEW3D_MT_PRESETS_OVERLAYS(Menu):
    bl_label = "Overlays Presets"
    preset_subdir = "scene/overlays"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset
class VIEW3D_MT_PRESETS_FRAME_RANGE_PREVIEW(Menu):
    bl_label = "Preview Range Presets"
    preset_subdir = "scene/frame_range_preview"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset

classes = (

    VIEW3D_MT_PRESETS_FRAME_RANGE_PREVIEW,
    VIEW3D_MT_PRESETS_OVERLAYS,
    VIEW3D_MT_PRESETS_BACKGROUND,

    VIEW3D_MT_ADD_MISC,
    VIEW3D_MT_ADD_LIGHT,
    VIEW3D_MT_ADD_GPENCIL,
    VIEW3D_MT_ADD_CURVE,
    VIEW3D_MT_ADD_ARMATURE,
    VIEW3D_MT_ADD_MESH,

    VIEW3D_MT_GP_LAYERS_2,
    VIEW3D_MT_GP_LAYERS_1,
    VIEW3D_MT_GP_MATERIALS,

    VIEW3D_MT_GP_BRUSH_1,
    VIEW3D_MT_GP_BRUSH_2,
    VIEW3D_MT_GP_BRUSH_3,
    VIEW3D_MT_GP_BRUSH_4,
    VIEW3D_MT_GP_BRUSH_5,
    VIEW3D_MT_GP_BRUSH_6,
    VIEW3D_MT_GP_BRUSH_7,
    VIEW3D_MT_GP_BRUSH_8,
    
    VIEW3D_MT_GP_TOOLS,
    VIEW3D_MT_GP_OPS,

    VIEW3D_MT_SEQUENCER_CONDITIONS, 
    VIEW3D_MT_STRIP_TOOLS,

    VIEW3D_MT_ABOUT_FRAMES,
    VIEW3D_MT_GRAPH_EDITOR_TRANSFORM,
    VIEW3D_MT_TIMELINE_TRANSFORM,
    VIEW3D_MT_ANIMATION_OPS,
    VIEW3D_MT_ANIMATION_PLAYBACK,

    VIEW3D_MT_EEVEE_OR_CYCLES,

    VIEW3D_MT_SCULPT_POPOVER,
    VIEW3D_MT_DYNTOPO_DETAILING,
    VIEW3D_MT_MASK_N_STUFF,
    VIEW3D_MT_SOME_BRUSHES,
    
    VIEW3D_MT_PIVOT,
    VIEW3D_MT_MERGE,
    VIEW3D_MT_CURSOR_POSITION,

    VIEW3D_MT_COMMON_MODELING_TOOLS,

    VIEW3D_MT_SHADING_OPTIONS_CAVITY,
    VIEW3D_MT_SHADING_OPTIONS,
    VIEW3D_MT_SHADING,
    
    VIEW3D_MT_SOME_MODES,
    
    VIEW3D_MT_TRANSFORM_GIZMO,
    
    VIEW3D_MT_VIEW_AXIS_ROLL,
    VIEW3D_MT_VIEW_VIEW,
    VIEW3D_MT_VIEW_ALIGN,
    VIEW3D_MT_VIEW,
    
    VIEW3D_MT_SELECT_MODE,
    VIEW3D_MT_SELECT,
    
    VIEW3D_MT_MODE,
    VIEW3D_MT_WORKSPACE,
)
def register():
    for c in classes:
        bpy.utils.register_class(c)
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()
