bl_info = {
"name": "Rotating Camera Setup",
"author": "Janine Rickmeyer",
"version": (0, 0, 1),
"blender": (2, 78, 3),
"location": "View3D > Object > Move",
"description": "Creates a Camera and Curve to rotate around an Object",
"warning": "",
"wiki_url": "",
"tracker_url": "",
"category": "Object"}

"""
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
"""  


import bpy

class CreateRotatingCamera(bpy.types.Operator):
    """Creates a Camera and Curve to rotate around an Object"""
    bl_idname = "object.create_rotating_camera"
    bl_label = "Create a Camera and Curve to rotate around an Object"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        try:
            for cam in bpy.data.objects:
                if obj.type == 'CAMERA':
                    bpy.ops.object.delete()
        except:
            print("something went wrong")

        try:
            for ob in bpy.context.scene.objects:
                ob.select = ob.type == 'CAMERA' and ob.name.startswith("Camera")
            bpy.ops.object.delete()
        except:
            print("Something went wrong")

        bpy.ops.object.camera_add()
        my_cam = bpy.context.scene.objects.active
        #my_cam.name = "Camera"
        #bpy.data.cameras["Camera"].type = 'ORTHO'
        #bpy.data.cameras[my_cam.name].type = 'ORTHO'
        #bpy.data.cameras[bpy.context.scene.camera.name].type = 'ORTHO'
        try:
            for cammy in bpy.data.cameras:
                bpy.data.cameras[cammy.name].type = 'ORTHO'
        except:
            print("Something went wrong")
        my_cam.constraints.new('FOLLOW_PATH')
        my_cam.constraints["Follow Path"].forward_axis = 'FORWARD_Y'
        my_cam.constraints["Follow Path"].up_axis = 'UP_Z'

        bpy.data.scenes["Scene"].frame_end = 200

        bpy.ops.curve.primitive_bezier_circle_add()
        my_curve = bpy.context.scene.objects.active
        my_curve.scale[0] = 10
        my_curve.scale[1] = 10
        my_curve.location[2] = 1.5

        #bpy.data.curves[my_curve.name].path_duration = 200
        my_cam.constraints["Follow Path"].target = my_curve
        # don't need to have it
        # my_cam.constraints["Follow Path"].use_curve_follow = True
        # this one doesn't work
        #bpy.ops.constraint.followpath_path_animate()
        try:
            override={'constraint':my_cam.constraints["Follow Path"]}
            bpy.ops.constraint.followpath_path_animate(override,constraint='Follow Path')
        except:
            print("something went wrong")

        try:
            for x in bpy.data.curves:
                bpy.data.curves[x.name].path_duration = 200
        except:
            print("Something went wrong")

        try:
            for cur in bpy.data.curves:
                if cur.name.startswith("BezierCircle"):
                    bpy.ops.constraint.followpath_path_animate()
        except:
            print("Something went wrong")

        my_cam.constraints.new('TRACK_TO')
        # my_cam.constraints["Track To"].target = bpy.data.objects["Cube"]
        my_cam.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        my_cam.constraints["Track To"].up_axis = 'UP_Y'

        bpy.data.scenes["Scene"].render.resolution_percentage = 100
        bpy.data.scenes["Scene"].render.resolution_x = 1080
        bpy.data.scenes["Scene"].render.resolution_y = 1080
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return ((len(context.selected_objects) > 2) and (context.mode == 'OBJECT'))


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

def menu_func(self, context):
    self.layout.operator(CreateRotatingCamera.bl_idname,
    icon = 'MESH_CIRCLE')
