import bpy  # type: ignore

addon_keymaps = []

def global_keymap():
    kc = bpy.context.window_manager.keyconfigs.addon
    pie = "wm.call_menu_pie"

    ################################# GLOBAL ##################################
    km = kc.keymaps.new('Window', space_type='EMPTY', region_type='WINDOW')
    addon_keymaps.append(km)

    # Magic context debugger
    km.keymap_items.new("aaa.test_context_debugger", 'P', 'PRESS',
                        shift=True, ctrl=True, alt=True)

    km.keymap_items.new(pie, 'SPACE', 'PRESS') \
        .properties.name = "PIE_MT_SPACE"

    km.keymap_items.new(pie, 'S', 'PRESS').properties.name = "PIE_MT_S"

    km.keymap_items.new(pie, 'A', 'PRESS').properties.name = "PIE_MT_ANIMATION"

    km.keymap_items.new(pie, 'Z', 'PRESS').properties\
        .name = "VIEW3D_MT_SHADING_PIE"

    km.keymap_items.new(pie, 'C', 'PRESS') \
        .properties.name = "PIE_MT_KEY_CONDITIONS"

    km.keymap_items.new(pie, 'S', 'PRESS', ctrl=True) \
        .properties.name = "PIE_MT_SAVE_N_STUFF"

    km.keymap_items.new("aaa.key_q", 'Q', 'PRESS')
    km.keymap_items.new("aaa.key_w", 'W', 'PRESS')
    km.keymap_items.new("aaa.key_e", 'E', 'PRESS')

    ################################# 3D VIEW #################################
    km = kc.keymaps.new('3D View', space_type='VIEW_3D', region_type='WINDOW')
    addon_keymaps.append(km)

    km.keymap_items.new(
        'aaa.roll_viewport', 'MIDDLEMOUSE', 'CLICK_DRAG', alt=True)

    ################################ OVERRIDES ################################
    # General keymaps for operators that already exist on Blender by default,
    # but that's it's convenient to add them here so you only have to disable
    # the default key bindings that could collide to use this ones.
    # You can probaly handle the collision programatically, but I don't know
    # how yet.

    km = kc.keymaps.new('3D View', space_type='VIEW_3D', region_type='WINDOW')
    addon_keymaps.append(km)

    km.keymap_items.new('view3d.view_selected', 'MIDDLEMOUSE',
                        'PRESS', shift=True, ctrl=True)
    km.keymap_items.new("view3d.view_center_pick", 'MIDDLEMOUSE', 'PRESS',
                        ctrl=True, alt=True)

    km = kc.keymaps.new('Image', space_type='IMAGE_EDITOR',
                        region_type='WINDOW')
    addon_keymaps.append(km)

    kmi = km.keymap_items.new('image.view_zoom_ratio', 'MIDDLEMOUSE',
                              'PRESS', shift=True, ctrl=True)
    kmi.properties.ratio = 1


def register():
    global_keymap()


def unregister():
    kc = bpy.context.window_manager.keyconfigs.addon
    for km in addon_keymaps:
        kc.keymaps.remove(km)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
