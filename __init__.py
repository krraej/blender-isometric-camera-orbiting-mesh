import bpy

# name of the file and then the name of the function
from .helperfunctions import myfunc

bl_info = {
	"name": "Isometric Camera Orbiting Mesh",
	"author": "krraej",
	"version": (0, 0, 1),
	"blender": (2, 79, 1),
	#"location": "View3D > Add > Mesh > Dummy Op",
	#"description": "A dummy operator that makes use of bundled modules",
	-"category": "Experimental development"}


class DummyOpModule(bpy.types.Operator):
	bl_idname = 'mesh.dummyopmodule'
	bl_label = 'Dummy Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		loc = context.active_object.location
		context.active_object.location = myfunc(loc)
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		DummyOpModule.bl_idname,
		text=DummyOpModule.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
