import bpy  # type: ignore

addon_keymaps = []

# Configuration table for global window shortcut mappings: (idname, key, type, modifiers, properties_dict)
WINDOW_KEYS = [
    ("aaa.test_context_debugger", 'P', 'PRESS', {'shift': True, 'ctrl': True, 'alt': True}, None),
    ("wm.call_menu_pie", 'SPACE', 'PRESS', {}, {"name": "PIE_MT_SPACE"}),
    ("wm.call_menu_pie", 'S', 'PRESS', {}, {"name": "PIE_MT_S"}),
    ("wm.call_menu_pie", 'A', 'PRESS', {}, {"name": "PIE_MT_ANIMATION"}),
    ("wm.call_menu_pie", 'Z', 'PRESS', {}, {"name": "VIEW3D_MT_SHADING_PIE"}),
    ("wm.call_menu_pie", 'C', 'PRESS', {}, {"name": "PIE_MT_KEY_CONDITIONS"}),
    ("wm.call_menu_pie", 'S', 'PRESS', {'ctrl': True}, {"name": "PIE_MT_SAVE_N_STUFF"}),
    ("aaa.key_q", 'Q', 'PRESS', {}, None),
    ("aaa.key_w", 'W', 'PRESS', {}, None),
    ("aaa.key_e", 'E', 'PRESS', {}, None),
]

# Configuration table for 3D View shortcut mappings
VIEW_3D_KEYS = [
    ("aaa.roll_viewport", 'MIDDLEMOUSE', 'CLICK_DRAG', {'alt': True}, None),
    ("view3d.view_selected", 'MIDDLEMOUSE', 'PRESS', {'shift': True, 'ctrl': True}, None),
    ("view3d.view_center_pick", 'MIDDLEMOUSE', 'PRESS', {'ctrl': True, 'alt': True}, None),
]

# Configuration table for Image Editor shortcut mappings
IMAGE_KEYS = [
    ("image.view_zoom_ratio", 'MIDDLEMOUSE', 'PRESS', {'shift': True, 'ctrl': True}, {"ratio": 1}),
]


def global_keymap():
    kc = bpy.context.window_manager.keyconfigs.addon
    if not kc:
        return

    # Helper function to create items from declarative list
    def setup_items(km, list_items):
        for idname, key, type_str, mods, props in list_items:
            kmi = km.keymap_items.new(idname, key, type_str,
                                      shift=mods.get('shift', False),
                                      ctrl=mods.get('ctrl', False),
                                      alt=mods.get('alt', False))
            if props:
                for k, v in props.items():
                    setattr(kmi.properties, k, v)

    # 1. WINDOW keymaps
    km_window = kc.keymaps.new('Window', space_type='EMPTY', region_type='WINDOW')
    addon_keymaps.append(km_window)
    setup_items(km_window, WINDOW_KEYS)

    # 2. 3D VIEW keymaps
    km_3d = kc.keymaps.new('3D View', space_type='VIEW_3D', region_type='WINDOW')
    addon_keymaps.append(km_3d)
    setup_items(km_3d, VIEW_3D_KEYS)

    # 3. IMAGE keymaps
    km_image = kc.keymaps.new('Image', space_type='IMAGE_EDITOR', region_type='WINDOW')
    addon_keymaps.append(km_image)
    setup_items(km_image, IMAGE_KEYS)


def register():
    global_keymap()


def unregister():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        for km in addon_keymaps:
            kc.keymaps.remove(km)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
