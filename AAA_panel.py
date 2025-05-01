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

        # LookDev is called 'MATERIAL' for some reason
        # elif shading.type == 'MATERIAL':
        elif context.scene.render.engine != 'BLENDER_WORKBENCH':
            if shading.type == 'MATERIAL':
                col.prop(shading, "use_scene_lights")
                col.prop(shading, "use_scene_world")
            else:
                col.prop(shading, "use_scene_lights_render")
                col.prop(shading, "use_scene_world_render")

            # bpy.context.space_data.shading.use_scene_lights_render = True
            # bpy.context.space_data.shading.use_scene_world_render = True

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


class VIEW3D_PT_background_color(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_label = "Background Color"

    def draw(self, context):
        LYT = self.layout
        shading = context.space_data.shading

        LYT.row().label(text="Background")
        LYT.row().prop(shading, "background_type", expand=True)

        if shading.background_type == 'VIEWPORT':
            LYT.row().prop(shading, "background_color", text="")

        if shading.background_type == 'WORLD':
            LYT.row().prop(context.scene.world, "color", text="")


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
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
