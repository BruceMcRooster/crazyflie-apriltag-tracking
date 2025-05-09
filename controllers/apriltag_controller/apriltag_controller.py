from dataclasses import Field

from controller import Supervisor
from controller import Keyboard

from math import cos, sin

if __name__ == '__main__':
    supervisor = Supervisor()
    timestep = int(supervisor.getBasicTimeStep())

    keyboard = Keyboard()
    keyboard.enable(timestep)

    translation_field = supervisor.getSelf().getField("translation")
    rotation_field = supervisor.getSelf().getField("rotation")

    print("====== AprilTag Controls ======\n\n")

    print(" The AprilTag can be positioned with your keyboard.\n")
    print(" - Use the up, down, left, or right keys to move the tag in the horizontal plane.\n")
    print(" - Use the Q and E buttons to rotate the face of the tag.\n")
    print(" - Use the W and S keys to move the tag up and down.\n")

    print("\n\n")

    while supervisor.step(timestep) != -1:
        forward_diff_desired = 0
        sideways_diff_desired = 0
        yaw_diff_desired = 0
        height_diff_desired = 0

        key = keyboard.getKey()
        while key > 0:
            if key == Keyboard.UP:
                forward_diff_desired += 0.15
            elif key == Keyboard.DOWN:
                forward_diff_desired -= 0.15
            elif key == Keyboard.RIGHT:
                sideways_diff_desired -= 0.15
            elif key == Keyboard.LEFT:
                sideways_diff_desired += 0.15
            elif key == ord('Q'):
                yaw_diff_desired = - 0.5
            elif key == ord('E'):
                yaw_diff_desired = + 0.5
            elif key == ord('W'):
                height_diff_desired = 0.15
            elif key == ord('S'):
                height_diff_desired = - 0.15
            key = keyboard.getKey()

        translation_values = translation_field.getSFVec3f()
        rotation = rotation_field.getSFRotation()[3] # Gets the radians property about the Z axis

        # Forward-backward relative to the facing direction
        new_x_position = translation_values[0] + (cos(rotation) * forward_diff_desired - sin(rotation) * sideways_diff_desired) * timestep / 1000
        # Sideways relative to the facing direction
        new_y_position = translation_values[1] + (sin(rotation) * forward_diff_desired + cos(rotation) * sideways_diff_desired) * timestep / 1000
        # Vertical position, not related to facing direction
        new_z_position = translation_values[2] + height_diff_desired * timestep / 1000

        new_rotation = rotation + yaw_diff_desired * timestep / 1000

        translation_field.setSFVec3f([new_x_position, new_y_position, new_z_position])
        rotation_field.setSFRotation([0, 0, 1, new_rotation])
