import customtkinter as ctk
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from user_progress import progress_manager
import numpy as np


class ProgressDashboardFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_dashboard()
        self.refresh_data()
    
    def setup_dashboard(self):
        self.master.change_geometry("1000x800")
        
        # Main frame
        self.dashboard_frame = ctk.CTkFrame(self, width=1000, height=800)
        self.dashboard_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title
        self.title_label = ctk.CTkLabel(self.dashboard_frame, text="Learning Progress Dashboard",
                                       font=("Old English Text", 24, "bold"))
        self.title_label.place(relx=0.35, rely=0.02)
        
        # Back button
        self.back_button = ctk.CTkLabel(self.dashboard_frame, text='<--',
                                       font=("Old English Text", 20, "bold"))
        self.back_button.place(relx=0.02, rely=0.02)
        self.back_button.bind("<Button-1>", lambda event:
        self.master.open_frame("progress_dashboard", 'mainmenuframe'))
        self.back_button.bind("<Enter>", lambda event:
        self.back_button.configure(cursor="hand2", text_color="green"))
        self.back_button.bind("<Leave>", lambda event:
        self.back_button.configure(cursor="arrow", text_color="white"))
        
        # Statistics cards row
        stats_frame = ctk.CTkFrame(self.dashboard_frame)
        stats_frame.place(relx=0.02, rely=0.08, relwidth=0.96, relheight=0.15)
        
        self.create_stats_cards(stats_frame)
        
        # Charts area
        charts_frame = ctk.CTkFrame(self.dashboard_frame)
        charts_frame.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.5)
        
        self.create_progress_charts(charts_frame)
        
        # Achievements and recommendations
        bottom_frame = ctk.CTkFrame(self.dashboard_frame)
        bottom_frame.place(relx=0.02, rely=0.77, relwidth=0.96, relheight=0.21)
        
        self.create_achievements_section(bottom_frame)
    
    def create_stats_cards(self, parent):
        """Create statistics cards showing key metrics"""
        summary = progress_manager.get_detailed_progress_summary()
        
        stats = [
            ("Total Score", summary.get("total_score", 0), "🎯"),
            ("Sessions", summary.get("sessions_completed", 0), "📚"),
            ("Current Streak", summary.get("current_streak", 0), "🔥"),
            ("Accuracy", f"{summary.get('overall_accuracy', 0)}%", "✅"),
            ("Time Practiced", f"{summary.get('time_practiced', 0)}min", "⏱️"),
            ("Words Learned", summary.get("words_learned", 0), "💭")
        ]
        
        for i, (title, value, icon) in enumerate(stats):
            card_frame = ctk.CTkFrame(parent)
            card_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            parent.grid_columnconfigure(i, weight=1)
            
            icon_label = ctk.CTkLabel(card_frame, text=icon, font=("Arial", 20))
            icon_label.pack(pady=5)
            
            value_label = ctk.CTkLabel(card_frame, text=str(value), 
                                      font=("Arial", 16, "bold"))
            value_label.pack()
            
            title_label = ctk.CTkLabel(card_frame, text=title, 
                                      font=("Arial", 10))
            title_label.pack(pady=2)
    
    def create_progress_charts(self, parent):
        """Create progress visualization charts"""
        # Create notebook for different chart views
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Progress over time chart
        progress_frame = ctk.CTkFrame(notebook)
        notebook.add(progress_frame, text="Progress Over Time")
        self.create_progress_timeline_chart(progress_frame)
        
        # Word type accuracy chart
        accuracy_frame = ctk.CTkFrame(notebook)
        notebook.add(accuracy_frame, text="Word Type Accuracy")
        self.create_accuracy_chart(accuracy_frame)
        
        # Level progress chart
        level_frame = ctk.CTkFrame(notebook)
        notebook.add(level_frame, text="Level Progress")
        self.create_level_progress_chart(level_frame)
    
    def create_progress_timeline_chart(self, parent):
        """Create a timeline chart showing progress over time"""
        try:
            fig, ax = plt.subplots(figsize=(8, 4), facecolor='#2b2b2b')
            ax.set_facecolor('#2b2b2b')
            
            # Get session history
            session_history = progress_manager.statistics.get("session_history", [])
            
            if session_history:
                # Extract data for plotting
                dates = []
                scores = []
                accuracies = []
                
                for session in session_history[-30:]:  # Last 30 sessions
                    try:
                        date = datetime.fromisoformat(session.get("timestamp", "")).date()
                        dates.append(date)
                        scores.append(session.get("score", 0))
                        
                        questions = session.get("questions_attempted", 1)
                        correct = session.get("correct_answers", 0)
                        accuracy = (correct / questions) * 100 if questions > 0 else 0
                        accuracies.append(accuracy)
                    except:
                        continue
                
                if dates:
                    # Plot score trend
                    ax2 = ax.twinx()
                    
                    line1 = ax.plot(dates, scores, 'b-o', linewidth=2, markersize=4, 
                                   label='Score', color='#4CAF50')
                    line2 = ax2.plot(dates, accuracies, 'r-s', linewidth=2, markersize=4, 
                                    label='Accuracy %', color='#FF9800')
                    
                    ax.set_xlabel('Date', color='white')
                    ax.set_ylabel('Score', color='#4CAF50')
                    ax2.set_ylabel('Accuracy (%)', color='#FF9800')
                    
                    # Formatting
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
                    
                    # Style
                    ax.tick_params(colors='white', rotation=45)
                    ax2.tick_params(colors='white')
                    ax.grid(True, alpha=0.3)
                    
                    # Legend
                    lines = line1 + line2
                    labels = [l.get_label() for l in lines]
                    ax.legend(lines, labels, loc='upper left')
                    
                    plt.tight_layout()
            else:
                ax.text(0.5, 0.5, 'No session data available', 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, color='white', fontsize=14)
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            print(f"Error creating progress chart: {e}")
            error_label = ctk.CTkLabel(parent, text="Chart unavailable - install matplotlib")
            error_label.pack(pady=50)
    
    def create_accuracy_chart(self, parent):
        """Create a bar chart showing accuracy by word type"""
        try:
            fig, ax = plt.subplots(figsize=(8, 4), facecolor='#2b2b2b')
            ax.set_facecolor('#2b2b2b')
            
            word_progress = progress_manager.user_progress.get("word_type_progress", {})
            
            if word_progress:
                word_types = list(word_progress.keys())
                accuracies = [progress.get("accuracy", 0) * 100 for progress in word_progress.values()]
                total_seen = [progress.get("total_seen", 0) for progress in word_progress.values()]
                
                # Create bars with different colors
                colors = ['#4CAF50', '#2196F3', '#FF9800', '#E91E63']
                bars = ax.bar(word_types, accuracies, color=colors[:len(word_types)])
                
                # Add total seen as text on bars
                for bar, total in zip(bars, total_seen):
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                               f'{total} words', ha='center', va='bottom', color='white')
                
                ax.set_ylabel('Accuracy (%)', color='white')
                ax.set_xlabel('Word Types', color='white')
                ax.set_ylim(0, 100)
                
                # Style
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                plt.tight_layout()
            else:
                ax.text(0.5, 0.5, 'No word type data available', 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, color='white', fontsize=14)
            
            # Embed chart
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            print(f"Error creating accuracy chart: {e}")
            error_label = ctk.CTkLabel(parent, text="Chart unavailable - install matplotlib")
            error_label.pack(pady=50)
    
    def create_level_progress_chart(self, parent):
        """Create a progress chart for different proficiency levels"""
        try:
            fig, ax = plt.subplots(figsize=(8, 4), facecolor='#2b2b2b')
            ax.set_facecolor('#2b2b2b')
            
            level_progress = progress_manager.user_progress.get("level_progress", {})
            
            if level_progress:
                levels = list(level_progress.keys())
                scores = [progress.get("score", 0) for progress in level_progress.values()]
                completed = [progress.get("completed", False) for progress in level_progress.values()]
                
                # Create horizontal bar chart
                colors = ['#4CAF50' if comp else '#757575' for comp in completed]
                bars = ax.barh(levels, scores, color=colors)
                
                # Add completion status
                for i, (bar, comp, score) in enumerate(zip(bars, completed, scores)):
                    status = "✓ Completed" if comp else f"Score: {score}"
                    ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                           status, va='center', color='white')
                
                ax.set_xlabel('Score', color='white')
                ax.set_ylabel('Proficiency Levels', color='white')
                
                # Style
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                plt.tight_layout()
            else:
                ax.text(0.5, 0.5, 'No level data available', 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, color='white', fontsize=14)
            
            # Embed chart
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            print(f"Error creating level chart: {e}")
            error_label = ctk.CTkLabel(parent, text="Chart unavailable - install matplotlib")
            error_label.pack(pady=50)
    
    def create_achievements_section(self, parent):
        """Create achievements and recommendations section"""
        # Left side - Achievements
        achievements_frame = ctk.CTkFrame(parent)
        achievements_frame.place(relx=0.02, rely=0.02, relwidth=0.46, relheight=0.96)
        
        achievements_title = ctk.CTkLabel(achievements_frame, text="🏆 Achievements",
                                         font=("Arial", 16, "bold"))
        achievements_title.pack(pady=10)
        
        achievements_text = ctk.CTkTextbox(achievements_frame, height=120)
        achievements_text.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Load achievements
        achievements = progress_manager.user_progress.get("achievements", [])
        if achievements:
            achievements_content = "\n".join([f"🏆 {achievement}" for achievement in achievements])
        else:
            achievements_content = "No achievements yet!\nKeep practicing to unlock achievements."
        
        achievements_text.insert("0.0", achievements_content)
        
        # Right side - Recommendations
        recommendations_frame = ctk.CTkFrame(parent)
        recommendations_frame.place(relx=0.52, rely=0.02, relwidth=0.46, relheight=0.96)
        
        recommendations_title = ctk.CTkLabel(recommendations_frame, text="💡 Recommendations",
                                           font=("Arial", 16, "bold"))
        recommendations_title.pack(pady=10)
        
        recommendations_text = ctk.CTkTextbox(recommendations_frame, height=120)
        recommendations_text.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Load recommendations
        recommendations = progress_manager.get_recommendations()
        if recommendations:
            recommendations_content = "\n".join([f"• {rec}" for rec in recommendations])
        else:
            recommendations_content = "Great work! Keep up your current learning routine."
        
        recommendations_text.insert("0.0", recommendations_content)
    
    def refresh_data(self):
        """Refresh dashboard data"""
        # This would typically reload all the charts and statistics
        # For now, we'll just update the display
        pass
    
    def export_report(self):
        """Export progress report"""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Progress Report"
        )
        
        if filename:
            progress_manager.export_progress_report(filename)
            # Show success message
            success_popup = ctk.CTkToplevel(self)
            success_popup.title("Export Complete")
            success_popup.geometry("300x100")
            
            success_label = ctk.CTkLabel(success_popup, text="Progress report exported successfully!")
            success_label.pack(pady=30)


# Import matplotlib and ttk with fallback
try:
    import matplotlib
    matplotlib.use('TkAgg')  # Set backend before importing pyplot
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.dates as mdates
    # Set dark theme for matplotlib
    plt.style.use('dark_background')
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available. Install with: pip install matplotlib")

try:
    from tkinter import ttk
    TTK_AVAILABLE = True
except ImportError:
    TTK_AVAILABLE = False
