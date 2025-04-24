import bpy
from bpy.props import *
from bpy.types import Panel
from bl_ui.utils import PresetPanel


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
    VIEW3D_PT_frame_range,

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
