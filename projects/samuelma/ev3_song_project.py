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


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()


class MyDelegate(object):

    def __init__(self):
        self.running = True

    # TODO: Set Color Function
    # drives 1 inch squares to set the light value of black, white, red(C), orange(D), yellow(E), green(F), blue(G), purple(A), pink(B)
    def set_color(self):
        robot = robo.Snatch3r()
        note_list =  ["C", "D", "E", "F", "G", "A", "B"]
        frequency_list = [261.6, 293.7, 329.6, 349.2, 391.9, 440.0, 493.9]
        global notes
        notes = []
        global bw
        bw = {}
        for k in range(9):
            rgb = [ev3.ColorSensor.red, ev3.ColorSensor.green, ev3.ColorSensor.blue]
            if k == 0:
                bw["black"] = ev3.ColorSensor.reflected_light_intensity
            elif k == 1:
                bw["white"] = ev3.ColorSensor.reflected_light_intensity
            else:
                notes[k] = Notes(note_list[k], frequency_list[k], rgb)
            robot.drive_inches(1, 300)
    #notes = [black, white, red(C), orange(D), yellow(E), green(F), blue(G), purple(A), pink(B)]


    # TODO: Record Function
    # everytime the sensor sees black the new key should start
    # should play the notes as seen and should make a list of the notes called song
    # should display the note being played on the screen
    # once done sends the song to the pc to be displayed
    def record_song(record_speed, num_keys):
        global song
        song = []
        next_note = ""
        started = 0
        while not len(song) == num_keys:
            if abs(ev3.ColorSensor.reflected_light_intensity - bw["black"]) <= 5:
                if started != 0:
                    song += [next_note]
            else:
                for k in range(7):
                    note = notes[k]
                    if (abs(note.color.red - ev3.ColorSensor().red) <=5 & abs(note.color.green - ev3.ColorSensor().green) <=5 & abs(note.color.blue - ev3.ColorSensor().blue) <=5):
                        ev3.Sound.tone(note.note_freq)
                        next_note = note.note
                started = 1



    # TODO: Playback command
    # plays song at received note length and delay between notes
    # should display the note being played on the screen
    def play_song(self, note_len, delay_len):
        song = []
        for k in range(len(self.note_freq)):
            song += [(self.song_freq[k], note_len, delay_len)]
        ev3.Sound.tone(song).wait()


# TODO: Create the Notes Class
class Notes(object):

    def __init__(self, name, frequency, rgb):
        self.note = name
        self.color = rgb
        self.color.red = self.color[0]
        self.color.blue = self.color[1]
        self.color.green = self.color[2]
        self.note_freq = frequency





main()