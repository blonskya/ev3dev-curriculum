# Displays the tkinter with which to interact

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Robo Song")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    line_break_0 = ttk.Label(main_frame, text="- - - - - - - - - - - -")
    line_break_0.grid(row=1, column=1, columnspan=3)
    line_break_1 = ttk.Label(main_frame, text="- - - - - - - - - - - -")
    line_break_1.grid(row=5, column=1, columnspan=3)

    song_freqs = []

    # Calls the set colors function
    # TODO: Tkinter Part One
    set_colors_button = ttk.Button(main_frame, text="Set Color Values")
    set_colors_button.grid(row=0, column=1, columnspan=3)
    set_colors_button['command'] = lambda: set_colors(mqtt_client)
    root.bind('<Up>', lambda event: set_colors(mqtt_client))

    # Calls the Record Song function
    # TODO: Tkinter Part Two
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
    record_song_button['command'] = lambda: record_song(mqtt_client, int(record_speed_entry.get()), int(record_keys_entry.get()))
    root.bind('<Right>', lambda event: record_song(mqtt_client, int(record_speed_entry.get()), int(record_keys_entry.get())))

    # Calls the Playback function
    # TODO: Tkinter Part Three
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
    play_song_button['command'] = lambda: play_song(mqtt_client, song_freqs, int(note_length_entry.get()), int(note_delay_entry.get()))
    root.bind('<Right>', lambda event: play_song(mqtt_client, song_freqs, int(note_length_entry.get()), int(note_delay_entry.get())))

    # Displays the song
    # TODO: Display song on Tkinter
    song_display = ttk.Label(main_frame, text="Song: _________________")
    song_display.grid(row=9, column=0, columnspan=5)

    root.mainloop()

# set up the call functions
# TODO: call Functions
def set_colors(mqtt_client):
    # run through the colors setting the reflective value...
    print("set_colors")
    mqtt_client.send_message("set_colors")

def record_song(mqtt_client, record_speed, num_keys):
    # calls the record function in ev3
    print("record_song")
    mqtt_client.send_message("record_song", [record_speed, num_keys])


def play_song(mqtt_client, note_length, delay_length):
    # calls the play song function in ev3
    print("play_song")
    mqtt_client.send_message("play_song", [note_length, delay_length])

main()