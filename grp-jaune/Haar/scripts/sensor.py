import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
print("Environment Ready")

cap = cv2.VideoCapture(0)

# Setup:
pipe = rs.pipeline()

# Skip 5 first frames to give the Auto-Exposure time to adjust
for x in range(5):
  pipe.wait_for_frames()

while True:

    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    objets = objet_cascade.detectMultiScale(gray, 1.3, 5)
    k = cv2.waitKey(30) & 0xff

    for (x, y, w, h) in objets:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    cv2.imshow('img', img)
    if k == 27:
        break
    # Create alignment primitive with color as its target stream:
    align = rs.align(rs.stream.color)
    frameset = align.process(frameset)


    # Create alignment primitive with color as its target stream:
    align = rs.align(rs.stream.color)
    frameset = align.process(frameset)

    # Update color and depth frames:
    aligned_depth_frame = frameset.get_depth_frame()

    scale = height / expected
    xmin_depth = int((xmin * expected + crop_start) * scale)
    ymin_depth = int((ymin * expected) * scale)
    xmax_depth = int((xmax * expected + crop_start) * scale)
    ymax_depth = int((ymax * expected) * scale)
    xmin_depth,ymin_depth,xmax_depth,ymax_depth


    depth = np.asanyarray(aligned_depth_frame.get_data())
    # Crop depth data:
    depth = depth[xmin_depth:xmax_depth,ymin_depth:ymax_depth].astype(float)

    # Get data scale from the device and convert to meters
    depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
    depth = depth * depth_scale
    dist,_,_,_ = cv2.mean(depth)
    print("Detected a {0} {1:.3} meters away.".format(className, dist))
    
cap.release()
cv2.destroyAllWindows()