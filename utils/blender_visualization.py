import bpy


def create_point_cloud_from_file(filepath):
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Ensure PLY import add-on is enabled
    if not bpy.ops.import_mesh.ply.poll():
        raise RuntimeError("PLY import operator is not available. Make sure the add-on is enabled.")

    # Load the PLY file
    bpy.ops.import_mesh.ply(filepath=filepath)

    # Get the imported mesh object
    obj = bpy.context.object

    # Check if the object is a mesh
    if obj and obj.type == 'MESH':
        # Switch to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Optionally, you can add more modifications here, such as scaling or positioning
        obj.scale = (1, 1, 1)  # Scale the object
        obj.location = (0, 0, 0)  # Position the object

        # Set shading to smooth
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = 1.0


# Replace with the path to your PLY file
point_cloud_path = '/home/bthd/WS/robotics/realsense-pointclouds/hr_blobs/output_point_cloud.ply'

create_point_cloud_from_file(point_cloud_path)
