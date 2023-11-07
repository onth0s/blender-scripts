# TODO <pep8-80 compliant>

import bpy
from bpy.types import Menu

from AAA_var import *

# 'VIEW3D_' is not necessary, it just looks cleaner this way, 
# because it's the context in which you shall call it

''' Useful API ENUMS
    bpy.context.area.type
        enum in [EMPTY, VIEW_3D, IMAGE_EDITOR, NODE_EDITOR, SEQUENCE_EDITOR, 
        CLIP_EDITOR, DOPESHEET_EDITOR, GRAPH_EDITOR, NLA_EDITOR, TEXT_EDITOR,
        CONSOLE, INFO, TOPBAR, STATUSBAR, OUTLINER, PROPERTIES, FILE_BROWSER,
        PREFERENCES], default VIEW_3D
    bpy.context.mode
        enum in [EDIT_MESH, EDIT_CURVE, EDIT_SURFACE, EDIT_TEXT, EDIT_ARMATURE,
        EDIT_METABALL, EDIT_LATTICE, POSE, SCULPT, PAINT_WEIGHT, PAINT_VERTEX,
        PAINT_TEXTURE, PARTICLE, OBJECT, PAINT_GPENCIL, EDIT_GPENCIL,
        SCULPT_GPENCIL, WEIGHT_GPENCIL], default EDIT_MESH
    bpy.context.object.type
        enum in [MESH, CURVE, SURFACE, META, FONT, ARMATURE, LATTICE, EMPTY,
        GPENCIL, CAMERA, LIGHT, SPEAKER, LIGHT_PROBE], default EMPTY
    '''

class PIE_MT_KEY_CONDITIONS(Menu):
    bl_idname = "PIE_MT_KEY_CONDITIONS"
    bl_label = "Conditions"
    def draw(self, context):
        CN = "aaa.conditions_switcher"
        layout = self.layout

        pie = layout.menu_pie()
        

        pie.operator(CN, text="").cond=""
        pie.operator(CN, text="Transform").cond="TRANSFORM"
        pie.operator("wm.call_menu", text="Sequencer Conds").name = "VIEW3D_MT_SEQUENCER_CONDITIONS"
        pie.operator(CN, text="").cond=""
        pie.operator(CN, text="").cond=""
        pie.operator(CN, text="Layers").cond="LAYERS"
        pie.operator(CN, text="").cond=""
        pie.operator(CN, text="Timeline").cond="TIMELINE"

class PIE_MT_SAVE_N_STUFF(Menu):
    bl_idname = "PIE_MT_SAVE_N_STUFF"
    bl_label = "Save N' Stuff"
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        if context.area.type == 'TEXT_EDITOR':
            pie.operator("text.run_script", text="Run Script")
        else:
            pie.operator("script.reload", text="Reload Scripts")

        pie.operator("aaa.save_file", text="Save")
        
        pie.operator_context = 'INVOKE_DEFAULT'
        pie.operator("wm.open_mainfile", text="Open")

        pie.operator("wm.save_homefile", text="Override Startup")
        pie.operator("import_scene.obj", text="Import OBJ")

        # leave 'app_template' in blank to load the 'startup' file
        pie.operator("wm.read_homefile", text="New File").app_template=""
        pie.operator("wm.append", text="Append")
        pie.operator("aaa.save_incremental", text="Save Incremental")

