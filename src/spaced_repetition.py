"""
Spaced Repetition System for LingoLeap
====================================

An advanced spaced repetition algorithm optimized for language learning,
incorporating the SuperMemo SM-2 algorithm with German-specific enhancements.
"""

import json
import os
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class ReviewCard:
    """Represents a single vocabulary item for spaced repetition"""
    word: str
    translation: str
    word_type: str
    difficulty: float = 2.5  # Initial difficulty (1.3-5.0 scale)
    interval: int = 1  # Days until next review
    repetitions: int = 0  # Number of successful reviews
    last_reviewed: str = ""  # ISO timestamp of last review
    next_review: str = ""  # ISO timestamp of next review
    context: str = ""  # Example sentence or context
    tags: List[str] = None  # Additional categorization
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if not self.last_reviewed:
            self.last_reviewed = datetime.now().isoformat()
        if not self.next_review:
            self.next_review = datetime.now().isoformat()


class SpacedRepetitionSystem:
    """Advanced spaced repetition system for German language learning"""
    
    def __init__(self):
        self.cards: Dict[str, ReviewCard] = {}
        self.data_file = os.path.join("user_data", "spaced_repetition.json")
        self.load_cards()
        
        # SM-2 Algorithm constants
        self.MIN_DIFFICULTY = 1.3
        self.MAX_DIFFICULTY = 5.0
        self.INITIAL_INTERVAL = 1
        self.SECOND_INTERVAL = 6
        self.DIFFICULTY_THRESHOLD = 2.5
    
    def load_cards(self):
        """Load review cards from storage"""
        try:
            os.makedirs("user_data", exist_ok=True)
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cards = {
                        word: ReviewCard(**card_data) 
                        for word, card_data in data.items()
                    }
        except Exception as e:
            print(f"Error loading spaced repetition data: {e}")
            self.cards = {}
    
    def save_cards(self):
        """Save review cards to storage"""
        try:
            data = {
                word: {
                    'word': card.word,
                    'translation': card.translation,
                    'word_type': card.word_type,
                    'difficulty': card.difficulty,
                    'interval': card.interval,
                    'repetitions': card.repetitions,
                    'last_reviewed': card.last_reviewed,
                    'next_review': card.next_review,
                    'context': card.context,
                    'tags': card.tags
                }
                for word, card in self.cards.items()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving spaced repetition data: {e}")
    
    def add_word(self, word: str, translation: str, word_type: str, 
                 context: str = "", tags: List[str] = None):
        """Add a new word to the spaced repetition system"""
        if word not in self.cards:
            card = ReviewCard(
                word=word,
                translation=translation,
                word_type=word_type,
                context=context,
                tags=tags or []
            )
            self.cards[word] = card
            self.save_cards()
            return True
        return False
    
    def get_due_cards(self, max_cards: int = 20) -> List[ReviewCard]:
        """Get cards that are due for review"""
        now = datetime.now()
        due_cards = []
        
        for card in self.cards.values():
            next_review = datetime.fromisoformat(card.next_review)
            if next_review <= now:
                due_cards.append(card)
        
        # Sort by priority (overdue cards first, then by difficulty)
        due_cards.sort(key=lambda c: (
            datetime.fromisoformat(c.next_review),
            -c.difficulty
        ))
        
        return due_cards[:max_cards]
    
    def review_card(self, word: str, quality: int) -> bool:
        """
        Review a card with quality rating (0-5)
        0: Complete blackout
        1: Incorrect response; correct answer recalled
        2: Incorrect response; correct answer seemed easy to recall  
        3: Correct response recalled with serious difficulty
        4: Correct response after a hesitation
        5: Perfect response
        """
        if word not in self.cards:
            return False
        
        card = self.cards[word]
        now = datetime.now()
        
        # Update last reviewed time
        card.last_reviewed = now.isoformat()
        
        # SM-2 Algorithm implementation
        if quality >= 3:  # Successful recall
            if card.repetitions == 0:
                card.interval = self.INITIAL_INTERVAL
            elif card.repetitions == 1:
                card.interval = self.SECOND_INTERVAL
            else:
                card.interval = int(card.interval * card.difficulty)
            
            card.repetitions += 1
        else:  # Failed recall
            card.repetitions = 0
            card.interval = self.INITIAL_INTERVAL
        
        # Update difficulty factor
        old_difficulty = card.difficulty
        card.difficulty = max(
            self.MIN_DIFFICULTY,
            min(
                self.MAX_DIFFICULTY,
                old_difficulty + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            )
        )
        
        # Calculate next review date
        next_review_date = now + timedelta(days=card.interval)
        card.next_review = next_review_date.isoformat()
        
        self.save_cards()
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics"""
        now = datetime.now()
        total_cards = len(self.cards)
        
        if total_cards == 0:
            return {"total_cards": 0, "due_cards": 0, "mastered_cards": 0}
        
        due_cards = len([
            card for card in self.cards.values()
            if datetime.fromisoformat(card.next_review) <= now
        ])
        
        mastered_cards = len([
            card for card in self.cards.values()
            if card.repetitions >= 5 and card.difficulty >= 2.5
        ])
        
        new_cards = len([
            card for card in self.cards.values()
            if card.repetitions == 0
        ])
        
        learning_cards = total_cards - new_cards - mastered_cards
        
        # Average retention rate
        successful_reviews = sum(1 for card in self.cards.values() if card.repetitions > 0)
        retention_rate = (successful_reviews / total_cards * 100) if total_cards > 0 else 0
        
        return {
            "total_cards": total_cards,
            "due_cards": due_cards,
            "new_cards": new_cards,
            "learning_cards": learning_cards,
            "mastered_cards": mastered_cards,
            "retention_rate": round(retention_rate, 1)
        }
    
    def get_word_types_breakdown(self) -> Dict[str, int]:
        """Get breakdown of cards by word type"""
        breakdown = {}
        for card in self.cards.values():
            word_type = card.word_type
            breakdown[word_type] = breakdown.get(word_type, 0) + 1
        return breakdown
    
    def get_difficulty_distribution(self) -> Dict[str, int]:
        """Get distribution of cards by difficulty level"""
        distribution = {"Easy": 0, "Medium": 0, "Hard": 0}
        
        for card in self.cards.values():
            if card.difficulty <= 2.0:
                distribution["Easy"] += 1
            elif card.difficulty <= 3.0:
                distribution["Medium"] += 1
            else:
                distribution["Hard"] += 1
        
        return distribution
    
    def suggest_review_schedule(self) -> Dict[str, int]:
        """Suggest optimal daily review schedule"""
        now = datetime.now()
        schedule = {}
        
        for i in range(7):  # Next 7 days
            date = now + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            cards_due = len([
                card for card in self.cards.values()
                if datetime.fromisoformat(card.next_review).date() == date.date()
            ])
            
            schedule[date_str] = cards_due
        
        return schedule
    
    def reset_card(self, word: str):
        """Reset a card's progress"""
        if word in self.cards:
            card = self.cards[word]
            card.repetitions = 0
            card.interval = self.INITIAL_INTERVAL
            card.difficulty = 2.5
            card.next_review = datetime.now().isoformat()
            self.save_cards()
    
    def delete_card(self, word: str):
        """Remove a card from the system"""
        if word in self.cards:
            del self.cards[word]
            self.save_cards()
    
    def import_vocabulary(self, vocabulary_data: List[Dict[str, str]]):
        """Import vocabulary from external source"""
        imported_count = 0
        
        for item in vocabulary_data:
            if all(key in item for key in ['word', 'translation', 'word_type']):
                if self.add_word(
                    word=item['word'],
                    translation=item['translation'],
                    word_type=item['word_type'],
                    context=item.get('context', ''),
                    tags=item.get('tags', [])
                ):
                    imported_count += 1
        
        return imported_count
    
    def export_vocabulary(self) -> List[Dict[str, Any]]:
        """Export vocabulary data"""
        return [
            {
                'word': card.word,
                'translation': card.translation,
                'word_type': card.word_type,
                'difficulty': card.difficulty,
                'repetitions': card.repetitions,
                'context': card.context,
                'tags': card.tags
            }
            for card in self.cards.values()
        ]
    
    def get_challenging_words(self, limit: int = 10) -> List[ReviewCard]:
        """Get the most challenging words for focused practice"""
        challenging = [
            card for card in self.cards.values()
            if card.difficulty > 3.0 or (card.repetitions > 0 and card.interval < 3)
        ]
        
        challenging.sort(key=lambda c: (-c.difficulty, -c.repetitions))
        return challenging[:limit]
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Generate learning insights and recommendations"""
        stats = self.get_statistics()
        word_types = self.get_word_types_breakdown()
        challenging = self.get_challenging_words(5)
        
        insights = {
            "daily_review_recommendation": min(20, max(5, stats["due_cards"])),
            "weakest_word_type": max(word_types.items(), key=lambda x: x[1])[0] if word_types else "None",
            "challenging_words": [card.word for card in challenging],
            "estimated_mastery_time": self._estimate_mastery_time(),
            "current_streak": self._calculate_streak(),
            "retention_trend": "improving" if stats["retention_rate"] > 70 else "needs_work"
        }
        
        return insights
    
    def _estimate_mastery_time(self) -> str:
        """Estimate time to master current vocabulary"""
        learning_cards = sum(1 for card in self.cards.values() if card.repetitions < 5)
        
        if learning_cards == 0:
            return "Vocabulary mastered!"
        
        # Rough estimation: 2-4 weeks per difficulty level
        avg_difficulty = sum(card.difficulty for card in self.cards.values()) / len(self.cards)
        weeks = int(avg_difficulty * learning_cards / 10)
        
        return f"Approximately {max(1, weeks)} weeks"
    
    def _calculate_streak(self) -> int:
        """Calculate current learning streak"""
        # Simple streak calculation based on recent reviews
        now = datetime.now()
        streak = 0
        
        for i in range(30):  # Check last 30 days
            date = now - timedelta(days=i)
            reviews_today = len([
                card for card in self.cards.values()
                if datetime.fromisoformat(card.last_reviewed).date() == date.date()
            ])
            
            if reviews_today > 0:
                streak += 1
            else:
                break
        
        return streak


# Global spaced repetition instance
spaced_repetition = SpacedRepetitionSystem()
