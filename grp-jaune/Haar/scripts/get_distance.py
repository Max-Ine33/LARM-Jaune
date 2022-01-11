# coding: utf-8
 
 import cv2
 import numpy as np
 from realsensecv import RealsenseCapture

# Carry out the processing at the time of the mouse event
  def mouse_event(event, x, y, flags, param):

    depth_frame = param

    distance = depth_frame.get_distance(x, y)

    # returns the coordinates in the left click
      if event == cv2.EVENT_LBUTTONUP:

        return print(distance)


cap = RealsenseCapture()
 cap.start()


while True:

    ret, frames = cap.read()

    color_frame = frames[0]

    depth_frame = frames[1]

    # conversion to heat map
      depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(

        depth_frame, alpha=0.08), cv2.COLORMAP_JET)

    # rendering
      images = np.hstack((color_frame, depth_colormap))

    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)

    cv2.imshow('RealSense', images)


    # Carry out the processing of the function mouse_event at the time of the mouse event
      cv2.setMouseCallback('RealSense', mouse_event, cap.depth_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):

        break


# Streaming Stop
  cap.release()
 cv2.destroyAllWindows()
 