import bpy
from bpy.props   import *
from bpy.types   import Panel
from bl_ui.utils import PresetPanel

class VIEW3D_PT_test_modifiers_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "alo alo alo"
    bl_ui_units_x = 12
    is_popover = True
    type: bpy.props.StringProperty(name="Type")
    def draw(self, context):
        layout = self.layout
        ob = context.object
        actdat = bpy.context.active_object.data
        
        row = layout.row()
        col = row.column(align=True)
        if ob.type == 'MESH':
            col.operator_menu_enum("object.modifier_add", "type")
            col.operator_menu_enum("object.modifier_add", "type")
            for md in ob.modifiers:
                box = col.template_modifier(md)
                if box:
                    getattr(self, md.type)(box, ob, md)
    def SUBSURF(self, layout, ob, md):
        from bpy import context
        layout.row().prop(md, "subdivision_type", expand=True)

        split = layout.split()
        col = split.column()

        scene = context.scene
        engine = context.engine
        show_adaptive_options = engine == 'CYCLES' and md == ob.modifiers[-1] and scene.cycles.feature_set == 'EXPERIMENTAL'
        
        col.label(text="Subdivisions:")
        col.prop(md, "levels", text="View")
        col.prop(md, "render_levels", text="Render")
        if hasattr(md, "quality"):
            col.prop(md, "quality")    

        col = split.column()
        col.label(text="Options:")

        sub = col.column()
        sub.active = (not show_adaptive_options) or (not ob.cycles.use_adaptive_subdivision)
        sub.prop(md, "uv_smooth", text="")

        col.prop(md, "show_only_control_edges")                
    def MIRROR(self, layout, ob, md):
        axis_text = "XYZ"
        split = layout.split(factor=0.33)

        col = split.column()
        col.label(text="Axis:")
        for i, text in enumerate(axis_text):
            col.prop(md, "use_axis", text=text, index=i)

        col = split.column()
        col.label(text="Bisect:")
        for i, text in enumerate(axis_text):
            colsub = col.column()
            colsub.prop(md, "use_bisect_axis", text=text, index=i)
            colsub.active = md.use_axis[i]

        col = split.column()
        col.label(text="Flip:")
        for i, text in enumerate(axis_text):
            colsub = col.column()
            colsub.prop(md, "use_bisect_flip_axis", text=text, index=i)
            colsub.active = md.use_axis[i] and md.use_bisect_axis[i]

        col = layout.column()
        col.label(text="Mirror Object:")
        col.prop(md, "mirror_object", text="")

