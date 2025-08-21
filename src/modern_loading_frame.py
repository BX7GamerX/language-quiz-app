"""
Modern Loading Frame with Enhanced UI and GIF Support
===================================================

A beautiful, modern loading screen that matches the new UI design
with proper frame handling and the requested 2-second minimum display time.
"""

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


class ModernLoadingFrame(ctk.CTkFrame):
    """Modern loading screen with beautiful UI and proper frame handling"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.start_time = time.time()  # Track loading start time
        self.minimum_loading_time = 2.0  # Minimum 2 seconds display as requested
        self.setup_modern_loading_frame()
        self.start_library_build()

    def setup_modern_loading_frame(self):
        """Create the modern loading interface"""
        self.master.change_geometry("900x700")
        
        # Main container with gradient background
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#0f1419")
        self.main_container.pack(fill="both", expand=True)
        
        # Header section
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=100)
        header_frame.pack(fill="x", pady=(30, 20))
        header_frame.pack_propagate(False)
        
        # Title with modern styling
        title_label = ctk.CTkLabel(
            header_frame,
            text="🚀 Building Vocabulary Library",
            font=("Segoe UI", 32, "bold"),
            text_color="#e2e8f0"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Preparing your German learning experience...",
            font=("Segoe UI", 14),
            text_color="#a0aec0"
        )
        subtitle_label.pack()
        
        # Center content area
        content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Logo and animation container
        logo_container = ctk.CTkFrame(content_frame, fg_color=("#f7fafc", "#1a202c"), 
                                    corner_radius=20, height=300)
        logo_container.pack(fill="x", pady=(0, 30))
        logo_container.pack_propagate(False)
        
        # Handle animated GIF loading
        self.handle_loading_gif(logo_container)
        
        # Progress section
        progress_container = ctk.CTkFrame(content_frame, fg_color=("#ffffff", "#2d3748"), 
                                        corner_radius=15, height=150)
        progress_container.pack(fill="x", pady=(0, 20))
        progress_container.pack_propagate(False)
        
        # Progress title
        ctk.CTkLabel(
            progress_container,
            text="Progress",
            font=("Segoe UI", 18, "bold"),
            text_color="#2d3748"
        ).pack(pady=(20, 10))
        
        # Progress bar with modern styling
        self.progress_var = tk.StringVar()
        self.progress_var.set("0%")
        
        progress_frame = ctk.CTkFrame(progress_container, fg_color="transparent")
        progress_frame.pack(pady=10, padx=40, fill="x")
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=15,
            progress_color="#48bb78",
            fg_color=("#e2e8f0", "#4a5568"),
            corner_radius=10
        )
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)
        
        # Progress percentage
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            textvariable=self.progress_var,
            font=("Segoe UI", 14, "bold"),
            text_color="#48bb78"
        )
        self.progress_label.pack()
        
        # Status section
        status_container = ctk.CTkFrame(content_frame, fg_color=("#f7fafc", "#2a2e38"), 
                                      corner_radius=12, height=80)
        status_container.pack(fill="x")
        status_container.pack_propagate(False)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            status_container,
            text="🔄 Initializing vocabulary database...",
            font=("Segoe UI", 14),
            text_color=("#4a5568", "#a0aec0")
        )
        self.status_label.pack(expand=True)
        
        # Footer with branding
        footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=50)
        footer_frame.pack(fill="x", pady=(0, 20))
        footer_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            footer_frame,
            text="LingoLeap • German Language Learning",
            font=("Segoe UI", 12),
            text_color="#718096"
        ).pack(pady=15)

    def handle_loading_gif(self, parent_frame):
        """Load and display animated GIF with modern styling"""
        try:
            # Try multiple GIF paths
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
                        # Resize to fit the modern container
                        frame_image = self.gif.copy().convert("RGBA").resize((250, 250))
                        ctk_image = ctk.CTkImage(frame_image, size=(250, 250))
                        self.frames.append(ctk_image)
                        self.gif.seek(len(self.frames))
                except EOFError:
                    pass
                
                if self.frames:
                    # Create container for GIF
                    gif_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
                    gif_container.pack(expand=True)
                    
                    self.gif_label = ctk.CTkLabel(gif_container, text="")
                    self.gif_label.pack(pady=20)
                    
                    # Get delay from GIF, minimum 80ms for smooth animation
                    self.delay = max(self.gif.info.get('duration', 100), 80)
                    self.current_frame = 0
                    self.animate_gif()
                else:
                    print("No frames loaded from GIF, using fallback")
                    self.create_fallback_animation(parent_frame)
            else:
                print("Loading GIF not found, using animated logo")
                self.create_fallback_animation(parent_frame)
                
        except Exception as e:
            print(f"Could not load loading GIF: {e}")
            self.create_fallback_animation(parent_frame)

    def animate_gif(self):
        """Smooth GIF animation"""
        if hasattr(self, 'frames') and self.frames and hasattr(self, 'gif_label'):
            try:
                frame = self.frames[self.current_frame]
                self.gif_label.configure(image=frame)
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                
                # Continue animation with proper timing
                self.gif_label.after(self.delay, self.animate_gif)
            except Exception as e:
                print(f"Error animating GIF: {e}")

    def create_fallback_animation(self, parent_frame):
        """Create beautiful fallback animation when GIF is not available"""
        # Logo container
        logo_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
        logo_container.pack(expand=True)
        
        # Animated logo
        self.logo_label = ctk.CTkLabel(logo_container, image=lingleap_pic, text="")
        self.logo_label.pack(pady=30)
        
        # Create pulsing dots animation
        dots_frame = ctk.CTkFrame(logo_container, fg_color="transparent")
        dots_frame.pack(pady=20)
        
        self.loading_dots = []
        colors = ["#48bb78", "#4299e1", "#9f7aea"]
        
        for i in range(3):
            dot = ctk.CTkLabel(
                dots_frame,
                text="●",
                font=("Arial", 20),
                text_color=colors[i]
            )
            dot.pack(side="left", padx=8)
            self.loading_dots.append(dot)
        
        self.dot_animation_step = 0
        self.animate_fallback()

    def animate_fallback(self):
        """Animate the fallback loading indicators"""
        try:
            # Animate dots
            if hasattr(self, 'loading_dots'):
                for i, dot in enumerate(self.loading_dots):
                    # Create pulsing effect
                    opacity_factor = 0.3 + 0.7 * abs((self.dot_animation_step + i * 10) % 60 - 30) / 30
                    
                    # Update dot appearance
                    if (self.dot_animation_step + i * 15) % 90 < 30:
                        dot.configure(text="●", font=("Arial", 24))
                    else:
                        dot.configure(text="●", font=("Arial", 18))
            
            # Animate logo size for pulsing effect
            if hasattr(self, 'logo_label'):
                size_variation = int(10 * abs((self.dot_animation_step % 40) - 20) / 20)
                base_size = 80
                new_size = base_size + size_variation
                
                # Update logo with pulsing size
                try:
                    resized_image = ctk.CTkImage(
                        dark_image=lingleap_pic._dark_image, 
                        light_image=lingleap_pic._light_image, 
                        size=(new_size, new_size)
                    )
                    self.logo_label.configure(image=resized_image)
                except:
                    pass  # Ignore if image update fails
            
            self.dot_animation_step += 1
            
            # Continue animation
            if hasattr(self, 'logo_label'):
                self.logo_label.after(100, self.animate_fallback)
                
        except Exception as e:
            print(f"Error in fallback animation: {e}")

    def start_library_build(self):
        """Start the vocabulary library building process or quick load if already built"""
        def build_thread():
            try:
                # Check if library is already built
                if game_properties.is_library_built:
                    # Show quick loading animation for visual consistency
                    status_updates = [
                        "📚 Loading vocabulary library...",
                        "✨ Preparing learning interface...",
                        "🎉 Ready to learn German!"
                    ]
                    
                    for i, status in enumerate(status_updates):
                        self.master.after(0, lambda s=status: self.status_label.configure(text=s))
                        # Quick progress updates for visual feedback
                        progress_val = (i + 1) / len(status_updates)
                        self.master.after(0, lambda p=progress_val: self.progress_bar.set(p))
                        self.master.after(0, lambda pct=int(progress_val*100): self.progress_var.set(f"{pct}%"))
                        time.sleep(0.3)  # Brief pause between updates
                    
                    # Ensure minimum display time is met
                    elapsed_time = time.time() - self.start_time
                    remaining_time = max(0, self.minimum_loading_time - elapsed_time)
                    
                    if remaining_time > 0:
                        time.sleep(remaining_time)
                    
                    # Proceed to main menu
                    self.master.after(0, self.proceed_to_main_menu)
                    return
                
                # Library needs to be built - show full loading process
                status_updates = [
                    "📂 Reading vocabulary files...",
                    "🔍 Processing German words...", 
                    "📚 Building word database...",
                    "🎯 Optimizing for learning...",
                    "✨ Finalizing library..."
                ]
                
                # Simulate progress steps with status updates
                for i, status in enumerate(status_updates[:-1]):
                    self.master.after(0, lambda s=status: self.status_label.configure(text=s))
                    time.sleep(0.2)  # Brief delay between status updates
                
                # Build the actual library
                read_csv_files(self, wordlib_location, self.progress_bar, self.progress_var)
                
                # Update game properties and persistent status
                game_properties.is_library_built = True
                write_to_csv(CSVPaths.APP_PROPERTIES.value, game_properties.data)
                
                # Also update the libstatus file that main.py reads from
                try:
                    libstatus_path = os.path.join(os.path.dirname(__file__), "../wordlib/libstatus")
                    with open(libstatus_path, 'w') as f:
                        f.write("0\n")  # Mark as built (0 means built)
                        f.write("1.0\n")  # Version or completion status
                    print("✅ Library status files updated")
                except Exception as e:
                    print(f"Warning: Could not update libstatus file: {e}")
                    # Try alternative path
                    try:
                        alt_libstatus_path = "wordlib/libstatus"
                        with open(alt_libstatus_path, 'w') as f:
                            f.write("0\n")
                            f.write("1.0\n")
                        print("✅ Library status files updated (alternative path)")
                    except Exception as e2:
                        print(f"Warning: Could not update libstatus file (alternative): {e2}")
                
                if hasattr(game_properties, 'user_language') and hasattr(game_properties, 'word_type'):
                    try:
                        game_properties.default_answer = random_word_gen(
                            game_properties.user_language, 
                            game_properties.word_type
                        )
                        # If it returns the error message, set a fallback
                        if game_properties.default_answer == "word library not found":
                            game_properties.default_answer = "library building complete"
                    except Exception as e:
                        print(f"Warning: Could not generate default answer: {e}")
                        game_properties.default_answer = "library building complete"
                
                # Final status updates
                self.master.after(0, lambda: self.status_label.configure(
                    text="✅ Library built successfully!"
                ))
                self.master.after(0, lambda: self.progress_var.set("100%"))
                self.master.after(0, lambda: self.progress_bar.set(1.0))
                
                # Calculate remaining time to meet minimum display duration
                elapsed_time = time.time() - self.start_time
                remaining_time = max(0, self.minimum_loading_time - elapsed_time)
                
                # Add completion message during wait
                self.master.after(800, lambda: self.status_label.configure(
                    text="🎉 Ready to learn German!"
                ))
                
                # Wait minimum time then transition to main menu
                total_wait_time = int((remaining_time + 0.8) * 1000)  # Convert to milliseconds
                self.master.after(total_wait_time, self.proceed_to_main_menu)
                
            except Exception as e:
                error_msg = f"❌ Error building library: {str(e)}"
                self.master.after(0, lambda: self.status_label.configure(text=error_msg))
                print(f"Library build error: {e}")
                
                # Still respect minimum time even on error
                elapsed_time = time.time() - self.start_time
                remaining_time = max(0, self.minimum_loading_time - elapsed_time)
                total_wait_time = int((remaining_time + 2.0) * 1000)  # Extra time on error
                
                self.master.after(total_wait_time, self.proceed_to_main_menu)
        
        # Start the building process in a separate thread
        threading.Thread(target=build_thread, daemon=True).start()

    def proceed_to_main_menu(self):
        """Transition to the modern main menu after library building is complete"""
        try:
            # Ensure we go to the modern main menu
            self.master.open_frame("loading_frame", 'mainmenuframe')
        except Exception as e:
            print(f"Error transitioning to main menu: {e}")

    def update_progress(self, progress_value, status_text=""):
        """Update progress bar and status (called from library building)"""
        try:
            # Update progress bar
            self.progress_bar.set(progress_value / 100.0)
            self.progress_var.set(f"{progress_value:.1f}%")
            
            # Update status if provided
            if status_text:
                self.status_label.configure(text=status_text)
                
        except Exception as e:
            print(f"Error updating progress: {e}")


# Alias for compatibility
LoadingFrame = ModernLoadingFrame
