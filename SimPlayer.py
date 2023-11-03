import tkinter as tk
import pygame
from tkinter import Scale
from tkinter import filedialog
from tkinter import messagebox
import os
import json
import pathlib

version = 1.0

class SimPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title(f"SimPlayer v{version}")
        self.playing = False
        self.paused = False
        self.playlist = []
        self.current_track_index = 0
        self.audio_file = ""
        self.current_time = 0
        self.volume = 0.5  # Initial volume level

        button_width = 12  # Set a fixed width for the buttons
        button_height = 2  # Set a fixed height for the buttons

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_audio, width=button_width, height=button_height, bg="#212121", fg="#ffffff")
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_audio, width=button_width, height=button_height, bg="#212121", fg="#ffffff")
        self.skip_forward_button = tk.Button(root, text="Skip Forward", command=self.skip_forward, width=button_width, height=button_height, bg="#212121", fg="#ffffff")
        self.skip_backward_button = tk.Button(root, text="Skip Backward", command=self.skip_backward, width=button_width, height=button_height, bg="#212121", fg="#ffffff")
        self.replay_button = tk.Button(root, text="Replay", command=self.replay, width=button_width, height=button_height, bg="#212121", fg="#ffffff")
        self.add_to_playlist_button = tk.Button(root, text="Add to Playlist", command=self.add_to_playlist, width=button_width, height=button_height, bg="#212121", fg="#ffffff")

        self.audio_label = tk.Label(root, text="Not playing", bg="#212121", fg="#ffffff")
        self.volume_label = tk.Label(root, text="Volume:", bg="#212121", fg="#ffffff")

        self.volume_slider = Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", command=self.update_volume, bg="#212121", fg="#ffffff")
        self.playlist_label = tk.Label(root, text="Playlist:", bg="#212121", fg="#ffffff")

        self.playlistbox = tk.Listbox(root, selectmode=tk.SINGLE, width=40, height=10, bg="#212121", fg="#ffffff", selectbackground="black")  # Adjust the width and height

        self.pause_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.skip_backward_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.skip_forward_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.replay_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.add_to_playlist_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.audio_label.grid(row=3, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.volume_label.grid(row=4, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.volume_slider.grid(row=5, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.playlist_label.grid(row=6, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.playlistbox.grid(row=7, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.playlistbox.bind("<<ListboxSelect>>", self.playlist_select)  # Bind selection event

        # Load the playlist from a configuration file
        self.load_playlist_from_config()

    def play_audio(self, track_index=None):
        if track_index is not None:
            self.current_track_index = track_index
        if self.playlist:
            if not self.playing:
                pygame.init()
                pygame.mixer.init()
                current_track = self.playlist[self.current_track_index]
                pygame.mixer.music.load(current_track)
                self.volume_slider.set(self.volume)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(start=self.current_time)
                self.playing = True
                self.paused = False
                self.audio_label.config(text="Now playing: " + os.path.basename(current_track))  # Update the label
                self.update_label()  # Start monitoring when audio finishes
        else:
            messagebox.showerror("SimPlayer", "The playlist is empty. Add music to the playlist.")

    # Add a method to check if music is playing and update the label accordingly
    def update_label(self):
        if self.playing:
            if pygame.mixer.music.get_busy() == 0:  # Check if music has finished
                self.audio_label.config(text="Not playing")
            else:
                self.root.after(1000, self.update_label)  # Check again in 1 second

    def pause_audio(self):
        if self.playing:
            if not self.paused:
                pygame.mixer.music.pause()
                self.paused = True
            else:
                pygame.mixer.music.unpause()
                self.paused = False
        else:
            if self.playlist:  # Check if there are musics in the playlist
                messagebox.showerror("SimPlayer", "Please click on a music to play")
            else:
                messagebox.showerror("SimPlayer", "No musics in the playlist")

    def stop_audio(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False
            self.current_time = 0
            self.audio_label.config(text="Not playing")  # Update the label
        else:
            if self.playlist:  # Check if there are musics in the playlist
                messagebox.showerror("SimPlayer", "Please click on a music to play")
            else:
                messagebox.showerror("SimPlayer", "No musics in the playlist")

    def skip_forward(self):
        if self.playing:
            self.current_time += 10  # Skip 10 seconds
            pygame.mixer.music.set_pos(self.current_time)
        else:
            if self.playlist:  # Check if there are musics in the playlist
                messagebox.showerror("SimPlayer", "Please click on a music to play")
            else:
                messagebox.showerror("SimPlayer", "No musics in the playlist")

    def skip_backward(self):
        if self.playing:
            self.current_time -= 10  # Go back 10 seconds
            if self.current_time < 0:
                self.current_time = 0
            pygame.mixer.music.set_pos(self.current_time)
        else:
            if self.playlist:  # Check if there are musics in the playlist
                messagebox.showerror("SimPlayer", "Please click on a music to play")
            else:
                messagebox.showerror("SimPlayer", "No musics in the playlist")

    def replay(self):
        if self.playlist:
            current_track = self.playlist[self.current_track_index]
            pygame.mixer.music.load(current_track)
            self.volume_slider.set(self.volume)
            pygame.mixer.music.set_volume(self.volume)
            self.current_time = 0
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
            self.audio_label.config(text="Now playing: " + os.path.basename(current_track))
            self.update_label()  # Start monitoring when audio finishes
        else:
            messagebox.showerror("SimPlayer", "No musics in the playlist")

    def add_to_playlist(self):
        audio_files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac *.m4a *.wma")])
        if audio_files:
            for audio_file in audio_files:
                if os.path.exists(audio_file):
                    song_title = os.path.basename(audio_file)
                    self.playlist.append(audio_file)
                    self.playlistbox.insert(tk.END, song_title)

                    # Save the updated playlist to the configuration file
                    self.save_playlist_to_config()
                else:
                    messagebox.showerror("SimPlayer", "File does not exist: " + audio_file)

    def update_volume(self, value):
        self.volume = float(value)
        if self.playing:
            pygame.mixer.music.set_volume(self.volume)

    def playlist_select(self, event):
        selected_index = self.playlistbox.curselection()
        if selected_index:
            if self.playing:
                self.stop_audio()
            self.play_audio(int(selected_index[0]))

    def save_playlist_to_config(self):
        def create_folder_in_localappdata(folder_name):
            # Get the LocalAppData directory path for the current user
            localappdata_dir = os.getenv('LOCALAPPDATA')

            if not localappdata_dir:
                pass

            # Combine the LocalAppData directory path with the desired folder name
            folder_path = os.path.join(localappdata_dir, folder_name)

            # Check if the folder already exists
            if not os.path.exists(folder_path):
                try:
                    # Create the folder if it doesn't exist
                    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    pass

        folder_name = "SimPlayer"  # Replace with the desired folder name
        create_folder_in_localappdata(folder_name)

        audio_path = os.path.expanduser("~\\AppData\\Local\\SimPlayer\\config.json")

        # Save the playlist to a JSON configuration file
        config = {
            "playlist": self.playlist
        }
        with open(audio_path, "w") as config_file:
            json.dump(config, config_file)

    def load_playlist_from_config(self):
        audio_path = os.path.expanduser("~\\AppData\\Local\\SimPlayer\\config.json")
        # Load the playlist from the JSON configuration file
        if os.path.exists(audio_path):
            with open(audio_path, "r") as config_file:
                config = json.load(config_file)
                self.playlist = config.get("playlist", [])
                self.playlistbox.delete(0, tk.END)  # Clear the listbox
                for audio_file in self.playlist:
                    if os.path.exists(audio_file):
                        song_title = os.path.basename(audio_file)
                        self.playlistbox.insert(tk.END, song_title)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("250x410")  # Set the width and height in pixels (420x420)
    root.resizable(False, False)
    root.configure(bg="#212121")
    app = SimPlayer(root)
    for i in range(8):
        root.grid_rowconfigure(i, weight=1)  # Make rows expandable
    for i in range(2):
        root.grid_columnconfigure(i, weight=1)  # Make columns expandable
    root.mainloop()
