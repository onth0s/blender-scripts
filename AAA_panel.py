import bpy  # type: ignore
from bpy.props import *  # type: ignore
from bpy.types import Panel  # type: ignore
from bl_ui.utils import PresetPanel

from AAA_utils import *


# the '_2' is there to not collide with the built-in Panel
class VIEW3D_PT_proportional_edit_2(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Proportional Editing"
    bl_ui_units_x = 8

    def draw(self, context):
        layout = self.layout
        tool_settings = context.tool_settings

        layout.label(text="Proportional Editing")

        row = layout.row()
        row.prop(tool_settings, "use_proportional_edit_objects", text="")
        row.prop(tool_settings, "proportional_distance",
                 text="Distance")

        col = layout.column()
        if context.mode == MHE:
            col.prop(tool_settings, "use_proportional_connected")
            sub = col.column()
            sub.active = not tool_settings.use_proportional_connected
            sub.prop(tool_settings, "use_proportional_projected")

        col.separator()
        col.prop(tool_settings, "proportional_edit_falloff",
                 text="", expand=False)


class VIEW3D_PT_frame_range(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_ui_units_x = 8
    bl_label = "Frame Range"

    def draw(self, context):
        SC = context.scene
        layout = self.layout
        row = layout.row(align=True)

        row.prop(SC, "use_preview_range", text="")
        row.prop(SC, "loop_frames", text="", icon="FILE_REFRESH")
        row.prop(SC, "frame_current", text="Frame")

        if SC.use_preview_range:
            row = layout.row(align=True)
            row.prop(SC, "frame_preview_start", text="Start")
            row.prop(SC, "frame_preview_end", text="End")
        else:
            row = layout.row(align=True)
            row.prop(SC, "frame_start", text="Start")
            row.prop(SC, "frame_end", text="End")


class VIEW3D_PT_object_color(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "Object Color"

    def draw(self, context):
        shading = context.space_data.shading
        LYT = self.layout
        OB = context.active_object

        LYT.grid_flow(columns=3, align=True).prop(
            shading, "color_type", expand=True)

        if shading.color_type == 'SINGLE':
            LYT.row().prop(shading, "single_color", text="")

        elif shading.color_type == 'OBJECT':
            LYT.row().prop(context.object, "color", text="")

        elif shading.color_type == 'MATERIAL':
            if OB.active_material is not None:
                LYT.row().prop(context.object.active_material,
                               "diffuse_color", text="")
                LYT.row().template_ID(OB, "active_material",
                                      new="material.new")
            else:
                LYT.row().label(text="No Material Found")
                row = LYT.row(align=True)
                row.operator("aaa.add_material", text="Add New").mode = "NEW"
                if bpy.data.materials:
                    row.operator("aaa.add_material", text="Use Lastest") \
                        .mode = "LAST"


class VIEW3D_PT_matcap(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "MatCap"
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
                    sub.template_icon_view(
                        shading, "studio_light", scale_popup=3.0)
                else:
                    sub.prop(system, "use_studio_light_edit",
                             text="Disable Studio Light Edit", icon='NONE', toggle=True)

                col = split.column()
                col.operator("wm.studiolight_userpref_show",
                             emboss=False, text="", icon='PREFERENCES')

                split = layout.split(factor=0.9)
                col = split.column()

                row = col.row()
                row.prop(shading, "use_world_space_lighting",
                         text="", icon='WORLD', toggle=True)
                row = row.row()
                row.active = shading.use_world_space_lighting
                row.prop(shading, "studiolight_rotate_z", text="Rotation")
                col = split.column()  # to align properly with above
            elif shading.light == 'MATCAP':
                sub.scale_y = 0.6  # smaller matcap preview

                sub.template_icon_view(
                    shading, "studio_light", scale_popup=2.4)

                col = split.column()
                col.operator("wm.studiolight_userpref_show",
                             emboss=False, text="", icon='PREFERENCES')
                col.operator("view3d.toggle_matcap_flip",
                             emboss=False, text="", icon='ARROW_LEFTRIGHT')

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


class VIEW3D_PT_background_color(Panel):
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
            row.operator("aaa.preset_background", text="",
                         icon='REMOVE').remove_active = True

        if shading.background_type == 'WORLD':
            row = layout.row()
            row.prop(context.scene.world, "color", text="")

        # row.operator_menu_enum("object.modifier_add", "type")


class AAA_BASE_PANEL():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


class VIEW3D_PT_INFO(AAA_BASE_PANEL, Panel):
    bl_category = 'AAA'
    bl_label = "VIEW3D_PT_INFO Label"
    bl_order = 0

    # bl_options = {'HIDE_HEADER'}

    def draw_header(self, context):
        layout = self.layout
        col = layout.column()

        sub = col.row(align=True)

        spc = "                                                                   "
        sub.label(text="INFO" + spc)

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
                layout.label(text="Obj Type       -       " +
                             context.object.type)
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


class VIEW3D_PT_INFO_SHOW(AAA_BASE_PANEL, Panel):
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

        sub.prop(context.scene, "pt_info_1",
                 expand=True, text="Name", toggle=True)
        sub.prop(context.scene, "pt_info_2",
                 expand=True, text="Type", toggle=True)
        sub.prop(context.scene, "pt_info_3",
                 expand=True, text="Mode", toggle=True)
        sub.prop(context.scene, "pt_info_4",
                 expand=True, text="Cond", toggle=True)
        sub.prop(context.scene, "pt_info_5", expand=True,
                 text="ActTool", toggle=True)


class VIEW3D_PT_FRAME(AAA_BASE_PANEL, Panel):
    bl_category = 'AAC'
    bl_label = " "
    bl_order = 0

    def draw_header(self, context):
        self.layout.label(text="ABOUT FRAMES")

    def draw(self, context):
        pass


class VIEW3D_PT_FRAME_RATE(AAA_BASE_PANEL, Panel):
    bl_label = " "
    bl_parent_id = "VIEW3D_PT_FRAME"
    # bl_options = {'HIDE_HEADER'}

    def draw_header(self, context):
        self.layout.label(text="FRAME RATE")

    def draw(self, context):
        VIEW3D_PT_frame_range.draw(self, context)


class VIEW3D_PT_FRAME_RANGE(AAA_BASE_PANEL, Panel):
    bl_label = " "
    bl_parent_id = "VIEW3D_PT_FRAME"
    # bl_options = {'HIDE_HEADER'}

    def draw_header(self, context):
        self.layout.label(text="FRAME RANGE")

    def draw(self, context):
        VIEW3D_PT_frame_range.draw(self, context)


class VIEW3D_PT_FRAME_RANGE_PREVIEW(AAA_BASE_PANEL, Panel):
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
        row.template_list("LIST_UL_PRESET_FRAME_RANGE_PREVIEW", "", SC.ptr2,
                          "coll", SC.ptr2, "indx", rows=rows_len, sort_lock=True)

        col = row.column(align=True)
        srow = col.row(align=True)
        srow.operator("aaa.preset_frame_range_preview_add",
                      text="", icon="ADD", emboss=True)
        col.operator("aaa.preset_frame_range_preview_remove",
                     text="", icon="REMOVE", emboss=True)

        col.separator()
        col.operator("aaa.preset_frame_range_preview_overwrite",
                     text="", icon="FILE_REFRESH", emboss=True)

        col.separator()
        col.operator("aaa.preset_frame_range_preview_move",
                     text="", icon="TRIA_UP").type = 'UP'
        col.operator("aaa.preset_frame_range_preview_move",
                     text="", icon="TRIA_DOWN").type = 'DOWN'


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
    VIEW3D_PT_proportional_edit_2,

    VIEW3D_PT_frame_range,

    VIEW3D_PT_object_color,
    VIEW3D_PT_matcap,
    VIEW3D_PT_background_color,

    VIEW3D_PT_INFO,
    VIEW3D_PT_INFO_SHOW,

    VIEW3D_PT_FRAME,
    VIEW3D_PT_FRAME_RATE,
    VIEW3D_PT_FRAME_RANGE,
    VIEW3D_PT_FRAME_RANGE_PREVIEW,
    VIEW3D_PT_FRAME_RANGE_PREVIEW_ADD,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
