import bpy
import os
import re
from datetime import datetime

from bpy.props import (FloatProperty, IntProperty, BoolProperty, StringProperty)
from bpy.types            import (Menu, Operator)
from bl_operators.presets import AddPresetBase
from mathutils            import *
from math                 import *
 
from AAA_var import *


''' Notes

    I dont know how to set up the poll() function

    bpy.ops.info.reports_display_update()
    doesnt work as expected. well, it doesnt work at all
    I need to register the operator and get some flood if i wanna update the Info Editor
'''

class VSEAlignStrip(Operator):
    bl_idname = "aaa.vse_align_strip"
    bl_label = "Align Strip"
    bl_options = {'REGISTER'}
    
    location: bpy.props.StringProperty()

    @classmethod #this shit is necessary
    def poll(cls, context):
        strip = context.active_sequence_strip

        tmp = False
        for sq in bpy.context.scene.sequence_editor.sequences_all:
            if sq.select:
                tmp = True
                break

        return tmp and (strip.type in ['IMAGE', 'MOVIE'])

    def execute(self, context):
        strip = context.active_sequence_strip
        
        x = context.scene.render.resolution_x
        y = context.scene.render.resolution_y
        
        width = strip.elements[0].orig_width * strip.transform.scale_x
        height = strip.elements[0].orig_height * strip.transform.scale_y
        
        offset_x = 0
        offset_y = 0

        if self.location == 'TOP_LEFT':
            offset_x = (x - width) / 2 * -1   
            offset_y = (y - height) / 2
        elif self.location == 'TOP_CENTRE':
            offset_x = 0
            offset_y = (y - height) / 2
        elif self.location == 'TOP_RIGHT':
            offset_x = (x - width) / 2
            offset_y = (y - height) / 2

        elif self.location == 'MIDDLE_LEFT':
            offset_x = (x - width) / 2 * -1   
            offset_y = 0
        elif self.location == 'MIDDLE_CENTRE':
            offset_x = 0
            offset_y = 0
        elif self.location == 'MIDDLE_RIGHT':
            offset_x = (x - width) / 2
            offset_y = 0

        elif self.location == 'BOTTOM_LEFT':
            offset_x = (x - width) / 2 * -1   
            offset_y = (y - height) / 2 * -1   
        elif self.location == 'BOTTOM_CENTRE':
            offset_x = 0
            offset_y = (y - height) / 2 * -1   
        elif self.location == 'BOTTOM_RIGHT':
            offset_x = (x - width) / 2
            offset_y = (y - height) / 2 * -1   

        strip.transform.offset_x = offset_x
        strip.transform.offset_y = offset_y

        return {'FINISHED'}
class VSECustomFade(Operator):
    bl_idname = "aaa.vse_custom_fade"
    bl_label = ""
    bl_options = {'REGISTER'}
    
    type: bpy.props.StringProperty()
    
    @classmethod # TODO this shit now it doesn't work as it should
    def poll(cls, context):
        strip = context.active_sequence_strip

        tmp = False
        for sq in bpy.context.scene.sequence_editor.sequences_all:
            if sq.select:
                tmp = True
                break

        return tmp and (strip.type in ['TEXT', 'IMAGE', 'MOVIE'])
    
    def execute(self, context):
        #fc = C.scene.animation_data.action.fcurves.find(C.active_sequence_strip.path_from_id("blend_alpha"))
        C = context 
        FADE_LENGHT = 6
        
        strip = C.active_sequence_strip
        datapath = strip.path_from_id("blend_alpha")

        frame_start = strip.frame_start
        frame_start2 = frame_start + FADE_LENGHT

        frame_end = strip.frame_final_end - 1
        frame_end2 = frame_end - FADE_LENGHT

        fc = C.scene.animation_data.action.fcurves.find(datapath) if hasattr(C.scene.animation_data.action, 'fcurves') else bpy.data.actions.new(name="CustomFade")        
        if self.type == 'START':
            if hasattr(fc, 'keyframe_points'):
                if len(fc.keyframe_points) == 2:
                    if int(fc.keyframe_points[0].co.x) == strip.frame_start:
                        # if the first keyframe is at the start of the active stip, then we know it a fade in
                        pass
                    else:
                        strip.keyframe_insert(data_path='blend_alpha', frame=frame_start)
                        strip.keyframe_insert(data_path='blend_alpha', frame=frame_start2)

                        fc.keyframe_points[0].co.y = 0      
                        fc.keyframe_points[1].co.y = 1

                        fc.keyframe_points[0].handle_left.x  = frame_start  - (FADE_LENGHT / 3) 
                        fc.keyframe_points[0].handle_right.x = frame_start  + (FADE_LENGHT / 3) 
                        fc.keyframe_points[1].handle_left.x  = frame_start2 - (FADE_LENGHT / 3)
                        fc.keyframe_points[1].handle_right.x = frame_start2 + (FADE_LENGHT / 3)
                        
                        fc.keyframe_points[2].handle_left.x = frame_end2 - (FADE_LENGHT / 3) 

                        fc.keyframe_points[0].handle_left.y  = 0
                        fc.keyframe_points[0].handle_right.y = 0
                        fc.keyframe_points[1].handle_left.y  = 1
                        fc.keyframe_points[1].handle_right.y = 1
                else: 
                    bpy.ops.error.message('INVOKE_DEFAULT', type="Error", message="incorrect number of keyframes, something is fucked (aaa.vse_custom_fade)")
            else: 
                strip.keyframe_insert(data_path='blend_alpha', frame=frame_start)
                strip.keyframe_insert(data_path='blend_alpha', frame=frame_start2)

                fc = C.scene.animation_data.action.fcurves.find(datapath)

                fc.keyframe_points[0].co.y = 0      
                fc.keyframe_points[1].co.y = 1

                fc.keyframe_points[0].handle_left.y  = 0
                fc.keyframe_points[0].handle_right.y = 0
                fc.keyframe_points[1].handle_left.y  = 1
                fc.keyframe_points[1].handle_right.y = 1
       
        elif self.type == 'END':
            if hasattr(fc, 'keyframe_points'):
                if len(fc.keyframe_points) == 2:
                    if int(fc.keyframe_points[1].co.x) + 1 == frame_end:
                        # if the last keyframe is at the end of the active stip, then we know it a fade out
                        pass
                    else:
                        strip.keyframe_insert(data_path='blend_alpha', frame=frame_end)
                        strip.keyframe_insert(data_path='blend_alpha', frame=frame_end2)

                        fc.keyframe_points[0 + 2].co.y = 1      
                        fc.keyframe_points[1 + 2].co.y = 0

                        fc.keyframe_points[0 + 2].handle_left.x  = frame_end2 - (FADE_LENGHT / 3) 
                        fc.keyframe_points[0 + 2].handle_right.x = frame_end2 + (FADE_LENGHT / 3) 
                        fc.keyframe_points[1 + 2].handle_left.x  = frame_end  - (FADE_LENGHT / 3)
                        fc.keyframe_points[1 + 2].handle_right.x = frame_end  + (FADE_LENGHT / 3)

                        fc.keyframe_points[1].handle_right.x = frame_start2 + (FADE_LENGHT / 3)

                        fc.keyframe_points[0 + 2].handle_left.y  = 1
                        fc.keyframe_points[0 + 2].handle_right.y = 1
                        fc.keyframe_points[1 + 2].handle_left.y  = 0
                        fc.keyframe_points[1 + 2].handle_right.y = 0
                else: 
                    bpy.ops.error.message('INVOKE_DEFAULT', type="Error", message="incorrect number of keyframes, something is fucked (aaa.vse_custom_fade)")
            else: 
                strip.keyframe_insert(data_path='blend_alpha', frame=frame_end - 1)
                strip.keyframe_insert(data_path='blend_alpha', frame=frame_end2)

                fc = C.scene.animation_data.action.fcurves.find(datapath)

                fc.keyframe_points[0].co.y = 1      
                fc.keyframe_points[1].co.y = 0

                fc.keyframe_points[0].handle_left.y  = 1
                fc.keyframe_points[0].handle_right.y = 1
                fc.keyframe_points[1].handle_left.y  = 0
                fc.keyframe_points[1].handle_right.y = 0
        
        elif self.type == 'BOTH' and not hasattr(fc, 'keyframe_points'):
            strip.keyframe_insert(data_path='blend_alpha', frame=frame_start)
            strip.keyframe_insert(data_path='blend_alpha', frame=frame_start2)
            strip.keyframe_insert(data_path='blend_alpha', frame=frame_end)
            strip.keyframe_insert(data_path='blend_alpha', frame=frame_end2)
           
            fc = C.scene.animation_data.action.fcurves.find(datapath)

            fc.keyframe_points[0].co.y = 0      
            fc.keyframe_points[1].co.y = 1
            fc.keyframe_points[2].co.y = 1      
            fc.keyframe_points[3].co.y = 0

            fc.keyframe_points[0].handle_left.y  = 0
            fc.keyframe_points[0].handle_right.y = 0
            fc.keyframe_points[1].handle_left.y  = 1
            fc.keyframe_points[1].handle_right.y = 1
            fc.keyframe_points[2].handle_left.y  = 1
            fc.keyframe_points[2].handle_right.y = 1
            fc.keyframe_points[3].handle_left.y  = 0
            fc.keyframe_points[3].handle_right.y = 0

            fc.keyframe_points[0].handle_left.x  = frame_start  - (FADE_LENGHT / 3) 
            fc.keyframe_points[0].handle_right.x = frame_start  + (FADE_LENGHT / 3) 
            fc.keyframe_points[1].handle_left.x  = frame_start2 - (FADE_LENGHT / 3)
            fc.keyframe_points[1].handle_right.x = frame_start2 + (FADE_LENGHT / 3)
            fc.keyframe_points[2].handle_left.x  = frame_end2   - (FADE_LENGHT / 3) 
            fc.keyframe_points[2].handle_right.x = frame_end2   + (FADE_LENGHT / 3) 
            fc.keyframe_points[3].handle_left.x  = frame_end    - (FADE_LENGHT / 3)
            fc.keyframe_points[3].handle_right.x = frame_end    + (FADE_LENGHT / 3)

        return {'FINISHED'}
