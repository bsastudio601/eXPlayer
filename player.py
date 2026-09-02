import pygame
import threading
import time
import msvcrt 
import shutil
import os



#load the stuff






#global variables and stuff
global playing
playing = False
paused = False
song_name = "SONG NAME"
current_lyric = "♪ Lyrics ♪"
current_time = 0
total_time = 0
WIDTH = shutil.get_terminal_size().columns
last_width = WIDTH

os.system("cls")
pygame.mixer.init()

song_path = "music/Ravyn Lenae - Love Me Not.mp3"

pygame.mixer.music.load(song_path)
song_name = os.path.splitext(os.path.basename(song_path))[0]
song_length = pygame.mixer.Sound(song_path).get_length()

lyrics_path = os.path.splitext(song_path)[0] + ".lrc"


#the time converting function for song

def format_time(seconds):
    minutes = int(seconds //60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

total_time = format_time(song_length)



#lyrics converting stuff

Lyrics = []

if os.path.exists(lyrics_path):
    with open(lyrics_path, encoding="utf-8") as file:
        for line in file:
            time_stamp, lyric = line.strip().split("]", 1)
            time_stamp = time_stamp[1:]

            minutes, seconds = time_stamp.split(":")
            lyric_time = int(minutes) * 60 + float(seconds)

            Lyrics.append((lyric_time, lyric))
else:
    Lyrics = [(0, "♪ No lyrics found ♪")]



#drawing the ui 

print("\033[2J\033[H", end="")
def draw_ui():

    print(r"""
       ____  _____________.__
  ____ \   \/  /\______   \  | _____  ___.__. ___________
_/ __ \ \     /  |     ___/  | \__  \<   |  |/ __ \_  __ \
\  ___/ /     \  |    |   |  |__/ __ \\___  \  ___/|  | \/
 \___  >___/\  \ |____|   |____(____  / ____|\___  >__|
     \/      \_/                    \/\/         \/
""")

    print(song_name.center(WIDTH))
    print()

    print(current_lyric.center(WIDTH))
    print()

    print("progress_bar".center(WIDTH))
    print()

    print(f"{current_time} / {total_time}".center(WIDTH))
    print()

    print("[ P ] Play".center(WIDTH))
    print("[ SPACE ] Pause".center(WIDTH))
    print("[ R ] Resume".center(WIDTH))
    print("[ S ] Stop".center(WIDTH))
    print("[ Q ] Quit".center(WIDTH))
draw_ui()



#playing the lyrics

def lyrics_player():
    global playing
    global current_lyric, current_time, progress_bar
    global WIDTH

 
    last_lyric = ""

    while True:
        new_width = shutil.get_terminal_size().columns 
        
        if new_width != WIDTH:
                WIDTH = new_width
                os.system("cls")
                draw_ui()

            

        if playing:

            current_time = pygame.mixer.music.get_pos() / 1000

            progress = current_time / song_length
            filled = int(progress * 40)
            progress_bar = "[" + "=" * filled + ">" + "-" * (39 - filled) + "]"
            print(f"\033[13;1H\033[2K", end="")
            print(progress_bar.center(WIDTH), end="", flush=True)

            current_lyric = ""

            for lyric_time, lyric in Lyrics:
                if current_time >= lyric_time:
                    current_lyric = lyric
                else:
                    break
            if current_lyric != last_lyric:

                print(f"\033[11;1H\033[2K", end="")
                print(current_lyric.center(WIDTH), end="", flush=True)
                last_lyric = current_lyric

            show_time= format_time(current_time)
            print(f"\033[15;1H\033[2K", end="")
            print(f"{show_time} / {total_time}".center(WIDTH), end="", flush=True)
            time.sleep(0.1)

def command_win():
    os.system("cls")

    print("exPlayer Commands")
    print("-----------------")
    print('type "help" for available commands')
    print('type "back" to return to player')
    print()

    while True:
        commands = input('eXPlayer> ')
        if commands == "help":
            print("Available commands:")
            print("help - Show available commands")
            print("back - Return to the player")
            print("exit - Exit the program")
            print()
        elif commands == "back":
            os.system("cls")
            draw_ui()
            pygame.mixer.music.unpause()
            playing = True
            break
        else:
            print(f"Unknown command: {commands}")
            print('type "help" for available commands')
            print('type "back" to return to player')
            print()

# thread loading

thread = threading.Thread(target=lyrics_player,daemon=True)
thread.start()


# music control

while True:

    if msvcrt.kbhit():
        key = msvcrt.getwch()

        if key == "p":
            pygame.mixer.music.play()
            playing = True

        elif key == " ":
            pygame.mixer.music.pause()
            playing = False

        elif key == "r":
            pygame.mixer.music.unpause()
            playing = True

        elif key == "s":
            pygame.mixer.music.stop()
            playing = False
        
        elif key == "c":
            pygame.mixer.music.pause()
            playing = False
            command_win()
            

        elif key == "q":
            pygame.mixer.music.stop()
            break

    time.sleep(0.05)





        