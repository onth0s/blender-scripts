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


def global_keymap():
    C = bpy.context

    kc = C.window_manager.keyconfigs.addon
    pie = "wm.call_menu_pie"

    ################################# GLOBAL ##################################
    km = kc.keymaps.new('Window', space_type='EMPTY')

    km.keymap_items.new(pie, 'C', 'PRESS') \
        .properties.name = "PIE_MT_KEY_CONDITIONS"
    km.keymap_items.new(pie, 'S', 'PRESS', ctrl=True) \
        .properties.name = "PIE_MT_SAVE_N_STUFF"

    ################################# 3D VIEW #################################
    km = kc.keymaps.new('3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new(
        'aaa.roll_viewport', 'MIDDLEMOUSE', 'CLICK_DRAG', alt=True)

    ################################ OUTLINER #################################
    km = kc.keymaps.new('Outliner', space_type='OUTLINER')
    kmi = km.keymap_items.new(
        "outliner.collection_new", 'N', 'PRESS', ctrl=True)

    ################################ OVERRIDES ################################
    km = kc.keymaps.new('3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new(
        "view3d.view_center_pick", 'MIDDLEMOUSE', 'CLICK',
        ctrl=True, alt=True)


def register():
    global_keymap()


def unregister():
    global_keymap()


if __name__ == "__main__":
    register()