class VSECustomFadeClear(Operator):
    bl_idname = "aaa.vse_custom_fade_clear"
    bl_label = ""
    bl_options = {'REGISTER'}
    
    type: bpy.props.StringProperty()


    def execute(self, context):
        C = context 
        
        strip = C.active_sequence_strip
        datapath = strip.path_from_id("blend_alpha")
     
        if self.type == 'START':
            pass
        elif self.type == 'END':
            pass
        elif self.type == 'BOTH':
            # fc = C.scene.animation_data.action.fcurves.find(datapath)
            # fc.keyframe_points.clear()
            pass


        return {'FINISHED'}
    
class SwitchWorkspace(Operator):
    bl_idname = "aaa.switch_workspace"
    bl_label = ""
    bl_options = {'REGISTER'}
    
    name: bpy.props.StringProperty()
    def execute(self, context):
        bpy.context.window.workspace = bpy.data.workspaces[self.name]
        return {'FINISHED'}

class ToggleOverlays(Operator):
    bl_idname = "aaa.toggle_overlays"
    bl_label = ""
    bl_options = {'REGISTER'}

    header: bpy.props.BoolProperty()
    def execute(self, context):
        CSD = context.space_data
        CS  = context.scene
        
        if self.header:
            CSD.show_region_header = not CSD.show_region_header
        else:
            # currentState = [
            #     CSD.overlay.show_overlays,
            #     CSD.show_gizmo           ,
            #     CSD.show_region_ui       ,
            #     CSD.show_region_toolbar  ,
            # ]

            if not CS.show_bool_toggle: 
                CS.show_overlays = CSD.overlay.show_overlays
                CS.show_gizmo    = CSD.show_gizmo          
                CS.show_t_menu   = CSD.show_region_ui      
                CS.show_n_menu   = CSD.show_region_toolbar 

                CSD.overlay.show_overlays = False
                CSD.show_gizmo            = False
                CSD.show_region_ui        = False
                CSD.show_region_toolbar   = False
            else: 
                CSD.overlay.show_overlays = CS.show_overlays
                CSD.show_gizmo            = CS.show_gizmo    
                CSD.show_region_ui        = CS.show_t_menu   
                CSD.show_region_toolbar   = CS.show_n_menu   

            CS.show_bool_toggle = not CS.show_bool_toggle

            # print("currentState: {}".format(currentState))
            # print("boolToggle: {}".format(CS.show_bool_toggle))
           
        return {'FINISHED'}
class ToggleSolidWireframe(Operator):
    bl_idname = "aaa.toggle_solid_wireframe"
    bl_label = ""
    bl_options = {'REGISTER'}
    def execute(self, context):
        if context.space_data.shading.type == 'WIREFRAME':
            context.space_data.shading.type = 'SOLID'
        else:
            context.space_data.shading.type = 'WIREFRAME'    
        bpy.data.scenes[0].solidwireframe = not bpy.data.scenes[0].solidwireframe
        return {'FINISHED'}
    def invoke(self, context, event):
        if context.space_data.shading.type == 'WIREFRAME':
            bpy.data.scenes[0].solidwireframe = False
        else:
            bpy.data.scenes[0].solidwireframe = True
        return self.execute(context)
class ToggleWireframeOverlay(Operator):
    bl_idname = "aaa.toggle_wireframe_overlay"
    bl_label = ""
    bl_options = {'REGISTER'}
    
    mode: bpy.props.StringProperty()
    def execute(self, context):
        if self.mode == "ALL_EDGES":
            context.space_data.overlay.show_wireframes = not context.space_data.overlay.show_wireframes
        elif self.mode == "CONTROL_EDGES":
            context.object.modifiers["Subdivision"].show_only_control_edges = not context.object.modifiers["Subdivision"].show_only_control_edges
        return {'FINISHED'}
class ToggleXRay(Operator):
    bl_idname = "aaa.toggle_xray"
    bl_label = ""
    bl_options = {'REGISTER'}
    def execute(self, context):
        if not bpy.data.scenes[0].solidwireframe:
            context.space_data.shading.show_xray_wireframe = not context.space_data.shading.show_xray_wireframe
        else:
            context.space_data.shading.show_xray = not context.space_data.shading.show_xray
        return {'FINISHED'}
class ToggleFaceOrientation(Operator):
    bl_idname = "aaa.toggle_face_orientation"
    bl_label = ""
    bl_options = {'REGISTER'}

    def execute(self, context):
        context.space_data.overlay.show_face_orientation = not context.space_data.overlay.show_face_orientation    
        return {'FINISHED'}

