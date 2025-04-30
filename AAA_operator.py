import bpy  # type: ignore
import os
import re
from datetime import datetime

from bpy.props import (FloatProperty, IntProperty,  # type: ignore
                       BoolProperty, StringProperty)
from bpy.types import (Menu, Operator)  # type: ignore
from bl_operators.presets import AddPresetBase
from mathutils import *  # type: ignore
from math import *

from AAA_utils import *

''' Notes
    I dont know how to set up the poll() function

    bpy.ops.info.reports_display_update()
    doesnt work as expected. well, it doesnt work at all
    I need to register the operator and get some flood if i wanna update the Info Editor
'''

# if you call it from other operator the self.report() function prints to the console instead of the Info Editor, independently of the 'execution context'

''' Preset Operator
class test(Operator):
    bl_idname = "aaa.test"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):

        return {'FINISHED'}
'''


class SaveFile(Operator):
    """Save the current file and check if it has already been saved."""

    bl_idname = "aaa.save_file"
    bl_label = "Save File"
    bl_options = {'REGISTER'}

    def execute(self, context):
        filename = bpy.path.basename(context.blend_data.filepath)
        bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

        if bpy.data.is_saved:
            if bpy.data.is_dirty:
                saved = "Saved: " + filename
                self.report({'INFO'}, saved)

                bpy.data.scenes[0].already_saved_counter = 0
            else:
                bpy.data.scenes[0].already_saved_counter += 1
                st = "No changes have been made to '" + filename + \
                    "'. Already saved file (" + \
                    str(bpy.data.scenes[0].already_saved_counter) + ")"
                self.report({'INFO'}, st)

        return {'FINISHED'}


class SaveIncremental(Operator):
    bl_idname = "aaa.save_incremental"
    bl_label = ""
    bl_options = {'REGISTER'}

    def execute(self, context):
        currentblend = bpy.data.filepath
        if currentblend:
            save_path = self.get_incremented_path(currentblend)
            # self.add_path_to_recent_files(save_path)
            if os.path.exists(save_path):
                self.report(
                    {'INFO'}, "File '%s' exists already!\nBlend has NOT been saved incrementally!" % (save_path))
            else:
                bpy.ops.wm.save_as_mainfile(filepath=save_path)
                self.report({'INFO'}, "Saved blend incrementally:" + save_path)

                bpy.data.scenes[0].already_saved_counter = 0
        else:
            bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
        return {'FINISHED'}

    def get_incremented_path(self, currentblend):
        path = os.path.dirname(currentblend)
        filename = os.path.basename(currentblend)

        filenameRegex = re.compile(r"(.+)\.blend\d*$")

        mo = filenameRegex.match(filename)

        if mo:
            name = mo.group(1)
            numberendRegex = re.compile(r"(.*?)(\d+)$")

            mo = numberendRegex.match(name)

            if mo:
                basename = mo.group(1)
                numberstr = mo.group(2)
            else:
                basename = name + "_"
                numberstr = "000"

            number = int(numberstr)

            incr = number + 1
            incrstr = str(incr).zfill(len(numberstr))
            incrname = basename + incrstr + ".blend"

            return os.path.join(path, incrname)

    def add_path_to_recent_files(self, path):
        """
        add the path to the recent files list, for some reason it's not done automatically when saving or loading
        """

        try:
            recent_path = bpy.utils.user_resource('CONFIG', "recent-files.txt")
            with open(recent_path, "r+") as f:
                content = f.read()
                f.seek(0, 0)
                f.write(path.rstrip('\r\n') + '\n' + content)

        except (IOError, OSError, FileNotFoundError):
            pass


class SwitchWorkspace(Operator):
    """Switch Workspace"""
    bl_idname = "aaa.switch_workspace"
    bl_label = ""
    bl_options = {'REGISTER'}

    name: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        context.window.workspace = bpy.data.workspaces[self.name]
        return {'FINISHED'}


