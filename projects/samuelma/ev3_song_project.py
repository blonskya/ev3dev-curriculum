# drive for a certain number of keys
# keys should be 1 inch long


import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo


c4 = 261.6
d4 = 293.7
e4 = 329.6
f4 = 349.2
g4 = 391.9
a4 = 440.0
b4 = 493.9


# DONE: Create the Notes Class
class Notes(object):

    def __init__(self, name, frequency, rgb):
        self.note = name
        self.color = rgb
        self.red = rgb[0]
        self.blue = rgb[2]
        self.green = rgb[1]
        self.note_freq = frequency


class SongMaster(object):

    def __init__(self):
        self.mqtt_client = None
        self.running = True
        self.note_list = [" ", "C", "D", "E", "F", "G", "A", "B"]
        self.frequency_list = [0, 262, 294, 330, 349, 392, 440, 494]
        self.notes = []
        self.song_freq = []


    def loop_forever(self):
        btn = ev3.Button()
        self.running = True
        while not btn.backspace and self.running:
            time.sleep(0.01)
        self.mqtt_client.close()
        # Copied from robot.shutdown

    # DONE: Set Color Function
    # drives 1 inch squares to set the light value of black, white, red(C), orange(D), yellow(E),
    # green(F), blue(G), purple(A), pink(B)
    def set_colors(self):
        self.notes = []
        for k in range(8):
            rgb = [ev3.ColorSensor().red, ev3.ColorSensor().green, ev3.ColorSensor().blue]
            self.notes += [Notes(self.note_list[k], self.frequency_list[k], rgb)]
            print(self.notes[k].color)
            robo.Snatch3r().drive_inches(0.99, 100)

    # DONE: Record Function
    # everytime the sensor sees black the new key should start
    # should play the notes as seen and should make a list of the notes called song
    # should display the note being played on the screen
    # once done sends the song to the pc to be displayed
    def record_song(self, record_speed, num_keys):
        self.song_freq = []
        song_str = ""
        for _ in range(num_keys):
            found = False
            k = 0
            while (k < 8) and (found == False):
                note = self.notes[k]
                print(note.note, end=" ")
                if abs(note.red - ev3.ColorSensor().red) <= 15:
                    print("{} - {} = {},".format(note.red, ev3.ColorSensor().red, note.red-ev3.ColorSensor().red), end=" ")
                    if abs(note.green - ev3.ColorSensor().green) <= 15:
                        print(
                            "{} - {} = {},".format(note.green, ev3.ColorSensor().green, note.green - ev3.ColorSensor().green),
                            end=" ")
                        if abs(note.blue - ev3.ColorSensor().blue) <= 15:
                            print("{} - {} = {},".format(
                                note.blue, ev3.ColorSensor().blue, note.blue - ev3.ColorSensor().blue), end=" ")
                            ev3.Sound.tone(note.note_freq, 100000/record_speed)
                            song_str += note.note
                            self.song_freq += [note.note_freq]
                            robo.Snatch3r().drive_inches(0.93, record_speed)
                            found = True
                        else:
                            print("Fail", note.blue, ev3.ColorSensor().blue)
                    else:
                        print("Fail", note.green, ev3.ColorSensor().green)
                else:
                    print("Fail", note.red, ev3.ColorSensor().red)
                k += 1
                print()
        robo.Snatch3r().stop()
        self.mqtt_client.send_message("set_song_string", [song_str])

    # DONE: Playback command
    # plays song at received note length and delay between notes
    # should display the note being played on the screen
    def play_song(self, note_len, delay_len):
        song = []
        for k in range(len(self.song_freq)):
            song += [(self.song_freq[k], note_len, delay_len)]
        print(song)
        ev3.Sound.tone(song).wait()

    def exit(self):
        self.running = False


def main():
    print("Ready")
    my_delegate = SongMaster()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    my_delegate.loop_forever()


main()