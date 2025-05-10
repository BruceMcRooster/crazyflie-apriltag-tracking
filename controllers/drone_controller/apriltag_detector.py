from typing import Tuple

import cv2
from cv2 import aruco as aruco
import numpy as np

from controller import Camera


class AprilTagDetector:
    def __init__(self, camera: Camera):
        apriltag_dict = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_16h5)
        parameters = aruco.DetectorParameters()
        self.detector = aruco.ArucoDetector(apriltag_dict, parameters)
        self.camera = camera


    def _get_camera_image(self) -> np.ndarray:
        """
        Gets the camera image representation in BGR format.
        :arg cam: The Camera to get the image from.
        :returns: The image from the camera, in BGR format.
        """
        img = np.frombuffer(self.camera.getImage(), dtype=np.uint8).reshape((self.camera.height, self.camera.width, 4))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


    def _get_min_id_apriltag(self, image: np.ndarray) -> Tuple[int, np.ndarray] | None:
        """
        Gets the id and corners of the lowest-ID AprilTag in the image.
        :param image: The image to process for AprilTags.
        :return: A tuple of the id and corners of the lowest-ID AprilTag, or None if no AprilTag found.
        """
        corners, ids, rejected_image_points = self.detector.detectMarkers(image)

        if ids is None or len(ids) == 0:
            return None

        min_index = int(np.argmin(ids))

        min_corners = corners[min_index]

        return int(ids[min_index]), min_corners
