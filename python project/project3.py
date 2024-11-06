import os
import json
import time
import threading
from tkinter import *
from tkinter import filedialog, messagebox
import tkinter.font as font
from mutagen.mp3 import MP3
from pygame import mixer
from PIL import Image, ImageTk
import random

# Initialize mixer
mixer.init()
current_song_index = None
all_songs = []
is_shuffle = False
is_repeat = False

def addsongs():
    temp_song = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    for s in temp_song:
        s = os.path.basename(s)
        if s not in all_songs:
            songs_list.insert(END, s)
            all_songs.append(s)

def deletesong():
    curr_song = songs_list.curselection()
    if curr_song:
        all_songs.remove(songs_list.get(curr_song))
        songs_list.delete(curr_song[0])

def Play():
    global current_song_index
    if songs_list.curselection():
        current_song_index = songs_list.curselection()[0]
        play_song(current_song_index)

def Pause():
    mixer.music.pause()

def Stop():
    mixer.music.stop()
    songs_list.selection_clear(ACTIVE)

def Resume():
    mixer.music.unpause()

def Previous():
    global current_song_index
    if current_song_index is not None:
        current_song_index = (current_song_index - 1) % songs_list.size()
        play_song(current_song_index)

def Next():
    global current_song_index
    if is_shuffle:
        current_song_index = random.randint(0, songs_list.size() - 1)
    else:
        current_song_index = (current_song_index + 1) % songs_list.size()
    play_song(current_song_index)

def play_song(index):
    global current_song_index
    song = songs_list.get(index)
    song_path = os.path.join(r"C:\Users\welcome.DESKTOP-UD20VQ4\Desktop\python\python project\song", song)  # Adjust this path accordingly

    background_path = r"C:\Users\welcome.DESKTOP-UD20VQ4\Desktop\python\python project\download.jpg"
    
    if os.path.exists(background_path):
        bg_image = Image.open(background_path)
        bg_image = bg_image.resize((1500, 800), Image.LANCZOS)
        bg_img = ImageTk.PhotoImage(bg_image)
        background_label.config(image=bg_img)
        background_label.image = bg_img

    if os.path.exists(song_path):
        mixer.music.load(song_path)
        mixer.music.play()
        update_current_track(song)
        update_duration(song_path)
        show_album_art(song_path)
        update_background_image(song_path)
    else:
        messagebox.showerror("Error", f"File not found: {song_path}")

def update_current_track(song):
    current_track_label.config(text=f"Playing: {song}")

def update_duration(song_path):
    if song_path and os.path.exists(song_path):
        audio = MP3(song_path)
        total_length = audio.info.length
        total_duration_label.config(text=f"{int(total_length // 60):02}:{int(total_length % 60):02}")
        root.after(1000, update_current_time, total_length)

def update_current_time(total_length):
    if mixer.music.get_busy():
        current_position = mixer.music.get_pos() / 1000
        current_time_label.config(text=f"{int(current_position // 60):02}:{int(current_position % 60):02}")
        track_progress.set(current_position / total_length * 100)
        if current_position < total_length:
            root.after(1000, update_current_time, total_length)
        else:
            Stop()
            if not is_repeat:
                show_end_message()

def show_end_message():
    messagebox.showinfo("Song Ended", "The song has finished playing.")

def show_album_art(song_path):
    album_art_path = os.path.splitext(song_path)[0] + ".jpg"
    if os.path.exists(album_art_path):
        image = Image.open(album_art_path)
        image = image.resize((1500, 800), Image.LANCZOS)
        img = ImageTk.PhotoImage(image)
        album_art_label.config(image=img)
        album_art_label.image = img
    else:
        album_art_label.config(image='')

def update_background_image(song_path):
    bg_image_path = os.path.splitext(song_path)[0] + ".jpg"
    if os.path.exists(bg_image_path):
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((1500, 800), Image.LANCZOS)
        bg_img = ImageTk.PhotoImage(bg_image)
        background_label.config(image=bg_img)
        background_label.image = bg_img

def set_volume(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)
    volume_label.config(text=f"Volume: {val}")

def search_songs():
    search_term = search_entry.get().lower()
    songs_list.delete(0, END)
    for song in all_songs:
        if search_term in song.lower():
            songs_list.insert(END, song)

def save_playlist():
    with open('playlist.json', 'w') as f:
        json.dump(all_songs, f)

def load_playlist():
    if os.path.exists('playlist.json'):
        with open('playlist.json', 'r') as f:
            songs = json.load(f)
            songs_list.delete(0, END)
            all_songs.clear()
            for song in songs:
                songs_list.insert(END, song)
                all_songs.append(song)

def toggle_shuffle():
    global is_shuffle
    is_shuffle = not is_shuffle
    shuffle_button.config(bg="#FFCC00" if is_shuffle else "#007ACC")

