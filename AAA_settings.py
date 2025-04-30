import bpy
from bpy.props import (
    IntProperty, FloatProperty,
    BoolProperty, StringProperty,
    EnumProperty, CollectionProperty,
    PointerProperty)
from bpy.types import (Operator, PropertyGroup, UIList)


class TestSettings(PropertyGroup):
    def dummy_update(self, context):
        pass

    bpy.types.Scene.conditions = StringProperty(
        name="Global Conditions",
        description="A global variable for storing conditions",
        default="TRANSFORM",
        update=dummy_update
    )

    bpy.types.Scene.axis_roll = StringProperty()

    bpy.types.Scene.loop_frames = BoolProperty(default=False)


# '_UL_' recommended infix


classes = [
    # keep the order to not break anything

    TestSettings,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
