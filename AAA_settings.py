import bpy  # type: ignore
from bpy.props import (  # type: ignore
    IntProperty, FloatProperty,
    BoolProperty, StringProperty,
    EnumProperty, CollectionProperty,
    PointerProperty)
from bpy.types import (Operator, PropertyGroup, UIList)  # type: ignore


class TestSettings(PropertyGroup):
    SN = bpy.types.Scene

    def dummy_update(self, context):
        pass

    SN.conditions = StringProperty(
        name="Global Conditions",
        description="A global variable for storing conditions",
        default="TRANSFORM",
        update=dummy_update
    )

    SN.show_overlays = BoolProperty(default=False, update=dummy_update)
    SN.show_gizmo = BoolProperty(default=False, update=dummy_update)
    SN.show_t_menu = BoolProperty(default=False, update=dummy_update)
    SN.show_n_menu = BoolProperty(default=False, update=dummy_update)
    SN.show_region_asset_shelf = BoolProperty(default=False, update=dummy_update)
    SN.show_bool_toggle = BoolProperty(default=False, update=dummy_update)

    SN.axis_roll = StringProperty()

    SN.loop_frames = BoolProperty(default=False)

    SN.already_saved_counter = IntProperty()



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
