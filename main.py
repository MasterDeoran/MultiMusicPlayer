# Import necessary libraries and modules from imports.py
from imports import *

# Set the visual theme for the application using ttkbootstrap
style = tb.Style(theme='darkly')

# Initialize the Pygame Mixer for handling audio
pygame.mixer.init()
pygame.init()

# Global variables to store sound objects and their controls
sounds = {}

#======================================================================================================================================
# MusicPlayer class
#
# This class represents the music player application.
#======================================================================================================================================
class MusicPlayer:
    """
    A class to represent the music player application.

    Attributes:
        songs (list): A list to store song objects.
        root (tk.Tk): The root window for the application.
        menuFrame (ttk.Frame): A frame to hold menu buttons and icons.
        header_frame (tk.Frame): A frame to display column headers.
        scrollbar (ttk.Scrollbar): A scrollbar for the canvas.
        canvas (ttk.Canvas): A canvas to make the songs list scrollable.
        frame (ttk.Frame): A frame inside the canvas to hold song widgets.
    """
    #--------------------------------------------------------------------------------------------------------------------------------
    # The constructor for MusicPlayer class.
    #--------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, root):
        """
        The constructor for MusicPlayer class.

        Parameters:
            root (tk.Tk): The root window for the application.
        """
        self.songs = []                     # List to store songs
        self.root = root                    # Root window
        self.root.title("Music-Player")     # Root window
        self.root.minsize(1366, 720)        # Minimum size of the window

        # Configure styles for different UI elements
        style.configure('Custom.TFrame', background='#375a7f')
        style.configure('VersionLabel.TLabel', foreground='white', background='#375a7f')

        # Menu frame for icons and buttons
        self.menuFrame = tb.Frame(root, width=100, style="Custom.TFrame")
        self.menuFrame.pack(side="left", fill=Y)

        # Calculate base path for resources, accounting for both development and bundled app scenarios
        base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

        # Icons-Pfade korrekt setzen
        self.load_icon_path = os.path.join(base_path, "icons", "songs-folder.png")
        self.saveS_icon_path = os.path.join(base_path, "icons", "arrow-down.png")
        self.loadS_icon_path = os.path.join(base_path, "icons", "arrow-up.png")
        self.new_icon_path = os.path.join(base_path, "icons", "new-file.png")

        # Load icons for buttons and store them as PhotoImage instances
        self.load_icon = tk.PhotoImage(file=self.load_icon_path)
        self.saveS_icon = tk.PhotoImage(file=self.saveS_icon_path)
        self.loadS_icon = tk.PhotoImage(file=self.loadS_icon_path)
        self.new_icon = tk.PhotoImage(file=self.new_icon_path)

        # UI setup for buttons and labels goes here...
        self.frameLabel = tb.Label(self.menuFrame, text="   Version 0.9", style='VersionLabel.TLabel')
        self.frameLabel.pack(side="bottom", fill="x")

        # Buttons for menu actions (New, Load Files, Save Settings, Load Settings)
        self.new_button = tb.Button(self.menuFrame, text="New", command=self.new_songs, image=self.new_icon, compound=TOP)
        self.new_button.pack(side="top", padx=20, pady=20, fill="both")
        self.load_button = tb.Button(self.menuFrame, text="Music load", command=self.load_songs, image=self.load_icon, compound=TOP)
        self.load_button.pack(side="top", padx=20, pady=20, fill="both")
        self.saveSetting_button = tb.Button(self.menuFrame, text="Playlist save", command=self.save_settings, image=self.saveS_icon, compound=TOP)
        self.saveSetting_button.pack(side="top", padx=20, pady=10, fill="both")
        self.loadSetting_button = tb.Button(self.menuFrame, text="Playlist load", command=self.load_settings, image=self.loadS_icon, compound=TOP)
        self.loadSetting_button.pack(side="top", padx=20, pady=10, fill="both")

        # Not used in this version
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(side="top", fill="x")

        # Scrollbar and Canvas for the songs list
        self.scrollbar = tb.Scrollbar(root)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas = tb.Canvas(root, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.canvas.yview)

        # Frame inside the canvas to hold song widgets
        self.frame = tb.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # Bind events for scrolling and resizing
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Add headers to the song list
        self.add_headers()

    #--------------------------------------------------------------------------------------------------------------------------------
    # Add headers to the table.
    #--------------------------------------------------------------------------------------------------------------------------------
    def add_headers(self):
        """
            Add headers to the table.

            This method adds headers to the table in the user interface.
            It configures the columns and sets the header text for each column.
        """
        headers = ["Song", "Play", "Volume", "Comment", "Dropdown", "Action"]  # Beispiele für Spaltenüberschriften
        headersColS = [3, 1, 1, 1, 1, 1]  # Beispiele für Spaltenüberschriften
        headersCol = [0, 3, 4, 5, 6, 7]  # Beispiele für Spaltenüberschriften
        for col, header_text in enumerate(headers):
            self.frame.columnconfigure(col, weight=1)
        return

    #--------------------------------------------------------------------------------------------------------------------------------  
    # Scroll the canvas based on mouse wheel movement.
    #--------------------------------------------------------------------------------------------------------------------------------
    def on_mousewheel(self, event):
        """
        Scroll the canvas based on mouse wheel movement.
        
        This method is called when the mouse wheel is scrolled. It adjusts the scrolling speed
        based on the delta value of the event. It scrolls the canvas vertically.
        
        Parameters:
            event (tk.Event): The mouse wheel event.
        """
        try:  # Try scrolling for Windows and MacOS
            scroll_speed = int(-1*(event.delta/120))
            self.canvas.yview_scroll(scroll_speed, "units")
        except:  # For Linux, where event.delta is not used
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    #--------------------------------------------------------------------------------------------------------------------------------
    # Callback function that is called when the frame is being configured.
    #--------------------------------------------------------------------------------------------------------------------------------
    def on_frame_configure(self, event):
        """
        Callback function that is called when the frame is being configured.

        Args:
            event (tkinter.Event): The event object that triggered the callback.
        """
        # Update the scroll region to the size of the frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Set the width of the canvas frame to the width of the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    #--------------------------------------------------------------------------------------------------------------------------------
    # Callback function that is called when the canvas is being configured.
    #--------------------------------------------------------------------------------------------------------------------------------
    def on_canvas_configure(self, event):
        """
        Callback function that is called when the canvas is being configured.

        Args:
            event (tkinter.Event): The event object that triggered the callback.
        """

        # Set the width of the canvas frame to the width of the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    #--------------------------------------------------------------------------------------------------------------------------------
    # Create a new list of songs
    #--------------------------------------------------------------------------------------------------------------------------------
    def new_songs(self):
        """
            Create a new list of songs.        
        """
        
        global sounds

        # Check if there are any songs loaded
        if len(sounds) > 0:
            # Ask the user if they want to create a new list
            answer = messagebox.askyesno("Neue Liste erstellen", "Bist du sicher, dass du eine neue Liste erstellen und die aktuelle löschen möchtest?")
            if answer:
                # stop all sounds and clear the list
                for sound in sounds.values():
                    sound.stop()
                sounds = {}
                for widget in self.frame.winfo_children():
                    widget.destroy()
            else:

                return
        else:
            # load songs if no songs are loaded
            self.load_songs()


    #--------------------------------------------------------------------------------------------------------------------------------
    # Load songs from the user's system
    #--------------------------------------------------------------------------------------------------------------------------------
    def load_songs(self):
        """
            Load songs from the user's system.
        """
        global sounds
        
        # Ask the user to select music files
        filenames = filedialog.askopenfilenames(title="Wähle Musikdateien",
                                                filetypes=(("MP3-Dateien", "*.mp3"), ("WAV-Dateien", "*.wav"), ("Alle Dateien", "*.*")),
                                                initialdir=os.getcwd(),
                                                multiple=True)
       
        # add headers to the table
        self.add_headers()

        # Load each selected file
        for filename in filenames:
            self.add_song(filename, 100)

    #--------------------------------------------------------------------------------------------------------------------------------
    # Add a song to the list of songs
    #--------------------------------------------------------------------------------------------------------------------------------
    def add_song(self, filename, volume):
        """
            Add a song to the list of songs.

            This method creates a new song object and adds it to the list of songs.
            It also updates the list of songs in the user interface.

            Args:
                filename (str): The path to the song file.
                volume (int): The volume level for the song.
        """
    
        # Check if the file exists
        if os.path.exists(filename):

            id = len(self.songs)
            row = id + 1
            print("Add Song ", id, " title: ", filename)
            song = Song(self.frame, filename, id, row, volume)
            self.songs.append(song)

            return song
        else:
            return
    #--------------------------------------------------------------------------------------------------------------------------------
    # Save settings to a JSON file
    #--------------------------------------------------------------------------------------------------------------------------------
    def save_settings(self):
        """
            Save the current settings to a JSON file.

            This method saves the current settings to a JSON file.
            It asks the user to select a location to save the file.
        """

        # Ask the user to select a location to save the settings file
        file = filedialog.asksaveasfile(title="Wo soll die Einstellungsdatei gespeichert werden", mode="w", defaultextension=".json",
                                                filetypes=(("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*")),
                                                initialdir=os.getcwd())
        
        # Check if the file exists and if its not None then return null
        if file is None:
            return
        
        # Create a dictionary to store the settings
        settings = {
            'Songs': [
                {'Path': song.filepath, 'Volume': song.volume, 'Comment': song.comment_field.get(), 'Category': song.dropdown.get()} 
                for song in self.songs]  # Liste der Pfade zu den geladenen Liedern
        }
        # dump the settings to the file
        json.dump(settings, file, indent=4)
        # close the file
        file.close

    #--------------------------------------------------------------------------------------------------------------------------------
    # Load settings from a JSON file
    #--------------------------------------------------------------------------------------------------------------------------------
    def load_settings(self):
        """
            Load settings from a JSON file.

            This method loads settings from a JSON file.
            It asks the user to select a settings file to load.
        """
        try:
            global sounds
            file = filedialog.askopenfilename(title="Wähle die Einstellungsdatei",
                                                filetypes=(("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*")),
                                                initialdir=os.getcwd())
            
            if file is None:
                return

            for song in self.songs:
                song.active = False  # Deaktiviere das Song-Objekt, bevor du es entfernst

            with open(file, 'r') as json_file:
                settings = json.load(json_file)
                
                # Stelle die Lautstärke wieder her (falls global gesetzt und nicht individuell pro Song)
                # self.volume_control.set(settings['Volume'])  # Beispiel, falls vorhanden
                
                # Lösche vorhandene Songs, bevor neue geladen werden
                for sound in sounds.values():
                    sound.stop()
                sounds = {}
                for widget in self.frame.winfo_children():
                    widget.destroy()
                self.songs.clear()
                
                # Lade jedes gespeicherte Lied und dessen Lautstärkeeinstellung
                for song_info in settings['Songs']:
                    # Erstelle ein Song-Objekt mit dem geladenen Pfad und der Lautstärke
                    song = self.add_song(song_info['Path'], song_info['Volume'])
                    song.comment_field.insert(0, song_info.get('Comment', ''))  # Füge den Kommentar hinzu, default ist ''
                    song.dropdown.set(song_info.get('Category', ''))  # Setze die Dropdown-Auswahl, default ist ''
                    
        except FileNotFoundError:
            print("Keine Einstellungsdatei gefunden. Standardwerte werden verwendet.")
        except Exception as e:
            print(f"Fehler beim Laden der Einstellungen: {e}")


    #--------------------------------------------------------------------------------------------------------------------------------
    # Update the list of songs
    #--------------------------------------------------------------------------------------------------------------------------------
    def update_songs_list(self):
        """
            Update the list of songs.

            This method updates the list of songs by removing any songs that have been deleted.
            It also updates the row and ID of each song in the list.
        """

        # Remove any songs that have been deleted
        new_songs_list = [song for song in self.songs if song.parent.winfo_exists()] # Check if the parent widget exists
        self.songs = new_songs_list

        # Update the row and ID of each song
        for i, song in enumerate(self.songs):
            song.id = i
            song.row = i + 1
            song.update_row()

