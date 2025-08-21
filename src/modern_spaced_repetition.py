"""
Modern Spaced Repetition Review Interface
=======================================

A sleek, modern interface for spaced repetition vocabulary reviews
with progress tracking and detailed analytics.
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import List, Optional
import random
import json
from datetime import datetime, timedelta

from spaced_repetition import spaced_repetition, ReviewCard


class ModernSpacedRepetitionFrame(ctk.CTkFrame):
    """Modern spaced repetition review interface"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=("gray85", "gray15"))
        self.controller = controller
        self.current_card: Optional[ReviewCard] = None
        self.review_cards: List[ReviewCard] = []
        self.current_index = 0
        self.session_stats = {"correct": 0, "total": 0}
        self.answer_revealed = False
        
        self.setup_styles()
        self.create_widgets()
        self.refresh_review_session()
    
    def setup_styles(self):
        """Define consistent styling"""
        self.colors = {
            'primary': "#2E8B57",      # Sea green
            'secondary': "#4682B4",     # Steel blue
            'success': "#228B22",       # Forest green
            'warning': "#FF8C00",       # Dark orange
            'danger': "#DC143C",        # Crimson
            'bg_light': "#F5F5F5",      # White smoke
            'bg_dark': "#1E1E1E",       # Dark gray
            'text_light': "#333333",    # Dark gray
            'text_dark': "#FFFFFF",     # White
            'accent': "#20B2AA"         # Light sea green
        }
        
        self.fonts = {
            'heading': ("Segoe UI", 24, "bold"),
            'subheading': ("Segoe UI", 18, "bold"),
            'body': ("Segoe UI", 14),
            'large_body': ("Segoe UI", 16),
            'button': ("Segoe UI", 12, "bold"),
            'small': ("Segoe UI", 11)
        }
    
    def create_widgets(self):
        """Create the main interface"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Main content area
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)
        
        # Create different views
        self.create_review_view()
        self.create_statistics_view()
        self.create_settings_view()
        
        # Show initial view
        self.show_review_view()
    
    def create_header(self):
        """Create the header with navigation and stats"""
        header = ctk.CTkFrame(self, height=80, fg_color=self.colors['primary'])
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header.grid_columnconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            header,
            text="🧠 Spaced Repetition",
            font=self.fonts['heading'],
            text_color="white"
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(header, fg_color="transparent")
        nav_frame.grid(row=0, column=1, padx=20, pady=20, sticky="e")
        
        self.review_btn = ctk.CTkButton(
            nav_frame,
            text="Review",
            command=self.show_review_view,
            width=80,
            height=35,
            font=self.fonts['button'],
            fg_color=self.colors['accent'],
            hover_color=self.colors['secondary']
        )
        self.review_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stats_btn = ctk.CTkButton(
            nav_frame,
            text="Statistics",
            command=self.show_statistics_view,
            width=80,
            height=35,
            font=self.fonts['button'],
            fg_color="transparent",
            border_width=2,
            border_color=self.colors['accent']
        )
        self.stats_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.settings_btn = ctk.CTkButton(
            nav_frame,
            text="Settings",
            command=self.show_settings_view,
            width=80,
            height=35,
            font=self.fonts['button'],
            fg_color="transparent",
            border_width=2,
            border_color=self.colors['accent']
        )
        self.settings_btn.grid(row=0, column=2)
        
        # Session stats
        self.session_label = ctk.CTkLabel(
            header,
            text="Session: 0/0",
            font=self.fonts['body'],
            text_color="white"
        )
        self.session_label.grid(row=0, column=2, padx=20, pady=20, sticky="e")
    
    def create_review_view(self):
        """Create the review interface"""
        self.review_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.review_frame.grid_columnconfigure(0, weight=1)
        self.review_frame.grid_rowconfigure(2, weight=1)
        
        # Progress bar
        self.progress_frame = ctk.CTkFrame(self.review_frame, height=60, fg_color=("gray90", "gray20"))
        self.progress_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.progress_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            self.progress_frame,
            text="Progress:",
            font=self.fonts['body']
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=15,
            progress_color=self.colors['success']
        )
        self.progress_bar.grid(row=0, column=1, padx=20, pady=15, sticky="ew")
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="0/0",
            font=self.fonts['small']
        )
        self.progress_label.grid(row=0, column=2, padx=20, pady=15, sticky="e")
        
        # Card display area
        self.card_frame = ctk.CTkFrame(self.review_frame, fg_color=("white", "gray25"))
        self.card_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.card_frame.grid_columnconfigure(0, weight=1)
        
        # Word display
        self.word_label = ctk.CTkLabel(
            self.card_frame,
            text="Click 'Start Review' to begin",
            font=("Segoe UI", 32, "bold"),
            text_color=self.colors['primary'],
            height=100
        )
        self.word_label.grid(row=0, column=0, padx=40, pady=30)
        
        # Context/hint display
        self.context_label = ctk.CTkLabel(
            self.card_frame,
            text="",
            font=self.fonts['large_body'],
            text_color=("gray50", "gray70"),
            wraplength=600
        )
        self.context_label.grid(row=1, column=0, padx=40, pady=(0, 30))
        
        # Answer area (initially hidden)
        self.answer_frame = ctk.CTkFrame(self.card_frame, fg_color=("gray95", "gray30"))
        self.answer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.answer_frame.grid_columnconfigure(0, weight=1)
        self.answer_frame.grid_remove()
        
        self.answer_label = ctk.CTkLabel(
            self.answer_frame,
            text="",
            font=self.fonts['subheading'],
            text_color=self.colors['success']
        )
        self.answer_label.grid(row=0, column=0, padx=20, pady=15)
        
        # Control buttons
        self.control_frame = ctk.CTkFrame(self.review_frame, fg_color="transparent")
        self.control_frame.grid(row=2, column=0, sticky="ew")
        self.control_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.show_answer_btn = ctk.CTkButton(
            self.control_frame,
            text="Show Answer",
            command=self.show_answer,
            font=self.fonts['button'],
            height=45,
            fg_color=self.colors['primary'],
            hover_color=self.colors['secondary']
        )
        self.show_answer_btn.grid(row=0, column=0, columnspan=3, padx=100, pady=20, sticky="ew")
        
        # Quality rating buttons (initially hidden)
        self.rating_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.rating_frame.grid(row=1, column=0, columnspan=3, pady=20)
        self.rating_frame.grid_remove()
        
        ctk.CTkLabel(
            self.rating_frame,
            text="How well did you remember?",
            font=self.fonts['body']
        ).grid(row=0, column=0, columnspan=6, pady=(0, 15))
        
        self.rating_buttons = []
        ratings = [
            ("😰", "Forgot", 0, self.colors['danger']),
            ("😕", "Hard", 2, self.colors['warning']),
            ("🤔", "Good", 3, "#FFA500"),
            ("😊", "Easy", 4, self.colors['success']),
            ("🎯", "Perfect", 5, self.colors['success'])
        ]
        
        for i, (emoji, text, quality, color) in enumerate(ratings):
            btn = ctk.CTkButton(
                self.rating_frame,
                text=f"{emoji}\n{text}",
                command=lambda q=quality: self.rate_card(q),
                width=80,
                height=60,
                font=self.fonts['small'],
                fg_color=color,
                hover_color=color
            )
            btn.grid(row=1, column=i, padx=5)
            self.rating_buttons.append(btn)
        
        # Action buttons at bottom
        self.action_frame = ctk.CTkFrame(self.review_frame, fg_color="transparent")
        self.action_frame.grid(row=3, column=0, sticky="ew", pady=20)
        self.action_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.start_review_btn = ctk.CTkButton(
            self.action_frame,
            text="Start Review Session",
            command=self.start_review_session,
            font=self.fonts['button'],
            height=40,
            fg_color=self.colors['primary'],
            hover_color=self.colors['secondary']
        )
        self.start_review_btn.grid(row=0, column=0, padx=10, sticky="ew")
        
        self.skip_btn = ctk.CTkButton(
            self.action_frame,
            text="Skip Card",
            command=self.skip_card,
            font=self.fonts['button'],
            height=40,
            fg_color="transparent",
            border_width=2,
            border_color=self.colors['warning'],
            text_color=self.colors['warning']
        )
        self.skip_btn.grid(row=0, column=1, padx=10, sticky="ew")
        
        self.end_session_btn = ctk.CTkButton(
            self.action_frame,
            text="End Session",
            command=self.end_review_session,
            font=self.fonts['button'],
            height=40,
            fg_color="transparent",
            border_width=2,
            border_color=self.colors['danger'],
            text_color=self.colors['danger']
        )
        self.end_session_btn.grid(row=0, column=2, padx=10, sticky="ew")
    
    def create_statistics_view(self):
        """Create the statistics display"""
        self.stats_frame = ctk.CTkScrollableFrame(self.main_content)
        self.stats_frame.grid_columnconfigure(0, weight=1)
        
        # Overall stats
        stats_header = ctk.CTkFrame(self.stats_frame, height=60, fg_color=self.colors['secondary'])
        stats_header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        stats_header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            stats_header,
            text="📊 Learning Statistics",
            font=self.fonts['heading'],
            text_color="white"
        ).grid(row=0, column=0, pady=15)
        
        # Stats cards
        self.create_stats_cards()
        
        # Charts and detailed analytics
        self.create_analytics_section()
    
    def create_stats_cards(self):
        """Create statistics cards"""
        stats = spaced_repetition.get_statistics()
        
        cards_frame = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        cards_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Total cards
        total_card = self.create_stat_card(
            cards_frame, "Total Words", str(stats['total_cards']), 
            self.colors['primary'], 0, 0
        )
        
        # Due cards
        due_card = self.create_stat_card(
            cards_frame, "Due Today", str(stats['due_cards']), 
            self.colors['warning'], 0, 1
        )
        
        # Mastered cards
        mastered_card = self.create_stat_card(
            cards_frame, "Mastered", str(stats['mastered_cards']), 
            self.colors['success'], 0, 2
        )
        
        # Retention rate
        retention_card = self.create_stat_card(
            cards_frame, "Retention", f"{stats['retention_rate']}%", 
            self.colors['accent'], 1, 0
        )
        
        # Learning cards
        learning_card = self.create_stat_card(
            cards_frame, "Learning", str(stats['learning_cards']), 
            self.colors['secondary'], 1, 1
        )
        
        # New cards
        new_card = self.create_stat_card(
            cards_frame, "New", str(stats['new_cards']), 
            "#9370DB", 1, 2
        )
    
    def create_stat_card(self, parent, title, value, color, row, col):
        """Create an individual statistics card"""
        card = ctk.CTkFrame(parent, fg_color=("white", "gray25"))
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            card,
            text=title,
            font=self.fonts['body'],
            text_color=("gray60", "gray80")
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color=color
        ).pack(pady=(0, 15))
        
        return card
    
    def create_analytics_section(self):
        """Create detailed analytics"""
        # Learning insights
        insights = spaced_repetition.get_learning_insights()
        
        insights_frame = ctk.CTkFrame(self.stats_frame, fg_color=("white", "gray25"))
        insights_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        
        ctk.CTkLabel(
            insights_frame,
            text="🎯 Learning Insights",
            font=self.fonts['subheading'],
            text_color=self.colors['primary']
        ).pack(pady=(20, 10))
        
        insights_text = f"""