class PIE_MT_SPACE(Menu):
    bl_idname = "PIE_MT_SPACE"
    bl_label = "General 1"
    def draw(self, context):
        C = context
        M = C.mode
        MN = "wm.call_menu"
        layout = self.layout
        
        pie = layout.menu_pie()

        # gotta check if there are duplicates in 'M in (...)'

        # ------------------------   LEFT   --------------------------------- #
        if M in (OBJ, MHT, MHW, MHV, GPE, GPS, GPP, ARE, ARP, LCE):
            pie.operator_context = 'EXEC_DEFAULT'
            pie.operator("aaa.test_operator", text="TEST OPS")
        if M in (MHE, MHS, GPW, CVE):
            pie.operator(MN, text="").name = ""
        # ------------------------   RIGHT   -------------------------------- #
        if M in (OBJ, MHE, GPE, GPP, ARE, ARP, CVE, LCE):
            pie.operator(MN, text="Transform Gizmo")\
                .name = "VIEW3D_MT_TRANSFORM_GIZMO"
        if M in (MHS, MHT, MHW, MHV, GPS, GPW):
            pie.operator(MN, text="").name = ""
        # ------------------------   BOTTOM   ------------------------------- #
        if M in (OBJ):
            pie.operator("aaa.test_operator", text="TEST OPS")
        if M in (MHE, MHT, MHW, MHV, ARE, ARP, CVE, LCE):
            pie.operator(MN, text="")
        if M in (MHS):
            pie.operator("wm.call_panel", text="Panel?")\
                .name = "VIEW3D_PT_overlays_panel"
        if M in (GPE, GPS, GPW, GPP):
            pie.operator("aaa.apply_modifiers", text="Apply Modifiers")
        # ------------------------   TOP   ---------------------------------- #
        if M in (ALL):
            pie.operator(MN, text="Workspace").name = "VIEW3D_MT_WORKSPACE"
        # ------------------------   TOP-LEFT   ----------------------------- #
        if M in (ALL):
            pie.operator(MN, text="View").name = "VIEW3D_MT_VIEW"
        # ------------------------   TOP-RIGHT   ---------------------------- #
        if M in (OBJ, ARP, CVE, LCE):
            pie.operator(MN, text="")
        if M in (MHS):
            pie.operator_context = 'EXEC_DEFAULT'
            pie.operator("sculpt.dynamic_topology_toggle", text="D - Dynatopo")
        if M in (MHE, MHW, MHV, GPE, GPS, GPW, GPP):
            # TODO Handle properly all of this "modes"
            pie.operator(MN, text="Select Mode")\
                .name = "VIEW3D_MT_SOME_MODES"
        if M in (MHT):
            pie.operator("aaa.toggle_prop", text="D - Face Mask")\
                .prop="context.object.data.use_paint_mask"
        if M in (ARE):
            pie.operator("wm.call_panel", text="Rename")\
                .name = "VIEW3D_PT_rename_bone"
        # ------------------------   BOTTOM-LEFT   -------------------------- #
        if M in (OBJ, MHE, MHV, MHW, GPE, GPS, ARE, ARP, CVE, LCE):
            pie.operator(MN, text="Select").name = "VIEW3D_MT_SELECT"
        if M in (MHT, MHW, GPW, GPP):
            pie.operator(MN, text="").name = ""
        if M in (MHS):
            pie.operator(MN, text="Detailing").name="VIEW3D_MT_MASK_N_STUFF"
        # ------------------------   BOTTOM-RIGHT   ------------------------- #
        if M in (OBJ, MHE, MHT, MHW, MHV, GPE, GPS, ARE, ARP, CVE, LCE):
            pie.operator(MN, text="Select Mode").name = "VIEW3D_MT_SELECT_MODE"
        if M in (MHS, SFE, GPW, GPP, MBE, PTC, TXE):
            pie.operator(MN, text="").name = ""  
class PIE_MT_S(Menu):
    bl_idname = "PIE_MT_S"
    bl_label = "General 2"
    def draw(self, context):
        C = context
        M = C.mode
        MT = "wm.call_menu"
        PT = "wm.call_panel"
        layout = self.layout
        
        pie = layout.menu_pie()

        # ------------------------   LEFT   --------------------------------- #
        if M in (OBJ, MHE, LCE, CVE):
            pie.operator(PT, text="Orientation")\
                .name="VIEW3D_PT_transform_orientations"
        if M in (MHS, MHW, MHV, MHT, ARE, ARP):
            pie.operator(MT, text="").name=""
        if M in (GPE, GPS, GPW, GPP):
            pie.operator(MT, text="Layers").name="VIEW3D_MT_GP_LAYERS_1"
        # ------------------------   RIGHT   -------------------------------- #
        if M in (OBJ, MHT, MHW, MHV, ARE, ARP, LCE):
            pie.operator(MT, text="").name=""
        if M in (MHE, CVE):
            pie.operator(MT, text="Tools").name="VIEW3D_MT_COMMON_MODELING_TOOLS"
        if M in (MHS):
            pie.operator(MT, text="Some Brushes").name="VIEW3D_MT_SOME_BRUSHES"
        if M in (GPE):
            pie.operator(MT, text="Some Ops").name="VIEW3D_MT_GP_OPS"
        if M in (GPS, GPW, GPP):
            pie.operator(MT, text="Tools").name="VIEW3D_MT_GP_TOOLS"
        # ------------------------   BOTTOM   ------------------------------- #
        if M in (OBJ, MHE, GPE, ARE, ARP, CVE, ):
            pie.operator(MT, text="Pivot Point").name="VIEW3D_MT_PIVOT"
        if M in (MHS, MHT, MHW, MHV, GPS, GPW, GPP, LCE):
            pie.operator(MT, text="").name=""
        # ------------------------   TOP   ---------------------------------- #
        if M in (ALL):
            pie.operator(MT, text="Mode").name="VIEW3D_MT_MODE"
        # ------------------------   TOP-LEFT   ----------------------------- #
        if M in (OBJ, MHE, GPE, ARE, ARP, CVE, LCE):
            pie.operator(PT, text="Snapping").name="VIEW3D_PT_snapping"
        if M in (MHS, MHT, MHW, MHV, GPS, GPW, GPP):
            pie.operator(MT, text="").name=""
        # ------------------------   TOP-RIGHT   ---------------------------- #
        if M in (OBJ, MHE, ARE, ARP, CVE, LCE):
            pie.operator(MT, text="").name=""
        if M in (MHS):
            pie.operator(MT, text="Ops").name="VIEW3D_MT_SCULPT_POPOVER"    
        if M in (MHT, MHW, MHV):
            pie.operator(MT, text="").name=""
        if M in (GPE, GPS, GPW, GPP):
            pie.operator(MT, text="Layers").name="VIEW3D_MT_GP_LAYERS_2"
        # ------------------------   BOTTOM-LEFT   -------------------------- #
        if M in (OBJ, MHE, GPE, ARE, ARP, CVE, LCE):
            pie.operator(PT, text="Proportional")\
                .name="VIEW3D_PT_proportional_edit_2"
        if M in (MHS, MHT, MHW, MHV):
            pie.operator(MT, text="").name=""
        if M in (GPS, GPW, GPP):
            pie.operator(MT, text="Select Layers").name="VIEW3D_GP_LAYERS_MT_2"
        # ------------------------   BOTTOM-RIGHT   ------------------------- #
        if M in (OBJ, MHE, GPE, ARE, ARP, CVE, LCE):
            pie.operator(MT, text="Cursor").name="VIEW3D_MT_CURSOR_POSITION"
        if M in (MHS):
            pie.operator(MT, text="Detailing").name="VIEW3D_MT_DYNTOPO_DETAILING"
        if M in (MHT, MHW, MHV, GPS, GPW, GPP, SFE):
            pie.operator(MT, text="").name=""

