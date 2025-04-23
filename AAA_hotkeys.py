import bpy  # type: ignore

""" USEFUL ENUMS: space_type, region_type 
space_types = {
    "Empty": "EMPTY",
    
    "General": ["VIEW_3D",
                "IMAGE_EDITOR",
                "NODE_EDITOR",
                "SEQUENCE_EDITOR",
                "CLIP_EDITOR"],
    
    "Animation": ["DOPESHEET_EDITOR",
                "GRAPH_EDITOR",
                "NLA_EDITOR"],
    
    "Scripting": ["TEXT_EDITOR",
                "CONSOLE",
                "INFO",
                "TOPBAR",
                "STATUSBAR"],
    
    "Data": ["OUTLINER",
            "PROPERTIES",
            "FILE_BROWSER",
            "SPREADSHEET",
            "PREFERENCES"]
}
region_types = [
    "WINDOW", "HEADER", "CHANNELS",
    "TEMPORARY", "UI", "TOOLS",
    "TOOL_PROPS", "ASSET_SHELF", "ASSET_SHELF_HEADER",
    "PREVIEW", "HUD", "NAVIGATION_BAR",
    "EXECUTE", "FOOTER", "TOOL_HEADER", "XR"
]
"""

# TODO THIS SHIT IS ACTUALLY MAGIC
# for km in bpy.context.window_manager.keyconfigs.active.keymaps:
#     print(km.name, km.space_type)
# TODO GET ***ALL*** KEYMAP-SPACE_TYPE COMBINATIONS


def global_keymap():
    C = bpy.context

    kc = C.window_manager.keyconfigs.addon
    pie = "wm.call_menu_pie"

    ################################# GLOBAL ##################################
    km = kc.keymaps.new('Window', space_type='EMPTY')

    km.keymap_items.new("aaa.test_context_debugger", 'P', 'PRESS',
                        shift=True, ctrl=True, alt=True)

    km.keymap_items.new(pie, 'SPACE', 'PRESS') \
        .properties.name = "PIE_MT_SPACE"
    km.keymap_items.new(pie, 'C', 'PRESS') \
        .properties.name = "PIE_MT_KEY_CONDITIONS"
    km.keymap_items.new(pie, 'S', 'PRESS', ctrl=True) \
        .properties.name = "PIE_MT_SAVE_N_STUFF"

    # currently if you try to use the Global Keys it will throw an error
    # when you call it while the mouse is over the transparent part of the
    # N Panel. The working fix is to simply limit the keymap to the
    # 3D View.
    # TODO: find a way to make it work globally.

    # km.keymap_items.new("aaa.key_q", 'Q', 'PRESS')
    # km.keymap_items.new("aaa.key_w", 'W', 'PRESS')
    # km.keymap_items.new("aaa.key_e", 'E', 'PRESS')

    ################################# 3D VIEW #################################
    km = kc.keymaps.new('3D View', space_type='VIEW_3D')
    km.keymap_items.new(
        'aaa.roll_viewport', 'MIDDLEMOUSE', 'CLICK_DRAG', alt=True)
    km.keymap_items.new(
        'view3d.view_selected', 'MIDDLEMOUSE', 'PRESS', shift=True, ctrl=True)

    km.keymap_items.new("aaa.key_q", 'Q', 'PRESS')
    km.keymap_items.new("aaa.key_w", 'W', 'PRESS')
    km.keymap_items.new("aaa.key_e", 'E', 'PRESS')

    ################################# FRAMES ##################################
    km = kc.keymaps.new('Dopesheet', space_type='DOPESHEET_EDITOR',
                        region_type='WINDOW')

    km.keymap_items.new("aaa.key_q", 'Q', 'PRESS')
    km.keymap_items.new("aaa.key_w", 'W', 'PRESS')
    km.keymap_items.new("aaa.key_e", 'E', 'PRESS')

    ################################ OUTLINER #################################
    km = kc.keymaps.new('Outliner', space_type='OUTLINER')
    km.keymap_items.new(
        "outliner.collection_new", 'N', 'PRESS', ctrl=True)

    ################################ OVERRIDES ################################
    km = kc.keymaps.new('3D View', space_type='VIEW_3D')
    km.keymap_items.new(
        "view3d.view_center_pick", 'MIDDLEMOUSE', 'CLICK',
        ctrl=True, alt=True)


def register():
    global_keymap()


def unregister():
    global_keymap()


if __name__ == "__main__":
    register()
