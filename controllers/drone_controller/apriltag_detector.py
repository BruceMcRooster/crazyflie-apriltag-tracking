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

        # Camera, at least on this simulator Crazyflie model, does not have a focal length set.
        # Thus, camera.getFocalLength() would return 0 and mess up calculations.
        # Instead, we compute these parameters using the width/height and FOV.
        # This does assume the FOV is the same for the width and height (the camera takes a square image).
        fx = (self.camera.width / 2) / (self.camera.fov / 2)
        fy = (self.camera.height / 2) / (self.camera.fov / 2)

        # Center of focus is the center of the camera view
        cx = self.camera.width / 2
        cy = self.camera.height / 2

        self.camera_matrix = np.array([[fx, 0, cx],
                                  [0, fy, cy],
                                  [0, 0, 1]], dtype=np.float32)

        self.marker_length = 0.1


    def _get_camera_image(self) -> np.ndarray:
        """
        Gets the camera image representation in BGR format.
        :returns: The image from the camera, in BGR format.
        """
        img = np.frombuffer(self.camera.getImage(), dtype=np.uint8).reshape((self.camera.height, self.camera.width, 4))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


    def _get_min_id_apriltag(self, image: np.ndarray) -> Tuple[int, np.ndarray] | Tuple[None, None]:
        """
        Gets the id and corners of the lowest-ID AprilTag in the image.
        :param image: The image to process for AprilTags.
        :return: A tuple of the id and corners of the lowest-ID AprilTag, or None if no AprilTag found.
        """
        corners, ids, rejected_image_points = self.detector.detectMarkers(image)

        if ids is None or len(ids) == 0:
            return None, None

        min_index = int(np.argmin(ids))

        min_corners = corners[min_index]

        return int(ids[min_index]), min_corners


    def _get_apriltag_orientation(self, corners: np.ndarray) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]] | None:
        """
        Gets the location and rotation of the given AprilTag in the image, relative to the camera.
        :param corners: The corners of the AprilTag, relative to the image frame.
        :return: If no AprilTag detected, returns None. Otherwise, returns the position and rotation of the lowest-ID AprilTag
        in the coordinate space of the camera. The rotation vector is a Rodrigues rotation vector.
        """

        obj_points = np.array([[-self.marker_length / 2.0, self.marker_length / 2.0, 0],
                               [self.marker_length / 2.0, self.marker_length / 2.0, 0],
                               [self.marker_length / 2.0, -self.marker_length / 2.0, 0],
                               [-self.marker_length / 2.0, -self.marker_length / 2.0, 0]],
                              dtype=np.float32)

        _, rvec, tvec = cv2.solvePnP(
            objectPoints=obj_points,
            imagePoints=corners,
            cameraMatrix=self.camera_matrix,
            distCoeffs=None
        )

        return rvec, tvec


    def get_min_tag_offset(self,
                           show_detection_window: bool = False) -> Tuple[np.ndarray, np.ndarray] | Tuple[None, None]:
        """
        Calculates the position and rotation of any detected AprilTag in the image in the frame of the camera.
        :param show_detection_window: Show external Python window with the detected AprilTag and pose annotations.
        This will almost certainly slow down the simulation, so it is intended more for debug purposes.
        :return: If an AprilTag is detected, return the position of the detected AprilTag in the frame of the camera,
        where the first part of the tuple is the transform
        in XYZ format (Z is forward, Y is upward, different Webots coordinate system)
        and the second part of the tuple is Rodrigues rotation vector.
        If no AprilTag is detected, returns None.
        """

        image = self._get_camera_image()
        tag_id, corners = self._get_min_id_apriltag(image)
        if tag_id is None or corners is None: # No detections
            return None, None

        rvec, tvec = self._get_apriltag_orientation(corners)

        if show_detection_window:
            aruco.drawDetectedMarkers(image, [corners], np.array([tag_id]))
            cv2.drawFrameAxes(
                image=image,
                cameraMatrix=self.camera_matrix,
                distCoeffs=None,
                rvec=rvec,
                tvec=tvec,
                length=self.marker_length * 1.5,
                thickness=2,
            )
            cv2.imshow('AprilTag Detection', image)
            cv2.waitKey(100)

        return rvec, tvec