class RollViewport(Operator):
    bl_idname = "aaa.roll_viewport"
    bl_label = "Roll Viewport"
    bl_options = {'GRAB_CURSOR'}
    
    initial_angle = 0
    angle_now = 0
    initial_rotation = Vector((0, 0, 0))
    camNormal = Vector((0, 0, -1))

    temp_degree = 0

    def toDegrees(radians):
        return radians * (180 / pi)
    def to360Degrees(test):
        return radians * (180 / pi)

    def invoke(self, context, event):
        rv3d = context.space_data.region_3d
        context.window_manager.modal_handler_add(self)
        
        ''' TODO
            takes you out from the camera view into the perspective view to call the rotation view modal 
            it should rotate the camera too, or be an option'''
        if rv3d.view_perspective == 'CAMERA':
            rv3d.view_perspective = 'PERSP'
            
        # get the center of the viewport
        self.view3d_bounds = Vector((context.region.width, context.region.height))
        self.view3d_center = self.view3d_bounds / 2
        
        # how far is the mouse from the center, returns a Vector
        mouseloc = Vector((event.mouse_region_x,event.mouse_region_y))
        mouseloc_centered = mouseloc - self.view3d_center
        
        # copy a Quaternion(w, x, y, z) into a Vector((x, y, z)), returns a Quaternion()
        self.initial_rotation = rv3d.view_rotation.copy()
        # the angle in radians from the center of the viewport to the position of the cursor
        # past 180 degrees (or PI radians) counterclockwise will get you negative numbers: 180 turn into -179, not 181 (it's not an integer though)
        self.initial_angle = atan2(mouseloc_centered.y, mouseloc_centered.x)
        self.angle_now = self.initial_angle

        # change the axis of rotation
        if bpy.data.scenes[0].axis_roll == "X": 
            self.camNormal = Vector((1 , 0, 0))
        elif bpy.data.scenes[0].axis_roll == "Y":
            self.camNormal = Vector((0 , 0, -1))
        elif bpy.data.scenes[0].axis_roll == "Z":
            self.camNormal = Vector((0 , 1, 0))

        return {'RUNNING_MODAL'}
    def execute(self, context):
        rv3d = context.space_data.region_3d

        angle_diff = self.angle_now - self.initial_angle
        quat = Quaternion(self.camNormal, angle_diff)
        rv3d.view_rotation = self.initial_rotation @ quat
        
        if angle_diff > 0:
            # print(toDegrees(angle_diff))
            self.temp_degree = angle_diff
        else:
            self.temp_degree = -1 * angle_diff
            a = 2 * pi - self.temp_degree
            # print(toDegrees(a)) 

        return {'FINISHED'}    
    def modal(self, context, event):
        rv3d = context.space_data.region_3d
        
        if event.type == 'MOUSEMOVE':
            mouseloc = Vector((event.mouse_region_x, event.mouse_region_y))
            mouseloc_centered = mouseloc - self.view3d_center
            self.angle_now = atan2(mouseloc_centered.y, mouseloc_centered.x)
            self.execute(context)
        elif event.type in {'LEFTMOUSE', 'MIDDLEMOUSE'}:
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            rv3d.view_rotation = self.initial_rotation
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}
class RollAxis(Operator):
    bl_idname = "aaa.roll_axis"
    bl_label = ""
    bl_options = {'REGISTER'}
    
    axis: bpy.props.StringProperty()
    def execute(self, context):
        if self.axis == 'X': 
            bpy.data.scenes[0].axis_roll = 'X'
        if self.axis == 'Y':
            bpy.data.scenes[0].axis_roll = 'Y'
        if self.axis == 'Z':
            bpy.data.scenes[0].axis_roll = 'Z'

        return {'FINISHED'}

class ModeSet(Operator):
    bl_idname = "aaa.mode_set"
    bl_label = ""
    bl_options = {'UNDO'}

    mode: StringProperty()
    def execute(self, context):
        bpy.ops.object.mode_set(mode=self.mode)

        if self.mode in ('EDIT', 'SCULPT', 'TEXTURE_PAINT', 'WEIGHT_PAINT', 'VERTEX_PAINT'):
            context.space_data.shading.cavity_type = 'WORLD' 
        if self.mode == 'OBJECT':
            context.space_data.shading.cavity_type = 'BOTH'   
        return {'FINISHED'}

class PivotSelector(Operator):
    bl_idname = "aaa.pivot_selector"
    bl_label = ""
    bl_options = {'REGISTER'}
    name: bpy.props.StringProperty()
    def execute(self, context):
        if self.name == "ONLY_ORIGINS":
            context.scene.tool_settings.use_transform_pivot_point_align = not context.scene.tool_settings.use_transform_pivot_point_align
        else:
            bpy.context.scene.tool_settings.transform_pivot_point = self.name
        return {'FINISHED'}    
class CommonTools(Operator):
    bl_idname = "aaa.common_tools"
    bl_label = ""
    bl_options = {'REGISTER'}
    name: bpy.props.StringProperty()
    def execute(self, context):
        if context.mode == MHE: 
            if self.name == "INSET":
                bpy.ops.mesh.inset('INVOKE_DEFAULT')
            if self.name == "BEVEL":
                bpy.ops.mesh.bevel('INVOKE_DEFAULT')
            if self.name == "EXTRUDE":
                bpy.ops.mesh.extrude_region_move('INVOKE_DEFAULT')
            if self.name == "CONNECT_PATH":
                bpy.ops.mesh.vert_connect_path()
            if self.name == "DUPLICATE":
                bpy.ops.mesh.duplicate_move('INVOKE_DEFAULT')
            if self.name == "SUBDIVIDE":
                bpy.ops.mesh.subdivide('INVOKE_DEFAULT')
            if self.name == "REMOVE_DOUBLES":
                bpy.ops.mesh.remove_doubles('INVOKE_DEFAULT')
            if self.name == "SPLIT":
                bpy.ops.mesh.split('INVOKE_DEFAULT')
        if context.mode == CVE: 
            if self.name == "EXTRUDE":
                bpy.ops.curve.extrude_move('INVOKE_DEFAULT')
                # bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        return {'FINISHED'}

class DyntopoDetailing(Operator):
    bl_idname = "aaa.dyntopo_detailing"
    bl_label = ""
    bl_options = {'REGISTER'}
    mode: bpy.props.StringProperty()
    def execute(self, context):
        if self.mode != "SAMPLE":
            context.scene.tool_settings.sculpt.detail_refine_method = self.mode
        else:  
            bpy.ops.sculpt.sample_detail_size('INVOKE_DEFAULT')
        return {'FINISHED'}

class RendererPicker(Operator):
    bl_idname = "aaa.eevee_or_cycles"
    bl_label = ""
    bl_options = {'REGISTER'}
    mode: bpy.props.StringProperty()
    def execute(self, context):
        # They call LookDev 'MATERIAL'
        if self.mode != 'MATERIAL':
                context.scene.render.engine = self.mode
                context.space_data.shading.type = 'RENDERED'
        else: 
            if context.scene.render.engine == 'BLENDER_WORKBENCH':
                context.scene.render.engine = 'BLENDER_EEVEE'
                context.space_data.shading.type = 'MATERIAL'
            else:
               context.space_data.shading.type = 'MATERIAL'
        return {'FINISHED'}        

class SwitchCavityType(Operator):
    bl_idname = "aaa.cavity_type"
    bl_label = ""
    bl_options = {'REGISTER'}

    mode: bpy.props.StringProperty()
    def execute(self, context):
        if self.mode == "TOGGLE":
            context.space_data.shading.show_cavity = not context.space_data.shading.show_cavity
        else:
            context.space_data.shading.cavity_type = self.mode

        return {'FINISHED'}

class ModeGPSwitcher(Operator):
    bl_idname = "aaa.mode_gp_switcher"
    bl_label = ""
    bl_options = {'REGISTER'}

    mode: bpy.props.StringProperty()
    def execute(self, context):
        bpy.context.scene.tool_settings.gpencil_selectmode_edit = self.mode
        return {'FINISHED'}

class GPLayerNew(Operator):
    bl_idname = "aaa.gp_layer_new"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        context.active_gpencil_layer.lock = True
        bpy.ops.gpencil.layer_add()
        context.active_object.data.layers.active.select = True
        context.active_gpencil_layer.lock = False
        return {'FINISHED'}
class GPLayerMergeDown(Operator):
    bl_idname = "aaa.gp_layer_merge_down"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        current_index = context.gpencil_data.layers.active_index 
        bpy.ops.gpencil.layer_merge()
        context.gpencil_data.layers.active_index = current_index - 1
        context.active_gpencil_layer.lock = False
        return {'FINISHED'}
class GPLayerDelete(Operator):
    bl_idname = "aaa.gp_layer_delete"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.ops.gpencil.layer_remove()
        context.active_gpencil_layer.lock = False
        context.active_object.data.layers.active.select = True
        return {'FINISHED'}
