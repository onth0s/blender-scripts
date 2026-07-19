import bpy  # type: ignore
from bpy.types import Operator  # type: ignore
from mathutils import Vector, Quaternion  # type: ignore
from math import atan2
import gpu  # type: ignore
from gpu_extras.batch import batch_for_shader  # type: ignore
from AAA_utils import MHS, OBJ

class SwitchWorkspace(Operator):
    """Switch Workspace"""

    bl_idname = "aaa.switch_workspace"
    bl_label = ""
    bl_options = {"REGISTER"}

    name: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        if self.name in bpy.data.workspaces:
            context.window.workspace = bpy.data.workspaces[self.name]
            return {"FINISHED"}
        self.report({"WARNING"}, f"Workspace '{self.name}' not found")
        return {"CANCELLED"}


class ToggleOverlays(Operator):
    bl_idname = "aaa.toggle_overlays"
    bl_label = "Toggle Overlays"
    bl_options = {"REGISTER"}

    header: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        SD = context.space_data
        SN = context.scene

        if self.header == "HEADER":
            SD.show_region_header = not SD.show_region_header
        elif self.header == "FLOOR":
            temp = (
                SD.overlay.show_axis_y
                or SD.overlay.show_axis_x
                or SD.overlay.show_floor
            )

            SD.overlay.show_axis_y = not temp
            SD.overlay.show_axis_x = not temp
            SD.overlay.show_floor = not temp

        elif self.header == "OVERLAYS":
            if not SN.show_bool_toggle:
                SN.show_overlays = SD.overlay.show_overlays
                SN.show_gizmo = SD.show_gizmo
                SN.show_t_menu = SD.show_region_ui
                SN.show_n_menu = SD.show_region_toolbar
                SN.show_region_asset_shelf = SD.show_region_asset_shelf

                SD.overlay.show_overlays = False
                SD.show_gizmo = False
                SD.show_region_ui = False
                SD.show_region_toolbar = False
                if context.mode == MHS:
                    SD.show_region_asset_shelf = False
            else:
                SD.overlay.show_overlays = SN.show_overlays
                SD.show_gizmo = SN.show_gizmo
                SD.show_region_ui = SN.show_t_menu
                SD.show_region_toolbar = SN.show_n_menu
                if context.mode == MHS:
                    SD.show_region_asset_shelf = SN.show_region_asset_shelf

            SN.show_bool_toggle = not SN.show_bool_toggle

        return {"FINISHED"}


