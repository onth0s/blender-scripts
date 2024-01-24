# TODO <pep8-80 compliant>

import bpy

def TestKeymap():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    pie = "wm.call_menu_pie"

    # Depending on the context.area.type (space_type) the same key does 
    # different things
    # but you cannot assign arbitrary conditions to be checked, like the 
    # object type
    # AFAIK

    # you can call it from anywhere
    # ------------------------   Any   ------------------------ #
    km = kc.keymaps.new('Window', space_type='EMPTY', region_type='WINDOW')
    
    kmi = km.keymap_items.new(pie, 'C', 'PRESS')\
        .properties.name="PIE_MT_KEY_CONDITIONS"

    kmi = km.keymap_items.new(pie, 'S', 'PRESS', ctrl=True)\
        .properties.name="PIE_MT_SAVE_N_STUFF"
    
    #####################################################################
    # START ------------------   GLOBAL KEYS   ------------------------ #
    #####################################################################
    
    # check arbitrary conditions before executing certain python code
    
    # shift, ctrl, alt
    # thats the order I'm gonna use

    kmi = km.keymap_items.new("aaa.key_e", 'E', 'PRESS')
    kmi = km.keymap_items.new("aaa.key_q", 'Q', 'PRESS')
    kmi = km.keymap_items.new("aaa.key_w", 'W', 'PRESS')
   
    kmi = km.keymap_items.new("aaa.shift_a"    , 'A', 'PRESS', shift=True)
    kmi = km.keymap_items.new("aaa.shift_e"    , 'E', 'PRESS', shift=True)
    kmi = km.keymap_items.new("aaa.shift_q"    , 'Q', 'PRESS', shift=True)
    kmi = km.keymap_items.new("aaa.shift_alt_f", 'F', 'PRESS', shift=True,\
        alt=True)
    
    kmi = km.keymap_items.new("aaa.ctrl_f"    , 'F', 'PRESS', ctrl=True)
    kmi = km.keymap_items.new("aaa.ctrl_alt_h", 'H', 'PRESS', ctrl=True,\
        alt=True)
    
    kmi = km.keymap_items.new("aaa.alt_a", 'A', 'PRESS', alt=True)
    kmi = km.keymap_items.new("aaa.alt_q", 'Q', 'PRESS', alt=True)
    kmi = km.keymap_items.new("aaa.alt_s", 'S', 'PRESS', alt=True)

    #####################################################################
    # END --------------------   GLOBAL KEYS   ------------------------ #
    #####################################################################

    # ------------------------   3D View   ------------------------ #
    km = kc.keymaps.new('3D View', space_type='VIEW_3D', region_type='WINDOW')

    # Roll View with Alt MMB
    kmi = km.keymap_items.new('aaa.roll_viewport', 'MIDDLEMOUSE', 'PRESS',\
        alt=True)
        
    # Unsorted Pie Menus TODO
    kmi = km.keymap_items.new(pie, 'SPACE', 'PRESS').properties\
        .name="PIE_MT_SPACE"
    kmi = km.keymap_items.new(pie, 'S', 'PRESS').properties.name="PIE_MT_S"
    kmi = km.keymap_items.new(pie, 'D', 'PRESS').properties.name="VIEW3D_MT_GP_BRUSHES_PIE"

    kmi = km.keymap_items.new(pie, 'A', 'PRESS').properties\
        .name="VIEW3D_MT_ANIMATION_PIE"
    kmi = km.keymap_items.new(pie, 'Z', 'PRESS').properties\
        .name="VIEW3D_MT_SHADING_PIE"



    km = kc.keymaps.new('Node Generic', space_type='NODE_EDITOR', region_type='WINDOW')
    kmi = km.keymap_items.new(pie, 'SPACE', 'PRESS').properties\
        .name="PIE_MT_SPACE"
    


    # It doesn't seem to work, even if it adds the Operator to the Keymap

    # km = kc.keymaps.new('Sequencer', space_type='SEQUENCE_EDITOR', region_type='WINDOW')
    # kmi = km.keymap_items.new(pie, 'A'    , 'PRESS').properties\
    #     .name="VIEW3D_MT_ANIMATION_PIE"
    # kmi = km.keymap_items.new(pie, 'SPACE', 'PRESS').properties\
    #     .name="PIE_MT_SPACE"



    # call a pie menu from the timeline. I belive. it looks like it
    # ------------------------   Timeline   ------------------------ #
    km = kc.keymaps.new('Animation', space_type='EMPTY', region_type='WINDOW')
    
    kmi = km.keymap_items.new(pie, 'A', 'PRESS').properties\
        .name="VIEW3D_MT_ANIMATION_PIE"
    kmi = km.keymap_items.new(pie, 'S', 'PRESS').properties\
        .name="VIEW3D_MT_TIMELINE_TEST"
    
    kmi = km.keymap_items.new(pie, 'SPACE', 'PRESS').properties\
        .name="VIEW3D_MT_TIMELINE_PIE"
   
def register():
    TestKeymap()
def unregister():
    TestKeymap()

if __name__ == "__main__":
    register()