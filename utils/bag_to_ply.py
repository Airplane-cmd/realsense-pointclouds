import numpy as np
import pyrealsense2 as rs
import pandas as pd
from pyntcloud import PyntCloud

# Configure the pipeline to use the .bag file
pipeline = rs.pipeline()
config = rs.config()
config.enable_device_from_file('/home/bthd/WS/robotics/realsense-pointclouds/bag_files/recorded_data.bag')
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

try:
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    if not depth_frame or not color_frame:
        print("No frames available")
        exit(1)

    # Convert to numpy arrays
    depth_image_np = np.asanyarray(depth_frame.get_data())
    color_image_np = np.asanyarray(color_frame.get_data())

    # Depth image parameters
    width, height = depth_image_np.shape[1], depth_image_np.shape[0]
    fx, fy = 382.722, 382.722
    cx, cy = 318.952, 239.211

    # Create a point cloud
    points = []
    colors = []

    for v in range(height):
        for u in range(width):
            depth = depth_image_np[v, u] * 0.001  # Convert depth to meters
            if depth == 0:
                continue
            x = (u - cx) * depth / fx
            y = (v - cy) * depth / fy
            z = depth
            color = color_image_np[v, u]
            r, g, b = color[2], color[1], color[0]  # BGR to RGB

            points.append((x, y, z))
            colors.append((r, g, b))

    df = pd.DataFrame(np.array(points), columns=['x', 'y', 'z'])
    df['red'] = [c[0] for c in colors]
    df['green'] = [c[1] for c in colors]
    df['blue'] = [c[2] for c in colors]

    cloud = PyntCloud(df)
    cloud.to_file('/home/bthd/WS/robotics/realsense-pointclouds/hr_blobs/output_point_cloud.ply')
    print("Point cloud saved successfully!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    pipeline.stop()