class VIEW3D_MT_SHADING_PIE(Menu):
    bl_idname = "VIEW3D_MT_SHADING_PIE"
    bl_label = "Viewport Shading"
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("wm.call_panel", text="Color").name = "VIEW3D_PT_color"
        
        pie.operator("wm.call_menu", text="Shading").name = "VIEW3D_MT_SHADING"
        
        pie.operator("wm.call_menu", text="Rendered").name = "VIEW3D_MT_EEVEE_OR_CYCLES"
        pie.operator("wm.call_panel", text="MatCap").name = "VIEW3D_PT_matcap"
        pie.operator("wm.call_panel", text="Background").name = "VIEW3D_PT_background"
            # This probably should be in 'Overlays', not 'Shading'
        pie.operator("wm.call_menu", text="Cycle Visibility")
        pie.operator("wm.call_menu", text="")
        pie.operator("wm.call_menu", text="Options").name = "VIEW3D_MT_SHADING_OPTIONS"    

class VIEW3D_MT_ADD_OBJECT_PIE(Menu):
    bl_idname = "VIEW3D_MT_ADD_OBJECT_PIE"
    bl_label = "Add Object"
    def draw(self, context):
        MT = "wm.call_menu"
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("object.text_add", text="TEXT")
        pie.operator(MT, text="ARMATURE").name = "VIEW3D_MT_ADD_ARMATURE"
        pie.operator(MT, text="LIGHT").name = "VIEW3D_MT_ADD_LIGHT"
        pie.operator(MT, text="GPENCIL").name = "VIEW3D_MT_ADD_GPENCIL"
        pie.operator(MT, text="MISC").name = "VIEW3D_MT_ADD_MISC"
        pie.operator(MT, text="MESH").name = "VIEW3D_MT_ADD_MESH"
        pie.operator("object.camera_add", text="CAMERA")
        pie.operator(MT, text="CURVE").name = "VIEW3D_MT_ADD_CURVE"
    
class VIEW3D_MT_ANIMATION_PIE(Menu):
    bl_idname = "VIEW3D_MT_ANIMATION_PIE"
    bl_label = "Animation"
    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        pie.operator("wm.call_menu", text="")
        pie.operator("wm.call_menu", text="Playback").name = "VIEW3D_MT_ANIMATION_PLAYBACK"
        
        if context.area.type == 'DOPESHEET_EDITOR':
            pie.operator("aaa.toggle_prop", text="test").prop="context.space_data.dopesheet.show_only_selected"
        else:
            pie.operator("wm.call_menu", text="")

        pie.operator("wm.call_menu", text="")
        pie.operator("wm.call_menu", text="dgsasg").name = "VIEW3D_MT_ANIMATION_OPS"
        pie.operator("wm.call_menu", text="About Frames").name="VIEW3D_MT_ABOUT_FRAMES"
        pie.operator("wm.call_menu", text="")
        pie.operator("anim.keyframe_insert_menu", text="Keyframe")