class VIEW3D_PT_matcap(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "Lighting"
    is_popover = True

    def draw(self, context):
        layout = self.layout
        shading = context.space_data.shading

        col = layout.column()
        split = col.split(factor=0.9)

        if shading.type == 'SOLID':
            split.row().prop(shading, "light", expand=True)
            col = split.column()

            split = layout.split(factor=0.9)
            col = split.column()
            sub = col.row()

            if shading.light == 'STUDIO':
                prefs = context.preferences
                system = prefs.system

                if not system.use_studio_light_edit:
                    sub.scale_y = 0.6  # smaller studiolight preview
                    sub.template_icon_view(shading, "studio_light", scale_popup=3.0)
                else:
                    sub.prop(system, "use_studio_light_edit", text="Disable Studio Light Edit", icon='NONE', toggle=True)

                col = split.column()
                col.operator("wm.studiolight_userpref_show", emboss=False, text="", icon='PREFERENCES')

                split = layout.split(factor=0.9)
                col = split.column()

                row = col.row()
                row.prop(shading, "use_world_space_lighting", text="", icon='WORLD', toggle=True)
                row = row.row()
                row.active = shading.use_world_space_lighting
                row.prop(shading, "studiolight_rotate_z", text="Rotation")
                col = split.column()  # to align properly with above
            elif shading.light == 'MATCAP':
                sub.scale_y = 0.6  # smaller matcap preview

                sub.template_icon_view(shading, "studio_light", scale_popup=2.4)

                col = split.column()
                col.operator("wm.studiolight_userpref_show", emboss=False, text="", icon='PREFERENCES')
                col.operator("view3d.toggle_matcap_flip", emboss=False, text="", icon='ARROW_LEFTRIGHT')

        # LookDev is called 'MATERIAL' for some reason 
        elif shading.type == 'MATERIAL':
            col.prop(shading, "use_scene_lights")
            col.prop(shading, "use_scene_world")

            if not shading.use_scene_world:
                col = layout.column()
                split = col.split(factor=0.9)

                col = split.column()
                sub = col.row()
                sub.scale_y = 0.6
                sub.template_icon_view(shading, "studio_light", scale_popup=3)

                # col = split.column()
                # col.operator("wm.studiolight_userpref_show", emboss=False, text="", icon='PREFERENCES')

                if shading.selected_studio_light.type == 'WORLD':
                    split = layout.split(factor=0.9)
                    col = split.column()
                    col.prop(shading, "studiolight_rotate_z", text="Rotation")
                    col.prop(shading, "studiolight_background_alpha")
                    col = split.column()  # to align properly with above
        else:
            layout.label(text="Just press the button below")
            layout.operator("aaa.toggle_solid_wireframe", text="Solid Shading")  
class VIEW3D_PT_background(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "Background Color"

    def draw(self, context):
        layout = self.layout
        shading = context.space_data.shading

        row = layout.row()
        row.label(text="Background")

        row = layout.row()
        row.prop(shading, "background_type", expand=True)
       
        if shading.background_type == 'VIEWPORT':
            row = layout.row()
            row.prop(shading, "background_color", text="")

            row = layout.row(align=True)
            row.menu("VIEW3D_MT_PRESETS_BACKGROUND", text="Background Presets")
            row.operator("aaa.preset_background", text="", icon='ADD')
            row.operator("aaa.preset_background", text="", icon='REMOVE').remove_active = True

        if shading.background_type == 'WORLD':
            row = layout.row()
            row.prop(context.scene.world, "color", text="")

        # row.operator_menu_enum("object.modifier_add", "type")
class VIEW3D_PT_color(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "Object Color"
    def draw(self, context):
        layout = self.layout
        shading = context.space_data.shading

        # row = layout.row(align=True)
        # row.menu("VIEW3D_MT_PRESETS_MT_OVERLAYS", text="Overlays Presets")
        # row.operator("aaa.preset_overlays", text="", icon='ADD')
        # row.operator("aaa.preset_overlays", text="", icon='REMOVE').remove_active = True

        layout.grid_flow(columns=3, align=True).prop(shading, "color_type", expand=True)
        
        if shading.color_type == 'SINGLE':
            layout.row().prop(shading, "single_color", text="")
        elif shading.color_type == 'OBJECT':
            layout.row().prop(context.object, "color", text="")
        elif shading.color_type == 'MATERIAL':
            if context.object.active_material is not None:
                layout.row().prop(context.object.active_material, "diffuse_color", text="")
            else:
                # TODO Show the "New Material" button
                # Now it doesn't work as expected. It creates a new material but doesn't add and assign it to a new material slot 
                layout.row().label(text="No material assigned")        

class VIEW3D_PT_sculpt_popup(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "Sculpt Context Menu"
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.tool_settings.sculpt.brush, "use_frontface", text="FrontFace")
        row.prop(context.tool_settings.sculpt.brush, "use_original_normal", text="OrigNormal")

        row = layout.row(align=True)
        
        row.operator("sculpt.symmetrize", text="XSymmetry")
        row.operator("sculpt.optimize", text="Optimize")
        row.operator("sculpt.detail_flood_fill", text="FloodFill")

class VIEW3D_PT_rename_bone(Panel):     
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "Rename Bone"
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Bone Name")
        layout.prop(context.active_bone, "name", text="")
class VIEW3D_PT_rename_gp_layer(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "Rename Layer"
    def draw(self, context):
        layout = self.layout

        layout.label(text="Layer Name")
        layout.prop(context.active_gpencil_layer, "info", text="")

# the '_2' is there to not collide with the built-in Panel
class VIEW3D_PT_proportional_edit_2(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Proportional Editing"
    bl_ui_units_x = 8

    def draw(self, context):
        layout = self.layout
        tool_settings = context.tool_settings
        col = layout.column()
        
        if context.mode == 'OBJECT':
            col.prop(tool_settings, "use_proportional_edit_objects", text="Proportional Editing")

        if context.mode != 'OBJECT':
            col.prop(tool_settings, "use_proportional_edit")
            col.prop(tool_settings, "use_proportional_connected")
            sub = col.column()
            sub.active = not tool_settings.use_proportional_connected
            sub.prop(tool_settings, "use_proportional_projected")
            col.separator()

        col.prop(tool_settings, "proportional_edit_falloff", expand=True)

class VIEW3D_PT_gp_frame_rate(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_ui_units_x = 12        
    bl_label = ""
    def draw(self, context):
        layout = self.layout

        fps_label_text = context.scene.render.fps * context.scene.fps_base 
        fps_label_text = "%.2f" % round(fps_label_text, 2) + " FPS"
        
        layout.menu("RENDER_MT_framerate_presets", text=str(fps_label_text))

        layout.prop(context.scene.render, "fps")
        layout.prop(bpy.data.scenes[0], "fps_base", text="Playback Speed", slider=True)

        layout.prop(context.scene, "fps_base_enum", expand=True)
class VIEW3D_PT_gp_frame_range(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_ui_units_x = 12
    bl_label = ""
    def draw(self, context):
        SC = context.scene
        layout = self.layout
        row = layout.row(align=True)
        # split = col.split(factor=0.2, align=True)
        
        row.prop(SC, "use_preview_range", text="")
        row.prop(SC, "loop_frames", text="", icon="FILE_REFRESH")
        row.prop(SC, "frame_current", text="Frame")

        if SC.use_preview_range:
            layout.prop(SC, "frame_preview_start", text="Start")
            layout.prop(SC, "frame_preview_end", text="End")
        else:
            layout.prop(SC, "frame_start", text="Start")
            layout.prop(SC, "frame_end", text="End")

# context.gpencil_data.layers ----- For all layers of the active GPencil
# context.active_gpencil_layer ---- self explanatory        
class VIEW3D_PT_gp_layer_1(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "Opacity"
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Set Opacity...")
        layout.prop(context.active_gpencil_layer, "opacity", text="Current", slider=True)
        layout.prop(bpy.data.scenes[0], "rest_layers_opacity", text="Rest", slider=True)
        layout.operator("aaa.gp_layer_reset_opacity", text="Reset All to 1")
class VIEW3D_PT_gpencil_layers(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_ui_units_x = 15
    bl_label = ""
    def draw(self, context):
        GD = context.gpencil_data
        layout = self.layout
        
        row = layout.row()
        col = row.column()
        col.template_list("GPENCIL_UL_layer", "", GD, "layers", GD.layers, "active_index", rows=len(GD.layers), sort_reverse=True, sort_lock=False)
        
        col = row.column()
        srow = col.row(align=True)
        srow.prop(GD, "use_autolock_layers", text="")
class VIEW3D_PT_gpencil_layers_2(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_ui_units_x = 8
    bl_label = ""
    def draw(self, context):
        SN = context.scene
        layout = self.layout
        layout.template_list("LIST_UL_GP_OBJECTS", "", SN.ptr, "coll", SN.ptr, "indx", rows=len(SN.ptr.coll), sort_lock=True)
class VIEW3D_PT_gpencil_layers_move(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_ui_units_x = 12
    bl_label = ""
    def draw(self, context):
        SN = context.scene
        layout = self.layout
        layout.label(text="Select the Object to move the layers to...")
        layout.template_list("LIST_UL_GP_OBJECTS", "", SN.ptr3, "coll", SN.ptr3, "indx", rows=len(SN.ptr3.coll), sort_lock=True)
            
        layout.operator("aaa.gp_layer_unlocked_move_to_selected", text="Select GP Object")

class VIEW3D_PT_helper_gpencil_brushes_manager(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_ui_units_x = 12
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        layout.label(text="Nothing to show here")

# ------------------------   Toolbar   ------------------------ #
class BasePanelAAA():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
 
class VIEW3D_PT_INFO(BasePanelAAA, Panel):
    bl_category = 'AAA'
    bl_label = " "
    bl_order = 0

    bl_options = {'HIDE_HEADER'}

    # def draw_header_preset(self, _context):
    #     VIEW3D_PT_INFO_PRESET.draw_panel_header(self.layout)
    
    def draw_header(self, context):
        layout = self.layout 
        col = layout.column()
        
        sub = col.row(align=True)
        
        spc = "                                                                   "
        sub.label(text="INFO"+spc)

        # if context.scene.panel_info_show:
        #     sub.operator("aaa.panel_info_show", icon="REMOVE")
        # else:
        #     sub.operator("aaa.panel_info_show", icon="ADD")
        
    def draw(self, context):
        SC = context.scene
        layout = self.layout

        if context.object is not None:
            if SC.pt_info_1:
                layout.label(text="Obj Name     -       "+context.object.name)
            if SC.pt_info_2:
                layout.label(text="Obj Type       -       "+context.object.type)
        if SC.pt_info_3:
            layout.label(text="Obj Mode      -       "+context.mode)
             
        txt = "Conditions    -       "
        if SC.pt_info_4:
            if SC.conditions == 'TRANSFORM':
                layout.label(text=txt+"TRANSFORM")
            if SC.conditions == 'LAYERS':
                layout.label(text=txt+"LAYERS")
            if SC.conditions == 'TIMELINE':
                layout.label(text=txt+"TIMELINE")       

        if SC.pt_info_5:
            layout.label(text="Active Tool   -       TODO")
class VIEW3D_PT_INFO_SHOW(BasePanelAAA, Panel):
    bl_label = " "
    bl_parent_id = "VIEW3D_PT_INFO"

    @classmethod
    def poll(cls, context):
        return context.scene.panel_info_show
    
    def draw_header(self, context):
        self.layout.label(text="Show")
    def draw(self, context):
        layout = self.layout
        col = layout.column()

        sub = col.row(align=True)

        sub.prop(context.scene, "pt_info_1", expand=True, text="Name", toggle=True)
        sub.prop(context.scene, "pt_info_2", expand=True, text="Type", toggle=True)
        sub.prop(context.scene, "pt_info_3", expand=True, text="Mode", toggle=True)
        sub.prop(context.scene, "pt_info_4", expand=True, text="Cond", toggle=True)
        sub.prop(context.scene, "pt_info_5", expand=True, text="ActTool" , toggle=True)
class VIEW3D_PT_INFO_PRESET(PresetPanel, Panel):
    bl_label = "Info Presets"
    preset_subdir = "scene/panel_info"
    preset_operator = "script.execute_preset"
    preset_add_operator = "aaa.preset_panel_info"

class VIEW3D_PT_FRAME(BasePanelAAA, Panel):
    bl_category = 'AAC'
    bl_label = " "
    bl_order = 0
    def draw_header(self, context):
        self.layout.label(text="ABOUT FRAMES")
    def draw(self, context):
        pass
class VIEW3D_PT_FRAME_RATE(BasePanelAAA, Panel):
    bl_label = " "
    bl_parent_id = "VIEW3D_PT_FRAME"
    # bl_options = {'HIDE_HEADER'}
    def draw_header(self, context):
        self.layout.label(text="FRAME RATE")
    def draw(self, context):
        VIEW3D_PT_gp_frame_rate.draw(self, context)
class VIEW3D_PT_FRAME_RANGE(BasePanelAAA, Panel):
    bl_label = " "
    bl_parent_id = "VIEW3D_PT_FRAME"
    # bl_options = {'HIDE_HEADER'}
    def draw_header(self, context):
        self.layout.label(text="FRAME RANGE")
    def draw(self, context):
        VIEW3D_PT_gp_frame_range.draw(self, context)
class VIEW3D_PT_FRAME_RANGE_PREVIEW(BasePanelAAA, Panel):
    bl_label = " "
    bl_parent_id = "VIEW3D_PT_FRAME_RANGE"
    # bl_options = {'HIDE_HEADER'}
    
    @classmethod
    def poll(cls, context):
        return context.scene.use_preview_range
    
    def draw_header(self, context):
        self.layout.label(text="FRAME RANGE PREVIEW PRESETS")
    def draw(self, context):
        SC = context.scene
        layout = self.layout
        
        c_len = len(SC.ptr2.coll)
        c_min = 5
        rows_len = c_len if c_len > c_min else c_min

        row = layout.row(align=False)
        row.template_list("LIST_UL_PRESET_FRAME_RANGE_PREVIEW", "", SC.ptr2, "coll", SC.ptr2, "indx", rows=rows_len, sort_lock=True)

        col = row.column(align=True)
        srow = col.row(align=True)
        srow.operator("aaa.preset_frame_range_preview_add", text="", icon="ADD", emboss=True)
        col.operator("aaa.preset_frame_range_preview_remove", text="", icon="REMOVE", emboss=True)
        
        col.separator()
        col.operator("aaa.preset_frame_range_preview_overwrite", text="", icon="FILE_REFRESH", emboss=True)

        col.separator()
        col.operator("aaa.preset_frame_range_preview_move", text="", icon="TRIA_UP").type='UP'
        col.operator("aaa.preset_frame_range_preview_move", text="", icon="TRIA_DOWN").type='DOWN'
class VIEW3D_PT_FRAME_RANGE_PREVIEW_ADD(Panel):     
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_ui_units_x = 20
    bl_label = "Add Preview Preset"
    def draw(self, context):
        SC = context.scene
        PR = SC.ptr2
        CL = SC.ptr2.coll
        layout = self.layout
        
        layout.label(text="Preview Name")

        var = 0 
        temp = PR.indx + 1
        if temp > len(CL):
            var = len(CL) - 1
        else:
            var = temp

        layout.activate_init = True
        layout.prop(CL[var], "name", text="")

class VIEW3D_PT_GPENCIL_OBJECTS(BasePanelAAA, Panel):
    bl_category = 'AAB'
    bl_label = " "
    bl_order = 0
    # bl_options = {'DEFAULT_CLOSED'}
    
    # this is how you should hide a panel I guess
    @classmethod
    def poll(cls, context):
        TP = None
        if context.active_object is not None:
            TP = context.active_object.type
        return TP is not None and TP == 'GPENCIL'
    
    def draw_header(self, context):
        layout = self.layout

        spc = "                                                                  "
        layout.label(text="GP OBJECTS"+spc)
        layout.operator("aaa.panel_gp_brushes_manager_refresh", text="", icon='FILE_REFRESH', emboss=False)
    def draw(self, context):
        if context.object is not None:
            if context.object.type == 'GPENCIL':
                VIEW3D_PT_gpencil_layers_2.draw(self, context)
class VIEW3D_PT_GPENCIL_LAYERS(BasePanelAAA, Panel):
    bl_category = 'AAB'
    bl_label = " "
    bl_order = 1
    # bl_options = {'DEFAULT_CLOSED'}
    
    # this is how you should hide a panel I guess
    @classmethod
    def poll(cls, context):
        TP = None
        if context.active_object is not None:
            TP = context.active_object.type
        return TP is not None and TP == 'GPENCIL'
    
    def draw_header(self, context):
        GD = context.gpencil_data
        layout = self.layout
        
        spc = "                                                                  "
        layout.label(text="GP LAYERS"+spc)
        layout.prop(GD, "use_autolock_layers", text="")
    def draw(self, context):
        GD = context.gpencil_data
        layout = self.layout
        if context.object is not None:
            if context.object.type == 'GPENCIL':
                
                row = layout.row()
                col = row.column()
                col.template_list("GPENCIL_UL_layer", "", GD, "layers", GD.layers, "active_index", rows=len(GD.layers), sort_reverse=True, sort_lock=False)

class VIEW3D_PT_GPENCIL_BRUSHES(BasePanelAAA, Panel):
    bl_category = 'AAD'
    bl_label = " "
    bl_order = 0

    @classmethod
    def poll(cls, context):
        TP = None
        if context.active_object is not None:
            TP = context.active_object.type
        return TP is not None and TP == 'GPENCIL'
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="GP BRUSHES")
    def draw(self, context):
        settings = context.scene.tool_settings.gpencil_paint
        
        layout = self.layout
        if context.object is not None:
            if context.object.type == 'GPENCIL' and context.mode == 'PAINT_GPENCIL':
                
                layout.template_ID_preview(settings, "brush", new="brush.add_gpencil", rows=3, cols=8)
            else:
                layout.label(text="Nothing to show here")
class VIEW3D_PT_GPENCIL_BRUSHES_MANAGER(BasePanelAAA, Panel):
    bl_label = " "
    bl_parent_id = "VIEW3D_PT_GPENCIL_BRUSHES"

    @classmethod
    def poll(cls, context):
        return context.mode == 'PAINT_GPENCIL'

    def draw_header(self, context):
        layout = self.layout

        spc = "                                                "
        layout.label(text="GP BRUSHES MANAGER"+spc)
        layout.operator("aaa.helper_gp_brushes_manager", text="", icon="QUESTION", emboss=False)
    def draw(self, context):
        SC = context.scene
        layout = self.layout
        
        for i in range(1, 9):
            exec("row = layout.row()\nsplit = row.split(factor=0.95, align=True)\nsplit.menu('VIEW3D_MT_GP_BRUSH_"+str(i)+"', text='Brush "+str(i)+":        '+SC.brush_name_"+str(i)+")\nsplit.operator('aaa.gp_remove_tool', text='', icon='X').index="+str(i))

class VIEW3D_PT_GPENCIL_MATERIALS(BasePanelAAA, Panel):
    bl_category = 'AAE'
    bl_label = " "
    bl_order = 0

    @classmethod
    def poll(cls, context):
        TP = None
        if context.active_object is not None:
            TP = context.active_object.type
        return TP is not None and TP == 'GPENCIL'
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="GP MATERIALS")
    def draw(self, context):
        OB = context.object
        layout = self.layout
        
        layout.template_list("GPENCIL_UL_matslots", "", OB, "material_slots", OB, "active_material_index", rows=4)


''' Panel Preset
class VIEW3D_PT_test(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "test"
    bl_ui_units_x = 12
    is_popover = True
    def draw(self, context):
        
'''        
classes = (

    VIEW3D_PT_GPENCIL_MATERIALS,

    VIEW3D_PT_GPENCIL_BRUSHES,
    VIEW3D_PT_GPENCIL_BRUSHES_MANAGER,

    VIEW3D_PT_GPENCIL_LAYERS,
    VIEW3D_PT_GPENCIL_OBJECTS,

    VIEW3D_PT_FRAME,
    VIEW3D_PT_FRAME_RATE,
    VIEW3D_PT_FRAME_RANGE,
    VIEW3D_PT_FRAME_RANGE_PREVIEW,
    VIEW3D_PT_FRAME_RANGE_PREVIEW_ADD,

    VIEW3D_PT_INFO,
    # VIEW3D_PT_INFO_SHOW,
    # VIEW3D_PT_INFO_PRESET,

    VIEW3D_PT_helper_gpencil_brushes_manager,
    
    VIEW3D_PT_gpencil_layers_move,
    VIEW3D_PT_gpencil_layers_2,
    VIEW3D_PT_gpencil_layers,
    VIEW3D_PT_gp_layer_1,
    VIEW3D_PT_gp_frame_range,
    VIEW3D_PT_gp_frame_rate,

    VIEW3D_PT_proportional_edit_2,
    
    VIEW3D_PT_rename_gp_layer,
    VIEW3D_PT_rename_bone,
    
    VIEW3D_PT_sculpt_popup,
    
    VIEW3D_PT_color,
    VIEW3D_PT_background,
    VIEW3D_PT_matcap,

    VIEW3D_PT_test_modifiers_panel,
)
def register():
    for c in classes:
        bpy.utils.register_class(c)
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()