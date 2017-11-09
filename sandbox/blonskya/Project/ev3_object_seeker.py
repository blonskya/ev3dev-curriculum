import robot_controller as robo
import mqtt_remote_method_calls as com

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.pixy.mode = "SIG1"


def Forward():
    robot = robo.Snatch3r()
    robot.drive_until_otherwise(800,800)

def Backward():
    robot = robo.Snatch3r()
    robot.drive_until_otherwise(-800, -800)

def Right():
    robot = robo.Snatch3r()
    robot.drive_until_otherwise(-100,100)

def Left():
    robot = robo.Snatch3r()
    robot.drive_until_otherwise(100,-100)

def Brake():
    robot = robo.Snatch3r()
    robot.stop()
