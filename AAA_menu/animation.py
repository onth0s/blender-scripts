import bpy  # type: ignore
from bpy.types import Menu  # type: ignore

class VIEW3D_MT_ANIMATION_PLAYBACK(Menu):
    bl_label = "Animation Playback"

    def draw(self, context):
        layout = self.layout
        layout.operator("screen.animation_play", text="D - Play")
        layout.operator("screen.frame_jump", text="A - Jump Start").end = False
        layout.operator("screen.frame_jump", text="Q - Jump End").end = True
        layout.operator("screen.animation_play", text="E - Reverse").reverse = True


class VIEW3D_MT_ABOUT_FRAMES(Menu):
    bl_label = "About Frames"

    def draw(self, context):
        LYT = self.layout

        LYT = self.layout
        LYT.operator("wm.call_panel", text="A - Rate").name = "VIEW3D_PT_FRAME_RATE"
        LYT.operator(
            "aaa.toggle_prop", text="D - Preview"
        ).prop = "context.scene.use_preview_range"
