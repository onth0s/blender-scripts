import bpy  # type: ignore
from bpy.types import Operator  # type: ignore

class ReorderModifiers(Operator):
    bl_idname = "aaa.reorder_modifiers"
    bl_label = "Reorder Modifiers"
    bl_options = {"REGISTER"}

    name: bpy.props.StringProperty()  # type: ignore
    where: bpy.props.StringProperty()  # type: ignore
    index: bpy.props.IntProperty()  # type: ignore

    def execute(self, context):
        OBJ_obj = context.active_object
        mods = OBJ_obj.modifiers

        print(">> self.index:")
        print(self.index)

        if self.where == "UP" and self.index > 0:
            mods.move(self.index, self.index - 1)
        elif self.where == "DOWN" and self.index < len(mods) - 1:
            mods.move(self.index, self.index + 1)

        elif self.where == "TOP":
            bpy.ops.object.modifier_move_to_index(modifier=self.name, index=0)
        elif self.where == "BOTTOM":
            bpy.ops.object.modifier_move_to_index(
                modifier=self.name, index=len(mods) - 1
            )

        return {"FINISHED"}


class AddMaterial(Operator):
    bl_idname = "aaa.add_material"
    bl_label = "Add Material"
    bl_options = {"REGISTER", "UNDO"}

    mode: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        OB = context.active_object

        if self.mode == "NEW":
            mat = bpy.data.materials.new(name="Material")
        elif self.mode == "LAST":
            mat = bpy.data.materials[-1]

        mat.use_nodes = True
        if OB.data.materials:
            OB.data.materials[0] = mat
        else:
            OB.data.materials.append(mat)

        return {"FINISHED"}


class AAA_OT_clear_all_transforms(Operator):
    bl_idname = "aaa.clear_all_transforms"
    bl_label = "Clear All Transforms"
    bl_options = {"UNDO"}

    def execute(self, context):
        for ob in context.selected_objects:
            ob.location = (0.0, 0.0, 0.0)
            if ob.rotation_mode == "QUATERNION":
                ob.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
            elif ob.rotation_mode == "AXIS_ANGLE":
                ob.rotation_axis_angle = (0.0, 0.0, 1.0, 0.0)
            else:
                ob.rotation_euler = (0.0, 0.0, 0.0)
            ob.scale = (1.0, 1.0, 1.0)
        return {"FINISHED"}


class AAA_OT_clear_except_location(Operator):
    bl_idname = "aaa.clear_except_location"
    bl_label = "Clear Except Location"
    bl_options = {"UNDO"}

    def execute(self, context):
        for ob in context.selected_objects:
            if ob.rotation_mode == "QUATERNION":
                ob.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
            elif ob.rotation_mode == "AXIS_ANGLE":
                ob.rotation_axis_angle = (0.0, 0.0, 1.0, 0.0)
            else:
                ob.rotation_euler = (0.0, 0.0, 0.0)
            ob.scale = (1.0, 1.0, 1.0)
        return {"FINISHED"}
