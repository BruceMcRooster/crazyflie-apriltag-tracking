import cv2
import numpy as np

from controller import Camera


class AprilTagDetector:
    def __init__(self, camera: Camera):
        self.camera = camera


    def _get_camera_image(self) -> np.ndarray:
        """
        Gets the camera image representation in BGR format.
        :arg cam: The Camera to get the image from.
        :returns: The image from the camera, in BGR format.
        """
        img = np.frombuffer(self.camera.getImage(), dtype=np.uint8).reshape((self.camera.height, self.camera.width, 4))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