class GPLayerSeparateSelection(Operator):
    bl_idname = "aaa.gp_layer_separate_selection"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        from_layer = context.active_gpencil_layer.info

        bpy.ops.gpencil.copy()
        bpy.ops.gpencil.delete(type='POINTS')
        bpy.ops.aaa.gp_layer_new()
        bpy.ops.gpencil.paste(type='ACTIVE')

        self.report({'INFO'}, "Separated from '" + from_layer + "'")
        return {'FINISHED'}
class GPLayerDuplicateHide(Operator):
    bl_idname = "aaa.gp_layer_duplicate_hide"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        from_layer = context.active_gpencil_layer.info

        context.active_gpencil_layer.hide = True
        bpy.ops.gpencil.layer_duplicate()
        self.report({'INFO'}, "Duplicated '" + from_layer + "'")
        context.active_gpencil_layer.hide = False
        return {'FINISHED'}
class GPLayerResetOpacity(Operator):
    bl_idname = "aaa.gp_layer_reset_opacity"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.data.scenes[0].rest_layers_opacity = 1
        for i in range(len(context.gpencil_data.layers)):
            context.gpencil_data.layers[i].opacity = 1
        return {'FINISHED'}
class GPLayerClear(Operator):
    bl_idname = "aaa.gp_layer_clear"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        if bpy.ops.gpencil.delete.poll():
            current_mode = bpy.context.mode
            bpy.ops.object.mode_set(mode='EDIT_GPENCIL')
            bpy.ops.gpencil.select_all(action='SELECT')
            bpy.ops.gpencil.delete(type='STROKES')
            bpy.ops.object.mode_set(mode=current_mode)
        else:
            self.report({'INFO'}, "Nothing to delete")
        return {'FINISHED'}
class GPLayerUnlockedMove(Operator):
    bl_idname = "aaa.gp_layer_unlocked_move"
    bl_label = ""
    def execute(self, context):
        C = context
        SN = C.scene
        SO = SN.objects
        CL = C.scene.ptr3.coll

        CL.clear()
        for i in range(len(SO)):
            if SO[i].type == 'GPENCIL' and (SO[i] != C.active_object):
                if SO[i].visible_get() and not SO[i].hide_select:
                    new_item = CL.add()
                    new_item.indx2 = i
                    new_item.name = SO[i].name
                    
        bpy.ops.wm.call_panel(name="VIEW3D_PT_gpencil_layers_move")
        return {'FINISHED'}
class GPLayerUnlockedMovetoSelected(Operator):
    bl_idname = "aaa.gp_layer_unlocked_move_to_selected"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        C = bpy.context
        SN = C.scene
        CL = SN.ptr3.coll
        
        active_object = C.active_object
        AL = active_object.data.layers

        # Active Object: get Unlocked Layers names in a list 
        actv_layer_names = []
        for i in AL:
            if not i.lock:
                actv_layer_names.append(i.info)      

        # get the Target Object
        target_object = SN.objects[CL[SN.ptr3.indx].indx2]
        TL = target_object.data.layers

        # Target Object: get All Layers name in a list 
        trgt_layer_names = []
        for i in TL:
            trgt_layer_names.append(i.info)

        # check name collisions
        layer_collisions = list(set(actv_layer_names).intersection(trgt_layer_names))

        def getKeyframes(gp_object, layer_name):
            keyframes = []
            for i in range(len(gp_object.data.layers[layer_name].frames)):
                keyframes.append(gp_object.data.layers[layer_name].frames[i].frame_number)
            return keyframes    

        # Active Object: get the keyframes of all the layers in 'layer_collisions'
        # Target Object: get the keyframes of all the layers in 'layer_collisions'
        active_ob_keyframes = {}
        target_ob_keyframes = {}
        for i in layer_collisions:
            active_ob_keyframes[i] = getKeyframes(active_object, i)
            target_ob_keyframes[i] = getKeyframes(target_object, i)
        
        if layer_collisions:
            self.report({'INFO'}, "Collisions in the name of the layers: "+str(layer_collisions))
            
            # Check for keyframe collisions in all layers in 'layer_collisions' between the Active Object and the Target Object
            keyframe_collisions = []
            temp_int = 0
            keyframe_colls_bool = []
            collision_messages = []
            for i in layer_collisions:
                keyframe_collisions.append(list(set(active_ob_keyframes[i]).intersection(target_ob_keyframes[i])))
                if keyframe_collisions[temp_int]:
                    keyframe_colls_bool.append(True)
                    collision_messages.append("There are collisions in the keyframes of the layer '"+i+"' on frames: "+str(keyframe_collisions[temp_int]))
                else:
                    self.report({'INFO'}, "No collisions in the keyframes")
                    keyframe_colls_bool.append(False)
                temp_int += 1

            # if there are not keyframe collisions at all
            if not True in keyframe_colls_bool:    
                # duplicate all unlocked layers 
                for i in actv_layer_names:
                    self.report({'INFO'}, "bbbbbbDuplicating '"+i+"'...")
                    AL.active = AL[i] 
                    bpy.ops.gpencil.layer_duplicate_object(object=target_object.name)
            else:
                for i in collision_messages:
                    self.report({'INFO'}, i)
        else:
            # duplicate all unlocked layers 
            for i in actv_layer_names:
                self.report({'INFO'}, "ccccccccDuplicating '"+i+"'...")
                AL.active = AL[i] 
                bpy.ops.gpencil.layer_duplicate_object(object=target_object.name)
        
        # No fucking clue on how to automatically merge the copied layers. It seems that I'd need to learn some shit about sorting algorithms but I'm not in the mood, so fuck that
        # TODO Learn about sorting algorithms and automatically merge the copied layers 
        # ******bpy.ops.gpencil.layer_move(type='UP')
        # ******bpy.ops.gpencil.layer_merge()

        # switch to Target Object
        temp_mode = C.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        target_object.select_set(state=True)
        context.view_layer.objects.active = target_object
        bpy.ops.object.mode_set(mode=temp_mode)
        return {'FINISHED'}

class GPSwitchTool(Operator):
    bl_idname = "aaa.gp_switch_tool"
    bl_label = ""
    bl_options = {'UNDO'}

    name: bpy.props.StringProperty()
    def execute(self, context):
        if self.name != "":
            bpy.ops.wm.tool_set_by_id(name="builtin_brush.Draw")
            context.scene.tool_settings.gpencil_paint.brush = bpy.data.brushes[self.name]
        else:
            pass
        return {'FINISHED'}

class GPSetTool1(Operator):
    bl_idname = "aaa.gp_set_tool_1"
    bl_label = ""
    bl_options = {'UNDO'}
    name: bpy.props.StringProperty()
    def execute(self, context):
        context.scene.brush_name_1 = self.name
        return {'FINISHED'}
class GPSetTool2(Operator):
    bl_idname = "aaa.gp_set_tool_2"
    bl_label = ""
    bl_options = {'UNDO'}
    name: bpy.props.StringProperty()
    def execute(self, context):
        context.scene.brush_name_2 = self.name
        return {'FINISHED'}
class GPSetTool3(Operator):
    bl_idname = "aaa.gp_set_tool_3"
    bl_label = ""
    bl_options = {'UNDO'}
    name: bpy.props.StringProperty()
    def execute(self, context):
        context.scene.brush_name_3 = self.name
        return {'FINISHED'}
class GPSetTool4(Operator):
    bl_idname = "aaa.gp_set_tool_4"
    bl_label = ""
    bl_options = {'UNDO'}
    name: bpy.props.StringProperty()
    def execute(self, context):
        context.scene.brush_name_4 = self.name
        return {'FINISHED'}
class GPSetTool5(Operator):
    bl_idname = "aaa.gp_set_tool_5"
    bl_label = ""
    bl_options = {'UNDO'}
    name: bpy.props.StringProperty()
    def execute(self, context):
        context.scene.brush_name_5 = self.name
        return {'FINISHED'}
