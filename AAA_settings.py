import bpy  # type: ignore
from bpy.props import BoolProperty, IntProperty, StringProperty  # type: ignore


def register():
    bpy.types.Scene.conditions = StringProperty(
        name="Global Conditions",
        description="A global variable for storing conditions",
        default="TRANSFORM",
    )

    bpy.types.Scene.show_overlays = BoolProperty(default=False)
    bpy.types.Scene.show_gizmo = BoolProperty(default=False)
    bpy.types.Scene.show_t_menu = BoolProperty(default=False)
    bpy.types.Scene.show_n_menu = BoolProperty(default=False)
    bpy.types.Scene.show_region_asset_shelf = BoolProperty(default=False)
    bpy.types.Scene.show_bool_toggle = BoolProperty(default=False)

    bpy.types.Scene.axis_roll = StringProperty()

    bpy.types.Scene.loop_frames = BoolProperty(default=False)

    bpy.types.Scene.already_saved_counter = IntProperty()


def unregister():
    del bpy.types.Scene.conditions
    del bpy.types.Scene.show_overlays
    del bpy.types.Scene.show_gizmo
    del bpy.types.Scene.show_t_menu
    del bpy.types.Scene.show_n_menu
    del bpy.types.Scene.show_region_asset_shelf
    del bpy.types.Scene.show_bool_toggle
    del bpy.types.Scene.axis_roll
    del bpy.types.Scene.loop_frames
    del bpy.types.Scene.already_saved_counter


if __name__ == "__main__":
    register()
