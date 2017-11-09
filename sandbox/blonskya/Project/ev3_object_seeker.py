import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import math
import mqtt_remote_method_calls as com

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.pixy.mode = "SIG1"
