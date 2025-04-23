import bpy
import os
import re
from datetime import datetime

from bpy.props import (FloatProperty, IntProperty,
                       BoolProperty, StringProperty)
from bpy.types import (Menu, Operator)
from bl_operators.presets import AddPresetBase
from mathutils import *
from math import *

from AAA_var import *

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

    name: bpy.props.StringProperty()

    def execute(self, context):
        context.window.workspace = bpy.data.workspaces[self.name]
        return {'FINISHED'}


class RollViewport(Operator):
    bl_idname = "aaa.roll_viewport"
    bl_label = "Roll Viewport"
    bl_options = {'GRAB_CURSOR'}

    initial_angle = 0
    angle_now = 0
    initial_rotation = Vector((0, 0, 0))
    camNormal = Vector((0, 0, -1))

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
        self.view3d_bounds = Vector(
            (context.region.width, context.region.height))
        self.view3d_center = self.view3d_bounds / 2

        # how far is the mouse from the center, returns a Vector
        mouseloc = Vector((event.mouse_region_x, event.mouse_region_y))
        mouseloc_centered = mouseloc - self.view3d_center

        # copy a Quaternion(w, x, y, z) into a Vector((x, y, z)), returns a Quaternion()
        self.initial_rotation = rv3d.view_rotation.copy()
        # the angle in radians from the center of the viewport to the position of the cursor
        # past 180 degrees (or PI radians) counterclockwise will get you negative numbers: 180 turn into -179, not 181 (it's not an integer though)
        self.initial_angle = atan2(mouseloc_centered.y, mouseloc_centered.x)
        self.angle_now = self.initial_angle

        # change the axis of rotation
        if bpy.data.scenes[0].axis_roll == "X":
            self.camNormal = Vector((1, 0, 0))
        elif bpy.data.scenes[0].axis_roll == "Y":
            self.camNormal = Vector((0, 0, -1))
        elif bpy.data.scenes[0].axis_roll == "Z":
            self.camNormal = Vector((0, 1, 0))

        return {'RUNNING_MODAL'}

    def execute(self, context):
        rv3d = context.space_data.region_3d

        angle_diff = self.angle_now - self.initial_angle
        quat = Quaternion(self.camNormal, angle_diff)
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
            mouseloc = Vector((event.mouse_region_x, event.mouse_region_y))
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

    axis: bpy.props.StringProperty()

    def execute(self, context):
        if self.axis == 'X':
            bpy.data.scenes[0].axis_roll = 'X'
        if self.axis == 'Y':
            bpy.data.scenes[0].axis_roll = 'Y'
        if self.axis == 'Z':
            bpy.data.scenes[0].axis_roll = 'Z'

        return {'FINISHED'}


class ToggleProp(Operator):
    bl_idname = "aaa.toggle_prop"
    bl_label = ""
    bl_options = {'UNDO'}

    prop: bpy.props.StringProperty()

    def execute(self, context):
        exec(self.prop+" = not "+self.prop)
        return {'FINISHED'}


class TestOperator(Operator):
    """Test Operator Docstring"""

    bl_idname = "aaa.test_operator"
    bl_label = "Test Operator"
    bl_options = {'REGISTER', 'UNDO'}

    testVal: bpy.props.IntProperty()

    def execute(self, context):
        time = str(datetime.time(datetime.now()))
        print("{}: {}".format(self.testVal, time[:-7]))

        return {'FINISHED'}


classes = (
    SaveFile,
    SaveIncremental,

    SwitchWorkspace,

    RollViewport,
    RollAxis,

    ToggleProp,
    TestOperator,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
