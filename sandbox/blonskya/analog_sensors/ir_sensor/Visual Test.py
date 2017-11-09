import ev3dev.ev3 as ev3
import time

ev3.Sound.speak("Visual Test").wait()

touch_sensor = ev3.TouchSensor()
ir_sensor = ev3.InfraredSensor()
assert ir_sensor
assert touch_sensor
time.sleep(1)
beacon_seeker = ev3.BeaconSeeker(channel=1)
assert beacon_seeker

while not touch_sensor.is_pressed:
    current_distance = beacon_seeker.distance  # use the beacon_seeker distance
    print("Dist:", current_distance)
    current_heading = beacon_seeker.heading  # use the beacon_seeker heading
    print("Heading:", current_heading)

    time.sleep(0.3)


print("goodbye")