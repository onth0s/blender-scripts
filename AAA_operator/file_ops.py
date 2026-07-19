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


class ReloadScripts(Operator):
    bl_idname = "aaa.reload_scripts"
    bl_label = "Reload AAA Scripts"
    bl_options = {"REGISTER"}

    def execute(self, context):
        import bpy
        import sys

        def delayed_reload():
            # 1. Unregister top-level modules
            for name in list(sys.modules.keys()):
                if name.startswith("AAA_") and "." not in name:
                    mod = sys.modules[name]
                    if hasattr(mod, "unregister"):
                        try:
                            mod.unregister()
                        except Exception as e:
                            print(f"Error unregistering {name}: {e}")

            # 2. Clear all AAA modules from sys.modules
            for name in list(sys.modules.keys()):
                if name.startswith("AAA"):
                    del sys.modules[name]

            # 3. Re-import and Register in order
            try:
                import AAA_utils
                import AAA_settings
                import AAA_operator
                import AAA_menu
                import AAA_panel
                import AAA_pie
                import AAA_keymap

                modules = [
                    AAA_utils,
                    AAA_settings,
                    AAA_operator,
                    AAA_menu,
                    AAA_panel,
                    AAA_pie,
                    AAA_keymap,
                ]

                for mod in modules:
                    if hasattr(mod, "register"):
                        mod.register()

                print("Reloaded AAA scripts successfully")
            except Exception as e:
                print(f"Failed to reload AAA scripts: {e}")

            return None

        # Schedule execution to run outside of the operator call stack
        bpy.app.timers.register(delayed_reload, first_interval=0.01)
        self.report({"INFO"}, "Scripts Reloaded!")
        return {"FINISHED"}

