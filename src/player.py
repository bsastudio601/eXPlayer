import pygame
import threading
import time
import msvcrt 
import shutil
import os
import random
import json


#global variables and stuff

global playing
playing = False
paused = False
song_name = "No Song Name found"
current_lyric = "♪ Lyrics ♪"
current_time = 0
total_time = 0
WIDTH = shutil.get_terminal_size().columns
last_width = WIDTH
songs = []
current_song_index = 0
song_length = 0
music_folder = "music"
selected_song = None
shuffle_mode = True

#config save and load function

def load_config():
    global music_folder,shuffle_mode
    if os.path.exists("config.json"):
        with open("config.json","r") as f:
            config = json.load(f)
        music_folder = config.get("music_folder","music")
        shuffle_mode = config.get("shuffle_mode",True)


def save_config():
    config = {
        "music_folder": music_folder,
        "shuffle_mode": shuffle_mode
    }
    with open("config.json","w") as f:
        json.dump(config, f, indent=4)


#the time converting function for song

def format_time(seconds):
    minutes = int(seconds //60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

total_time = format_time(song_length)


def load_songs(song_path):
    global song_name, song_length, total_time, lyrics_path, Lyrics
    pygame.mixer.music.load(song_path)

    song_name = os.path.splitext(os.path.basename(song_path))[0]
    song_length = pygame.mixer.Sound(song_path).get_length()

    total_time = format_time(song_length)

    lyrics_path = os.path.splitext(song_path)[0] + ".lrc"


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


def select_song(song_path):
    global selected_song

    load_songs(song_path)
    selected_song = song_path


def select_first_song():
    global selected_song, current_song_index, playing

    songs = get_songs()
    if not songs:
        return
    current_song_index = 0
    selected_song = songs[0]
    load_songs(selected_song)
    pygame.mixer.music.play()
    playing = True

    print(f"\033[9;1H\033[2K", end="")
    print(song_name.center(WIDTH), end="", flush=True)


def play_next_shuffle():
    global selected_song,current_song_index

    songs = get_songs()

    if not songs:
        return

    current_song_index = random.randrange(len(songs))
    selected_song = songs[current_song_index]

    load_songs(selected_song)
    pygame.mixer.music.play()

    print(f"\033[9;1H\033[2K", end="")
    print(song_name.center(WIDTH), end="", flush=True)


def play_next():
    global selected_song, current_song_index,playing

    songs = get_songs()
    if not songs:
        return
    current_song_index += 1

    if current_song_index >= len(songs):
        current_song_index = 0

    selected_song = songs[current_song_index]
    load_songs(selected_song)
    pygame.mixer.music.play()
    time.sleep(0.1)

    playing = True

    print(f"\033[9;1H\033[2K", end="")
    print(song_name.center(WIDTH), end="", flush=True)


def play_previous():
    global selected_song, current_song_index, playing

    songs = get_songs()
    if not songs:
        return
    current_song_index -= 1

    if current_song_index <0:
        current_song_index = len(songs) -1
        
    selected_song = songs[current_song_index]
    load_songs(selected_song)
    pygame.mixer.music.play()
    time.sleep(0.1)

    playing = True

    print(f"\033[9;1H\033[2K", end="")
    print(song_name.center(WIDTH), end="", flush=True)


def list_folder():
    if not os.path.exists(music_folder):
        print("Music folder not found. Please select a folder with mp3 files")
        return
    print("Available songs:")
    print(f"Contents of: {music_folder}")

    files = os.listdir(music_folder)

    for file in files:
        print(file)
    print()


def get_songs():
    if not os.path.isdir(music_folder):
        return []
    return [os.path.join(music_folder,file)
            for file in os.listdir(music_folder)
            if file.lower().endswith(".mp3")
            ]


#drawing the ui 


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

    print("[ P ] Play             [ O ] Pause".center(WIDTH))
    print("[ B ] Previous         [ N ] Next ".center(WIDTH))
    print("[ R ] Resume           [ Q ] Quit".center(WIDTH))
    print("[ C ] Settings and Modes".center(WIDTH))



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

            
        if playing and not pygame.mixer.music.get_busy():
            if shuffle_mode:
                play_next_shuffle()
            else:
                playing = False

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
    global playing,music_folder,songs,current_song_index,shuffle_mode,command_mode,selected_song
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
            print("help                - Show available commands")
            print("about               - info about eXplayer and how to use it")
            print("back                - Return to the player")
            print('cd "[path]"         - Select the music folder')
            print('ls                  - show available files in the folder')
            print('select "[song name]"- select individual song to play')
            print('shuffle             - toggle shuffle on and off (normally on)')
            print()

        elif commands == "about":
            print("eXPlayer")
            print("made by Aritro Halder")
            print("version: 1.0.0")
            print("=====================")
            print()
            print("How to Play Music")
            print("=====================")
            print("To play song you first have to change the directory using command 'cd' to the folder containing your musics. " \
            "then go back to the player using command 'back' and you can play musics by pressing [ P ] on your keyboard")
            print()
            print("How to add lyrics")
            print("=====================")
            print("To add lyrics to a song. first create a '.lrc' file and copy and paste the lyrics with timestamps in the lrc file. " \
            "rename the file with the same name as your song or '.mp3' and save the both file in the same folder." \
            "the player will automatically find the lyrics file")
            print()
            print("Additional Info")
            print("=====================")
            print("The player saves your seleted file path in a config.json file.when shuffle is on, pressing N or B to select previous and next song will play next song randomly")
            print("")
            print("leave feedback in my insta @arthi_bsa_studio or leave an email in: studiozzzz033@gmail.com")

        elif commands == "back":
            command_mode = False
            os.system("cls")
            draw_ui()
            break

        elif commands.startswith("cd "):
            folder = commands[3:].strip('"')

            if os.path.isdir(folder):
                music_folder = os.path.abspath(folder)
                save_config()
                selected_song = None
                current_song_index = 0
                
                print()
                print(f"Music folder changed to: {music_folder}")

            else:
                print("Directory not found")

        elif commands == "ls":
            list_folder()

        elif commands == "shuffle":
            shuffle_mode = not shuffle_mode
            save_config()

            if shuffle_mode:
                print()
                print("Shuffle mode: ON")
                print()
            else:
                print()
                print("Shuffle mode: OFF")
                print()            


        elif commands.startswith("select "):
            song = commands[7:].strip('"')
            song_path = os.path.join(music_folder, song)

            if os.path.isfile(song_path) and song.lower().endswith(".mp3"):

                songs = get_songs()

                if song_path in songs:
                    current_song_index = songs.index(song_path)

                select_song(song_path)

                print()
                print(f"Selected: {song_name}")
                print()

            else:
                print()
                print("Song not found")
                print()
                
        else:
            print(f"Unknown command: {commands}")
            print('type "help" for available commands')
            print('type "back" to return to player')
            print()


# thread loading

def main ():
    os.system("cls")
    pygame.mixer.init()

    load_config()

    print("\033[2J\033[H", end="")
    draw_ui()


    thread = threading.Thread(target=lyrics_player,daemon=True)
    thread.start()


    # music control

    while True:

        if msvcrt.kbhit():
            key = msvcrt.getwch()

            if key == "p":
                if selected_song:
                    pygame.mixer.music.play()
                    playing = True
                elif shuffle_mode:
                    play_next_shuffle()
                    playing = True
                else:
                    select_first_song()
                    playing = True

            elif key == "o":
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

            elif key == "n":
                play_next()
                
            elif key == "b":
                play_previous()    

            elif key == "q":
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                os.system("cls")
                break

        time.sleep(0.05)

if __name__ == "__main__":
    main()





        