#======================================================================================================================================
# Song class
            
# This class represents a song in the music player application.
# It contains methods to play, stop, and delete the song, as well as to adjust the volume and update the progress bar.
# The song object also contains widgets for displaying the song information and controls in the user interface.
#======================================================================================================================================
class Song:
    """
    A class to represent a song in the music player application.
    """
    
    #--------------------------------------------------------------------------------------------------------------------------------
    # The constructor for Song class.
    #--------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, filepath, sound_id, row, volume):
        """
        The constructor for Song class.

        Parameters:
            parent (tk.Frame): The parent frame for the song widget.
            filepath (str): The path to the song file.
            sound_id (int): The ID of the sound object.
            row (int): The row number for the song widget in the user interface.
            volume (int): The volume level for the song.
        """

        # Initialize the song object with the given parameters
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.isPlaying = False
        self.isPause = False
        self.id = sound_id
        self.parent = parent
        self.active = True
        sounds[self.id] = pygame.mixer.Sound(filepath)
        self.length = self.get_length(self.filepath)

        # Label for the song
        self.label = tb.Label(parent, text=self.filename)
        self.label.grid(row=row, column=0, columnspan=3, padx=10, pady=10)

        # Play button for the song
        self.play_button = tb.Button(parent, text="Play ▶", command=self.play,width=10)
        self.play_button.grid(row=row, column=3, columnspan=1, padx=10, pady=10)

        # Delete button for the song
        self.delete_button = ttk.Button(parent, text="Delete", command=self.delete_song)
        self.delete_button.grid(row=row, column=4, padx=5, pady=5) 

        # Progress bar for the song
        self.progress = ttk.Progressbar(parent, length=100, mode='determinate', bootstyle="striped")
        self.progress.grid(row=row, column=5, padx=10, pady=10)

        # Volume control for the song
        self.volume_control = tk.Scale(parent, from_=0, to=100, orient=tk.HORIZONTAL, command=self.adjust_volume)
        self.volume_control.set(volume*100)  # Set the volume control to the initial volume level
        self.volume_control.grid(row=row, column=6, padx=10, pady=10)

        # Dropdown-Menu for song categories
        self.dropdown_texts = ["Text 1", "Text 2", "Text 3"] # Default-Texts for the dropdown
        self.dropdown = ttk.Combobox(parent, values=self.dropdown_texts, state="readonly")
        self.dropdown.grid(row=row, column=7, padx=10, pady=10, sticky="ew")

        # Comment field for the song
        self.comment_field = ttk.Entry(parent)
        self.comment_field.grid(row=row, column=8, padx=10, pady=10, sticky="ew")

        # Initialize the progress bar and volume control
        self.update_progress()
        self.adjust_volume(volume*100)

    #--------------------------------------------------------------------------------------------------------------------------------
    # Play the song.
    #--------------------------------------------------------------------------------------------------------------------------------
    def play(self):
        """
        Play the song.

        This method plays the song using the Pygame mixer.
        """
        print("Play ID: ", self.id, " - ", self.filename)
        # start the song if it is not playing
        if not self.isPlaying:
            sounds[self.id].play(loops=-1)
            self.isPlaying = True
            self.play_button.config(text="Stop ■", style="danger.TButton")
            self.start_time = time.time() 
            self.update_progress()
        # stop the song if it is playing
        else:
            sounds[self.id].stop()
            self.isPlaying = False
            self.play_button.config(text="Play ▶", style='primary.TButton')

    #--------------------------------------------------------------------------------------------------------------------------------
    # Get the length of the song.
    #--------------------------------------------------------------------------------------------------------------------------------
    def get_length(self, filename):
        """
        Get the length of the song.
        """
        audio = MP3(filename)
        return audio.info.length

    #--------------------------------------------------------------------------------------------------------------------------------
    # Stop the song.
    #--------------------------------------------------------------------------------------------------------------------------------
    def stop(self):
        """
        Stop the song.

        This method stops the song using the Pygame mixer.
        """
        sounds[self.id].stop()
        self.isPause = False
        self.isPlaying = False
        self.play_button.config(text="Play")

    #--------------------------------------------------------------------------------------------------------------------------------
    # Update the progress bar.
    #--------------------------------------------------------------------------------------------------------------------------------
    def update_progress(self):
        """
        Update the progress bar.

        This method updates the progress bar to show the progress of the song.
        It calculates the progress as a percentage of the total length of the song.
        """
        # Stop the progress bar if the song is not active
        if not self.active:
                return
        # Calculate the progress of the song
        if self.isPlaying:
            elapsed_time = time.time() - self.start_time
            progress_percent = (elapsed_time / self.length) * 100
            if progress_percent >= 100:
                progress_percent = 0
                self.start_time = time.time()
            self.progress['value'] = min(progress_percent, 100)
        # Reset the progress bar if the song is not playing
        else:
            self.progress['value'] = 0
        # Update the progress bar every 100 milliseconds
        self.parent.after(100, self.update_progress)

    #--------------------------------------------------------------------------------------------------------------------------------
    # Adjust the volume of the song.
    #--------------------------------------------------------------------------------------------------------------------------------
    def adjust_volume(self, volume):
        """
        Adjust the volume of the song.

        This method adjusts the volume of the song using the Pygame mixer.
        It converts the volume value from the scale widget (0-100) to the Pygame mixer volume (0.0-1.0).
        
        Parameters:
            volume (int): The volume level for the song.
        """
        # Set the volume of the song
        self.volume = int(volume) / 100  # Convert the volume from 0-100 to 0.0-1.0
        sounds[self.id].set_volume(self.volume)

    #--------------------------------------------------------------------------------------------------------------------------------
    # Delete the song.
    #--------------------------------------------------------------------------------------------------------------------------------
    def delete_song(self):
        """
        Delete the song.

        This method deletes the song from the list of songs and the user interface.
        """
        self.active = False  # deactivate the song before removing it
        # Stop the song if it is playing
        if self.isPlaying:
            self.stop()

        # Remove the song widgets from the user interface
        self.label.destroy()
        self.play_button.destroy()
        self.volume_control.destroy()
        self.comment_field.destroy()
        self.dropdown.destroy()
        self.delete_button.destroy()
        self.progress.destroy()

        # Remove the song from the list of songs
        try:
            self.songs.remove(self)
        except ValueError:
            pass

       # delete the sound object from the global dictionary
        del sounds[self.id]

        # Update the row and ID of each song in the list
        for i, song in enumerate(self.songs):
            song.id = i
            song.row = i + 1 # set the row number for the song + 1 because the header is at row 0
            song.update_row()
        
        # Update the list of songs in the user interface
        self.parent.update_songs_list()  # Update the list of songs

    #--------------------------------------------------------------------------------------------------------------------------------
    # Update the row of the song.
    #--------------------------------------------------------------------------------------------------------------------------------
    def update_row(self):
        """
        Update the row of the song.

        This method updates the row of the song in the user interface.
        """
        # Update the row of each widget in the song
        self.label.grid(row=self.row)
        self.play_button.grid(row=self.row)
        self.volume_control.grid(row=self.row)
        self.comment_field.grid(row=self.row)
        self.dropdown.grid(row=self.row)
        self.delete_button.grid(row=self.row)
        self.progress.grid(row=self.row)

# Main function to run the application
# Create the root window and the music player application
# Run the main event loop
if __name__ == "__main__":
    root = style.master
    app = MusicPlayer(root)
    root.mainloop()