class ModeSet(Operator):
    bl_idname = "aaa.mode_set"
    bl_label = ""
    bl_options = {'UNDO'}
    # bl_options = {'REGISTER', 'UNDO'}

    mode: StringProperty()  # type: ignore

    def execute(self, context):
        bpy.ops.object.mode_set(mode=self.mode)

        if self.mode in (MHE):
            context.space_data.shading.cavity_type = 'WORLD'
        if self.mode == OBJ:
            context.space_data.shading.cavity_type = 'BOTH'
        return {'FINISHED'}


class ToggleOverlays(Operator):
    bl_idname = "aaa.toggle_overlays"
    bl_label = "Toggle Overlays"
    bl_options = {'REGISTER'}

    header: bpy.props.BoolProperty()  # type: ignore

    def execute(self, context):
        SD = context.space_data
        SN = context.scene

        if self.header:
            SD.show_region_header = not SD.show_region_header
        else:
            if not SN.show_bool_toggle:
                SN.show_overlays = SD.overlay.show_overlays
                SN.show_gizmo = SD.show_gizmo
                SN.show_t_menu = SD.show_region_ui
                SN.show_n_menu = SD.show_region_toolbar

                SD.overlay.show_overlays = False
                SD.show_gizmo = False
                SD.show_region_ui = False
                SD.show_region_toolbar = False
            else:
                SD.overlay.show_overlays = SN.show_overlays
                SD.show_gizmo = SN.show_gizmo
                SD.show_region_ui = SN.show_t_menu
                SD.show_region_toolbar = SN.show_n_menu

            SN.show_bool_toggle = not SN.show_bool_toggle

        return {'FINISHED'}


class RollViewport(Operator):
    bl_idname = "aaa.roll_viewport"
    bl_label = "Roll Viewport"
    bl_options = {'GRAB_CURSOR'}

    initial_angle = 0
    angle_now = 0
    initial_rotation = Vector((0, 0, 0))  # type: ignore
    camNormal = Vector((0, 0, -1))  # type: ignore

    temp_degree = 0

    def toDegrees(radians):
        return radians * (180 / pi)

    def to360Degrees(test):
        return radians * (180 / pi)

    def invoke(self, context, event):
        rv3d = context.space_data.region_3d
        context.window_manager.modal_handler_add(self)

        ''' TODO
            takes you out from the camera view into the perspective view to call the rotation view modal
            it should rotate the camera too, or be an option'''
        if rv3d.view_perspective == 'CAMERA':
            rv3d.view_perspective = 'PERSP'

        # get the center of the viewport
        self.view3d_bounds = Vector(  # type: ignore
            (context.region.width, context.region.height))
        self.view3d_center = self.view3d_bounds / 2

        # how far is the mouse from the center, returns a Vector
        mouseloc = Vector(  # type: ignore
            (event.mouse_region_x, event.mouse_region_y))
        mouseloc_centered = mouseloc - self.view3d_center

        # copy a Quaternion(w, x, y, z) into a Vector((x, y, z)), returns a Quaternion()
        self.initial_rotation = rv3d.view_rotation.copy()
        # the angle in radians from the center of the viewport to the position of the cursor
        # past 180 degrees (or PI radians) counterclockwise will get you negative numbers: 180 turn into -179, not 181 (it's not an integer though)
        self.initial_angle = atan2(mouseloc_centered.y, mouseloc_centered.x)
        self.angle_now = self.initial_angle

        # change the axis of rotation
        if bpy.data.scenes[0].axis_roll == "X":
            self.camNormal = Vector((1, 0, 0))  # type: ignore
        elif bpy.data.scenes[0].axis_roll == "Y":
            self.camNormal = Vector((0, 0, -1))  # type: ignore
        elif bpy.data.scenes[0].axis_roll == "Z":
            self.camNormal = Vector((0, 1, 0))  # type: ignore

        return {'RUNNING_MODAL'}

    def execute(self, context):
        rv3d = context.space_data.region_3d

        angle_diff = self.angle_now - self.initial_angle
        quat = Quaternion(self.camNormal, angle_diff)  # type: ignore
        rv3d.view_rotation = self.initial_rotation @ quat

        if angle_diff > 0:
            # print(toDegrees(angle_diff))
            self.temp_degree = angle_diff
        else:
            self.temp_degree = -1 * angle_diff
            a = 2 * pi - self.temp_degree
            # print(toDegrees(a))

        return {'FINISHED'}

    def modal(self, context, event):
        rv3d = context.space_data.region_3d

        if event.type == 'MOUSEMOVE':
            mouseloc = Vector(  # type: ignore
                (event.mouse_region_x, event.mouse_region_y))
            mouseloc_centered = mouseloc - self.view3d_center
            self.angle_now = atan2(mouseloc_centered.y, mouseloc_centered.x)
            self.execute(context)
        elif event.type in {'LEFTMOUSE', 'MIDDLEMOUSE'}:
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            rv3d.view_rotation = self.initial_rotation
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}


