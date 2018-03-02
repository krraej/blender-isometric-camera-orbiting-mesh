bl_info = {
"name": "Isometric Camera",
"author": "krraej",
"version": (0, 0, 1),
"blender": (2, 79, 1),
"location": "View3D > View",
"description": "Creates a Camera in an Isometric Perspective",
"warning": "",
"wiki_url": "",
"tracker_url": "",
"category": "View"}

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
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "object"
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        layout.operator("object.camera_add", text="Add Cam", icon="CAMERA_DATA")
        
        
#def register():
#    bpy.utils.register_module(__name__)
    
#def unregister():
 #   bpy.utils.unregister_module(__name__)
    
#if __name__ == "__main__":
#    register()
    



class CreateIsometricCamera(bpy.types.Operator):
    """Create Camera with isometric View"""
    bl_idname = "object.create_isometric_camera"
    bl_label = "Create Camera with isometric View"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        try:
            for ob in bpy.context.scene.objects:
                ob.select = ob.type == 'CAMERA' and ob.name.startswith("Camera")
            bpy.ops.object.delete()
        except:
            print("Something went wrong.")

        bpy.ops.object.camera_add()
  
        try:
            for cammy in bpy.data.cameras:
                bpy.data.cameras[cammy.name].type = 'ORTHO'
        except:
            print("Something went wrong.")


        scene = bpy.data.scenes["Scene"]
        scene.render.resolution_percentage = 100
        scene.render.resolution_x = 1080
        scene.render.resolution_y = 1080
        scene.camera.rotation_mode = 'QUATERNION'
        bpy.ops.view3D.camera_to_view()
        scene.camera.rotation_quaternion = 0.8, 0.462, 0.191, 0.331
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_view.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_view.remove(menu_func)

def menu_func(self, context):
    self.layout.operator(CreateIsometricCamera.bl_idname,
    icon = 'CAMERA_DATA')
