import customtkinter as ctk
import tkinter
from assetlibmanager import learn_deutsch_pic
from app_variables import mainmenu_colour
import subprocess
import sys
import os


class ModernMainMenuFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Remove fg_color from kwargs if it exists, we'll use our own styling
        kwargs.pop('fg_color', None)
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_modern_main_menu()

    def setup_modern_main_menu(self):
        self.master.change_geometry("1400x900")
        
        # Create main container with gradient-like background
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#0f1419")
        self.main_container.pack(fill="both", expand=True)
        
        # Header section
        self.create_header()
        
        # Main content area
        self.create_main_content()
        
        # Footer with quick actions
        self.create_footer()
    
    def create_header(self):
        """Create modern header with logo and navigation"""
        header_frame = ctk.CTkFrame(self.main_container, height=120, 
                                  fg_color="#1e2328", corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Logo and title section
        logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_frame.pack(side="left", fill="y", padx=30)
        
        # App title with modern typography
        title_label = ctk.CTkLabel(logo_frame, text="LingoLeap",
                                 font=("Helvetica", 36, "bold"),
                                 text_color="#00d4aa")
        title_label.pack(pady=(20, 5))
        
        subtitle_label = ctk.CTkLabel(logo_frame, text="Advanced German Learning Platform",
                                    font=("Helvetica", 14),
                                    text_color="#8892b0")
        subtitle_label.pack()
        
        # Quick stats section
        stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_frame.pack(side="right", fill="y", padx=30)
        
        self.create_quick_stats(stats_frame)
    
    def create_quick_stats(self, parent):
        """Create quick statistics display"""
        try:
            from user_progress import progress_manager
            summary = progress_manager.get_progress_summary()
            
            stats_title = ctk.CTkLabel(parent, text="Your Progress",
                                     font=("Helvetica", 16, "bold"),
                                     text_color="#ccd6f6")
            stats_title.pack(pady=(15, 10))
            
            # Create stats in a grid
            stats_grid = ctk.CTkFrame(parent, fg_color="#2d3748", corner_radius=10)
            stats_grid.pack(pady=10)
            
            stats_data = [
                ("Level", summary.get("level", "A1")),
                ("Score", summary.get("total_score", 0)),
                ("Streak", f"{summary.get('current_streak', 0)} days"),
                ("Accuracy", f"{summary.get('overall_accuracy', 0)}%")
            ]
            
            for i, (label, value) in enumerate(stats_data):
                row = i // 2
                col = i % 2
                
                stat_frame = ctk.CTkFrame(stats_grid, fg_color="transparent")
                stat_frame.grid(row=row, column=col, padx=10, pady=5)
                
                value_label = ctk.CTkLabel(stat_frame, text=str(value),
                                         font=("Helvetica", 18, "bold"),
                                         text_color="#00d4aa")
                value_label.pack()
                
                label_label = ctk.CTkLabel(stat_frame, text=label,
                                         font=("Helvetica", 10),
                                         text_color="#8892b0")
                label_label.pack()
                
        except Exception as e:
            # Fallback if progress system isn't available
            placeholder = ctk.CTkLabel(parent, text="Progress Stats\nComing Soon",
                                     font=("Helvetica", 12),
                                     text_color="#8892b0")
            placeholder.pack(pady=30)
    
    def create_main_content(self):
        """Create the main learning content area"""
        content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Left sidebar with features
        self.create_sidebar(content_frame)
        
        # Center content - German levels
        self.create_level_selection(content_frame)
        
        # Right panel - additional features
        self.create_feature_panel(content_frame)
    
    def create_sidebar(self, parent):
        """Create modern sidebar with quick actions"""
        sidebar = ctk.CTkFrame(parent, width=280, fg_color="#1a202c", corner_radius=15)
        sidebar.pack(side="left", fill="y", padx=(0, 20))
        sidebar.pack_propagate(False)
        
        # Sidebar title
        sidebar_title = ctk.CTkLabel(sidebar, text="🚀 Quick Actions",
                                   font=("Helvetica", 18, "bold"),
                                   text_color="#e2e8f0")
        sidebar_title.pack(pady=(25, 20))
        
        # Action buttons with modern styling
        actions = [
            ("🧠 Spaced Repetition", self.open_spaced_repetition, "#e53e3e"),
            ("📊 Progress Dashboard", self.open_progress_dashboard, "#4299e1"),
            ("📝 Vocabulary Editor", self.open_vocabulary_editor, "#48bb78"),
            ("🎮 Interactive Practice", self.open_interactive_modes, "#ed8936"),
            ("🎤 Pronunciation", self.open_pronunciation, "#9f7aea"),
            ("📚 Study Schedule", self.open_study_schedule, "#38b2ac"),
            ("⚙️ Settings", self.open_settings, "#718096")
        ]
        
        for text, command, color in actions:
            btn = ctk.CTkButton(sidebar, text=text,
                              command=command,
                              width=240, height=45,
                              font=("Helvetica", 13, "bold"),
                              fg_color=color,
                              hover_color=self.darken_color(color),
                              corner_radius=8)
            btn.pack(pady=8, padx=20)
    
    def create_level_selection(self, parent):
        """Create modern German level selection"""
        center_frame = ctk.CTkFrame(parent, fg_color="transparent")
        center_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        # Title section
        title_frame = ctk.CTkFrame(center_frame, fg_color="transparent", height=100)
        title_frame.pack(fill="x", pady=(0, 30))
        title_frame.pack_propagate(False)
        
        main_title = ctk.CTkLabel(title_frame, text="🇩🇪 Learn German",
                                font=("Helvetica", 32, "bold"),
                                text_color="#f7fafc")
        main_title.pack(pady=(20, 5))
        
        subtitle = ctk.CTkLabel(title_frame, 
                              text="Choose your proficiency level to begin your German learning journey",
                              font=("Helvetica", 14),
                              text_color="#a0aec0")
        subtitle.pack()
        
        # Level cards container
        levels_container = ctk.CTkFrame(center_frame, fg_color="transparent")
        levels_container.pack(fill="both", expand=True)
        
        # Create level cards
        self.create_level_cards(levels_container)
    
    def create_level_cards(self, parent):
        """Create modern level selection cards"""
        levels = [
            {
                "name": "A1 - Beginner", 
                "description": "Basic vocabulary and simple phrases",
                "features": ["Essential vocabulary", "Basic grammar", "Common phrases"],
                "color": "#4299e1",
                "action": lambda: self.open_level("a1_deutsch_frame")
            },
            {
                "name": "A2 - Elementary", 
                "description": "Compound words and cultural context",
                "features": ["Compound words", "Cultural context", "Grammar patterns"],
                "color": "#48bb78",
                "action": lambda: self.open_level("a2_deutsch_frame")
            },
            {
                "name": "B1 - Intermediate", 
                "description": "Complex grammar and business German",
                "features": ["Passive voice", "Business German", "News comprehension"],
                "color": "#ed8936",
                "action": lambda: self.open_level("b1_deutsch_frame")
            },
            {
                "name": "B2 - Advanced", 
                "description": "Idioms, academic writing, and technical German",
                "features": ["German idioms", "Academic writing", "Technical vocabulary"],
                "color": "#9f7aea",
                "action": lambda: self.open_level("b2_deutsch_frame")
            }
        ]
        
        # Create cards in a 2x2 grid
        for i, level in enumerate(levels):
            row = i // 2
            col = i % 2
            
            card_frame = ctk.CTkFrame(parent, fg_color="#2d3748", corner_radius=15,
                                    width=300, height=200)
            card_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            card_frame.grid_propagate(False)
            
            # Configure grid weights
            parent.grid_rowconfigure(row, weight=1)
            parent.grid_columnconfigure(col, weight=1)
            
            # Level name
            level_name = ctk.CTkLabel(card_frame, text=level["name"],
                                    font=("Helvetica", 20, "bold"),
                                    text_color=level["color"])
            level_name.pack(pady=(20, 10))
            
            # Description
            description = ctk.CTkLabel(card_frame, text=level["description"],
                                     font=("Helvetica", 12),
                                     text_color="#cbd5e0",
                                     wraplength=250)
            description.pack(pady=(0, 15))
            
            # Features list
            features_text = "• " + "\n• ".join(level["features"])
            features_label = ctk.CTkLabel(card_frame, text=features_text,
                                        font=("Helvetica", 10),
                                        text_color="#a0aec0",
                                        justify="left")
            features_label.pack(pady=(0, 15))
            
            # Action button
            action_btn = ctk.CTkButton(card_frame, text="Start Learning",
                                     command=level["action"],
                                     width=200, height=35,
                                     font=("Helvetica", 12, "bold"),
                                     fg_color=level["color"],
                                     hover_color=self.darken_color(level["color"]),
                                     corner_radius=8)
            action_btn.pack(pady=(0, 20))
            
            # Hover effects
            self.add_hover_effects(card_frame, level["color"])
    
    def create_feature_panel(self, parent):
        """Create right feature panel"""
        feature_panel = ctk.CTkFrame(parent, width=300, fg_color="#1a202c", corner_radius=15)
        feature_panel.pack(side="right", fill="y", padx=(20, 0))
        feature_panel.pack_propagate(False)
        
        # Panel title
        panel_title = ctk.CTkLabel(feature_panel, text="🎯 Learning Tools",
                                 font=("Helvetica", 18, "bold"),
                                 text_color="#e2e8f0")
        panel_title.pack(pady=(25, 20))
        
        # Feature showcase
        self.create_feature_showcase(feature_panel)
        
        # Tips section
        self.create_learning_tips(feature_panel)
    
    def create_feature_showcase(self, parent):
        """Create feature showcase section"""
        showcase_frame = ctk.CTkFrame(parent, fg_color="#2d3748", corner_radius=10)
        showcase_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        showcase_title = ctk.CTkLabel(showcase_frame, text="✨ New Features",
                                    font=("Helvetica", 14, "bold"),
                                    text_color="#00d4aa")
        showcase_title.pack(pady=(15, 10))
        
        features = [
            "🎭 Cultural Context Learning",
            "🧠 Spaced Repetition System", 
            "📊 Advanced Progress Analytics",
            "🎵 Audio Pronunciation Guide",
            "🎮 Interactive Grammar Games"
        ]
        
        for feature in features:
            feature_label = ctk.CTkLabel(showcase_frame, text=feature,
                                       font=("Helvetica", 11),
                                       text_color="#cbd5e0")
            feature_label.pack(pady=3, anchor="w", padx=15)
        
        # Explore button
        explore_btn = ctk.CTkButton(showcase_frame, text="Explore All Features",
                                  command=self.show_all_features,
                                  width=200, height=30,
                                  font=("Helvetica", 11, "bold"),
                                  fg_color="#00d4aa",
                                  hover_color="#00b894")
        explore_btn.pack(pady=15)
    
    def create_learning_tips(self, parent):
        """Create learning tips section"""
        tips_frame = ctk.CTkFrame(parent, fg_color="#2d3748", corner_radius=10)
        tips_frame.pack(pady=10, padx=20, fill="x")
        
        tips_title = ctk.CTkLabel(tips_frame, text="💡 Learning Tips",
                                font=("Helvetica", 14, "bold"),
                                text_color="#ffd700")
        tips_title.pack(pady=(15, 10))
        
        tips = [
            "Practice 15-20 minutes daily for best results",
            "Focus on speaking German out loud", 
            "Learn words in context, not isolation",
            "Use German media to improve listening"
        ]
        
        for tip in tips:
            tip_label = ctk.CTkLabel(tips_frame, text=f"• {tip}",
                                   font=("Helvetica", 10),
                                   text_color="#cbd5e0",
                                   wraplength=250)
            tip_label.pack(pady=2, anchor="w", padx=15)
        
        tips_frame.pack(pady=(0, 15))
    
    def create_footer(self):
        """Create modern footer with additional options"""
        footer_frame = ctk.CTkFrame(self.main_container, height=60,
                                  fg_color="#1e2328", corner_radius=0)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        # Left side - version info
        version_info = ctk.CTkLabel(footer_frame, text="LingoLeap v2.0 - Enhanced Learning Experience",
                                  font=("Helvetica", 10),
                                  text_color="#718096")
        version_info.pack(side="left", padx=30, pady=20)
        
        # Right side - quick actions
        actions_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        actions_frame.pack(side="right", padx=30, pady=10)
        
        help_btn = ctk.CTkButton(actions_frame, text="Help & Support",
                               width=100, height=30,
                               font=("Helvetica", 10),
                               fg_color="#4a5568",
                               hover_color="#2d3748")
        help_btn.pack(side="left", padx=5)
        
        about_btn = ctk.CTkButton(actions_frame, text="About",
                                width=80, height=30,
                                font=("Helvetica", 10),
                                fg_color="#4a5568",
                                hover_color="#2d3748")
        about_btn.pack(side="left", padx=5)
    
    def add_hover_effects(self, frame, color):
        """Add hover effects to level cards"""
        original_color = "#2d3748"
        hover_color = "#4a5568"
        
        def on_enter(event):
            frame.configure(fg_color=hover_color)
        
        def on_leave(event):
            frame.configure(fg_color=original_color)
        
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
    
    def darken_color(self, color):
        """Darken a hex color for hover effects"""
        # Simple color darkening (you can enhance this)
        color_map = {
            "#4299e1": "#3182ce",
            "#48bb78": "#38a169", 
            "#ed8936": "#dd6b20",
            "#9f7aea": "#805ad5",
            "#38b2ac": "#319795",
            "#718096": "#4a5568",
            "#00d4aa": "#00b894"
        }
        return color_map.get(color, color)
    
    # Action methods
    def open_spaced_repetition(self):
        try:
            self.master.open_frame("mainmenuframe", "spaced_repetition_frame")
        except Exception as e:
            print(f"Error opening spaced repetition: {e}")
    
    def open_progress_dashboard(self):
        try:
            self.master.open_frame("mainmenuframe", "progress_dashboard")
        except Exception as e:
            print(f"Error opening progress dashboard: {e}")
    
    def open_vocabulary_editor(self):
        """Open vocabulary editor as a separate window"""
        try:
            editor_path = os.path.join(os.path.dirname(__file__), "vocabulary_editor.py")
            subprocess.Popen([sys.executable, editor_path])
        except Exception as e:
            print(f"Error opening vocabulary editor: {e}")
    
    def open_interactive_modes(self):
        try:
            self.master.open_frame("mainmenuframe", "interactive_mode")
        except Exception as e:
            print(f"Error opening interactive modes: {e}")
    
    def open_pronunciation(self):
        try:
            self.master.open_frame("mainmenuframe", "pronunciation_practice")
        except Exception as e:
            print(f"Error opening pronunciation practice: {e}")
    
    def open_study_schedule(self):
        try:
            self.master.open_frame("mainmenuframe", "practice_schedule")
        except Exception as e:
            print(f"Error opening study schedule: {e}")
    
    def open_settings(self):
        # Implementation for settings
        pass
    
    def open_level(self, level_frame):
        try:
            self.master.open_frame("mainmenuframe", level_frame)
        except Exception as e:
            print(f"Error opening level {level_frame}: {e}")
    
    def show_all_features(self):
        """Show all features overview"""
        # Implementation for feature overview
        pass


# Keep the original MainMenuFrame for compatibility
class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_main_menu_frame()

    def setup_main_menu_frame(self):
        self.master.change_geometry("1280x720")

        self.Learn_Deutch_frame = ctk.CTkFrame(self, width=320, height=380, fg_color="#424242",
                                               corner_radius=25)
        self.Learn_Deutch_frame.bind("<Enter>", lambda event: self.Learn_Deutch_frame.configure(
            fg_color=mainmenu_colour.frame_light))
        self.Learn_Deutch_frame.bind("<Leave>", lambda event: self.Learn_Deutch_frame.configure(
            fg_color=mainmenu_colour.frame_dark))
        self.Learn_Deutch_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        self.Deutsch_label = ctk.CTkLabel(self.Learn_Deutch_frame, text="Learn Deutsch",
                                          font=('Century Gothic', 25))
        self.Deutsch_label.place(x=75, rely=0.05)

        self.Learn_Deutsch_logo_label = ctk.CTkLabel(self.Learn_Deutch_frame, image=learn_deutsch_pic, text="",
                                                     font=ctk.CTkFont(size=20, weight="bold"))
        self.Learn_Deutsch_logo_label.place(relx=0.18, y=60)

        self.A1_label = ctk.CTkLabel(self.Learn_Deutch_frame, text="A1 - Deutsch",
                                     font=('Century Gothic', 15))
        self.A1_label.place(relx=0.35, rely=0.45)
        self.A1_label.bind("<Button-1>", lambda event: self.master.open_frame("mainmenuframe",
                                                                              "a1_deutsch_frame"))
        self.A1_label.bind("<Enter>", lambda event: self.A1_label.configure(cursor="hand2", text_color="green",
                                                                            fg_color='transparent'))
        self.A1_label.bind("<Leave>", lambda event: self.A1_label.configure(cursor="arrow", text_color="white",
                                                                            fg_color='transparent'))

        self.A2_label = ctk.CTkLabel(self.Learn_Deutch_frame, text="A2 - Deutsch",
                                     font=('Century Gothic', 15))
        self.A2_label.place(relx=0.35, rely=0.55)
        self.A2_label.bind("<Button-1>", lambda event: self.master.open_frame("mainmenuframe",
                                                                              "a2_deutsch_frame"))
        self.A2_label.bind("<Enter>", lambda event: self.A2_label.configure(cursor="hand2", text_color="green",
                                                                            fg_color='transparent'))
        self.A2_label.bind("<Leave>", lambda event: self.A2_label.configure(cursor="arrow", text_color="white",
                                                                            fg_color='transparent'))

        self.B1_label = ctk.CTkLabel(self.Learn_Deutch_frame, text="B1 - Deutsch",
                                     font=('Century Gothic', 15))
        self.B1_label.place(relx=0.35, rely=0.65)
        self.B1_label.bind("<Button-1>", lambda event: self.master.open_frame("mainmenuframe",
                                                                              "b1_deutsch_frame"))
        self.B1_label.bind("<Enter>", lambda event: self.B1_label.configure(cursor="hand2", text_color="green",
                                                                            fg_color='transparent'))
        self.B1_label.bind("<Leave>", lambda event: self.B1_label.configure(cursor="arrow", text_color="white",
                                                                            fg_color='transparent'))

        self.B2_label = ctk.CTkLabel(self.Learn_Deutch_frame, text="B2 - Deutsch",
                                     font=('Century Gothic', 15))
        self.B2_label.place(relx=0.35, rely=0.75)
        self.B2_label.bind("<Button-1>", lambda event: self.master.open_frame("mainmenuframe",
                                                                              "b2_deutsch_frame"))
        self.B2_label.bind("<Enter>", lambda event: self.B2_label.configure(cursor="hand2", text_color="green",
                                                                            fg_color='transparent'))
        self.B2_label.bind("<Leave>", lambda event: self.B2_label.configure(cursor="arrow", text_color="white",
                                                                            fg_color='transparent'))

        self.Cant_decide_label = ctk.CTkLabel(self.Learn_Deutch_frame, text="Can't Decide?",
                                              font=('Century Gothic', 10))
        self.Cant_decide_label.place(relx=0.38, rely=0.85)
        self.Cant_decide_label.bind("<Button-1>",
                                    lambda event: self.master.open_frame("mainmenuframe", 'update_app_frame'))
        self.Cant_decide_label.bind("<Enter>",
                                    lambda event: self.Cant_decide_label.configure(cursor="hand2", text_color="blue",
                                                                                   fg_color='transparent'))
        self.Cant_decide_label.bind("<Leave>",
                                    lambda event: self.Cant_decide_label.configure(cursor="arrow", text_color="white",
                                                                                   fg_color='transparent'))
        
        # Add progress dashboard button
        self.progress_button = ctk.CTkButton(self, text="📊 Progress Dashboard",
                                           font=('Century Gothic', 14, 'bold'),
                                           width=180, height=40,
                                           fg_color="#2E8B57",
                                           hover_color="#228B22")
        self.progress_button.place(relx=0.02, rely=0.02)
        self.progress_button.configure(command=lambda: self.master.open_frame("mainmenuframe", "progress_dashboard"))
        
        # Add vocabulary editor button
        self.vocab_editor_button = ctk.CTkButton(self, text="📝 Edit Vocabulary",
                                               font=('Century Gothic', 14, 'bold'),
                                               width=180, height=40,
                                               fg_color="#4169E1",
                                               hover_color="#1E90FF")
        self.vocab_editor_button.place(relx=0.02, rely=0.12)
        self.vocab_editor_button.configure(command=self.open_vocabulary_editor)
        
        # Add interactive modes button
        self.interactive_button = ctk.CTkButton(self, text="🎮 Interactive Modes",
                                              font=('Century Gothic', 14, 'bold'),
                                              width=180, height=40,
                                              fg_color="#FF6347",
                                              hover_color="#FF4500")
        self.interactive_button.place(relx=0.02, rely=0.22)
        self.interactive_button.configure(command=lambda: self.master.open_frame("mainmenuframe", "interactive_mode"))
        
        # Add pronunciation practice button
        self.pronunciation_button = ctk.CTkButton(self, text="🎤 Pronunciation",
                                                font=('Century Gothic', 14, 'bold'),
                                                width=180, height=40,
                                                fg_color="#8A2BE2",
                                                hover_color="#9932CC")
        self.pronunciation_button.place(relx=0.02, rely=0.32)
        self.pronunciation_button.configure(command=lambda: self.master.open_frame("mainmenuframe", "pronunciation_practice"))
    
    def open_vocabulary_editor(self):
        """Open vocabulary editor as a separate window"""
        import subprocess
        import sys
        import os
        
        # Get the path to the vocabulary editor
        editor_path = os.path.join(os.path.dirname(__file__), "vocabulary_editor.py")
        
        try:
            # Run the vocabulary editor as a separate process
            subprocess.Popen([sys.executable, editor_path])
        except Exception as e:
            print(f"Error opening vocabulary editor: {e}")


pass
