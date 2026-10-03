# eXPlayer

**Platform:** eXPlayer currently supports **Windows only**.

eXPlayer is a terminal based music player with lyrics support. The player includes a command window to change settings and other functions!

# Installing

## runing the exe release [ recommended to use this ]


you have to download the latest explayer.exe from the release and double click on it to run it. 
It required python 3.11 or later.

## running the pip package [ Only python 3.11.9 it is a bit broken for now ]

```bash
pip install explayer 
```
to install eXPlayer. You need to have python 3.11 install and run it ! 

if you have explayer already installed or want to update run this 

```bash
pip install explayer -U
```

# How to use it? 
After using the command to install it simply run

```bash
explayer
```

it will open the player window, now you need to set the directory or music folder. press [c] on your keyboard to open the command window from there you can set the music folder using command:

```bash
cd "[music folder path]"
```
## YOU HAVE TO USE "" ORTHERWISE IT WON'T WORK.

and head back to the player with
```bash
back
```
And now just simply press [p] to play the songs in shuffle!

run the command
```bash
help
```
to learn about more commands!

# Debugging 
one issue might occur if you have an old config.json file
in this case delete the config.json from: 

```bash
%LOCALAPPDATA%\eXPlayer
```
and rerun the program

# Screenshot and videos

![pic of the player runnin gin terminal](assets/player.png) 
![pic of the command window running 'help' command](assets/commands.png)
![gif of it showing it working](assets/show.gif)

# Usage of AI in thi project
Just Gpt is used in this project mainly to fix bugs. Though i did not fully copy gpts code i did write the snippets it gave me. It was used in making the lyrics function, config.json saving and loading function, playing next and previous song function, shuffle function, centering the logo. Other places i use it to help me fix bugs like 2 songs skipping at once when pressed next, not setted directory crashing the player.

# Conclusion 
hey its my first time creating project in python its really comfortable. making package was something new for me too!



