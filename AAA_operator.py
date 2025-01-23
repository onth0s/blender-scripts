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
    bl_idname = "aaa.save_file"
    bl_label = "saveFile"
    bl_options = {'REGISTER'}

    def execute(self, context):
        filename = bpy.path.basename(bpy.context.blend_data.filepath)
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


class TestOperator(Operator):
    bl_idname = "aaa.test_operator"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    testVal: bpy.props.IntProperty()

    def execute(self, context):
        time = str(datetime.time(datetime.now()))
        print("{}: {}".format(self.testVal, time[:-7]))

        return {'FINISHED'}


classes = (
    SaveFile,
    SaveIncremental,

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
