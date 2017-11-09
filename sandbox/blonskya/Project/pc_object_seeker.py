import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk


class MyDelegate (object):
    def talk_back(self,message_from_ev3):
        print(message_from_ev3)


class Memory (object):
    def __init__(self):
        self.mode = "Follow"
        self.manual_speed=100
    def printself(self):
        print(self.mode,self.manual_speed)


def main():
    has_extra = False
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()
    root = tkinter.Tk()
    root.title("Tailer")
    hold_variable = Memory()
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    mode_label = ttk.Label(main_frame, text='Mode:')
    mode_label.grid(columnspan=5)
    Follow_mode = ttk.Button(main_frame, text="Follow")
    Follow_mode.grid(row=1, column=0)
    Follow_mode['command'] = lambda: mode(mqtt_client,hold_variable, "Follow")
    Chase_mode = ttk.Button(main_frame, text="Chase")
    Chase_mode.grid(row=1, column=1)
    Chase_mode['command'] = lambda: mode(mqtt_client,hold_variable, "Chase")
    Guard_mode = ttk.Button(main_frame, text="Guard")
    Guard_mode.grid(row=1, column=2)
    Guard_mode['command'] = lambda: mode(mqtt_client,hold_variable, "Guard")
    Manual_mode = ttk.Button(main_frame, text="Manual")
    Manual_mode.grid(row=1, column=3)
    Manual_mode['command'] = lambda: mode(mqtt_client,hold_variable, "Manual")
    Distract_mode = ttk.Button(main_frame, text="Distract")
    Distract_mode.grid(row=1, column=4)
    Distract_mode['command'] = lambda: mode(mqtt_client,hold_variable, "Distract")
    while True:
        if hold_variable.mode == "Manual":
            if not has_extra:
                manual_label = ttk.Label(main_frame, text='Controls:')
                manual_label.grid(columnspan=5)
                Forward = ttk.Button(main_frame, text="Forward")
                Forward.grid(row=3, column=2)
                Forward['command'] = lambda: send(mqtt_client, "Forward")
                Backward = ttk.Button(main_frame, text="Backward")
                Backward.grid(row=5, column=2)
                Backward['command'] = lambda: send(mqtt_client, "Backward")
                Left = ttk.Button(main_frame, text="Left")
                Left.grid(row=4, column=0)
                Left['command'] = lambda: send(mqtt_client, "Left")
                Right = ttk.Button(main_frame, text="Right")
                Right.grid(row=4, column=4)
                Right['command'] = lambda: send(mqtt_client, "Right")
                Brake = ttk.Button(main_frame, text="Brake")
                Brake.grid(row=4, column=2)
                Brake['command'] = lambda: send(mqtt_client, "Brake")
                has_extra = True
        root.update_idletasks()
        root.update()


def mode(mqtt_client,holder,new_mode):
    holder.mode = new_mode
    mqtt_client.send_message("Mode",[new_mode])


def send(mqtt_client, message):
    mqtt_client.send_message(message)

main()