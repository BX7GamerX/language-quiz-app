import customtkinter as ctk
import tkinter
import random
from functions import game_properties
from word_library import random_word_gen, translate_two


class InteractiveModeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.conversation_data = self.load_conversation_scenarios()
        self.current_scenario = None
        self.setup_interactive_mode_frame()
    
    def load_conversation_scenarios(self):
        """Load conversation scenarios for interactive mode"""
        return {
            "restaurant": {
                "title": "At the Restaurant",
                "scenario": [
                    ("Waiter", "Guten Tag! Was möchten Sie bestellen?", "Good day! What would you like to order?"),
                    ("Customer", "__USER_INPUT__", ""),
                    ("Waiter", "Sehr gut! Möchten Sie etwas zu trinken?", "Very good! Would you like something to drink?"),
                    ("Customer", "__USER_INPUT__", ""),
                    ("Waiter", "Perfekt! Das dauert etwa 15 Minuten.", "Perfect! That will take about 15 minutes.")
                ]
            },
            "shopping": {
                "title": "Shopping",
                "scenario": [
                    ("Shopkeeper", "Kann ich Ihnen helfen?", "Can I help you?"),
                    ("Customer", "__USER_INPUT__", ""),
                    ("Shopkeeper", "Das kostet 25 Euro.", "That costs 25 euros."),
                    ("Customer", "__USER_INPUT__", ""),
                    ("Shopkeeper", "Vielen Dank! Auf Wiedersehen!", "Thank you very much! Goodbye!")
                ]
            },
            "directions": {
                "title": "Asking for Directions",
                "scenario": [
                    ("Tourist", "Entschuldigung, wo ist der Bahnhof?", "Excuse me, where is the train station?"),
                    ("Local", "__USER_INPUT__", ""),
                    ("Tourist", "Wie lange dauert es zu Fuß?", "How long does it take on foot?"),
                    ("Local", "__USER_INPUT__", ""),
                    ("Tourist", "Vielen Dank für Ihre Hilfe!", "Thank you very much for your help!")
                ]
            }
        }
    
    def setup_interactive_mode_frame(self):
        self.master.change_geometry("800x700")
        
        # Main frame
        self.interactive_frame = ctk.CTkFrame(self, width=800, height=700)
        self.interactive_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title
        self.title_label = ctk.CTkLabel(self.interactive_frame, text="Interactive Conversation Practice",
                                       font=("Old English Text", 20, "bold"))
        self.title_label.place(relx=0.25, rely=0.05)
        
        # Back button
        self.back_button = ctk.CTkLabel(self.interactive_frame, text='<--',
                                       font=("Old English Text", 20, "bold"))
        self.back_button.place(relx=0.05, rely=0.05)
        self.back_button.bind("<Button-1>", lambda event:
        self.master.open_frame("interactive_mode_frame", 'a2_deutsch_frame'))
        self.back_button.bind("<Enter>", lambda event:
        self.back_button.configure(cursor="hand2", text_color="green"))
        self.back_button.bind("<Leave>", lambda event:
        self.back_button.configure(cursor="arrow", text_color="white"))
        
        # Scenario selection
        self.scenario_frame = ctk.CTkFrame(self.interactive_frame)
        self.scenario_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.2)
        
        scenario_label = ctk.CTkLabel(self.scenario_frame, text="Choose a scenario:",
                                     font=("Arial", 16, "bold"))
        scenario_label.pack(pady=10)
        
        button_frame = ctk.CTkFrame(self.scenario_frame)
        button_frame.pack(pady=10)
        
        for key, scenario in self.conversation_data.items():
            btn = ctk.CTkButton(button_frame, text=scenario["title"],
                               command=lambda k=key: self.start_scenario(k))
            btn.pack(side="left", padx=10)
        
        # Conversation display
        self.conversation_frame = ctk.CTkFrame(self.interactive_frame)
        self.conversation_frame.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.45)
        
        self.conversation_text = ctk.CTkTextbox(self.conversation_frame, width=600, height=250,
                                               font=("Arial", 12))
        self.conversation_text.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Input area
        self.input_frame = ctk.CTkFrame(self.interactive_frame)
        self.input_frame.place(relx=0.1, rely=0.87, relwidth=0.8, relheight=0.1)
        
        self.user_input = ctk.CTkEntry(self.input_frame, width=500, placeholder_text="Type your response in German...")
        self.user_input.pack(side="left", padx=10, pady=10)
        
        self.submit_btn = ctk.CTkButton(self.input_frame, text="Submit", command=self.submit_response)
        self.submit_btn.pack(side="right", padx=10, pady=10)
        
        self.user_input.bind("<Return>", lambda event: self.submit_response())
    
    def start_scenario(self, scenario_key):
        """Start a conversation scenario"""
        self.current_scenario = self.conversation_data[scenario_key]
        self.scenario_step = 0
        self.conversation_text.delete("0.0", "end")
        self.conversation_text.insert("0.0", f"=== {self.current_scenario['title']} ===\n\n")
        self.next_conversation_step()
    
    def next_conversation_step(self):
        """Display the next step in the conversation"""
        if self.scenario_step < len(self.current_scenario["scenario"]):
            speaker, german_text, english_text = self.current_scenario["scenario"][self.scenario_step]
            
            if german_text == "__USER_INPUT__":
                self.conversation_text.insert("end", f"\nYou: [Your turn - respond in German]\n")
                self.user_input.configure(state="normal")
                self.submit_btn.configure(state="normal")
                self.user_input.focus()
            else:
                display_text = f"\n{speaker}: {german_text}"
                if english_text:
                    display_text += f"\n({english_text})"
                display_text += "\n"
                
                self.conversation_text.insert("end", display_text)
                self.conversation_text.see("end")
                self.scenario_step += 1
                
                if self.scenario_step < len(self.current_scenario["scenario"]):
                    self.master.after(2000, self.next_conversation_step)
                else:
                    self.conversation_text.insert("end", "\n=== Conversation Complete! ===\n")
        else:
            self.user_input.configure(state="disabled")
            self.submit_btn.configure(state="disabled")
    
    def submit_response(self):
        """Handle user response submission"""
        user_response = self.user_input.get().strip()
        if user_response:
            self.conversation_text.insert("end", f"You: {user_response}\n")
            self.conversation_text.see("end")
            self.user_input.delete(0, "end")
            
            # Simple feedback (could be enhanced with NLP)
            feedback = self.provide_feedback(user_response)
            if feedback:
                self.conversation_text.insert("end", f"💡 Tip: {feedback}\n")
            
            self.scenario_step += 1
            self.user_input.configure(state="disabled")
            self.submit_btn.configure(state="disabled")
            
            self.master.after(1000, self.next_conversation_step)
    
    def provide_feedback(self, user_input):
        """Provide simple feedback on user input"""
        common_greetings = ["hallo", "guten tag", "guten morgen", "guten abend"]
        common_politeness = ["bitte", "danke", "entschuldigung"]
        
        feedback = []
        
        user_lower = user_input.lower()
        if not any(greeting in user_lower for greeting in common_greetings) and self.scenario_step == 1:
            feedback.append("Consider starting with a greeting like 'Hallo' or 'Guten Tag'")
        
        if not any(polite in user_lower for polite in common_politeness):
            feedback.append("German conversations often include polite words like 'bitte' or 'danke'")
        
        return "; ".join(feedback) if feedback else None


class AdvancedTranslationFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_advanced_translation_frame()
    
    def setup_advanced_translation_frame(self):
        self.master.change_geometry("600x700")
        
        # Main frame
        self.advanced_frame = ctk.CTkFrame(self, width=600, height=700)
        self.advanced_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title
        self.title_label = ctk.CTkLabel(self.advanced_frame, text="Advanced Translation Challenge",
                                       font=("Old English Text", 20, "bold"))
        self.title_label.place(relx=0.2, rely=0.05)
        
        # Back button
        self.back_button = ctk.CTkLabel(self.advanced_frame, text='<--',
                                       font=("Old English Text", 20, "bold"))
        self.back_button.place(relx=0.05, rely=0.05)
        self.back_button.bind("<Button-1>", lambda event:
        self.master.open_frame("advanced_translation_frame", 'b1_deutsch_frame'))
        self.back_button.bind("<Enter>", lambda event:
        self.back_button.configure(cursor="hand2", text_color="green"))
        self.back_button.bind("<Leave>", lambda event:
        self.back_button.configure(cursor="arrow", text_color="white"))
        
        # Sentence translation area
        self.sentence_frame = ctk.CTkFrame(self.advanced_frame)
        self.sentence_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.6)
        
        sentence_label = ctk.CTkLabel(self.sentence_frame, text="Translate this sentence:",
                                     font=("Arial", 16, "bold"))
        sentence_label.pack(pady=10)
        
        self.sentence_display = ctk.CTkTextbox(self.sentence_frame, height=100, font=("Arial", 14))
        self.sentence_display.pack(pady=10, padx=20, fill="x")
        
        self.translation_input = ctk.CTkTextbox(self.sentence_frame, height=100, font=("Arial", 14))
        self.translation_input.pack(pady=10, padx=20, fill="x")
        
        # Control buttons
        button_frame = ctk.CTkFrame(self.sentence_frame)
        button_frame.pack(pady=10)
        
        self.new_sentence_btn = ctk.CTkButton(button_frame, text="New Sentence",
                                             command=self.load_new_sentence)
        self.new_sentence_btn.pack(side="left", padx=10)
        
        self.check_btn = ctk.CTkButton(button_frame, text="Check Translation",
                                      command=self.check_translation)
        self.check_btn.pack(side="left", padx=10)
        
        self.hint_btn = ctk.CTkButton(button_frame, text="Hint",
                                     command=self.show_hint)
        self.hint_btn.pack(side="left", padx=10)
        
        # Feedback area
        self.feedback_label = ctk.CTkLabel(self.sentence_frame, text="",
                                          font=("Arial", 12), wraplength=500)
        self.feedback_label.pack(pady=10)
        
        # Load initial sentence
        self.current_sentences = self.load_sentence_examples()
        self.current_sentence_data = None
        self.load_new_sentence()
    
    def load_sentence_examples(self):
        """Load example sentences for translation"""
        return [
            {
                "german": "Ich würde gerne einen Tisch für zwei Personen reservieren.",
                "english": "I would like to reserve a table for two people.",
                "hint": "Focus on the conditional 'würde gerne' (would like to)"
            },
            {
                "german": "Könnten Sie mir bitte dabei helfen, mein Gepäck zu tragen?",
                "english": "Could you please help me carry my luggage?",
                "hint": "This uses the polite form 'Könnten Sie' (Could you)"
            },
            {
                "german": "Es tut mir leid, aber ich verstehe nicht, was Sie meinen.",
                "english": "I'm sorry, but I don't understand what you mean.",
                "hint": "Note the phrase 'Es tut mir leid' (I'm sorry) and 'was Sie meinen' (what you mean)"
            },
            {
                "german": "Nachdem ich meine Hausaufgaben gemacht hatte, bin ich ins Kino gegangen.",
                "english": "After I had done my homework, I went to the movies.",
                "hint": "This sentence uses the past perfect 'hatte gemacht' (had done)"
            }
        ]
    
    def load_new_sentence(self):
        """Load a new sentence for translation"""
        self.current_sentence_data = random.choice(self.current_sentences)
        self.sentence_display.delete("0.0", "end")
        self.sentence_display.insert("0.0", self.current_sentence_data["german"])
        self.translation_input.delete("0.0", "end")
        self.feedback_label.configure(text="")
    
    def check_translation(self):
        """Check the user's translation"""
        user_translation = self.translation_input.get("0.0", "end").strip()
        correct_translation = self.current_sentence_data["english"]
        
        if not user_translation:
            self.feedback_label.configure(text="Please enter your translation first!")
            return
        
        # Simple similarity check (could be enhanced with NLP)
        similarity_score = self.calculate_similarity(user_translation.lower(), correct_translation.lower())
        
        if similarity_score > 0.7:
            self.feedback_label.configure(text="🎉 Excellent! Your translation is very good!",
                                         text_color="green")
        elif similarity_score > 0.5:
            self.feedback_label.configure(text="👍 Good attempt! Here's the reference translation:\n" + 
                                         correct_translation, text_color="orange")
        else:
            self.feedback_label.configure(text="🤔 Let's try again. Here's the reference translation:\n" + 
                                         correct_translation, text_color="red")
    
    def show_hint(self):
        """Show a hint for the current sentence"""
        if self.current_sentence_data:
            self.feedback_label.configure(text="💡 Hint: " + self.current_sentence_data["hint"],
                                         text_color="blue")
    
    def calculate_similarity(self, text1, text2):
        """Calculate simple word-based similarity between two texts"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)


class PracticeScheduleFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_schedule_frame()
    
    def setup_schedule_frame(self):
        self.master.change_geometry("700x600")
        
        # Main frame
        self.schedule_frame = ctk.CTkFrame(self, width=700, height=600)
        self.schedule_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title
        self.title_label = ctk.CTkLabel(self.schedule_frame, text="Vocabulary Practice Schedule",
                                       font=("Old English Text", 20, "bold"))
        self.title_label.place(relx=0.25, rely=0.05)
        
        # Back button
        self.back_button = ctk.CTkLabel(self.schedule_frame, text='<--',
                                       font=("Old English Text", 20, "bold"))
        self.back_button.place(relx=0.05, rely=0.05)
        self.back_button.bind("<Button-1>", lambda event:
        self.master.open_frame("practice_schedule_frame", 'mainmenuframe'))
        self.back_button.bind("<Enter>", lambda event:
        self.back_button.configure(cursor="hand2", text_color="green"))
        self.back_button.bind("<Leave>", lambda event:
        self.back_button.configure(cursor="arrow", text_color="white"))
        
        # Schedule configuration
        config_frame = ctk.CTkFrame(self.schedule_frame)
        config_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.3)
        
        config_label = ctk.CTkLabel(config_frame, text="Configure Your Practice Schedule",
                                   font=("Arial", 16, "bold"))
        config_label.pack(pady=10)
        
        # Daily practice time
        time_frame = ctk.CTkFrame(config_frame)
        time_frame.pack(pady=10, fill="x", padx=20)
        
        time_label = ctk.CTkLabel(time_frame, text="Daily practice time (minutes):")
        time_label.pack(side="left")
        
        self.time_var = tk.StringVar(value="15")
        time_entry = ctk.CTkEntry(time_frame, textvariable=self.time_var, width=100)
        time_entry.pack(side="right")
        
        # Practice focus
        focus_frame = ctk.CTkFrame(config_frame)
        focus_frame.pack(pady=10, fill="x", padx=20)
        
        focus_label = ctk.CTkLabel(focus_frame, text="Focus area:")
        focus_label.pack(side="left")
        
        self.focus_var = tk.StringVar(value="Mixed")
        focus_menu = ctk.CTkOptionMenu(focus_frame, variable=self.focus_var,
                                      values=["Mixed", "Nouns", "Verbs", "Adjectives", "Weak Areas"])
        focus_menu.pack(side="right")
        
        # Difficulty level
        difficulty_frame = ctk.CTkFrame(config_frame)
        difficulty_frame.pack(pady=10, fill="x", padx=20)
        
        difficulty_label = ctk.CTkLabel(difficulty_frame, text="Difficulty level:")
        difficulty_label.pack(side="left")
        
        self.difficulty_var = tk.StringVar(value="Intermediate")
        difficulty_menu = ctk.CTkOptionMenu(difficulty_frame, variable=self.difficulty_var,
                                           values=["Beginner", "Intermediate", "Advanced"])
        difficulty_menu.pack(side="right")
        
        # Schedule display
        schedule_display_frame = ctk.CTkFrame(self.schedule_frame)
        schedule_display_frame.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.35)
        
        schedule_title = ctk.CTkLabel(schedule_display_frame, text="Your Practice Schedule",
                                     font=("Arial", 16, "bold"))
        schedule_title.pack(pady=10)
        
        self.schedule_text = ctk.CTkTextbox(schedule_display_frame, height=150)
        self.schedule_text.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.schedule_frame)
        button_frame.place(relx=0.1, rely=0.88, relwidth=0.8, relheight=0.1)
        
        generate_btn = ctk.CTkButton(button_frame, text="Generate Schedule",
                                    command=self.generate_schedule)
        generate_btn.pack(side="left", padx=10, pady=10)
        
        save_btn = ctk.CTkButton(button_frame, text="Save Schedule",
                                command=self.save_schedule)
        save_btn.pack(side="left", padx=10, pady=10)
        
        start_btn = ctk.CTkButton(button_frame, text="Start Today's Practice",
                                 command=self.start_practice)
        start_btn.pack(side="right", padx=10, pady=10)
        
        # Generate initial schedule
        self.generate_schedule()
    
    def generate_schedule(self):
        """Generate a personalized practice schedule"""
        daily_time = int(self.time_var.get())
        focus = self.focus_var.get()
        difficulty = self.difficulty_var.get()
        
        schedule_text = f"=== Personal Practice Schedule ===\n\n"
        schedule_text += f"Daily commitment: {daily_time} minutes\n"
        schedule_text += f"Focus area: {focus}\n"
        schedule_text += f"Difficulty level: {difficulty}\n\n"
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        activities = {
            "Mixed": ["Translation quiz", "Vocabulary review", "Grammar exercises", "Listening practice"],
            "Nouns": ["Noun-article matching", "Plural forms", "Case practice", "Thematic vocabulary"],
            "Verbs": ["Conjugation practice", "Irregular verbs", "Tense exercises", "Modal verbs"],
            "Adjectives": ["Declension practice", "Comparative forms", "Descriptive exercises", "Color/size vocab"],
            "Weak Areas": ["Review mistakes", "Targeted practice", "Repetition exercises", "Progress check"]
        }
        
        for i, day in enumerate(days):
            if focus in activities:
                activity = activities[focus][i % len(activities[focus])]
            else:
                activity = "Mixed practice"
            
            schedule_text += f"{day}: {activity} ({daily_time} min)\n"
        
        schedule_text += f"\n💡 Tips for {difficulty} level:\n"
        if difficulty == "Beginner":
            schedule_text += "• Focus on basic vocabulary and simple sentences\n"
            schedule_text += "• Use visual aids and mnemonics\n"
            schedule_text += "• Practice pronunciation daily\n"
        elif difficulty == "Intermediate":
            schedule_text += "• Challenge yourself with longer sentences\n"
            schedule_text += "• Practice real-world conversations\n"
            schedule_text += "• Learn idioms and expressions\n"
        else:  # Advanced
            schedule_text += "• Focus on complex grammar structures\n"
            schedule_text += "• Read German texts and news\n"
            schedule_text += "• Practice formal and informal registers\n"
        
        self.schedule_text.delete("0.0", "end")
        self.schedule_text.insert("0.0", schedule_text)
    
    def save_schedule(self):
        """Save the current schedule"""
        # In a real implementation, this would save to a file or database
        messagebox.showinfo("Saved", "Your practice schedule has been saved!")
    
    def start_practice(self):
        """Start today's practice session"""
        # This would typically launch the appropriate practice mode
        self.master.open_frame("practice_schedule_frame", 'translation_game_frame')
