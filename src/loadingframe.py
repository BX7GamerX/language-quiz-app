import threading
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
from assetlibmanager import lingleap_pic
from word_library import read_csv_files, random_word_gen
from functions import game_properties, write_to_csv
from app_variables import CSVPaths, wordlib_location

class LoadingFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_loading_frame()
        self.start_library_build()

    def setup_loading_frame(self):
        self.master.change_geometry("800x600")
        
        # Main loading frame
        self.loading_frame = ctk.CTkFrame(self, width=800, height=600, fg_color='#292929')
        self.loading_frame.pack(fill="both", expand=True)
        
        # Title
        self.title_label = ctk.CTkLabel(self.loading_frame, text="Building Vocabulary Library...",
                                       font=("Old English Text", 24, "bold"))
        self.title_label.pack(pady=(50, 20))
        
        # Progress bar
        self.progress_var = tk.StringVar()
        self.progress_var.set("0.00%")
        
        self.progress_bar = ttk.Progressbar(self.loading_frame, orient='horizontal', 
                                          mode='determinate', maximum=100, length=400)
        self.progress_bar.pack(pady=20)
        
        self.progress_label = ctk.CTkLabel(self.loading_frame, textvariable=self.progress_var,
                                         font=("Arial", 14))
        self.progress_label.pack(pady=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(self.loading_frame, text="Initializing...",
                                       font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Animated logo
        self.logo_label = ctk.CTkLabel(self.loading_frame, image=lingleap_pic, text="")
        self.logo_label.pack(pady=20)
        
        # Load and display animated GIF
        self.handle_loading_gif()

    def handle_loading_gif(self):
        try:
            gif_path = '../images/buildlib_gif_dark.gif'
            self.gif = Image.open(gif_path)
            self.frames = []
            
            try:
                while True:
                    frame_image = self.gif.copy().convert("RGBA").resize((200, 200))
                    ctk_image = ctk.CTkImage(frame_image, size=(200, 200))
                    self.frames.append(ctk_image)
                    self.gif.seek(len(self.frames))
            except EOFError:
                pass
            
            if self.frames:
                self.gif_label = ctk.CTkLabel(self.loading_frame, text="")
                self.gif_label.pack(pady=10)
                self.delay = self.gif.info.get('duration', 100)
                self.update_gif(0)
        except (FileNotFoundError, Exception) as e:
            print(f"Could not load loading GIF: {e}")

    def update_gif(self, frame_index):
        if hasattr(self, 'frames') and self.frames:
            frame = self.frames[frame_index]
            frame_index = (frame_index + 1) % len(self.frames)
            if hasattr(self, 'gif_label'):
                self.gif_label.configure(image=frame)
                self.gif_label.image = frame
                self.gif_label.after(self.delay, self.update_gif, frame_index)

    def start_library_build(self):
        def build_thread():
            try:
                # Update status
                self.master.after(0, lambda: self.status_label.configure(text="Reading vocabulary files..."))
                
                # Build the library
                read_csv_files(self, wordlib_location, self.progress_bar, self.progress_var)
                
                # Update game properties
                game_properties.is_library_built = True
                write_to_csv(CSVPaths.APP_PROPERTIES.value, game_properties.data)
                
                if hasattr(game_properties, 'user_language') and hasattr(game_properties, 'word_type'):
                    game_properties.default_answer = random_word_gen(game_properties.user_language, 
                                                                   game_properties.word_type)
                
                # Update status and proceed to main menu
                self.master.after(0, lambda: self.status_label.configure(text="Library built successfully!"))
                self.master.after(0, lambda: self.progress_var.set("100%"))
                self.master.after(0, lambda: self.progress_bar.configure(value=100))
                
                # Wait a moment then transition to main menu
                self.master.after(2000, self.proceed_to_main_menu)
                
            except Exception as e:
                self.master.after(0, lambda: self.status_label.configure(
                    text=f"Error building library: {str(e)}"))
                print(f"Library build error: {e}")
                # Still proceed to main menu after error
                self.master.after(3000, self.proceed_to_main_menu)
        
        # Start the building process in a separate thread
        threading.Thread(target=build_thread, daemon=True).start()

    def proceed_to_main_menu(self):
        """Transition to the main menu after library building is complete"""
        try:
            self.master.open_frame("loading_frame", 'mainmenuframe')
        except Exception as e:
            print(f"Error transitioning to main menu: {e}")
