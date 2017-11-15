"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        self.running=True
        self.touch_sensor = ev3.TouchSensor()
        self.seeker=ev3.BeaconSeeker(channel=1)
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.mode = "Follow"

    def distance(self):
        self.eyes=ev3.InfraredSensor()
        assert self.eyes.connected

        return self.eyes.proximity


    def beep(self):
        ev3.Sound.beep().wait()

    def seek_beacon(self):
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)
            # Done: 3. Use the beacon_seeker object to get the current heading and distance.
            time.sleep(0.35)
            current_heading = self.seeker.heading  # use the beacon_seeker heading
            current_distance = self.seeker.distance  # use the beacon_seeker distance
            print(current_heading, current_distance, math.fabs(current_heading))

            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                # Done: 4. Implement the following strategy to find the beacon.
                # If the absolute value of the current_heading is less than 2, you are on the right heading.
                #     If the current_distance is 0 return from this function, you have found the beacon!  return True
                #     If the current_distance is greater than 0 drive straight forward (forward_speed, forward_speed)
                # If the absolute value of the current_heading is NOT less than 2 but IS less than 10, you need to spin
                #     If the current_heading is less than 0 turn left (-turn_speed, turn_speed)
                #     If the current_heading is greater than 0 turn right  (turn_speed, -turn_speed)
                # If the absolute value of current_heading is greater than 10, then stop and print Heading too far off
                #
                # Using that plan you should find the beacon if the beacon is in range.  If the beacon is not in range your
                # robot should just sit still until the beacon is placed into view.  It is recommended that you always print
                # something each pass through the loop to help you debug what is going on.  Examples:
                #    print("On the right heading. Distance: ", current_distance)
                #    print("Adjusting heading: ", current_heading)
                #    print("Heading is too far off to fix: ", current_heading)

                # Here is some code to help get you started
                if math.fabs(current_heading) <= 1:
                    if current_distance > 1:
                        # Close enough of a heading to move forward
                        self.left_motor.run_forever(speed_sp=forward_speed)
                        print("On the right heading. Distance: ", current_distance)
                        self.right_motor.run_forever(speed_sp=forward_speed)
                        # You add more!
                    else:
                        print("Found it")
                        time.sleep(1)
                        self.right_motor.stop(stop_action="brake")
                        self.left_motor.stop(stop_action="brake")
                        return True
                elif math.fabs(current_heading) > 10:
                    print("Heading is too far off to fix: ", current_heading)
                    self.left_motor.stop(stop_action="brake")
                    self.right_motor.stop(stop_action="brake")
                    return False
                elif current_heading > 2:
                    print("Adjusting heading: ", current_heading)
                    current_heading = self.seeker.heading  # use the beacon_seeker heading
                    self.right_motor.run_forever(speed_sp=-turn_speed)
                    self.left_motor.run_forever(speed_sp=turn_speed)
                elif current_heading < -2:
                    print("Adjusting heading: ", current_heading)
                    current_heading = self.seeker.heading  # use the beacon_seeker heading
                    self.right_motor.run_forever(speed_sp=turn_speed)
                    self.left_motor.run_forever(speed_sp=-turn_speed)
                else:
                    print("failure")
        self.stop()


    def drive_inches(self, distance, speed):
        self.left_motor.run_to_rel_pos(position_sp=distance * 360 / 4, speed_sp=speed, stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=distance * 360 / 4, speed_sp=speed, stop_action="brake")
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def drive_until_otherwise(self, rspeed, lspeed):
        self.left_motor.run_forever(speed_sp=lspeed)
        self.right_motor.run_forever(speed_sp=rspeed)

    # DONE: Implement the Snatch3r class as needed when working the sandbox exercises
    def loop_forever(self):
        ''' waits forever'''
        while self.running:
            time.sleep(0.01)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """turns the amount of degrees specified in the speed specified"""
        self.left_motor.run_to_rel_pos(position_sp=(-degrees_to_turn/360)*((6-0.0153)/0.011)*math.pi, speed_sp=turn_speed_sp,
                                       stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=(degrees_to_turn/360)*((6-0.0153)/0.011)*math.pi, speed_sp=turn_speed_sp,
                                        stop_action="brake")
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
    def stop(self):
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

    def shutdown(self):
        # stops all the motors
        self.running = False
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print("Goodbye")
        ev3.Sound.speak("Goodbye")

    def arm_calibration(self):
        # calibrates the arm top and bottom of motion
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected
        assert self.touch_sensor

        arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_motor.run_to_rel_pos(position_sp=(-14.2*360))
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        # moves the arm to the top of its range motion
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected

        assert self.touch_sensor

        max_speed = 900
        arm_motor.run_forever(speed_sp=max_speed)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        # moves the arm to the bottom of its range of motion
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected

        arm_motor.run_to_abs_pos(position_sp=0)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

