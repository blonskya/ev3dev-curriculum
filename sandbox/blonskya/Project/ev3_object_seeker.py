import robot_controller as robo
import mqtt_remote_method_calls as com
import time
import math

class MyDelegate(object):

    def __init__(self):
        self.running = True

    def Forward(self):
        robot = robo.Snatch3r()
        robot.drive_until_otherwise(800,800)

    def Backward(self):
        robot = robo.Snatch3r()
        robot.drive_until_otherwise(-800, -800)


    def Right(self):
        robot = robo.Snatch3r()
        robot.drive_until_otherwise(-100,100)


    def Left(self):
        robot = robo.Snatch3r()
        robot.drive_until_otherwise(100,-100)


    def Brake(self):
        robot = robo.Snatch3r()
        robot.stop()


    def Mode(self, replace):
        if replace == "Follow":
            self.Following_Procedure()
        if replace == "Chase":
            self.Chasing_Procedure()
        if replace == "Manual":
            self.Manual_Procedure()
        if replace == "Guard":
            self.Guard_Procedure()
        if replace == "Distract":
            self.Distract_Procedure()

    def Following_Procedure(self):
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
        robot.stop()


    def Chasing_Procedure(self):
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
        robot.stop()


    def Manual_Procedure(self):
        print("Switching to non-autonomus mode.")


    def Guard_Procedure(self):
        robot = robo.Snatch3r()
        robot.pixy.mode = "SIG1"
        Holdsize = robot.pixy.value(3) * robot.pixy.value(4)
        timehold = 0
        while timehold < 10:
            if (Holdsize - (robot.pixy.value(3) * robot.pixy.value(4))) < -1:
                robot.beep()
            timehold += 0.05
            time.sleep(0.05)

    def Distract_Procedure(self):
        robot = robo.Snatch3r()
        robot.drive_until_otherwise(100,-100)
        robot.beep()
        time.sleep(10)
        robot.stop()


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    while my_delegate.running:
        time.sleep(0.01)

main()