def toggle_repeat():
    global is_repeat
    is_repeat = not is_repeat
    repeat_button.config(bg="#FFCC00" if is_repeat else "#007ACC")

# Create the main window
root = Tk()
root.title('Stylish Music Player')
root.geometry('600x450')
root.configure(bg='#2E2E2E')

# Load default background image
background_path = r"C:\Users\welcome.DESKTOP-UD20VQ4\Desktop\python\python project\download.jpg"
if os.path.exists(background_path):
    bg_image = Image.open(background_path)
    bg_image = bg_image.resize((1500, 800), Image.LANCZOS)
    bg_img = ImageTk.PhotoImage(bg_image)
    background_label = Label(root, image=bg_img)
    background_label.place(relwidth=1, relheight=1)

# Create the song list box
songs_list = Listbox(root, selectmode=SINGLE, bg="#1E1E1E", fg="white", font=('Arial', 12), height=15, width=60, selectbackground="#007ACC", selectforeground="black")
songs_list.grid(columnspan=6, pady=20)

# Create a label to display the current track
current_track_label = Label(root, text="Playing: None", bg='#2E2E2E', fg='white', font=('Arial', 12))
current_track_label.grid(row=2, columnspan=6)

# Current time label
current_time_label = Label(root, text="00:00", bg='#2E2E2E', fg='white', font=('Arial', 12))
current_time_label.grid(row=3, column=0)

# Total duration label
total_duration_label = Label(root, text="00:00", bg='#2E2E2E', fg='white', font=('Arial', 12))
total_duration_label.grid(row=3, column=1)

# Album art label
album_art_label = Label(root, bg='#2E2E2E')
album_art_label.grid(row=3, column=2, padx=10)

# Track progress bar
track_progress = Scale(root, from_=0, to=100, orient=HORIZONTAL, bg='#2E2E2E', fg='white', sliderlength=20, state=DISABLED)
track_progress.grid(row=4, column=0, columnspan=6, pady=5)

# Define a custom font for buttons
button_font = font.Font(family='Helvetica', size=10, weight='bold')

# Create buttons with styling
play_button = Button(root, text="Play", width=8, command=Play, bg="#007ACC", fg="white", font=button_font)
play_button.grid(row=1, column=0, padx=5)

pause_button = Button(root, text="Pause", width=8, command=Pause, bg="#007ACC", fg="white", font=button_font)
pause_button.grid(row=1, column=1, padx=5)

stop_button = Button(root, text="Stop", width=8, command=Stop, bg="#007ACC", fg="white", font=button_font)
stop_button.grid(row=1, column=2, padx=5)

resume_button = Button(root, text="Resume", width=8, command=Resume, bg="#007ACC", fg="white", font=button_font)
resume_button.grid(row=1, column=3, padx=5)

previous_button = Button(root, text="Prev", width=8, command=Previous, bg="#007ACC", fg="white", font=button_font)
previous_button.grid(row=1, column=4, padx=5)

next_button = Button(root, text="Next", width=8, command=Next, bg="#007ACC", fg="white", font=button_font)
next_button.grid(row=1, column=5, padx=5)

# Shuffle and Repeat Buttons
shuffle_button = Button(root, text="Shuffle", command=toggle_shuffle, bg="#007ACC", fg="white", font=button_font)
shuffle_button.grid(row=1, column=6, padx=5)

repeat_button = Button(root, text="Repeat", command=toggle_repeat, bg="#007ACC", fg="white", font=button_font)
repeat_button.grid(row=1, column=7, padx=5)

# Volume Control
volume_label = Label(root, text="Volume: 100", bg='#2E2E2E', fg='white', font=('Arial', 12))
volume_label.grid(row=5, column=0)

volume_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, bg='#2E2E2E', fg='white', command=set_volume)
volume_slider.set(100)  # Set initial volume
volume_slider.grid(row=5, column=1, columnspan=6)

# Search functionality
search_label = Label(root, text="Search:", bg='#2E2E2E', fg='white', font=('Arial', 12))
search_label.grid(row=6, column=0)

search_entry = Entry(root, bg="#1E1E1E", fg="white", font=('Arial', 12))
search_entry.grid(row=6, column=1, columnspan=4)

search_button = Button(root, text="Search", command=search_songs, bg="#007ACC", fg="white", font=button_font)
search_button.grid(row=6, column=5)

# Load and Save Playlist Buttons
load_button = Button(root, text="Load Playlist", command=load_playlist, bg="#007ACC", fg="white", font=button_font)
load_button.grid(row=7, column=0)

save_button = Button(root, text="Save Playlist", command=save_playlist, bg="#007ACC", fg="white", font=button_font)
save_button.grid(row=7, column=1)

# Run the application
root.mainloop()

#rajan music player  