class VIEW3D_MT_TIMELINE_PIE(Menu):
    bl_idname = "VIEW3D_MT_TIMELINE_PIE"
    bl_label = "Timeline"
    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        
        pie.operator_context = 'EXEC_DEFAULT'
        pie.operator("aaa.test_operator", text="TEST OPS")

        # Different Transform Operators per Editor
        if bpy.context.area.type == 'DOPESHEET_EDITOR':
            pie.operator("wm.call_menu", text="Transform").name = "VIEW3D_TIMELINE_TRANSFORM"
        elif bpy.context.area.type == 'GRAPH_EDITOR':
            pie.operator("wm.call_menu", text="Transform").name = "VIEW3D_GRAPH_EDITOR_TRANSFORM"
        else:
            pie.operator("wm.call_menu", text="").name = ""
       
        pie.operator("wm.call_menu", text="").name = ""

        pie.operator("wm.call_menu", text="Workspace").name = "VIEW3D_MT_WORKSPACE"
        pie.operator("wm.call_menu", text="").name = ""
        pie.operator("wm.call_menu", text="").name = ""
        pie.operator("wm.call_menu", text="Select").name = "VIEW3D_MT_SELECT"
        pie.operator("wm.call_menu", text="").name = ""
class VIEW3D_MT_TIMELINE_TEST(Menu):
    bl_idname = "VIEW3D_MT_TIMELINE_TEST"
    bl_label = "Test Pie"
    def draw(self, context):
        layout = self.layout
        OPS = "aaa.test_operator"

        pie = layout.menu_pie()
        pie.operator_context = 'EXEC_DEFAULT'
        
        pie.operator(OPS, text="").testVal = 0
        pie.operator(OPS, text="").testVal = 0
        pie.operator(OPS, text="").testVal = 0
        pie.operator(OPS, text="").testVal = 0
        pie.operator(OPS, text="FADE IN").testVal = 1
        pie.operator("wm.call_menu", text="Strip Tools").name = "VIEW3D_MT_STRIP_TOOLS"
        pie.operator(OPS, text="").testVal = 0
        pie.operator(OPS, text="FADE OUT").testVal = 2


class VIEW3D_MT_GP_BRUSHES_PIE(Menu):
    bl_idname = "VIEW3D_MT_GP_BRUSHES_PIE"
    bl_label = "Some Tools"

    @classmethod
    def poll(cls, context):
        return context.mode in (MHV, MHT, GPP)

    def draw(self, context):
        ST = "aaa.gp_switch_tool"
        TL = "wm.tool_set_by_id"
        SC = context.scene
        M = context.mode
        layout = self.layout

        pie = layout.menu_pie()
                
        if M == MHV:
            pie.operator(TL, text="Draw").name="builtin_brush.Draw"
            pie.operator(TL, text="Draw").name="builtin_brush.Draw"
            pie.operator(TL, text="Draw").name="builtin_brush.Draw"
            pie.operator(TL, text="Draw").name="builtin_brush.Draw"
            pie.operator(TL, text="Draw").name="builtin_brush.Draw"
            pie.operator(TL, text="Draw").name="builtin_brush.Draw"
            pie.operator(TL, text="Draw").name="builtin_brush.Draw"
            pie.operator(TL, text="Draw").name="builtin_brush.Draw"
        if M == MHT:
            pie.operator("wm.call_menu", text="").name=""
            pie.operator("aaa.set_prop", text="Draw").prop_set="context.tool_settings.image_paint.brush = bpy.data.brushes['TexDraw']"
            pie.operator("wm.call_menu", text="").name=""
            pie.operator("wm.call_menu", text="").name=""
            pie.operator("wm.call_menu", text="").name=""
            pie.operator("aaa.set_prop", text="Erase").prop_set="context.tool_settings.image_paint.brush = bpy.data.brushes['TexErase_1']"
            pie.operator("wm.call_menu", text="").name=""
            pie.operator("wm.call_menu", text="").name=""

        if M == GPP:
            for i in range(1, 9):
                exec("pie.operator(ST, text=SC.brush_name_"+str(i)+").name=SC.brush_name_"+str(i))
        
classes = (

    VIEW3D_MT_GP_BRUSHES_PIE,
    
    VIEW3D_MT_TIMELINE_TEST,
    VIEW3D_MT_TIMELINE_PIE,
    VIEW3D_MT_ANIMATION_PIE,
    
    VIEW3D_MT_ADD_OBJECT_PIE,

    VIEW3D_MT_SHADING_PIE,
    
    PIE_MT_S,
    PIE_MT_SPACE,

    PIE_MT_SAVE_N_STUFF,

    PIE_MT_KEY_CONDITIONS,
)
def register():
    for c in classes:
        bpy.utils.register_class(c)
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()