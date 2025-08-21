"""
Modern Update Frame with Enhanced UI
===================================

A beautiful, modern update screen that matches the new UI design
with proper frame handling and improved user experience.
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


class ModernUpdateAppFrame(ctk.CTkFrame):
    """Modern update screen with beautiful UI and proper frame handling"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.update_in_progress = False
        self.setup_modern_update_frame()

    def setup_modern_update_frame(self):
        """Create the modern update interface"""
        self.master.change_geometry("1000x800")
        
        # Main container with gradient background
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#0f1419")
        self.main_container.pack(fill="both", expand=True)
        
        # Header section with back button
        self.create_header()
        
        # Main content area
        self.create_main_content()
        
        # Footer
        self.create_footer()

    def create_header(self):
        """Create the header with title and back button"""
        header_frame = ctk.CTkFrame(self.main_container, fg_color="#1a202c", height=80)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Back button
        self.back_button = ctk.CTkButton(
            header_frame,
            text="← Back to Menu",
            command=self.return_to_main_menu,
            width=120,
            height=35,
            font=("Segoe UI", 12, "bold"),
            fg_color="transparent",
            border_width=2,
            border_color="#4299e1",
            text_color="#4299e1",
            hover_color="#2d3748"
        )
        self.back_button.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔄 Update Vocabulary Library",
            font=("Segoe UI", 24, "bold"),
            text_color="#e2e8f0"
        )
        title_label.grid(row=0, column=1, pady=20)

    def create_main_content(self):
        """Create the main content area"""
        content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Info section
        info_container = ctk.CTkFrame(content_frame, fg_color=("#ffffff", "#2d3748"), 
                                    corner_radius=15, height=120)
        info_container.pack(fill="x", pady=(0, 30))
        info_container.pack_propagate(False)
        
        ctk.CTkLabel(
            info_container,
            text="📋 Vocabulary Library Update",
            font=("Segoe UI", 18, "bold"),
            text_color="#2d3748"
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            info_container,
            text="This will rebuild your vocabulary database with the latest word lists.\n" + 
                 "The process may take a few moments depending on your vocabulary size.",
            font=("Segoe UI", 12),
            text_color=("#4a5568", "#a0aec0"),
            justify="center"
        ).pack(pady=(0, 20))
        
        # Status and progress section
        self.create_progress_section(content_frame)
        
        # Animation/Logo section
        self.create_animation_section(content_frame)
        
        # Action section
        self.create_action_section(content_frame)

    def create_progress_section(self, parent):
        """Create the progress tracking section"""
        self.progress_container = ctk.CTkFrame(parent, fg_color=("#f7fafc", "#2a2e38"), 
                                             corner_radius=15, height=150)
        self.progress_container.pack(fill="x", pady=(0, 30))
        self.progress_container.pack_propagate(False)
        
        # Initially hidden, will be shown during update
        self.progress_container.pack_forget()
        
        # Progress title
        ctk.CTkLabel(
            self.progress_container,
            text="Update Progress",
            font=("Segoe UI", 16, "bold"),
            text_color="#2d3748"
        ).pack(pady=(20, 10))
        
        # Progress bar
        progress_frame = ctk.CTkFrame(self.progress_container, fg_color="transparent")
        progress_frame.pack(pady=10, padx=40, fill="x")
        
        self.progress_var = tk.StringVar()
        self.progress_var.set("0%")
        
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
            font=("Segoe UI", 12, "bold"),
            text_color="#48bb78"
        )
        self.progress_label.pack()
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.progress_container,
            text="Ready to start update...",
            font=("Segoe UI", 12),
            text_color=("#4a5568", "#a0aec0")
        )
        self.status_label.pack(pady=(0, 20))

    def create_animation_section(self, parent):
        """Create the animation/logo section"""
        self.animation_container = ctk.CTkFrame(parent, fg_color=("#ffffff", "#1a202c"), 
                                              corner_radius=20, height=250)
        self.animation_container.pack(fill="x", pady=(0, 30))
        self.animation_container.pack_propagate(False)
        
        # Initially show static logo
        self.logo_label = ctk.CTkLabel(
            self.animation_container, 
            image=lingleap_pic, 
            text=""
        )
        self.logo_label.pack(expand=True, pady=30)

    def create_action_section(self, parent):
        """Create the action buttons section"""
        action_container = ctk.CTkFrame(parent, fg_color="transparent", height=80)
        action_container.pack(fill="x")
        action_container.pack_propagate(False)
        
        # Start update button
        self.start_button = ctk.CTkButton(
            action_container,
            text="🚀 Start Vocabulary Update",
            command=self.start_update,
            width=250,
            height=50,
            font=("Segoe UI", 16, "bold"),
            fg_color="#48bb78",
            hover_color="#38a169",
            corner_radius=12
        )
        self.start_button.pack(expand=True, pady=20)

    def create_footer(self):
        """Create the footer"""
        footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=50)
        footer_frame.pack(fill="x", pady=(0, 20))
        footer_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            footer_frame,
            text="LingoLeap • Keep Your Vocabulary Up to Date",
            font=("Segoe UI", 12),
            text_color="#718096"
        ).pack(pady=15)

    def start_update(self):
        """Start the vocabulary update process"""
        if self.update_in_progress:
            return
            
        self.update_in_progress = True
        
        # Update UI for update mode
        self.start_button.configure(
            text="🔄 Update in Progress...",
            state="disabled",
            fg_color="#a0aec0"
        )
        
        # Show progress section
        self.progress_container.pack(fill="x", pady=(0, 30))
        
        # Hide the static logo and show animation
        self.logo_label.pack_forget()
        self.handle_loading_gif()
        
        # Start update thread
        threading.Thread(target=self.update_thread, daemon=True).start()

    def handle_loading_gif(self):
        """Load and display animated GIF during update"""
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
                        frame_image = self.gif.copy().convert("RGBA").resize((200, 200))
                        ctk_image = ctk.CTkImage(frame_image, size=(200, 200))
                        self.frames.append(ctk_image)
                        self.gif.seek(len(self.frames))
                except EOFError:
                    pass
                
                if self.frames:
                    self.gif_label = ctk.CTkLabel(self.animation_container, text="")
                    self.gif_label.pack(expand=True, pady=30)
                    
                    self.delay = max(self.gif.info.get('duration', 100), 80)
                    self.current_frame = 0
                    self.animate_gif()
                else:
                    self.create_fallback_animation()
            else:
                self.create_fallback_animation()
                
        except Exception as e:
            print(f"Could not load update GIF: {e}")
            self.create_fallback_animation()

    def animate_gif(self):
        """Animate the GIF frames"""
        if (hasattr(self, 'frames') and self.frames and 
            hasattr(self, 'gif_label') and self.update_in_progress):
            try:
                frame = self.frames[self.current_frame]
                self.gif_label.configure(image=frame)
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                
                # Continue animation
                self.gif_label.after(self.delay, self.animate_gif)
            except Exception as e:
                print(f"Error animating GIF: {e}")

    def create_fallback_animation(self):
        """Create fallback animation when GIF is not available"""
        # Animated dots
        dots_frame = ctk.CTkFrame(self.animation_container, fg_color="transparent")
        dots_frame.pack(expand=True)
        
        ctk.CTkLabel(
            dots_frame,
            text="🔄 Updating",
            font=("Segoe UI", 18, "bold"),
            text_color="#4299e1"
        ).pack(pady=(50, 20))
        
        # Create animated dots
        self.loading_dots_frame = ctk.CTkFrame(dots_frame, fg_color="transparent")
        self.loading_dots_frame.pack()
        
        self.loading_dots = []
        colors = ["#48bb78", "#4299e1", "#9f7aea"]
        
        for i in range(3):
            dot = ctk.CTkLabel(
                self.loading_dots_frame,
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
        if not self.update_in_progress:
            return
            
        try:
            if hasattr(self, 'loading_dots'):
                for i, dot in enumerate(self.loading_dots):
                    # Create pulsing effect
                    if (self.dot_animation_step + i * 15) % 90 < 30:
                        dot.configure(text="●", font=("Arial", 24))
                    else:
                        dot.configure(text="●", font=("Arial", 18))
            
            self.dot_animation_step += 1
            
            # Continue animation
            if hasattr(self, 'loading_dots_frame'):
                self.loading_dots_frame.after(100, self.animate_fallback)
                
        except Exception as e:
            print(f"Error in fallback animation: {e}")

    def update_thread(self):
        """Background thread for vocabulary update"""
        try:
            # Status updates
            status_updates = [
                "🔍 Scanning vocabulary files...",
                "📂 Reading word lists...",
                "🔄 Processing updates...",
                "💾 Saving to database...",
                "✨ Finalizing update..."
            ]
            
            # Update status
            for i, status in enumerate(status_updates[:-1]):
                self.master.after(0, lambda s=status: self.status_label.configure(text=s))
                time.sleep(0.5)
            
            # Word lists for update
            word_lists = [
                (CSVPaths.NOUNS.value, 'nouns'),
                (CSVPaths.VERBS.value, 'verbs'),
                (CSVPaths.ADVERBS.value, 'adverbs'),
                (CSVPaths.ADJECTIVES.value, 'adjectives')
            ]
            
            # Perform the actual update
            read_csv_files(self, word_lists, self.progress_bar, self.progress_var)
            
            # Update game properties
            game_properties.is_library_built = True
            write_to_csv(CSVPaths.APP_PROPERTIES.value, game_properties.data)
            
            if hasattr(game_properties, 'user_language') and hasattr(game_properties, 'word_type'):
                game_properties.default_answer = random_word_gen(
                    game_properties.user_language, 
                    game_properties.word_type
                )
            
            # Final status
            self.master.after(0, lambda: self.status_label.configure(
                text="✅ Vocabulary update completed successfully!"
            ))
            self.master.after(0, lambda: self.progress_var.set("100%"))
            self.master.after(0, lambda: self.progress_bar.set(1.0))
            
            # Wait a moment then re-enable the interface
            time.sleep(2)
            self.master.after(0, self.update_completed)
            
        except Exception as e:
            error_msg = f"❌ Update failed: {str(e)}"
            self.master.after(0, lambda: self.status_label.configure(text=error_msg))
            print(f"Update error: {e}")
            
            # Re-enable interface after error
            time.sleep(3)
            self.master.after(0, self.update_completed)

    def update_completed(self):
        """Handle update completion"""
        self.update_in_progress = False
        
        # Update button
        self.start_button.configure(
            text="✅ Update Complete",
            state="normal",
            fg_color="#48bb78"
        )
        
        # Stop animations
        if hasattr(self, 'gif_label'):
            self.gif_label.pack_forget()
        if hasattr(self, 'loading_dots_frame'):
            self.loading_dots_frame.pack_forget()
        
        # Show completion message
        completion_frame = ctk.CTkFrame(self.animation_container, fg_color="transparent")
        completion_frame.pack(expand=True)
        
        ctk.CTkLabel(
            completion_frame,
            text="🎉",
            font=("Arial", 48)
        ).pack(pady=(30, 10))
        
        ctk.CTkLabel(
            completion_frame,
            text="Update Complete!",
            font=("Segoe UI", 18, "bold"),
            text_color="#48bb78"
        ).pack(pady=(0, 30))
        
        # Auto return to main menu after 3 seconds
        self.master.after(3000, self.return_to_main_menu)

    def return_to_main_menu(self):
        """Return to the main menu"""
        try:
            self.master.open_frame('update_app_frame', 'mainmenuframe')
        except Exception as e:
            print(f"Error returning to main menu: {e}")

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
UpdateAppFrame = ModernUpdateAppFrame