class RollViewport(Operator):
    bl_idname = "aaa.roll_viewport"
    bl_label = "Roll Viewport"
    bl_options = {"GRAB_CURSOR"}

    initial_angle = 0
    angle_now = 0
    initial_rotation = Vector((0, 0, 0))  # type: ignore
    camNormal = Vector((0, 0, -1))  # type: ignore

    temp_degree = 0

    _draw_handler = None

    # margin (px) offset from the mouse cursor for the rotation pivot.
    # the pivot is placed along the ray from viewport center through the mouse,
    # at mouse_position - margin in that direction (toward center).
    # the quadrant the mouse is in at invocation determines the direction:
    #   top-right -> pivot is pushed down-left toward center, etc.
    # a value of 0 rotates around the mouse itself.
    margin: bpy.props.IntProperty(default=100)  # type: ignore

    def invoke(self, context, event):
        rv3d = context.space_data.region_3d
        context.window_manager.modal_handler_add(self)

        self.camera = context.scene.camera
        self.rotate_camera = (
            rv3d.view_perspective == "CAMERA"
            and self.camera is not None
            and getattr(context.space_data, "lock_camera", False)
        )

        if not self.rotate_camera:
            if rv3d.view_perspective == "CAMERA":
                rv3d.view_perspective = "PERSP"

        if self.rotate_camera:
            self.camera_rotation_mode = self.camera.rotation_mode
            if self.camera_rotation_mode == "QUATERNION":
                self.initial_camera_rotation = self.camera.rotation_quaternion.copy()
                self.initial_camera_rotation_quat = self.initial_camera_rotation
            elif self.camera_rotation_mode == "AXIS_ANGLE":
                self.initial_camera_rotation = list(self.camera.rotation_axis_angle)
                axis = Vector(self.initial_camera_rotation[1:])
                angle = self.initial_camera_rotation[0]
                self.initial_camera_rotation_quat = Quaternion(axis, angle)
            else:
                self.initial_camera_rotation = self.camera.rotation_euler.copy()
                self.initial_camera_rotation_quat = (
                    self.initial_camera_rotation.to_quaternion()
                )

        # viewport size in pixels
        self.view3d_bounds = Vector(  # type: ignore
            (context.region.width, context.region.height)
        )
        viewport_center = self.view3d_bounds / 2

        # mouse position at invocation (region-relative coordinates)
        mouseloc = Vector(  # type: ignore
            (event.mouse_region_x, event.mouse_region_y)
        )

        # compute the rotation pivot: offset from the mouse toward viewport center.
        # the direction is the unit vector from viewport center to mouse (the quadrant).
        # subtracting margin pulls the pivot that many pixels back toward center.
        # if the mouse is exactly on the viewport center, no offset is applied.
        to_mouse = mouseloc - viewport_center
        length = to_mouse.length
        if length > 0:
            direction = to_mouse / length
        else:
            direction = Vector((0, 0))  # type: ignore
        self.view3d_center = mouseloc - direction * self.margin

        # DEBUG: draw the pivot as a crosshair in the viewport
        self._region_x = context.region.x
        self._region_y = context.region.y
        self._draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self._draw_pivot, (self,), "WINDOW", "POST_PIXEL"
        )

        # angle from the pivot to the mouse position at invocation (radians).
        # this is the baseline angle; subsequent mouse movement is compared against it.
        # atan2 returns values in [-pi, pi]: past 180 degrees counterclockwise
        # yields negative numbers (e.g. 181 -> -179).
        mouseloc_centered = mouseloc - self.view3d_center
        self.initial_rotation = rv3d.view_rotation.copy()
        self.initial_angle = atan2(mouseloc_centered.y, mouseloc_centered.x)
        self.angle_now = self.initial_angle

        # rotation axis mapped from the scene property
        if context.scene.axis_roll == "X":
            self.camNormal = Vector((1, 0, 0))  # type: ignore
        elif context.scene.axis_roll == "Y":
            self.camNormal = Vector((0, 0, -1))  # type: ignore
        elif context.scene.axis_roll == "Z":
            self.camNormal = Vector((0, 1, 0))  # type: ignore

        return {"RUNNING_MODAL"}

    def execute(self, context):
        rv3d = context.space_data.region_3d

        angle_diff = self.angle_now - self.initial_angle
        quat = Quaternion(self.camNormal, angle_diff)  # type: ignore

        if self.rotate_camera:
            new_quat = self.initial_camera_rotation_quat @ quat
            if self.camera_rotation_mode == "QUATERNION":
                self.camera.rotation_quaternion = new_quat
            elif self.camera_rotation_mode == "AXIS_ANGLE":
                axis_angle = new_quat.to_axis_angle()
                self.camera.rotation_axis_angle = (axis_angle[1], *axis_angle[0])
            else:
                self.camera.rotation_euler = new_quat.to_euler(
                    self.camera_rotation_mode
                )
        else:
            rv3d.view_rotation = self.initial_rotation @ quat

        if angle_diff > 0:
            # print(to_degrees(angle_diff))
            self.temp_degree = angle_diff
        else:
            self.temp_degree = -1 * angle_diff

        return {"FINISHED"}

    @staticmethod
    def _draw_pivot(op):
        """DEBUG: draw a red crosshair at the rotation pivot position."""
        shader = gpu.shader.from_builtin("UNIFORM_COLOR")
        # convert region-relative pivot coords to window coords for POST_PIXEL
        cx = op._region_x + op.view3d_center.x
        cy = op._region_y + op.view3d_center.y
        size = 10

        coords = [
            (cx - size, cy),
            (cx + size, cy),
            (cx, cy - size),
            (cx, cy + size),
        ]
        batch = batch_for_shader(shader, "LINES", {"pos": coords})
        shader.bind()
        shader.uniform_float("color", (1.0, 0.2, 0.2, 1.0))
        batch.draw(shader)

    def modal(self, context, event):
        rv3d = context.space_data.region_3d

        if event.type == "MOUSEMOVE":
            mouseloc = Vector(  # type: ignore
                (event.mouse_region_x, event.mouse_region_y)
            )
            mouseloc_centered = mouseloc - self.view3d_center
            self.angle_now = atan2(mouseloc_centered.y, mouseloc_centered.x)
            self.execute(context)
        elif event.type in {"LEFTMOUSE", "MIDDLEMOUSE"}:
            if self._draw_handler:
                bpy.types.SpaceView3D.draw_handler_remove(self._draw_handler, "WINDOW")
                self._draw_handler = None
            return {"FINISHED"}
        elif event.type in {"RIGHTMOUSE", "ESC"}:
            if self.rotate_camera:
                if self.camera_rotation_mode == "QUATERNION":
                    self.camera.rotation_quaternion = self.initial_camera_rotation
                elif self.camera_rotation_mode == "AXIS_ANGLE":
                    self.camera.rotation_axis_angle = self.initial_camera_rotation
                else:
                    self.camera.rotation_euler = self.initial_camera_rotation
            else:
                rv3d.view_rotation = self.initial_rotation

            if self._draw_handler:
                bpy.types.SpaceView3D.draw_handler_remove(self._draw_handler, "WINDOW")
                self._draw_handler = None
            return {"CANCELLED"}

        return {"RUNNING_MODAL"}


class RollAxis(Operator):
    bl_idname = "aaa.roll_axis"
    bl_label = ""
    bl_options = {"REGISTER"}

    axis: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        if self.axis == "X":
            context.scene.axis_roll = "X"
        if self.axis == "Y":
            context.scene.axis_roll = "Y"
        if self.axis == "Z":
            context.scene.axis_roll = "Z"

        return {"FINISHED"}


class SwitchRenderer(Operator):
    bl_idname = "aaa.switch_renderer"
    bl_label = "Switch Renderer"
    bl_options = {"REGISTER"}

    mode: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        if self.mode == "SOLID":
            context.space_data.shading.type = "SOLID"
        else:
            if self.mode != "MATERIAL":
                # EEVEE Next was renamed to BLENDER_EEVEE in Blender 4.2+
                engine = self.mode
                if (
                    engine == "BLENDER_EEVEE_NEXT"
                    and engine
                    not in bpy.types.RenderSettings.bl_rna.properties[
                        "engine"
                    ].enum_items
                ):
                    engine = "BLENDER_EEVEE"
                context.scene.render.engine = engine
                context.space_data.shading.type = "RENDERED"
            else:
                if context.scene.render.engine == "BLENDER_WORKBENCH":
                    engine = "BLENDER_EEVEE_NEXT"
                    if (
                        engine
                        not in bpy.types.RenderSettings.bl_rna.properties[
                            "engine"
                        ].enum_items
                    ):
                        engine = "BLENDER_EEVEE"
                    context.scene.render.engine = engine
                    context.space_data.shading.type = "MATERIAL"
                else:
                    context.space_data.shading.type = "MATERIAL"
        return {"FINISHED"}
