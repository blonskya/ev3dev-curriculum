"""
Author: Mary Ashley Samuelson
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time

import robot_controller as robo

def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Robo Song")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    set_colors_button = ttk.Button(main_frame, text="Set Color Values")
    set_colors_button.grid(row=0, column=1, columnspan=3)
    #set_colors_button['command'] = lambda: set_colors(mqtt_client)
    #root.bind('<Up>', lambda event: set_colors(mqtt_client))

    line_break_0 = ttk.Label(main_frame, text="- - - - - - - - - - - -")
    line_break_0.grid(row=1, column=1, columnspan=3)
    line_break_1 = ttk.Label(main_frame, text="- - - - - - - - - - - -")
    line_break_1.grid(row=5, column=1, columnspan=3)

    record_speed = ttk.Label(main_frame, text="Recording Speed")
    record_speed.grid(row=2, column=1, columnspan=2)
    record_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.CENTER)
    record_speed_entry.insert(0, "600")
    record_speed_entry.grid(row=2, column=3)

    record_keys_1 = ttk.Label(main_frame, text="Record", justify=tkinter.RIGHT)
    record_keys_1.grid(row=3, column=1)
    record_keys_entry = ttk.Entry(main_frame, width=4, justify=tkinter.CENTER)
    record_keys_entry.insert(0, "8")
    record_keys_entry.grid(row=3, column=2)
    record_keys_2 = ttk.Label(main_frame, text="Notes", justify=tkinter.LEFT)
    record_keys_2.grid(row=3, column=3)

    record_song_button = ttk.Button(main_frame, text="Record!")
    record_song_button.grid(row=4, column=1, columnspan=3)
    #record_song_button['command'] = lambda: record_song(mqtt_client)
    #root.bind('<Right>', lambda event: record_song(mqtt_client))

    note_length = ttk.Label(main_frame, text="Note Length")
    note_length.grid(row=6, column=1)
    note_length_entry = ttk.Entry(main_frame, width=8, justify=tkinter.CENTER)
    note_length_entry.insert(0, "600")
    note_length_entry.grid(row=7, column=1)

    note_delay = ttk.Label(main_frame, text="Note Delay")
    note_delay.grid(row=6, column=3)
    note_delay_entry = ttk.Entry(main_frame, width=8, justify=tkinter.CENTER)
    note_delay_entry.insert(0, "600")
    note_delay_entry.grid(row=7, column=3)

    play_song_button = ttk.Button(main_frame, text="Play Back")
    play_song_button.grid(row=8, column=1, columnspan=3)
    #play_song_button['command'] = lambda: play_song(mqtt_client)
    #root.bind('<Right>', lambda event: play_song(mqtt_client))

    song_display = ttk.Label(main_frame, text="Song: _________________")
    song_display.grid(row=9, column=0, columnspan=5)

    root.mainloop()


class songs():
    c4 = 261.6
    d4 = 293.7
    e4 = 329.6
    f4 = 349.2
    g4 = 391.9
    a4 = 440.0
    b4 = 493.9

    def __init__(self, song):
        self.song_key = song
        self.song_freq = []
        for k in range(len(song)):
            self.song_freq += [eval(song[k])]

    def play_song(self, note_len, delay_len):
        song = []
        for k in range(len(self.song_freq)):
            song += [(self.song_freq[k], note_len, delay_len)]
        ev3.Sound.tone(song).wait()

#def set_colors(mqtt_client):
    # run through the colors setting the reflective value...

#def record_song(mqtt_client):
    # run through the colors setting the reflective value...

main()