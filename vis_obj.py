import bpy
import os

obj_folder = 'E:/DATA/test/2024-01-19-21-14-10/body_mesh'
output_folder = 'E:/DATA/test/2024-01-19-21-14-10/mesh_image'
obj_files = [f for f in os.listdir(obj_folder) if f.endswith('.obj')]

for obj_file in obj_files:
    path_to_file = os.path.join(obj_folder, obj_file)
    bpy.ops.import_scene.obj(filepath=path_to_file)

    bpy.context.scene.render.image_settings.file_format = 'PNG'
    output_path = os.path.join(output_folder, os.path.splitext(obj_file)[0] + '.png')
    bpy.context.scene.render.filepath = output_path

    bpy.ops.render.render(write_still=True)

    bpy.ops.object.delete()