Daily Review Recommendation: {insights['daily_review_recommendation']} cards
Current Streak: {insights['current_streak']} days
Estimated Mastery Time: {insights['estimated_mastery_time']}
Retention Trend: {insights['retention_trend'].replace('_', ' ').title()}
        """.strip()
        
        ctk.CTkLabel(
            insights_frame,
            text=insights_text,
            font=self.fonts['body'],
            justify="left"
        ).pack(pady=(0, 20), padx=20)
        
        # Challenging words
        if insights['challenging_words']:
            ctk.CTkLabel(
                insights_frame,
                text="Most Challenging Words:",
                font=self.fonts['body'],
                text_color=self.colors['warning']
            ).pack(pady=(10, 5))
            
            for word in insights['challenging_words']:
                ctk.CTkLabel(
                    insights_frame,
                    text=f"• {word}",
                    font=self.fonts['small']
                ).pack()
    
    def create_settings_view(self):
        """Create settings interface"""
        self.settings_frame = ctk.CTkScrollableFrame(self.main_content)
        self.settings_frame.grid_columnconfigure(0, weight=1)
        
        # Settings header
        settings_header = ctk.CTkFrame(self.settings_frame, height=60, fg_color=self.colors['accent'])
        settings_header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        settings_header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            settings_header,
            text="⚙️ Spaced Repetition Settings",
            font=self.fonts['heading'],
            text_color="white"
        ).grid(row=0, column=0, pady=15)
        
        # Settings options
        self.create_settings_options()
    
    def create_settings_options(self):
        """Create settings options"""
        # Daily review limit
        limit_frame = ctk.CTkFrame(self.settings_frame, fg_color=("white", "gray25"))
        limit_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        ctk.CTkLabel(
            limit_frame,
            text="Daily Review Limit",
            font=self.fonts['body']
        ).pack(pady=(15, 5))
        
        self.daily_limit = ctk.CTkSlider(
            limit_frame,
            from_=5,
            to=50,
            number_of_steps=45,
            command=self.update_daily_limit
        )
        self.daily_limit.set(20)
        self.daily_limit.pack(pady=10, padx=20, fill="x")
        
        self.limit_label = ctk.CTkLabel(
            limit_frame,
            text="20 cards per day",
            font=self.fonts['small']
        )
        self.limit_label.pack(pady=(0, 15))
        
        # Import/Export section
        io_frame = ctk.CTkFrame(self.settings_frame, fg_color=("white", "gray25"))
        io_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        ctk.CTkLabel(
            io_frame,
            text="Data Management",
            font=self.fonts['body']
        ).pack(pady=(15, 10))
        
        buttons_frame = ctk.CTkFrame(io_frame, fg_color="transparent")
        buttons_frame.pack(pady=(0, 15))
        
        ctk.CTkButton(
            buttons_frame,
            text="Export Data",
            command=self.export_data,
            font=self.fonts['button'],
            fg_color=self.colors['primary']
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Import Data",
            command=self.import_data,
            font=self.fonts['button'],
            fg_color=self.colors['secondary']
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Reset Progress",
            command=self.reset_progress,
            font=self.fonts['button'],
            fg_color=self.colors['danger']
        ).pack(side="left", padx=10)
    
    def show_review_view(self):
        """Show the review interface"""
        self.stats_frame.grid_remove()
        self.settings_frame.grid_remove()
        self.review_frame.grid(row=0, column=0, sticky="nsew")
        
        # Update button states
        self.review_btn.configure(fg_color=self.colors['accent'])
        self.stats_btn.configure(fg_color="transparent")
        self.settings_btn.configure(fg_color="transparent")
    
    def show_statistics_view(self):
        """Show the statistics interface"""
        self.review_frame.grid_remove()
        self.settings_frame.grid_remove()
        self.stats_frame.grid(row=0, column=0, sticky="nsew")
        
        # Update button states
        self.stats_btn.configure(fg_color=self.colors['accent'])
        self.review_btn.configure(fg_color="transparent")
        self.settings_btn.configure(fg_color="transparent")
        
        # Refresh statistics
        self.refresh_statistics()
    
    def show_settings_view(self):
        """Show the settings interface"""
        self.review_frame.grid_remove()
        self.stats_frame.grid_remove()
        self.settings_frame.grid(row=0, column=0, sticky="nsew")
        
        # Update button states
        self.settings_btn.configure(fg_color=self.colors['accent'])
        self.review_btn.configure(fg_color="transparent")
        self.stats_btn.configure(fg_color="transparent")
    
    def refresh_review_session(self):
        """Refresh the review session with due cards"""
        self.review_cards = spaced_repetition.get_due_cards(20)
        self.current_index = 0
        
        if self.review_cards:
            self.update_progress_display()
        else:
            self.word_label.configure(text="No cards due for review! 🎉")
            self.context_label.configure(text="Check back later or add more vocabulary.")
    
    def start_review_session(self):
        """Start a new review session"""
        self.refresh_review_session()
        if self.review_cards:
            self.session_stats = {"correct": 0, "total": 0}
            self.current_index = 0
            self.load_current_card()
            self.update_session_stats()
        else:
            messagebox.showinfo("No Reviews", "No cards are due for review right now!")
    
    def load_current_card(self):
        """Load the current card for review"""
        if self.current_index < len(self.review_cards):
            self.current_card = self.review_cards[self.current_index]
            self.word_label.configure(text=self.current_card.word)
            
            context_text = ""
            if self.current_card.context:
                context_text = f"Context: {self.current_card.context}"
            if self.current_card.tags:
                context_text += f"\nType: {self.current_card.word_type}"
            
            self.context_label.configure(text=context_text)
            self.answer_revealed = False
            self.answer_frame.grid_remove()
            self.show_answer_btn.grid()
            self.rating_frame.grid_remove()
            self.update_progress_display()
        else:
            self.end_review_session()
    
    def show_answer(self):
        """Reveal the answer"""
        if self.current_card and not self.answer_revealed:
            self.answer_label.configure(text=self.current_card.translation)
            self.answer_frame.grid()
            self.show_answer_btn.grid_remove()
            self.rating_frame.grid()
            self.answer_revealed = True
    
    def rate_card(self, quality: int):
        """Rate the current card and move to next"""
        if self.current_card:
            spaced_repetition.review_card(self.current_card.word, quality)
            
            # Update session stats
            if quality >= 3:
                self.session_stats["correct"] += 1
            self.session_stats["total"] += 1
            
            self.current_index += 1
            self.load_current_card()
            self.update_session_stats()
    
    def skip_card(self):
        """Skip the current card"""
        if self.current_card:
            self.current_index += 1
            self.load_current_card()
    
    def end_review_session(self):
        """End the current review session"""
        if self.session_stats["total"] > 0:
            accuracy = (self.session_stats["correct"] / self.session_stats["total"]) * 100
            messagebox.showinfo(
                "Session Complete",
                f"Great job! 🎉\n\n"
                f"Cards reviewed: {self.session_stats['total']}\n"
                f"Accuracy: {accuracy:.1f}%\n"
                f"Keep up the excellent work!"
            )
        
        self.word_label.configure(text="Session Complete!")
        self.context_label.configure(text="Click 'Start Review' for another session.")
        self.answer_frame.grid_remove()
        self.show_answer_btn.grid()
        self.rating_frame.grid_remove()
    
    def update_progress_display(self):
        """Update the progress bar and labels"""
        if self.review_cards:
            progress = self.current_index / len(self.review_cards)
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"{self.current_index}/{len(self.review_cards)}")
        else:
            self.progress_bar.set(0)
            self.progress_label.configure(text="0/0")
    
    def update_session_stats(self):
        """Update session statistics display"""
        self.session_label.configure(
            text=f"Session: {self.session_stats['correct']}/{self.session_stats['total']}"
        )
    
    def refresh_statistics(self):
        """Refresh the statistics display"""
        # Remove existing stats cards
        for widget in self.stats_frame.winfo_children():
            if widget.winfo_class() == "CTkFrame":
                widget.destroy()
        
        # Recreate statistics
        self.create_statistics_view()
    
    def update_daily_limit(self, value):
        """Update daily review limit"""
        self.limit_label.configure(text=f"{int(value)} cards per day")
    
    def export_data(self):
        """Export vocabulary data"""
        try:
            data = spaced_repetition.export_vocabulary()
            # In a real implementation, this would open a file dialog
            messagebox.showinfo("Export", f"Exported {len(data)} vocabulary items!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {e}")
    
    def import_data(self):
        """Import vocabulary data"""
        # In a real implementation, this would open a file dialog
        messagebox.showinfo("Import", "Import functionality would open a file dialog.")
    
    def reset_progress(self):
        """Reset all learning progress"""
        if messagebox.askyesno("Reset Progress", "Are you sure you want to reset all progress?"):
            # Reset all cards
            for word in list(spaced_repetition.cards.keys()):
                spaced_repetition.reset_card(word)
            messagebox.showinfo("Reset", "All progress has been reset.")
            self.refresh_statistics()
            self.refresh_review_session()