class GPSetTool6(Operator):
    bl_idname = "aaa.gp_set_tool_6"
    bl_label = ""
    bl_options = {'UNDO'}
    name: bpy.props.StringProperty()
    def execute(self, context):
        context.scene.brush_name_6 = self.name
        return {'FINISHED'}
class GPSetTool7(Operator):
    bl_idname = "aaa.gp_set_tool_7"
    bl_label = ""
    bl_options = {'UNDO'}
    name: bpy.props.StringProperty()
    def execute(self, context):
        context.scene.brush_name_7 = self.name
        return {'FINISHED'}
class GPSetTool8(Operator):
    bl_idname = "aaa.gp_set_tool_8"
    bl_label = ""
    bl_options = {'UNDO'}
    name: bpy.props.StringProperty()
    def execute(self, context):
        context.scene.brush_name_8 = self.name
        return {'FINISHED'}
class GPRemoveTool(Operator):
    bl_idname = "aaa.gp_remove_tool"
    bl_label = ""
    bl_options = {'UNDO'}

    index: bpy.props.IntProperty()
    def execute(self, context):
        exec("context.scene.brush_name_"+str(self.index)+" = ''")
        return {'FINISHED'}
        
class GPSwitchMaterial(Operator):
    bl_idname = "aaa.gp_switch_material"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty()
    def execute(self, context):
        context.scene.tool_settings.gpencil_paint.brush.gpencil_settings.material = bpy.data.materials[self.name]
        return {'FINISHED'}        

class GPSetStrokesOpacity(Operator):
    bl_idname = "aaa.gp_set_strokes_opacity"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        C = context
        SN = C.scene
        GN = SN.tool_settings.gpencil_sculpt

        temp_mode = C.mode
        bpy.ops.object.mode_set(mode=GPS)
        
        temp_tool = C.tool_settings.gpencil_sculpt.sculpt_tool
        C.tool_settings.gpencil_sculpt.sculpt_tool = 'STRENGTH'

        temp_size = GN.brush.size
        GN.brush.size = 1000

        temp_strength = GN.brush.strength
        GN.brush.strength = 1

        temp_falloff = GN.brush.use_falloff
        GN.brush.use_falloff = False


        def f1(x, y):
            bpy.ops.gpencil.sculpt_paint(stroke=[{"name":"", "location":(0, 0, 0), "mouse":(x, y), "pressure":1, "size":0, "pen_flip":False, "time":0, "is_start":True}], wait_for_input=False)
        
        temp_frame       = SN.frame_current
        SN.frame_current = SN.frame_start
        for i in range(len(context.active_gpencil_layer.frames)):
            for i in range(0, 2000, 100):
                f1(0, i)
            for i in range(0, 1500, 100):
                f1(i, 0)
            bpy.ops.screen.keyframe_jump(next=True)
        
        for i in range(0, 2000, 100):
            f1(0, i)
        for i in range(0, 1500, 100):
            f1(i, 0)
            
        GN.brush.use_falloff                       = temp_falloff
        C.tool_settings.gpencil_sculpt.sculpt_tool = temp_tool
        GN.brush.strength                          = temp_strength
        GN.brush.size                              = temp_size
        SN.frame_current                           = temp_frame
        bpy.ops.object.mode_set(mode=temp_mode)    
        return {'FINISHED'}

class HelperGPBrushesManager(Operator):
    bl_idname = "aaa.helper_gp_brushes_manager"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.ops.wm.call_panel(name="VIEW3D_PT_helper_gpencil_brushes_manager")
        return {'FINISHED'}

class SetBaseFPS(Operator):
    bl_idname = "aaa.set_base_fps"
    bl_label = ""
    bl_options = {'REGISTER'}

    set_base: bpy.props.FloatProperty()
    def execute(self, context):
        bpy.data.scenes[0].fps_base = self.set_base
        return {'FINISHED'}

class ApplyModifiers(Operator):
    bl_idname = "aaa.apply_modifiers"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        current_context = bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        for mod in bpy.types.GpencilModifier.bl_rna.properties['type'].enum_items:
            bpy.ops.object.gpencil_modifier_apply(apply_as='DATA',modifier=mod.name)
        bpy.ops.object.mode_set(mode=current_context)
        return {'FINISHED'}

# if you call it from other operator the self.report() function prints to the console instead of the Info Editor, independently of the 'execution context'
class SaveIncremental(Operator):
    bl_idname = "aaa.save_incremental"
    bl_label = ""
    bl_options = {'REGISTER'}
    def execute(self, context):
        currentblend = bpy.data.filepath
        if currentblend:
            save_path = self.get_incremented_path(currentblend)
            # self.add_path_to_recent_files(save_path)
            if os.path.exists(save_path):
                self.report({'INFO'}, "File '%s' exists already!\nBlend has NOT been saved incrementally!" % (save_path))
            else:
                bpy.ops.wm.save_as_mainfile(filepath=save_path)
                self.report({'INFO'}, "Saved blend incrementally:" + save_path)
        else:
            bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
        return {'FINISHED'}
    def get_incremented_path(self, currentblend):
        path = os.path.dirname(currentblend)
        filename = os.path.basename(currentblend)

        filenameRegex = re.compile(r"(.+)\.blend\d*$")

        mo = filenameRegex.match(filename)

        if mo:
            name = mo.group(1)
            numberendRegex = re.compile(r"(.*?)(\d+)$")

            mo = numberendRegex.match(name)

            if mo:
                basename = mo.group(1)
                numberstr = mo.group(2)
            else:
                basename = name + "_"
                numberstr = "000"

            number = int(numberstr)

            incr = number + 1
            incrstr = str(incr).zfill(len(numberstr))
            incrname = basename + incrstr + ".blend"

            return os.path.join(path, incrname)
    def add_path_to_recent_files(self, path):
        """
        add the path to the recent files list, for some reason it's not done automatically when saving or loading
        """

        try:
            recent_path = bpy.utils.user_resource('CONFIG', "recent-files.txt")
            with open(recent_path, "r+") as f:
                content = f.read()
                f.seek(0, 0)
                f.write(path.rstrip('\r\n') + '\n' + content)

        except (IOError, OSError, FileNotFoundError):
            pass
class SaveFile(Operator):
    bl_idname = "aaa.save_file"
    bl_label = "saveFile"
    bl_options = {'REGISTER'}
    def execute(self, context):
        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
        if bpy.data.is_saved:
            if bpy.data.is_dirty:
                saved = "Saved: " + filename
                self.report({'INFO'}, saved)
                
                bpy.data.scenes[0].already_saved_counter = 0
            else:
                bpy.data.scenes[0].already_saved_counter += 1
                st = "No changes have been made to '" + filename + "'. Already saved file (" + str(bpy.data.scenes[0].already_saved_counter) + ")" 
                self.report({'INFO'}, st)
        return {'FINISHED'}

class SelectReferenceImage(Operator):
    bl_idname = "aaa.select_reference_image"
    bl_label = ""
    bl_options = {'UNDO'}
    def execute(self, context):
        SC = context.scene

        if bpy.context.object.type == 'EMPTY':
            
            bpy.data.scenes[0].current_image_name = context.object.name
            self.report({'INFO'}, "Selected image: " + bpy.data.objects[bpy.data.scenes[0].current_image_name].name)

        elif SC.current_image_name != "":
            if bpy.data.objects[SC.current_image_name].color[3] != 1:
                SC.current_alpha = bpy.data.objects[SC.current_image_name].color[3]
            
            if SC.toggle_ref_image:
                bpy.data.objects[SC.current_image_name].color[3] = 1
                bpy.data.objects[SC.current_image_name].empty_image_depth = 'FRONT'
            else:
                bpy.data.objects[SC.current_image_name].color[3] = SC.current_alpha
                bpy.data.objects[SC.current_image_name].empty_image_depth = 'DEFAULT'
            SC.toggle_ref_image = not SC.toggle_ref_image
        else:
            self.report({'INFO'}, "No image selected")
        return {'FINISHED'}

