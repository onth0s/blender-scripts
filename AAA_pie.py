import bpy # type: ignore
from bpy.types import Menu # type: ignore

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
        pie = self.layout.menu_pie()

        pie.operator('wm.call_menu', text="")
        pie.operator('wm.call_menu', text="")
        pie.operator('wm.call_menu', text="")
        pie.operator('wm.call_menu', text="")
        pie.operator('wm.call_menu', text="")
        pie.operator('wm.call_menu', text="")
        pie.operator('wm.call_menu', text="")
        pie.operator('wm.call_menu', text="")

classes = (
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