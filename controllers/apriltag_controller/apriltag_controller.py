from dataclasses import Field

from controller import Supervisor
from controller import Keyboard

from math import cos, sin

if __name__ == '__main__':
    # Supervisors allow us to edit the real position of the AprilTag,
    # without needing to use motors or something like that
    supervisor = Supervisor()
    # The amount of time, in milliseconds, between each simulation step
    timestep = int(supervisor.getBasicTimeStep())

    keyboard = Keyboard()
    keyboard.enable(timestep)

    # We get references to these fields so we can read and change their values.
    # Getting them only once instead of every time we need them saves on the cost of the lookup, however minimal
    translation_field = supervisor.getSelf().getField("translation")
    rotation_field = supervisor.getSelf().getField("rotation")

    print("====== AprilTag Controls ======\n")

    print(" The AprilTag can be positioned with your keyboard.")
    print(" - Use the up, down, left, or right keys to move the tag in the horizontal plane.")
    print(" - Use the Q and E buttons to rotate the face of the tag.")
    print(" - Use the W and S keys to move the tag up and down.")

    # supervisor.step() will return -1 when Webots terminates this controller
    while supervisor.step(timestep) != -1:
        forward_diff_desired = 0
        sideways_diff_desired = 0
        yaw_diff_desired = 0
        height_diff_desired = 0

        # This reads a key code from the keyboard.
        # It can be read repeatedly to get simultaneous key presses.
        key = keyboard.getKey()
        # As long as it is non-negative, it is still returning some current key press, so we keep looping
        while key > 0:
            if key == Keyboard.UP:
                forward_diff_desired += 0.15 # These values can be tweaked to change the speed of the AprilTag
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
                height_diff_desired = + 0.15
            elif key == ord('S'):
                height_diff_desired = - 0.15
            key = keyboard.getKey()

        # Translations are stored as an array of 3 floats ([x, y, z])
        translation_values = translation_field.getSFVec3f()
        # Rotations are stored as an array of 4 floats ([x, y, z, angle])
        # where x, y, and z are the axes to rotate on and the angle is in radians
        rotation = rotation_field.getSFRotation()[3] # We only care about the angle property,
                                                     # since the others don't change

        # Forward-backward relative to the facing direction
        new_x_position = translation_values[0] + (
                    cos(rotation) * forward_diff_desired - sin(rotation) * sideways_diff_desired
                ) * timestep / 1000 # We multiply by the timestep (divide by 1000 to compute in seconds)
                                    # to remain independent of the framerate of the program

        # Sideways relative to the facing direction
        new_y_position = translation_values[1] + (
                    sin(rotation) * forward_diff_desired + cos(rotation) * sideways_diff_desired
                ) * timestep / 1000
        # Vertical position, not related to facing direction
        new_z_position = translation_values[2] + height_diff_desired * timestep / 1000

        new_rotation = rotation + yaw_diff_desired * timestep / 1000

        # We convert these new values back into their original datatype layout
        # and overwrite the fields with the new values
        translation_field.setSFVec3f([new_x_position, new_y_position, new_z_position])
        rotation_field.setSFRotation([0, 0, 1, new_rotation])