class OnCallGPLayersPanel(Operator):
    bl_idname = "aaa.on_call_gp_layers_panel"
    bl_label = ""
    def execute(self, context):
        C = context
        SC = C.scene
        SO = SC.objects
        CL = C.scene.ptr.coll
        
        CL.clear()
        
        j = 0
        for i in range(len(SO)):
            if SO[i].type == 'GPENCIL':
                if SO[i].visible_get() and not SO[i].hide_select:
                    CL.add()
                    CL[j].indx2 = i
                    CL[j].name = SO[i].name
                    j += 1

        f_ind = 0
        for i in range(len(CL)):
            if CL[i].name == C.active_object.name:
                f_ind = i
        SC.ptr.indx = f_ind           

        bpy.ops.wm.call_panel(name="VIEW3D_PT_gpencil_layers_2")
        return {'FINISHED'}
class OnaddGPObject(Operator):
    bl_idname = "aaa.on_add_gp_object"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    
    type1: bpy.props.StringProperty()
    def execute(self, context):
        bpy.ops.object.gpencil_add('INVOKE_DEFAULT', type=self.type1)

        bpy.context.object.data.use_autolock_layers = True

        bpy.context.object.data.ghost_after_range = 3
        bpy.context.object.data.ghost_before_range = 3

        bpy.context.object.data.before_color = (0.862745, 0, 0.439216)
        bpy.context.object.data.after_color = (0, 0.294118, 1)
        return {'FINISHED'}

class PanelInfoShow(Operator):
    bl_idname = "aaa.panel_info_show"
    bl_label = ""
    def execute(self, context):
        bpy.ops.aaa.toggle_prop(prop="context.scene.panel_info_show")
        return {'FINISHED'}
class PanelGPBrushesManagerRefresh(Operator):
    bl_idname = "aaa.panel_gp_brushes_manager_refresh"
    bl_label = ""
    def execute(self, context):
        C = context
        SC = C.scene
        SO = SC.objects
        CL = C.scene.ptr.coll
        
        CL.clear()
        
        j = 0
        for i in range(len(SO)):
            if SO[i].type == 'GPENCIL':
                if SO[i].visible_get() and not SO[i].hide_select:
                    CL.add()
                    CL[j].indx2 = i
                    CL[j].name = SO[i].name
                    j += 1

        f_ind = 0
        for i in range(len(CL)):
            if CL[i].name == C.active_object.name:
                f_ind = i
        SC.ptr.indx = f_ind   
        return {'FINISHED'}

class ToggleProp(Operator):
    bl_idname = "aaa.toggle_prop"
    bl_label = ""
    bl_options = {'UNDO'}

    prop: bpy.props.StringProperty()
    def execute(self, context):
        exec(self.prop+" = not "+self.prop)
        return {'FINISHED'}
class SetProp(Operator):
    bl_idname = "aaa.set_prop"
    bl_label = ""
    bl_options = {'UNDO'}

    prop_set: bpy.props.StringProperty()
    def execute(self, context):
        exec(self.prop_set)
        return {'FINISHED'}

# very relevant
# bpy.ops.script.python_file_run(filepath="")
class PresetBackground(AddPresetBase, Operator):
    bl_idname = "aaa.preset_background"
    bl_label = "Overlays Presets"
    
    preset_menu = "VIEW3D_MT_PRESETS_BACKGROUND"
    preset_defines = [
        "shading = bpy.context.space_data.shading"
    ]
    preset_values = [
        "shading.background_color",
    ]
    preset_subdir = "scene/background"
class PresetOverlays(AddPresetBase, Operator):
    bl_idname = "aaa.preset_overlays"
    bl_label = "Overlays Presets"
    
    preset_menu = "VIEW3D_MT_PRESETS_MT_OVERLAYS"
    preset_defines = [
        "overlay = bpy.context.space_data.overlay"
    ]
    preset_values = [
        "overlay.show_ortho_grid",
        "overlay.show_floor",
        "overlay.show_axis_x",
        "overlay.show_axis_y",
        "overlay.show_axis_z",
        "overlay.grid_scale",
        "overlay.grid_subdivisions",
        "overlay.show_text",
        "overlay.show_cursor",
        "overlay.show_annotation",
        "overlay.show_extras",
        "overlay.show_bones",
        "overlay.show_relationship_lines",
        "overlay.show_motion_paths",
        "overlay.show_outline_selected",
        "overlay.show_object_origins",
        "overlay.show_object_origins_all",
        "overlay.show_wireframes",
        "overlay.wireframe_threshold",
        "overlay.show_face_orientation",
        # "overlay.show_reconstruction",
        # "overlay.show_camera_path",
        # "overlay.show_camera_path",
        # "overlay.tracks_display_type",
        # "overlay.tracks_display_size",
        "overlay.show_edges",
        "overlay.show_faces",
        "overlay.show_face_center",
        "overlay.show_edge_crease",
        "overlay.show_edge_sharp",
        "overlay.show_edge_bevel_weight",
        "overlay.show_edge_seams",
        "overlay.show_extra_indices",
        "overlay.show_occlude_wire",
        "overlay.show_weight",
        "overlay.show_statvis",
        "overlay.show_extra_edge_length",
        "overlay.show_extra_edge_angle",
        "overlay.show_extra_face_area",
        "overlay.show_extra_face_angle",
        "overlay.show_vertex_normals",
        "overlay.show_split_normals",
        "overlay.show_face_normals",
        "overlay.normals_length",
        "overlay.show_freestyle_edge_marks",
        "overlay.show_freestyle_face_marks",
        "overlay.use_gpencil_onion_skin",
        "overlay.use_gpencil_grid",
        "overlay.gpencil_grid_opacity",
        "overlay.use_gpencil_paper",
        "overlay.gpencil_paper_opacity",
        "overlay.use_gpencil_fade_layers",
        "overlay.gpencil_fade_layer",
        "overlay.show_curve_normals",
        "overlay.normals_length",
    ]
    preset_subdir = "scene/overlays"
class PresetPanelInfo(AddPresetBase, Operator):
    bl_idname = "aaa.preset_panel_info"
    bl_label = "Panel Info Presets"
    
    preset_menu = "VIEW3D_PT_INFO_PRESET"
    preset_defines = [
        "scn = bpy.context.scene"
    ]
    preset_values = [
        "scn.pt_info_1",
        "scn.pt_info_2",
        "scn.pt_info_3",
        "scn.pt_info_4",
        "scn.pt_info_5",
    ]
    preset_subdir = "scene/panel_info"

class PresetFrameRangePreviewAdd(Operator):
    bl_idname = "aaa.preset_frame_range_preview_add"
    bl_label = ""
    def execute(self, context):
        SC = context.scene
        PR = SC.ptr2
        CL = SC.ptr2.coll
        
        current = CL.add()
        current.name = "New Preview Range"
        current.frame_preview_start = SC.frame_preview_start
        current.frame_preview_end = SC.frame_preview_end

        bpy.ops.wm.call_panel(name="VIEW3D_PT_FRAME_RANGE_PREVIEW_ADD")

        temp = PR.indx + 1
        PR.indx = len(CL) - 1
        CL.move(PR.indx, temp)
        PR.indx = temp
        return {'FINISHED'}
class PresetFrameRangePreviewRemove(Operator):
    bl_idname = "aaa.preset_frame_range_preview_remove"
    bl_label = ""
    bl_options = {'UNDO'}
    def execute(self, context):
        SC = context.scene
        CL = SC.ptr2.coll
        
        CL.remove(SC.ptr2.indx)
        if SC.ptr2.indx >= len(CL):  
            SC.ptr2.indx = len(CL) - 1

        if CL:
            SC.frame_preview_start = CL[SC.ptr2.indx].frame_preview_start
            SC.frame_preview_end   = CL[SC.ptr2.indx].frame_preview_end
        return {'FINISHED'}
