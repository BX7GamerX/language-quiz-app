import json
import os
from datetime import datetime, timedelta
import csv
from typing import Dict, List, Any


class UserProgressManager:
    def __init__(self, user_data_path="../userdata"):
        self.user_data_path = user_data_path
        self.progress_file = os.path.join(user_data_path, "user_progress.json")
        self.statistics_file = os.path.join(user_data_path, "statistics.json")
        self.schedule_file = os.path.join(user_data_path, "practice_schedule.json")
        
        # Ensure directory exists
        os.makedirs(user_data_path, exist_ok=True)
        
        self.user_progress = self.load_progress()
        self.statistics = self.load_statistics()
        self.schedule = self.load_schedule()
    
    def load_progress(self) -> Dict[str, Any]:
        """Load user progress from file"""
        default_progress = {
            "current_level": "A1",
            "total_score": 0,
            "sessions_completed": 0,
            "words_learned": [],
            "difficult_words": [],
            "achievements": [],
            "daily_streaks": [],
            "last_practice_date": None,
            "level_progress": {
                "A1": {"completed": False, "score": 0, "time_spent": 0},
                "A2": {"completed": False, "score": 0, "time_spent": 0},
                "B1": {"completed": False, "score": 0, "time_spent": 0},
                "B2": {"completed": False, "score": 0, "time_spent": 0}
            },
            "word_type_progress": {
                "nouns": {"mastered": 0, "total_seen": 0, "accuracy": 0.0},
                "verbs": {"mastered": 0, "total_seen": 0, "accuracy": 0.0},
                "adjectives": {"mastered": 0, "total_seen": 0, "accuracy": 0.0},
                "adverbs": {"mastered": 0, "total_seen": 0, "accuracy": 0.0}
            }
        }
        
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    loaded_progress = json.load(f)
                    # Merge with default to ensure all keys exist
                    for key in default_progress:
                        if key not in loaded_progress:
                            loaded_progress[key] = default_progress[key]
                    return loaded_progress
        except Exception as e:
            print(f"Error loading progress: {e}")
        
        return default_progress
    
    def save_progress(self):
        """Save user progress to file"""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_progress, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving progress: {e}")
    
    def load_statistics(self) -> Dict[str, Any]:
        """Load user statistics"""
        default_stats = {
            "total_time_practiced": 0,
            "average_session_time": 0,
            "best_streak": 0,
            "current_streak": 0,
            "total_questions_answered": 0,
            "correct_answers": 0,
            "overall_accuracy": 0.0,
            "daily_goals_met": 0,
            "preferred_practice_time": "morning",
            "session_history": []
        }
        
        try:
            if os.path.exists(self.statistics_file):
                with open(self.statistics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading statistics: {e}")
        
        return default_stats
    
    def save_statistics(self):
        """Save user statistics"""
        try:
            with open(self.statistics_file, 'w', encoding='utf-8') as f:
                json.dump(self.statistics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving statistics: {e}")
    
    def load_schedule(self) -> Dict[str, Any]:
        """Load practice schedule"""
        default_schedule = {
            "daily_goal_minutes": 15,
            "preferred_times": ["morning"],
            "focus_areas": ["mixed"],
            "difficulty_level": "intermediate",
            "reminders_enabled": True,
            "weekly_schedule": {
                "monday": {"active": True, "focus": "vocabulary", "duration": 15},
                "tuesday": {"active": True, "focus": "grammar", "duration": 15},
                "wednesday": {"active": True, "focus": "translation", "duration": 15},
                "thursday": {"active": True, "focus": "conversation", "duration": 15},
                "friday": {"active": True, "focus": "review", "duration": 15},
                "saturday": {"active": True, "focus": "games", "duration": 20},
                "sunday": {"active": False, "focus": "rest", "duration": 0}
            }
        }
        
        try:
            if os.path.exists(self.schedule_file):
                with open(self.schedule_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading schedule: {e}")
        
        return default_schedule
    
    def save_schedule(self):
        """Save practice schedule"""
        try:
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                json.dump(self.schedule, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving schedule: {e}")
    
    def record_practice_session(self, session_data: Dict[str, Any]):
        """Record a completed practice session"""
        session_data["timestamp"] = datetime.now().isoformat()
        
        # Update progress
        self.user_progress["total_score"] += session_data.get("score", 0)
        self.user_progress["sessions_completed"] += 1
        self.user_progress["last_practice_date"] = datetime.now().date().isoformat()
        
        # Update word type progress
        word_type = session_data.get("word_type", "mixed")
        if word_type in self.user_progress["word_type_progress"]:
            progress = self.user_progress["word_type_progress"][word_type]
            progress["total_seen"] += session_data.get("questions_attempted", 0)
            correct = session_data.get("correct_answers", 0)
            if progress["total_seen"] > 0:
                progress["accuracy"] = (progress["accuracy"] * (progress["total_seen"] - session_data.get("questions_attempted", 0)) + correct) / progress["total_seen"]
        
        # Update statistics
        self.statistics["total_time_practiced"] += session_data.get("duration_minutes", 0)
        self.statistics["total_questions_answered"] += session_data.get("questions_attempted", 0)
        self.statistics["correct_answers"] += session_data.get("correct_answers", 0)
        
        if self.statistics["total_questions_answered"] > 0:
            self.statistics["overall_accuracy"] = self.statistics["correct_answers"] / self.statistics["total_questions_answered"]
        
        # Update session history
        self.statistics["session_history"].append(session_data)
        
        # Keep only last 100 sessions
        if len(self.statistics["session_history"]) > 100:
            self.statistics["session_history"] = self.statistics["session_history"][-100:]
        
        # Update streaks
        self.update_streaks()
        
        # Check for achievements
        self.check_achievements(session_data)
        
        # Save all data
        self.save_progress()
        self.save_statistics()
    
    def update_streaks(self):
        """Update daily practice streaks"""
        today = datetime.now().date()
        
        if self.user_progress["last_practice_date"]:
            last_date = datetime.fromisoformat(self.user_progress["last_practice_date"]).date()
            
            if last_date == today:
                # Already practiced today, maintain streak
                pass
            elif last_date == today - timedelta(days=1):
                # Practiced yesterday, increment streak
                self.statistics["current_streak"] += 1
                if self.statistics["current_streak"] > self.statistics["best_streak"]:
                    self.statistics["best_streak"] = self.statistics["current_streak"]
            else:
                # Streak broken
                self.statistics["current_streak"] = 1
        else:
            # First practice session
            self.statistics["current_streak"] = 1
    
    def check_achievements(self, session_data: Dict[str, Any]):
        """Check and award achievements"""
        achievements = []
        
        # Score-based achievements
        if self.user_progress["total_score"] >= 100 and "First Century" not in self.user_progress["achievements"]:
            achievements.append("First Century")
        
        if self.user_progress["total_score"] >= 1000 and "Score Master" not in self.user_progress["achievements"]:
            achievements.append("Score Master")
        
        # Streak achievements
        if self.statistics["current_streak"] >= 7 and "Week Warrior" not in self.user_progress["achievements"]:
            achievements.append("Week Warrior")
        
        if self.statistics["current_streak"] >= 30 and "Month Master" not in self.user_progress["achievements"]:
            achievements.append("Month Master")
        
        # Accuracy achievements
        if self.statistics["overall_accuracy"] >= 0.9 and "Accuracy Ace" not in self.user_progress["achievements"]:
            achievements.append("Accuracy Ace")
        
        # Session count achievements
        if self.user_progress["sessions_completed"] >= 50 and "Persistent Learner" not in self.user_progress["achievements"]:
            achievements.append("Persistent Learner")
        
        # Add new achievements
        self.user_progress["achievements"].extend(achievements)
        
        return achievements
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of user progress"""
        return {
            "level": self.user_progress["current_level"],
            "total_score": self.user_progress["total_score"],
            "sessions_completed": self.user_progress["sessions_completed"],
            "current_streak": self.statistics["current_streak"],
            "overall_accuracy": round(self.statistics["overall_accuracy"] * 100, 1),
            "achievements": len(self.user_progress["achievements"]),
            "time_practiced": self.statistics["total_time_practiced"],
            "words_learned": len(self.user_progress["words_learned"])
        }
    
    def get_recommendations(self) -> List[str]:
        """Get personalized learning recommendations"""
        recommendations = []
        
        # Check accuracy by word type
        for word_type, progress in self.user_progress["word_type_progress"].items():
            if progress["total_seen"] > 10 and progress["accuracy"] < 0.7:
                recommendations.append(f"Focus more on {word_type} - current accuracy: {progress['accuracy']*100:.1f}%")
        
        # Check practice frequency
        if self.statistics["current_streak"] == 0:
            recommendations.append("Try to practice daily to build a learning streak!")
        
        # Check session length
        if self.statistics["total_questions_answered"] > 0:
            avg_session_length = self.statistics["total_time_practiced"] / self.user_progress["sessions_completed"]
            if avg_session_length < 10:
                recommendations.append("Consider longer practice sessions (15-20 minutes) for better retention")
        
        # Level progression
        current_level_progress = self.user_progress["level_progress"][self.user_progress["current_level"]]
        if current_level_progress["score"] > 500 and not current_level_progress["completed"]:
            recommendations.append(f"You're ready to advance from {self.user_progress['current_level']} level!")
        
        return recommendations
    
    def export_progress_report(self, filename):
        """Export comprehensive progress report to CSV"""
        import csv
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Header
                writer.writerow(["LingoLeap Progress Report"])
                writer.writerow([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
                writer.writerow([])
                
                # Overall Statistics
                summary = self.get_detailed_progress_summary()
                writer.writerow(["Overall Statistics"])
                writer.writerow(["Metric", "Value"])
                for key, value in summary.items():
                    writer.writerow([key.replace('_', ' ').title(), value])
                writer.writerow([])
                
                # Word Type Progress
                writer.writerow(["Word Type Progress"])
                writer.writerow(["Word Type", "Total Seen", "Correct", "Accuracy (%)", "Average Time (s)"])
                for word_type, progress in self.user_progress.get("word_type_progress", {}).items():
                    accuracy = progress.get("accuracy", 0) * 100
                    writer.writerow([
                        word_type.title(),
                        progress.get("total_seen", 0),
                        progress.get("correct_count", 0),
                        f"{accuracy:.1f}",
                        f"{progress.get('average_time', 0):.1f}"
                    ])
                writer.writerow([])
                
                # Level Progress
                writer.writerow(["Level Progress"])
                writer.writerow(["Level", "Score", "Completed", "Sessions"])
                for level, progress in self.user_progress.get("level_progress", {}).items():
                    writer.writerow([
                        level,
                        progress.get("score", 0),
                        "Yes" if progress.get("completed", False) else "No",
                        progress.get("sessions", 0)
                    ])
                writer.writerow([])
                
                # Achievements
                writer.writerow(["Achievements"])
                for achievement in self.user_progress["achievements"]:
                    writer.writerow([achievement])
                writer.writerow([])
                
                # Recent session history (last 10 sessions)
                writer.writerow(["Recent Sessions"])
                writer.writerow(["Date", "Score", "Questions", "Correct", "Accuracy (%)", "Duration (min)"])
                for session in self.statistics["session_history"][-10:]:
                    accuracy = (session.get("correct_answers", 0) / session.get("questions_attempted", 1)) * 100
                    writer.writerow([
                        session.get("timestamp", "")[:10],
                        session.get("score", 0),
                        session.get("questions_attempted", 0),
                        session.get("correct_answers", 0),
                        f"{accuracy:.1f}",
                        session.get("duration_minutes", 0)
                    ])
                    
        except Exception as e:
            print(f"Error exporting progress report: {e}")
    
    def get_detailed_progress_summary(self):
        """Get comprehensive progress summary for dashboard"""
        # Calculate total practice time
        total_time = sum(session.get("duration_minutes", 0) for session in self.statistics.get("session_history", []))
        
        # Calculate overall accuracy
        total_questions = sum(session.get("questions_attempted", 0) for session in self.statistics.get("session_history", []))
        total_correct = sum(session.get("correct_answers", 0) for session in self.statistics.get("session_history", []))
        overall_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        # Count words learned (words seen more than 3 times)
        words_learned = 0
        for progress in self.user_progress.get("word_type_progress", {}).values():
            words_learned += sum(1 for count in progress.get("word_history", {}).values() if count >= 3)
        
        return {
            "total_score": self.user_progress.get("total_score", 0),
            "sessions_completed": len(self.statistics.get("session_history", [])),
            "current_streak": self.statistics.get("current_streak", 0),
            "overall_accuracy": round(overall_accuracy, 1),
            "time_practiced": total_time,
            "words_learned": words_learned,
            "achievements_unlocked": len(self.user_progress.get("achievements", [])),
            "levels_completed": sum(1 for progress in self.user_progress.get("level_progress", {}).values() 
                                  if progress.get("completed", False))
        }
    
    def record_session(self, session_data):
        """Record a learning session"""
        # Add timestamp if not provided
        if 'timestamp' not in session_data:
            session_data['timestamp'] = datetime.now().isoformat()
        
        # Add session to history
        self.statistics["session_history"].append(session_data)
        
        # Update overall statistics
        self.statistics["total_questions_answered"] += session_data.get("questions_attempted", 0)
        self.statistics["total_time_practiced"] += session_data.get("duration_minutes", 0)
        
        # Update accuracy
        total_questions = sum(s.get("questions_attempted", 0) for s in self.statistics["session_history"])
        total_correct = sum(s.get("correct_answers", 0) for s in self.statistics["session_history"])
        self.statistics["overall_accuracy"] = (total_correct / total_questions) if total_questions > 0 else 0
        
        # Update streak
        if session_data.get("correct_answers", 0) > 0:
            self.statistics["current_streak"] += 1
            if self.statistics["current_streak"] > self.statistics.get("best_streak", 0):
                self.statistics["best_streak"] = self.statistics["current_streak"]
        else:
            self.statistics["current_streak"] = 0
        
        # Update user progress
        self.user_progress["total_score"] += session_data.get("score", 0)
        self.user_progress["sessions_completed"] += 1
        
        # Save progress
        self.save_progress()
        self.save_statistics()
    
    def reset_progress(self, confirm=False):
        """Reset all user progress (use with caution)"""
        if not confirm:
            return False
        
        # Backup current data
        backup_file = os.path.join(self.user_data_path, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        try:
            backup_data = {
                "progress": self.user_progress,
                "statistics": self.statistics,
                "schedule": self.schedule
            }
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
        
        # Reset to defaults
        self.user_progress = self.load_progress()  # This will load defaults if file doesn't exist
        self.statistics = self.load_statistics()
        self.schedule = self.load_schedule()
        
        # Remove existing files
        for file_path in [self.progress_file, self.statistics_file, self.schedule_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return True


# Global instance
progress_manager = UserProgressManager()
