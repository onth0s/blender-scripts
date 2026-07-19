import bpy  # type: ignore
import os
from bpy.types import Operator  # type: ignore
from AAA_utils import resolve_incremented_path

class SaveFile(Operator):
    """Save the current file and check if it has already been saved."""

    bl_idname = "aaa.save_file"
    bl_label = "Save File"
    bl_options = {"REGISTER"}

    def execute(self, context):
        if not context.blend_data.filepath:
            if context.area is not None:
                bpy.ops.wm.save_mainfile("INVOKE_DEFAULT")
                return {"FINISHED"}
            self.report({"WARNING"}, "File has not been saved yet. Save it first.")
            return {"CANCELLED"}

        filename = bpy.path.basename(context.blend_data.filepath)
        bpy.ops.wm.save_mainfile("INVOKE_DEFAULT")

        if bpy.data.is_saved:
            if bpy.data.is_dirty:
                saved = "Saved: " + filename
                self.report({"INFO"}, saved)

                context.scene.already_saved_counter = 0
            else:
                context.scene.already_saved_counter += 1
                st = (
                    "No changes have been made to '"
                    + filename
                    + "'. Already saved file ("
                    + str(context.scene.already_saved_counter)
                    + ")"
                )
                self.report({"INFO"}, st)

        return {"FINISHED"}


class SaveIncremental(Operator):
    bl_idname = "aaa.save_incremental"
    bl_label = ""
    bl_options = {"REGISTER"}

    def execute(self, context):
        currentblend = bpy.data.filepath
        if currentblend:
            save_path = resolve_incremented_path(currentblend)
            # add_to_recent_files(save_path)
            if os.path.exists(save_path):
                self.report(
                    {"WARNING"},
                    "File '%s' exists already!\nBlend has NOT been saved incrementally!"
                    % (save_path),
                )
            else:
                bpy.ops.wm.save_as_mainfile(filepath=save_path)
                self.report({"INFO"}, "Saved blend incrementally:" + save_path)

                context.scene.already_saved_counter = 0
            return {"FINISHED"}
        else:
            # No filepath set – prompt user via the standard save dialog.
            # context.area is None in background/headless mode, so we cancel
            # gracefully there rather than crashing on INVOKE_DEFAULT.
            if context.area is not None:
                bpy.ops.wm.save_mainfile("INVOKE_DEFAULT")
                return {"FINISHED"}
            self.report({"WARNING"}, "File has not been saved yet. Save it first.")
            return {"CANCELLED"}