class PresetFrameRangePreviewOverwrite(Operator):
    '''Overwrite Active Preview Preset
    Use the current Preview Range to overwrite the Active Preset'''
    bl_idname = "aaa.preset_frame_range_preview_overwrite"
    bl_label = ""
    bl_options = {'UNDO'}
    def execute(self, context):
        SC = context.scene
        CL = SC.ptr2.coll

        if CL:
            CL[SC.ptr2.indx].frame_preview_start = SC.frame_preview_start
            CL[SC.ptr2.indx].frame_preview_end   = SC.frame_preview_end

        return {'FINISHED'}
class PresetFrameRangePreviewMove(Operator):
    bl_idname = "aaa.preset_frame_range_preview_move"
    bl_label = ""
    bl_options = {'UNDO'}

    type: StringProperty()
    def execute(self, context):
        SC = context.scene
        PR = SC.ptr2
        CL = PR.coll
        
        if self.type == 'UP' and PR.indx > 0:
            CL.move(PR.indx, PR.indx - 1)
            PR.indx -= 1
        if self.type == 'DOWN' and PR.indx + 1 < len(CL):
            CL.move(PR.indx, PR.indx + 1)
            PR.indx += 1
        return {'FINISHED'}

class CONDITIONS_SWITCHER(Operator):
    bl_idname = "aaa.conditions_switcher"
    bl_label = "CONDITIONS_SWITCHER"
    bl_options = {'REGISTER'}

    cond: bpy.props.StringProperty()
    def execute(self, context):
        context.scene.conditions = self.cond            
        return {'FINISHED'}
class CONDITIONS_SWITCHER_SEQUENCER(Operator):
    bl_idname = "aaa.conditions_switcher_sequencer"
    bl_label = "CONDITIONS_SWITCHER_SEQUENCER"
    bl_options = {'REGISTER'}

    def execute(self, context):
        context.scene.markersExist = not context.scene.markersExist
        print(context.scene.markersExist)
        return {'FINISHED'}

# shift, ctrl, alt
# thats the order

class GLOBAL_E(Operator):
    bl_idname = "aaa.key_e"
    bl_label = "GLOBAL_E"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        SN = context.scene
        CN = SN.conditions
        AT = context.area.type
        if CN in ('TRANSFORM'):
            if AT in ('VIEW_3D', 'GRAPH_EDITOR'):
                bpy.ops.transform.rotate('INVOKE_DEFAULT')
        if CN in ('LAYERS'):
            bpy.ops.aaa.gp_layer_duplicate_hide()
        if CN in ('TIMELINE'):
            if SN.loop_frames:
                if SN.use_preview_range:
                    if SN.frame_current == SN.frame_preview_end:
                        SN.frame_current = SN.frame_preview_start
                    else:
                        bpy.ops.screen.frame_offset(delta=1)
                else:
                    if SN.frame_current == SN.frame_end:
                        SN.frame_current = SN.frame_start
                    else:
                        bpy.ops.screen.frame_offset(delta=1)
            else:
                bpy.ops.screen.frame_offset(delta=1)
        return {'FINISHED'}
class GLOBAL_Q(Operator):
    bl_idname = "aaa.key_q"
    bl_label = "GLOBAL_Q"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        SN = context.scene
        CN = context.scene.conditions
        AT = context.area.type
        if CN in ('TRANSFORM'):
            if AT in ("VIEW_3D", 'GRAPH_EDITOR'):
                bpy.ops.transform.translate('INVOKE_DEFAULT')
            if AT == "DOPESHEET_EDITOR":
                bpy.ops.transform.transform('INVOKE_DEFAULT', mode="TIME_TRANSLATE")
            if AT == "SEQUENCE_EDITOR":
                bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        if CN in ('LAYERS'):
            bpy.ops.aaa.gp_layer_new()
        if CN in ('TIMELINE'):
            # 'loop_frames' is a BoolProperty in 'AAA_settings'
            if SN.loop_frames:
                if SN.use_preview_range:
                    if SN.frame_current == SN.frame_preview_start:
                        SN.frame_current = SN.frame_preview_end
                    else:
                        bpy.ops.screen.frame_offset(delta=-1)
                else:
                    if SN.frame_current == SN.frame_start:
                        SN.frame_current = SN.frame_end
                    else:
                        bpy.ops.screen.frame_offset(delta=-1)
            else:
                bpy.ops.screen.frame_offset(delta=-1)
        return {'FINISHED'}
class GLOBAL_W(Operator):
    bl_idname = "aaa.key_w"
    bl_label = "GLOBAL_W"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        CN = context.scene.conditions
        AT = context.area.type
        if CN in ('TRANSFORM'):
            if AT in ("VIEW_3D", 'GRAPH_EDITOR'):
                bpy.ops.transform.resize('INVOKE_DEFAULT')
            if AT == "DOPESHEET_EDITOR":
                bpy.ops.transform.transform('INVOKE_DEFAULT', mode="TIME_SCALE")
        if CN in ('LAYERS'):
            bpy.ops.aaa.gp_layer_merge_down()
        if CN in ('TIMELINE'):
            if context.scene.use_preview_range:
                context.scene.frame_current = context.scene.frame_preview_start
            else:
                context.scene.frame_current = context.scene.frame_start
        return {'FINISHED'}

class GLOBAL_SHIFT_A(Operator):
    bl_idname = "aaa.shift_a"
    bl_label = "GLOBAL_SHIFT_A"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        C = context
        M = C.mode
        A = C.area.type
        if A in 'VIEW_3D':
            if M in (OBJ, MHE):
                bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_ADD_OBJECT_PIE")
            if M in (GPE, GPS, GPP):
                bpy.ops.gpencil.layer_move(type='DOWN')
        if A in 'IMAGE_EDITOR':
            C.space_data.image.render_slots.active_index -= 1
        return {'FINISHED'}
class GLOBAL_SHIFT_E(Operator):
    bl_idname = "aaa.shift_e"
    bl_label = "GLOBAL_SHIFT_E"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        C  = context
        M  = C.mode
        A  = C.area.type
        SN = C.scene
        if A in 'VIEW_3D':
            pass
        if A in 'SEQUENCE_EDITOR':
            if SN.timeline_markers.items() and SN.markersExist:
                # 'loop_frames' is a BoolProperty in 'AAA_settings'
                if SN.loop_frames:
                    temp_list = []
                    for i in SN.timeline_markers:
                        temp_list.append(i.frame)
                    temp_list.sort()

                    if SN.frame_current == temp_list[-1]:
                        SN.frame_current = temp_list[0]
                    else:
                        bpy.ops.screen.marker_jump(next=True)
                else:
                    bpy.ops.screen.marker_jump(next=True)
            else:
                bpy.ops.sequencer.strip_jump(next=True, center=False)
        return {'FINISHED'}
class GLOBAL_SHIFT_Q(Operator):
    bl_idname = "aaa.shift_q"
    bl_label = "GLOBAL_SHIFT_Q"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        C  = context
        M  = C.mode
        A  = C.area.type
        SN = C.scene
        if A in 'VIEW_3D':
            if M in (GPE, GPS, GPP):
                bpy.ops.gpencil.layer_move(type='UP')
        if A in 'IMAGE_EDITOR':
            C.space_data.image.render_slots.active_index += 1
        if A in 'SEQUENCE_EDITOR':
            if SN.timeline_markers.items() and SN.markersExist:
                # 'loop_frames' is a BoolProperty in 'AAA_settings'
                if SN.loop_frames:
                    temp_list = []
                    for i in SN.timeline_markers:
                        temp_list.append(i.frame)
                    temp_list.sort()

                    if SN.frame_current == temp_list[0]:
                        SN.frame_current = temp_list[-1]
                    else:
                        bpy.ops.screen.marker_jump(next=False)
                else:
                    bpy.ops.screen.marker_jump(next=False)
            else:
                bpy.ops.sequencer.strip_jump(next=False, center=False)
        return {'FINISHED'}
