import bpy
from bpy.types import Menu, Panel, UIList

class View3DPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
class OpenIsometricCameraPanel(View3DPanel, Panel):
    # bl_space_type = 'CLIP_EDITOR'
    bl_label = "Add IsoCamera"
    bl_context = "objectmode"
    bl_category = "Open IsoCamera" #name of the tab displayed
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        layout.operator("object.camera_add", text="Add Cam", icon="CAMERA_DATA")
        
        
def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()
    
