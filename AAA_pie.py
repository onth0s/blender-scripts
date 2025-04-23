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


class PIE_MT_SPACE(Menu):
    bl_idname = "PIE_MT_SPACE"
    bl_label = "General"

    def draw(self, context):
        M = context.mode
        MN = "wm.call_menu"

        pie = self.layout.menu_pie()
        pie.operator_context = 'EXEC_DEFAULT'

        # ------------------------   LEFT   --------------------------------- #
        if M in (OBJ, MHT, MHW, MHV):
            pie.operator("aaa.test_operator", text="TEST OPERATOR")
        if M in (MHE, MHS):
            pie.operator(MN, text="").name = ""

        # ------------------------   RIGHT   -------------------------------- #
        if M in (OBJ, MHE):
            pie.operator(MN, text="Transform Gizmo")\
                .name = "VIEW3D_MT_TRANSFORM_GIZMO"
        if M in (MHS, MHT, MHW, MHV):
            pie.operator(MN, text="").name = ""

        # ------------------------   BOTTOM   ------------------------------- #
        if M in (ALL):
            pie.operator(MN, text="Apply/Clear").name = "VIEW3D_MT_APPLY_CLEAR"

        # ------------------------   TOP   ---------------------------------- #
        if M in (ALL):
            pie.operator(MN, text="Workspace").name = "VIEW3D_MT_WORKSPACE"

        # ------------------------   TOP-LEFT   ----------------------------- #
        if M in (ALL):
            pie.operator(MN, text="View").name = "VIEW3D_MT_VIEW"

        # ------------------------   TOP-RIGHT   ---------------------------- #
        if M in (OBJ):
            pie.operator(MN, text="Object Operations") \
                .name = "VIEW3D_MT_OBJECT_OPERATIONS"
        if M in (MHE):
            pie.operator(MN, text="Select Mode") \
                .name = "VIEW3D_MT_MHE_MODE"

        # ------------------------   BOTTOM-LEFT   -------------------------- #
        if M in (ALL):
            pie.operator(MN, text="Select").name = "VIEW3D_MT_SELECT"

        # ------------------------   BOTTOM-RIGHT   ------------------------- #
        if M in (OBJ, MHE):
            pie.operator(MN, text="Select Mode").name = "VIEW3D_MT_SELECT_MODE"


class PIE_MT_KEY_CONDITIONS(Menu):
    bl_idname = "PIE_MT_KEY_CONDITIONS"
    bl_label = "Conditions"

    def draw(self, context):
        FN = "aaa.conditions_switcher"
        pie = self.layout.menu_pie()

        pie.operator("wm.call_panel", text="Frame Range") \
            .name = "VIEW3D_PT_frame_range"
        
        pie.operator(FN, text="Transform").cond = "TRANSFORM"
        pie.operator(FN, text="").cond = ""
        pie.operator(FN, text="").cond = ""
        pie.operator(FN, text="").cond = ""
        pie.operator(FN, text="").cond = ""
        pie.operator(FN, text="").cond = ""
        pie.operator(FN, text="Timeline").cond = "TIMELINE"


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
        pie.operator("wm.obj_import", text="Import OBJ")

        pie.operator("wm.append", text="Append")

        # leave 'app_template' in blank to load the 'startup' file
        pie.operator("wm.read_homefile", text="New File").app_template = ""
        pie.operator("aaa.save_incremental", text="Save Incremental")


classes = (
    PIE_MT_SPACE,
    PIE_MT_KEY_CONDITIONS,
    PIE_MT_SAVE_N_STUFF,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