class RollAxis(Operator):
    bl_idname = "aaa.roll_axis"
    bl_label = ""
    bl_options = {'REGISTER'}

    axis: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        if self.axis == 'X':
            bpy.data.scenes[0].axis_roll = 'X'
        if self.axis == 'Y':
            bpy.data.scenes[0].axis_roll = 'Y'
        if self.axis == 'Z':
            bpy.data.scenes[0].axis_roll = 'Z'

        return {'FINISHED'}


class STDTools(Operator):
    bl_idname = "aaa.std_tools"
    bl_label = "Standard Tools"
    bl_options = {'REGISTER'}

    name: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        if self.name == 'SPIN_TOOL':
            bpy.ops.wm.tool_set_by_id(name="builtin.spin")
            context.scene.tool_settings.workspace_tool_type = 'DEFAULT'

        return {'FINISHED'}


class AddMaterial(Operator):
    bl_idname = "aaa.add_material"
    bl_label = "Add Material"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        OB = context.active_object

        if self.mode == 'NEW':
            mat = bpy.data.materials.new(name="Material")
        elif self.mode == 'LAST':
            mat = bpy.data.materials[-1]

        mat.use_nodes = True
        if OB.data.materials:
            OB.data.materials[0] = mat
        else:
            OB.data.materials.append(mat)

        return {'FINISHED'}


class SWITCH_CONDITION(Operator):
    bl_idname = "aaa.switch_condition"
    bl_label = "SWITCH_CONDITION"
    bl_options = {'REGISTER'}

    cond: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        context.scene.conditions = self.cond

        return {'FINISHED'}


class SWITCH_VALUE(Operator):
    bl_idname = "aaa.switch_value"
    bl_label = "SWITCH_VALUE"
    bl_options = {'REGISTER'}

    val_a: bpy.props.StringProperty()  # type: ignore
    val_b: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        # this is a workaround to set a property from the outside
        # it's not a good practice, but it works
        # TODO find a better way to do this
        exec(f"{self.val_a} = '{self.val_b}'")

        return {'FINISHED'}


class GLOBAL_Q(Operator):
    bl_idname = "aaa.key_q"
    bl_label = "GLOBAL_Q"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        SN = context.scene
        CN = context.scene.conditions
        AT = context.area.type

        if CN == 'TRANSFORM':
            if AT in ("VIEW_3D", 'GRAPH_EDITOR'):
                bpy.ops.transform.translate('INVOKE_DEFAULT')

        if CN == 'TIMELINE':
            # 'loop_frames' is a BoolProperty in 'AAA_settings'

            if SN.loop_frames:
                if SN.use_preview_range:
                    if SN.frame_current == SN.frame_preview_start:
                        SN.frame_current = SN.frame_preview_end
                    else:
                        bpy.ops.screen.frame_offset(delta=-1)
                else:
                    if SN.frame_current == SN.frame_start:
                        SN.frame_current = SN.frame_end
                    else:
                        bpy.ops.screen.frame_offset(delta=-1)
            else:
                bpy.ops.screen.frame_offset(delta=-1)

        return {'FINISHED'}


