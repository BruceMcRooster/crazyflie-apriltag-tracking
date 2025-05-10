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


    def _get_apriltag_orientation(self, image: np.ndarray, corners: np.ndarray) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]] | None:
        """
        Gets the location and rotation of the given AprilTag in the image, relative to the camera.
        :param image: The image that contains the AprilTag.
        :param corners: The corners of the AprilTag, relative to the image frame.
        :return: If no AprilTag detected, returns None. Otherwise, returns the position and rotation of the lowest-ID AprilTag
        in the coordinate space of the camera. The rotation vector is a Rodrigues rotation vector.
        """

        # Camera, at least on this simulator Crazyflie model, does not have a focal length set.
        # Thus, camera.getFocalLength() would return 0 and mess up calculations.
        # Instead, we compute these parameters using the width/height and FOV.
        # This does assume the FOV is the same for the width and height (the camera takes a square image).
        fx = (self.camera.width / 2) / (self.camera.fov / 2)
        fy = (self.camera.height / 2) / (self.camera.fov / 2)

        # Center of focus is the center of the camera view
        cx = self.camera.width / 2
        cy = self.camera.height / 2

        camera_matrix = np.array([[fx, 0, cx],
                                  [0, fy, cy],
                                  [0, 0, 1]], dtype=np.float32)

        marker_length = 0.1
        obj_points = np.array([[-marker_length / 2.0, marker_length / 2.0, 0],
                               [marker_length / 2.0, marker_length / 2.0, 0],
                               [marker_length / 2.0, -marker_length / 2.0, 0],
                               [-marker_length / 2.0, -marker_length / 2.0, 0]],
                              dtype=np.float32)

        _, rvec, tvec = cv2.solvePnP(
            objectPoints=obj_points,
            imagePoints=corners,
            cameraMatrix=camera_matrix,
            distCoeffs=None
        )

        return rvec, tvec