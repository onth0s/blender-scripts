import bpy  # type: ignore
from bpy.props import BoolProperty, IntProperty, StringProperty  # type: ignore

# Declarative scene properties configuration mapping: (name, property_factory_ref, args_dict)
SCENE_PROPERTIES = [
    ("conditions", StringProperty, {
        "name": "Global Conditions",
        "description": "A global variable for storing conditions",
        "default": "TRANSFORM",
    }),
    ("show_overlays", BoolProperty, {"default": False}),
    ("show_gizmo", BoolProperty, {"default": False}),
    ("show_t_menu", BoolProperty, {"default": False}),
    ("show_n_menu", BoolProperty, {"default": False}),
    ("show_region_asset_shelf", BoolProperty, {"default": False}),
    ("show_bool_toggle", BoolProperty, {"default": False}),
    ("axis_roll", StringProperty, {}),
    ("loop_frames", BoolProperty, {"default": False}),
    ("already_saved_counter", IntProperty, {}),
]


def register():
    for name, prop_type, kwargs in SCENE_PROPERTIES:
        setattr(bpy.types.Scene, name, prop_type(**kwargs))


def unregister():
    for name, _, _ in SCENE_PROPERTIES:
        if hasattr(bpy.types.Scene, name):
            delattr(bpy.types.Scene, name)


if __name__ == "__main__":
    register()
