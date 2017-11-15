import robot_controller as robo
import mqtt_remote_method_calls as com
import time
import math

robot = robo.Snatch3r()
mqtt_client = com.MqttClient(robot)
mqtt_client.connect_to_pc()



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


def Mode(replace):
    if replace == "Follow":
        Following_Procedure()
    if replace == "Chase":
        Chasing_Procedure()
    if replace == "Manual":
        Manual_Procedure()
    if replace == "Guard":
        Guard_Procedure()
    if replace == "Distract":
        Distract_Procedure()

def Following_Procedure():
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    Holdex = robot.pixy.value(1)
    Holdsize = robot.pixy.value(3)*robot.pixy.value(4)
    timehold = 0
    while timehold < 10:
        if Holdex > robot.pixy.value(1):
            robot.drive_until_otherwise(100,-100)
        elif Holdex < robot.pixy.value(1):
            robot.drive_until_otherwise(-100,100)
        time.sleep(0.05)
        if Holdsize > robot.pixy.value(3)*robot.pixy.value(4):
            robot.drive_until_otherwise(300,300)
        elif Holdex < robot.pixy.value(3)*robot.pixy.value(4):
            robot.drive_until_otherwise(-300,-300)
        timehold += 0.1
        time.sleep(0.05)


def Chasing_Procedure():
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    Holdex = robot.pixy.value(1)
    timehold = 0
    while timehold < 10:
        if Holdex > robot.pixy.value(1):
            robot.drive_until_otherwise(200, 0)
        elif Holdex < robot.pixy.value(1):
            robot.drive_until_otherwise(0, 200)
        time.sleep(0.05)
        timehold += 0.05
        if math.fabs(Holdex - robot.pixy.value(1)) <= 1:
            robot.drive_until_otherwise(300, 300)
            time.sleep(0.05)
            timehold += 0.05


def Manual_Procedure():
    print("Switching to non-autonomus mode.")


def Guard_Procedure():
    Holdex = robot.pixy.value(1)
    Holdsize = robot.pixy.value(3) * robot.pixy.value(4)
    timehold = 0
    while timehold < 10:
        if (Holdsize - (robot.pixy.value(3) * robot.pixy.value(4))) < -1:
            robot.beep()