import pygame
import threading
import time
import msvcrt 
import shutil

pygame.mixer.init()

pygame.mixer.music.load("music/song.mp3")

playing = False
paused = False
current_lyric = ""

WIDTH = shutil.get_terminal_size().columns

def lyrics_player():

    Lyrics = []

    with open("lyrics/song.lrc", encoding="utf-8") as file:
        for line in file:
            time_stamp, lyric = line.strip().split("]", 1)
            time_stamp = time_stamp[1:]

            minutes, seconds = time_stamp.split(":")
            lyric_time = int(minutes) * 60 + float(seconds)

            Lyrics.append((lyric_time, lyric))

    last_lyric = ""

    while True:
        if playing:

            current_time = pygame.mixer.music.get_pos() / 1000

            current_lyric = ""


            for lyric_time, lyric in Lyrics:
                if current_time >= lyric_time:
                    current_lyric = lyric
                else:
                    break
            if current_lyric != last_lyric:

                print("\033[11;1H\033[2K", end="")
                print(f"♪ {current_lyric} ♪".center(WIDTH))

                last_lyric = current_lyric
            time.sleep(0.1)
        
thread = threading.Thread(target=lyrics_player)
thread.start()
def draw_ui():
    print(r"""
       ____  _____________.__                              
  ____ \   \/  /\______   \  | _____  ___.__. ___________  current_lyric
_/ __ \ \     /  |     ___/  | \__  \<   |  |/ __ \_  __ \ 
\  ___/ /     \  |    |   |  |__/ __ \\___  \  ___/|  | \/ 
 \___  >___/\  \ |____|   |____(____  / ____|\___  >__|    
     \/      \_/                    \/\/         \/        
""")

    print()
    print("                 LEVEL FIVE - TUMI")
    print()
    print()
    print("              [===================>-----]")
    print("                    01:24 / 03:42")
    print()
    print("              [ P ] Play")
    print("              [ SPACE ] Pause")
    print("              [ R ] Resume")
    print("              [ S ] Stop")
    print("              [ Q ] Quit")
    
draw_ui()

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

        elif key == "q":
            pygame.mixer.music.stop()
            break

    time.sleep(0.05)



        