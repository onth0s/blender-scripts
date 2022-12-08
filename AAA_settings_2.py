import bpy
from bpy.props import (
    IntProperty, FloatProperty, 
    BoolProperty, StringProperty, 
    EnumProperty, CollectionProperty, 
    PointerProperty)
from bpy.types import (Operator, PropertyGroup, UIList)

class TestSettings(PropertyGroup):
    def updateFPSBase(self, context):
        bpy.context.scene.render.fps_base = 1/bpy.data.scenes[0].fps_base   
    def updateFPSBaseEnum(self, context):
        if context.scene.fps_base_enum == '1':
            context.scene.fps_base=0.25
        if context.scene.fps_base_enum == '2':
            context.scene.fps_base=0.50
        if context.scene.fps_base_enum == '3':
            context.scene.fps_base=1
        if context.scene.fps_base_enum == '4':
            context.scene.fps_base=1.5
        if context.scene.fps_base_enum == '5':
            context.scene.fps_base=2    

    def updateGPLayerOpacity(self, context): 
        for i in range(len(context.gpencil_data.layers)):
            if context.gpencil_data.layers[i] != context.active_gpencil_layer:
                context.gpencil_data.layers[i].opacity = bpy.data.scenes[0].rest_layers_opacity
    def dummyUpdate(self, context):
        pass

    bpy.types.Scene.solidwireframe        = BoolProperty()

    bpy.types.Scene.toggle_ref_image      = BoolProperty()
    bpy.types.Scene.current_alpha         = FloatProperty()
    bpy.types.Scene.current_image_name    = StringProperty()
 
    bpy.types.Scene.axis_roll             = StringProperty()

    bpy.types.Scene.some_iteration        = IntProperty()

    bpy.types.Scene.already_saved_counter = IntProperty()

    bpy.types.Scene.fps_base              = FloatProperty(update=updateFPSBase, min=0.05, max=2, default=1, precision=2)
    bpy.types.Scene.fps_base_enum         = EnumProperty(default='3', update=updateFPSBaseEnum,
        items = [
            ("1", "0.25x", "a"),
            ("2", "0.50x", "s"),
            ("3", " 1x " , "d"),
            ("4", "1.50x", "q"),
            ("5", "2.00x", "w"),]
    )
    
    bpy.types.Scene.rest_layers_opacity   = FloatProperty(update=updateGPLayerOpacity, min=0, max=1, default=1)

    bpy.types.Scene.conditions            = StringProperty(update=dummyUpdate)

    bpy.types.Scene.loop_frames           = BoolProperty(default=False)
    bpy.types.Scene.panel_info_show       = BoolProperty()

    bpy.types.Scene.pt_info_1 = BoolProperty(default=False, update=dummyUpdate)
    bpy.types.Scene.pt_info_2 = BoolProperty(default=True, update=dummyUpdate)
    bpy.types.Scene.pt_info_3 = BoolProperty(default=True, update=dummyUpdate)
    bpy.types.Scene.pt_info_4 = BoolProperty(default=True, update=dummyUpdate)
    bpy.types.Scene.pt_info_5 = BoolProperty(default=False, update=dummyUpdate)
    
    bpy.types.Scene.brush_name_1 = StringProperty(update=dummyUpdate)
    bpy.types.Scene.brush_name_2 = StringProperty(update=dummyUpdate)
    bpy.types.Scene.brush_name_3 = StringProperty(update=dummyUpdate)
    bpy.types.Scene.brush_name_4 = StringProperty(update=dummyUpdate)
    bpy.types.Scene.brush_name_5 = StringProperty(update=dummyUpdate)
    bpy.types.Scene.brush_name_6 = StringProperty(update=dummyUpdate)
    bpy.types.Scene.brush_name_7 = StringProperty(update=dummyUpdate)
    bpy.types.Scene.brush_name_8 = StringProperty(update=dummyUpdate)

# '_UL_' recommended infix
class LIST_UL_GP_OBJECTS(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item:
                # this shit fucks things up, dont do it
                # layout.prop(item, "name", text="", emboss=False)
                layout.label(text=item.name)
class LIST_UL_PRESET_FRAME_RANGE_PREVIEW(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item:
                col = layout.column()
                split = col.split(factor=0.7)

                split.prop(item, "name", text="", emboss=False)
                
                split.label(text="(" + str(item.frame_preview_start) + " - " + str(item.frame_preview_end) + ")")

class stg1(PropertyGroup):
    def updateName(self, context):
        # this shit fucks things up, dont do it
        # context.active_object.name = self.name
        pass

    indx2: IntProperty(min = -1, default = -1)
    name:  StringProperty(update=updateName)
class stg2(PropertyGroup):
    def switchActiveGP(self, context):
        current_mode = context.mode
        scn = context.scene
        coll = scn.ptr.coll

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        scn.objects[coll[scn.ptr.indx].indx2].select_set(state=True)
        context.view_layer.objects.active = scn.objects[coll[scn.ptr.indx].indx2]
        
        bpy.ops.object.mode_set(mode=current_mode)

    coll: CollectionProperty(type=stg1)
    indx: IntProperty(min = -1, default = -1, update=switchActiveGP)

# TODO refactor this shit. I think I created reduntant variables
class stg3(PropertyGroup):
    frame_preview_start: IntProperty(default = 0)
    frame_preview_end:   IntProperty(default = 10)
class stg4(PropertyGroup):
    def switchPreviewRange(self, context):
        SC = context.scene

        if self.coll:
            SC.frame_preview_start = self.coll[self.indx].frame_preview_start
            SC.frame_preview_end   = self.coll[self.indx].frame_preview_end
    
    coll: CollectionProperty(type=stg3)
    indx: IntProperty(min = -1, default = -1, update=switchPreviewRange)

class stg5(PropertyGroup):
    def updateName(self, context):
        pass

    indx2: IntProperty(min = -1, default = -1)
    name:  StringProperty(update=updateName)
class stg6(PropertyGroup):
    def switchActiveGP(self, context):
        pass

    coll: CollectionProperty(type=stg5)
    indx: IntProperty(min = -1, default = -1, update=switchActiveGP)

classes = [

    LIST_UL_PRESET_FRAME_RANGE_PREVIEW,
    LIST_UL_GP_OBJECTS,

    # keep this order to not break anything
    stg1,
    stg2,

    stg3,
    stg4,

    stg5,
    stg6,

    TestSettings,
]
def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.ptr = PointerProperty(type=stg2)
    bpy.types.Scene.ptr2 = PointerProperty(type=stg4)
    bpy.types.Scene.ptr3 = PointerProperty(type=stg6)
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    
    del bpy.types.Scene.ptr
    del bpy.types.Scene.ptr2
    del bpy.types.Scene.ptr3
if __name__ == "__main__":
    register()