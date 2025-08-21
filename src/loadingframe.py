import threading
import time
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
import os
from assetlibmanager import lingleap_pic
from word_library import read_csv_files, random_word_gen
from functions import game_properties, write_to_csv
from app_variables import CSVPaths, wordlib_location

class LoadingFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.start_time = time.time()  # Track loading start time
        self.minimum_loading_time = 4.0  # Minimum 2 seconds display
        self.setup_loading_frame()
        self.start_library_build()

    def setup_loading_frame(self):
        self.master.change_geometry("800x600") # type: ignore
        
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
        """Load and display animated GIF for loading screen"""
        try:
            # Try both possible paths
            gif_paths = [
                os.path.join('..', 'images', 'buildlib_gif_dark.gif'),
                os.path.join('images', 'buildlib_gif_dark.gif'),
                os.path.join('..', 'images', 'buildlib_gif_light.gif'),
                os.path.join('images', 'buildlib_gif_light.gif')
            ]
            
            gif_path = None
            for path in gif_paths:
                if os.path.exists(path):
                    gif_path = path
                    break
            
            if gif_path:
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
                    self.delay = max(self.gif.info.get('duration', 100), 100)  # Minimum 100ms per frame
                    self.current_frame = 0
                    self.animate_gif()
                else:
                    print("No frames loaded from GIF")
            else:
                print("Loading GIF not found, using static logo")
                # Fallback to rotating the static logo
                self.animate_static_logo()
                
        except Exception as e:
            print(f"Could not load loading GIF: {e}")
            self.animate_static_logo()

    def animate_gif(self):
        """Animate the GIF frames"""
        if hasattr(self, 'frames') and self.frames and hasattr(self, 'gif_label'):
            try:
                frame = self.frames[self.current_frame]
                self.gif_label.configure(image=frame)
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                
                # Continue animation
                self.gif_label.after(self.delay, self.animate_gif)
            except Exception as e:
                print(f"Error animating GIF: {e}")

    def animate_static_logo(self):
        """Fallback animation for static logo"""
        try:
            # Simple rotation effect or pulsing
            self.logo_animation_step = getattr(self, 'logo_animation_step', 0)
            
            # Create a simple pulsing effect by changing the size
            size_variation = int(20 * (1 + 0.2 * (self.logo_animation_step % 20) / 20))
            base_size = 180
            new_size = base_size + size_variation
            
            # Update logo size for pulsing effect
            if hasattr(self, 'logo_label'):
                # Create new image with varying size
                resized_image = ctk.CTkImage(
                    dark_image=lingleap_pic.cget("dark_image"), 
                    light_image=lingleap_pic.cget("light_image"), 
                    size=(new_size, new_size)
                )
                self.logo_label.configure(image=resized_image)
            
            self.logo_animation_step += 1
            
            # Continue animation every 100ms
            if hasattr(self, 'logo_label'):
                self.logo_label.after(100, self.animate_static_logo)
                
        except Exception as e:
            print(f"Error in static logo animation: {e}")

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
                
                # Update status
                self.master.after(0, lambda: self.status_label.configure(text="Library built successfully!"))
                self.master.after(0, lambda: self.progress_var.set("100%"))
                self.master.after(0, lambda: self.progress_bar.configure(value=100))
                
                # Calculate remaining time to meet minimum display duration
                elapsed_time = time.time() - self.start_time
                remaining_time = max(0, self.minimum_loading_time - elapsed_time)
                
                # Wait for remaining time plus a bit extra for user experience
                total_wait_time = int((remaining_time + 0.5) * 1000)  # Convert to milliseconds
                
                # Add a completion message during the wait
                self.master.after(500, lambda: self.status_label.configure(text="Finalizing..."))
                
                # Wait minimum time then transition to main menu
                self.master.after(total_wait_time, self.proceed_to_main_menu)
                
            except Exception as e:
                self.master.after(0, lambda: self.status_label.configure(
                    text=f"Error building library: {str(e)}"))
                print(f"Library build error: {e}")
                
                # Still respect minimum time even on error
                elapsed_time = time.time() - self.start_time
                remaining_time = max(0, self.minimum_loading_time - elapsed_time)
                total_wait_time = int((remaining_time + 1.0) * 1000)  # Extra second on error
                
                self.master.after(total_wait_time, self.proceed_to_main_menu)
        
        # Start the building process in a separate thread
        threading.Thread(target=build_thread, daemon=True).start()

    def proceed_to_main_menu(self):
        """Transition to the main menu after library building is complete"""
        try:
            self.master.open_frame("loading_frame", 'mainmenuframe')
        except Exception as e:
            print(f"Error transitioning to main menu: {e}")

#test it