class GLOBAL_W(Operator):
    bl_idname = "aaa.key_w"
    bl_label = "GLOBAL_W"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        C = context
        CN = C.scene.conditions
        AT = C.area.type

        if CN == 'TRANSFORM':
            if AT in ("VIEW_3D", 'GRAPH_EDITOR'):
                bpy.ops.transform.resize('INVOKE_DEFAULT')
            elif AT == "DOPESHEET_EDITOR":
                bpy.ops.transform.transform(
                    'INVOKE_DEFAULT', mode="TIME_SCALE")

        if CN == 'TIMELINE':
            if C.scene.use_preview_range:
                C.scene.frame_current = C.scene.frame_preview_start
            else:
                C.scene.frame_current = C.scene.frame_start

        return {'FINISHED'}


class GLOBAL_E(Operator):
    bl_idname = "aaa.key_e"
    bl_label = "GLOBAL_E"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        SN = context.scene
        CN = SN.conditions
        AT = context.area.type

        if CN == 'TRANSFORM':
            if AT in ('VIEW_3D', 'GRAPH_EDITOR'):
                bpy.ops.transform.rotate('INVOKE_DEFAULT')

        if CN == 'TIMELINE':
            if SN.loop_frames:
                if SN.use_preview_range:
                    if SN.frame_current == SN.frame_preview_end:
                        SN.frame_current = SN.frame_preview_start
                    else:
                        bpy.ops.screen.frame_offset(delta=1)
                else:
                    if SN.frame_current == SN.frame_end:
                        SN.frame_current = SN.frame_start
                    else:
                        bpy.ops.screen.frame_offset(delta=1)
            else:
                bpy.ops.screen.frame_offset(delta=1)

        return {'FINISHED'}


class ToggleProp(Operator):
    bl_idname = "aaa.toggle_prop"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    prop: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        exec(self.prop+" = not "+self.prop)

        return {'FINISHED'}


class TestOperator(Operator):
    """Test Operator Docstring"""

    bl_idname = "aaa.test_operator"
    bl_label = "Test Operator"
    bl_options = {'REGISTER', 'UNDO'}

    testVal: bpy.props.IntProperty()  # type: ignore

    def execute(self, context):
        time = str(datetime.time(datetime.now()))
        print("{}: {}".format(self.testVal, time[:-7]))

        return {'FINISHED'}


class TestContextDebugger(Operator):
    bl_idname = "aaa.test_context_debugger"
    bl_label = "Test Context Debugger"
    bl_options = {'REGISTER'}

    def execute(self, context):
        print("\n=============== FULL CONTEXT DUMP ===============\n")

        print("""  >>> context.area.type:
    Active Area:""", context.area.type)

        print("""\n  >>> context.area.ui_type:
    UI Type:""", context.area.ui_type)

        print("""\n  >>> context.active_object:
    Active Object:""", context.active_object)

        print("""\n  >>> context.selected_objects:
    Selected Objects:""", context.selected_objects)

        print("""\n  >>> context.mode:
    Mode:""", context.mode)

        print("""\n  >>> context.screen.name:
    Screen:""", context.screen.name)

        print("""\n  >>> context.region.type:
    Region:""", context.region.type)

        return {'FINISHED'}


classes = (
    SaveFile,
    SaveIncremental,

    SwitchWorkspace,
    ModeSet,

    ToggleOverlays,

    RollViewport,
    RollAxis,

    STDTools,

    AddMaterial,

    SWITCH_CONDITION,
    SWITCH_VALUE,

    GLOBAL_Q,
    GLOBAL_W,
    GLOBAL_E,

    ToggleProp,
    TestOperator,
    TestContextDebugger
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