class GLOBAL_SHIFT_ALT_F(Operator):
    bl_idname = "aaa.shift_alt_f"
    bl_label = "GLOBAL_SHIFT_ALT_F"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        M = context.mode
        if M in (GPE, GPS, GPP):
            from_layer = context.active_gpencil_layer.info
            bpy.ops.aaa.gp_layer_delete()
            self.report({'INFO'}, "Layer '"+from_layer+"' Deleted")
        return {'FINISHED'}

class GLOBAL_SHIFT_CTRL_F(Operator):
    bl_idname = "aaa.shift_ctrl_f"
    bl_label = "GLOBAL_SHIFT_CTRL_F"
    bl_options = {'UNDO'}
    def execute(self, context):
        C = context
        strip = C.active_sequence_strip
        if strip.select: 
            if strip.blend_alpha == 0:
                strip.blend_alpha = 1
            elif strip.blend_alpha == 1: 
                strip.blend_alpha = 0
            else:
                strip.blend_alpha = 1
        return {'FINISHED'}
    
class GLOBAL_SHIFT_ALT_Z(Operator):
    bl_idname = "aaa.shift_alt_z"
    bl_label = "GLOBAL_SHIFT_ALT_Z"
    bl_options = {'UNDO'}
    def execute(self, context):
        C = context
        strip = C.active_sequence_strip
        
        if strip.select: 
            if strip.parent_meta():
                C.scene.sequence_editor.sequences_all[strip.parent_meta().name].channels[strip.channel].lock = not C.scene.sequence_editor.sequences_all[strip.parent_meta().name].channels[strip.channel].lock
            else:
                C.scene.sequence_editor.channels[strip.channel].lock = not C.scene.sequence_editor.channels[strip.channel].lock

            C.scene.sequence_editor.channels[strip.channel].lock = not C.scene.sequence_editor.channels[strip.channel].lock
        return {'FINISHED'}

class GLOBAL_CTRL_F(Operator):
    bl_idname = "aaa.ctrl_f"
    bl_label = "GLOBAL_CTRL_F"
    bl_options = {'UNDO'}
    def execute(self, context):
        C = context
        M = C.mode
        strip = C.active_sequence_strip

        if M in (GPE, GPS, GPP):
            bpy.ops.aaa.toggle_prop(prop="context.active_gpencil_layer.hide")
        
        elif hasattr(strip, 'select') and strip.select:
            if strip.parent_meta():
                C.scene.sequence_editor.sequences_all[strip.parent_meta().name].channels[strip.channel].mute = not C.scene.sequence_editor.sequences_all[strip.parent_meta().name].channels[strip.channel].mute
            else:
                strip = strip
                C.scene.sequence_editor.channels[strip.channel].mute = not C.scene.sequence_editor.channels[strip.channel].mute

            # for i in range(20):
            #     # print(f">>{i if i > 10 else f"0{i}"}: {strip.channel}")
            #     print('>>>>>>>>>>>>>>>> select?')

        
        return {'FINISHED'}
class GLOBAL_CTRL_ALT_H(Operator):
    bl_idname = "aaa.ctrl_alt_h"
    bl_label = "GLOBAL_CTRL_ALT_H"
    bl_options = {'REGISTER'}

    toggle_mirror: bpy.props.BoolProperty()
    def execute(self, context):
        M = context.mode
        if M in (OBJ, GPE, GPS, GPP):
            self.toggle_mirror = not self.toggle_mirror
            if self.toggle_mirror:
                bpy.ops.view3d.view_axis(type='FRONT')
            else:
                bpy.ops.view3d.view_axis(type='BACK')
           
            # TODO

            '''bpy.data.scenes[0].roll_viewport_angle
             No fucking clue how a Quaternion works

            roll_angl = bpy.data.scenes[0].roll_viewport_angle

            camNormal = Vector((0, 0, -1))
            q = Quaternion(camNormal, roll_angl)
            
            context.space_data.region_3d.view_rotation =  q
            '''
        return {'FINISHED'}

class GLOBAL_ALT_A(Operator):
    bl_idname = "aaa.alt_a"
    bl_label = "GLOBAL_ALT_A"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        M = context.mode
        if M in (GPE, GPS, GPP):
            context.active_gpencil_layer.lock = True
            context.gpencil_data.layers.active_index -= 1 
            context.active_gpencil_layer.lock = False
        return {'FINISHED'}
class GLOBAL_ALT_Q(Operator):
    bl_idname = "aaa.alt_q"
    bl_label = "GLOBAL_ALT_Q"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        M = context.mode
        if M in (GPE, GPS, GPP):
            context.active_gpencil_layer.lock = True
            context.gpencil_data.layers.active_index += 1 
            context.active_gpencil_layer.lock = False
        return {'FINISHED'}
class GLOBAL_ALT_S(Operator):
    bl_idname = "aaa.alt_s"
    bl_label = "GLOBAL_ALT_S"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        M = context.mode
        if M in (GPE, GPS, GPP):
            bpy.ops.aaa.gp_layer_clear()
        return {'FINISHED'}

class TestOperator(Operator):
    bl_idname = "aaa.test_operator"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    testVal: bpy.props.IntProperty()
    def execute(self, context):
        time = str(datetime.time(datetime.now()))
        print("{}: {}".format(self.testVal, time[:-7]))

        return {'FINISHED'}

''' Preset Operator
class test(Operator):
    bl_idname = "aaa.test"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        
        return {'FINISHED'}
'''
classes = (
    
    TestOperator,

    GLOBAL_ALT_S,
    GLOBAL_ALT_Q,
    GLOBAL_ALT_A,

    GLOBAL_CTRL_ALT_H,
    GLOBAL_CTRL_F,

    GLOBAL_SHIFT_CTRL_F,

    GLOBAL_SHIFT_ALT_Z,

    GLOBAL_SHIFT_ALT_F,
    GLOBAL_SHIFT_Q,
    GLOBAL_SHIFT_E,
    GLOBAL_SHIFT_A,
    
    GLOBAL_W,
    GLOBAL_Q,
    GLOBAL_E,

    CONDITIONS_SWITCHER_SEQUENCER,
    CONDITIONS_SWITCHER,

    PresetFrameRangePreviewMove,
    PresetFrameRangePreviewOverwrite,
    PresetFrameRangePreviewRemove,
    PresetFrameRangePreviewAdd,

    # PresetPanelInfo,
    PresetOverlays,
    PresetBackground,
    
    SetProp,
    ToggleProp,

    PanelGPBrushesManagerRefresh,
    PanelInfoShow,

    OnaddGPObject,
    OnCallGPLayersPanel,

    SelectReferenceImage,

	SaveFile,
    SaveIncremental,

    ApplyModifiers,
    
    SetBaseFPS,

    HelperGPBrushesManager,

    GPSetStrokesOpacity,

    GPSwitchMaterial,

    GPRemoveTool,

    GPSetTool1,
    GPSetTool2,
    GPSetTool3,
    GPSetTool4,
    GPSetTool5,
    GPSetTool6,
    GPSetTool7,
    GPSetTool8,

    GPSwitchTool,

    GPLayerUnlockedMovetoSelected,
    GPLayerUnlockedMove,
    GPLayerClear,
    GPLayerResetOpacity,
    GPLayerDuplicateHide,
    GPLayerSeparateSelection,
    GPLayerDelete,
    GPLayerMergeDown,
    GPLayerNew,
    
    ModeGPSwitcher,
    
    SwitchCavityType,

    RendererPicker,
    
    DyntopoDetailing,

    CommonTools,
    PivotSelector,
    
    ModeSet,

    RollAxis,
    RollViewport,

    ToggleFaceOrientation,
    ToggleXRay,
    ToggleWireframeOverlay,
    ToggleSolidWireframe,
    ToggleOverlays,
    
    SwitchWorkspace,

    VSECustomFadeClear,
    VSECustomFade,
    VSEAlignStrip,
)
def register():
    for c in classes:
        bpy.utils.register_class(c)
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
        
if __name__ == "__main__":
    register()