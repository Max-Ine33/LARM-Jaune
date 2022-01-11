import cv2                                # state of the art computer vision algorithms library
import numpy as np  
import pyrealsense2 as rs    
from cv_bridge import CvBridge, CvBridgeError                  # fundamental package for scientific computing
print("démarrage script")

class RealsenseCapture:

    def __init__(self, width='640', height='480', fps='30'):

        # Variables for setup
        self.width = width
            self.height = height
        self.fps = fps
        self.imgs = np.zeros((480, 640, 3))
        self.img0 = np.zeros((480, 640, 3))
        self.img_size = 416
        self.half = False
        self.updated_image = False
        self.bridge = CvBridge()

        self.color_sub = rospy.Subscriber("/camera/color/image_raw", Image, self.callback)

        print("streaming at w = " + str(self.width) + " h = " + str(self.height) + " fps = " + str(self.fps))

    def callback(self, data):

        try:
            self.img0 = self.bridge.imgmsg_to_cv2(data, "bgr8")
            # print(type(self.color_image))
            self.updated_image = True
        except CvBridgeError as e:
            print(e)

    def __iter__(self):
        self.count = -1
        return self

    def __next__(self):
        self.count += 1
        # self.rect = self.update()
        # while not self.updated_image:
        self.imgs = np.expand_dims(self.img0, axis=0)
        self.updated_image = True
        # print("ini img expand: " + str(np.shape(self.imgs)))

        s = np.stack([letterbox(x, new_shape=self.img_size)[0].shape for x in self.imgs], 0)  # inference shapes

        self.rect = np.unique(s, axis=0).shape[0] == 1

        if not self.rect:
            print('WARNING: Different stream shapes detected. For optimal performance supply similarly-shaped streams.')

        time.sleep(0.01)  # wait time
        img0 = self.imgs.copy()

        if cv2.waitKey(1) == ord('q'):  # q to quit
            cv2.destroyAllWindows()
            raise StopIteration

        img_path = 'realsense.jpg'

        # Letterbox
        img = [letterbox(x, new_shape=self.img_size, interp=cv2.INTER_LINEAR)[0] for x in img0]

        # Stack
        img = np.stack(img, 0)

        # Convert Image
        img = img[:, :, :, ::-1].transpose(0, 3, 1, 2)  # BGR to RGB, to 3x416x416, uint8 to float32
        img = np.ascontiguousarray(img, dtype=np.float16 if self.half else np.float32)
        img /= 255.0  # 0 - 255 to 0.0 - 1.0

        # Return depth, depth0, img, img0
        return str(img_path), img, img0, None

    def __len__(self):
        return 0  # 1E12 frames = 32 streams at 30 FPS for 30 years