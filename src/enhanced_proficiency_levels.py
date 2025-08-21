import customtkinter as ctk
import tkinter
import random
from functions import game_properties
from spaced_repetition import spaced_repetition


class AdvancedLearningFeatures:
    """Advanced learning features for higher proficiency levels"""
    
    @staticmethod
    def get_compound_words():
        """German compound word construction exercises"""
        return [
            {"parts": ["Haus", "Tier"], "answer": "Haustier", "meaning": "pet"},
            {"parts": ["Hand", "Schuh"], "answer": "Handschuh", "meaning": "glove"},
            {"parts": ["Feuer", "Wehr"], "answer": "Feuerwehr", "meaning": "fire brigade"},
            {"parts": ["Regen", "Bogen"], "answer": "Regenbogen", "meaning": "rainbow"},
            {"parts": ["Sonnen", "Schirm"], "answer": "Sonnenschirm", "meaning": "parasol"},
            {"parts": ["Zeit", "Reise"], "answer": "Zeitreise", "meaning": "time travel"},
            {"parts": ["Wasser", "Fall"], "answer": "Wasserfall", "meaning": "waterfall"},
            {"parts": ["Kinder", "Garten"], "answer": "Kindergarten", "meaning": "kindergarten"}
        ]
    
    @staticmethod
    def get_cultural_contexts():
        """German cultural context and expressions"""
        return [
            {
                "context": "Oktoberfest",
                "vocabulary": ["Bier", "Brezel", "Lederhose", "Dirndl", "Prost"],
                "phrases": ["Ein Prosit!", "O'zapft is!", "Auf geht's!"],
                "cultural_note": "Traditional Bavarian festival with beer, food, and music"
            },
            {
                "context": "Christmas Markets",
                "vocabulary": ["Glühwein", "Lebkuchen", "Tannenbaum", "Weihnachtsmarkt"],
                "phrases": ["Frohe Weihnachten!", "Schöne Adventszeit!"],
                "cultural_note": "Traditional German Christmas tradition with warm wine and cookies"
            },
            {
                "context": "German Workplace",
                "vocabulary": ["Arbeitgeber", "Arbeitnehmer", "Urlaub", "Überstunden"],
                "phrases": ["Guten Arbeitstag!", "Feierabend!", "Erfolgreiche Besprechung!"],
                "cultural_note": "German work culture emphasizes punctuality and efficiency"
            }
        ]
    
    @staticmethod
    def get_grammar_patterns():
        """Advanced grammar patterns for different levels"""
        return {
            "A2": {
                "modal_verbs": [
                    {"sentence": "Ich _____ Deutsch lernen.", "answer": "möchte", "options": ["möchte", "muss", "kann"]},
                    {"sentence": "Du _____ pünktlich sein.", "answer": "sollst", "options": ["sollst", "willst", "darfst"]}
                ],
                "conjunctions": [
                    {"sentence": "Ich lerne Deutsch, _____ es wichtig ist.", "answer": "weil", "options": ["weil", "aber", "oder"]},
                    {"sentence": "Er kommt spät, _____ der Zug hatte Verspätung.", "answer": "denn", "options": ["denn", "und", "aber"]}
                ]
            },
            "B1": {
                "passive_voice": [
                    {"active": "Der Chef unterschreibt den Vertrag.", "passive": "Der Vertrag wird vom Chef unterschrieben."},
                    {"active": "Sie repariert das Auto.", "passive": "Das Auto wird von ihr repariert."}
                ],
                "subjunctive": [
                    {"sentence": "Wenn ich Zeit _____, würde ich reisen.", "answer": "hätte", "options": ["hätte", "habe", "hatte"]},
                    {"sentence": "Könnten Sie mir bitte helfen?", "meaning": "Polite request using Konjunktiv II"}
                ]
            },
            "B2": {
                "advanced_prepositions": [
                    {"sentence": "_____ des Regens blieben wir zu Hause.", "answer": "Wegen", "options": ["Wegen", "Während", "Trotz"]},
                    {"sentence": "_____ der Arbeit denke ich an Urlaub.", "answer": "Während", "options": ["Während", "Wegen", "Statt"]}
                ]
            }
        }
    
    @staticmethod
    def get_german_idioms():
        """German idioms and proverbs with explanations"""
        return [
            {
                "idiom": "Das ist mir Wurst",
                "literal": "That's sausage to me",
                "meaning": "I don't care",
                "usage": "Used to express indifference about something"
            },
            {
                "idiom": "Die Katze aus dem Sack lassen",
                "literal": "Let the cat out of the bag",
                "meaning": "Reveal a secret",
                "usage": "Similar to English expression"
            },
            {
                "idiom": "Tomaten auf den Augen haben",
                "literal": "Have tomatoes on the eyes",
                "meaning": "Be blind to something obvious",
                "usage": "Unable to see what's right in front of you"
            },
            {
                "idiom": "Schwein haben",
                "literal": "Have pig",
                "meaning": "Be lucky",
                "usage": "Express unexpected good fortune"
            }
        ]


class A2DeutschFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.features = AdvancedLearningFeatures()
        self.setup_a2_deutsch_frame()
    
    def set_from_language(self, language):
        game_properties.user_language = language
    
    def set_to_language(self, language):
        game_properties.second_language = language
    
    def setup_a2_deutsch_frame(self):
        self.master.change_geometry("800x700")
        
        # Main frame with modern styling
        self.a2_deutsch_frame = ctk.CTkFrame(self, width=800, height=700, 
                                           corner_radius=20, fg_color="#2d3436")
        self.a2_deutsch_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title with enhanced styling
        self.a2_deutch_label = ctk.CTkLabel(self.a2_deutsch_frame, text="A2 Deutsch - Intermediate Level",
                                           font=("Helvetica", 26, "bold"),
                                           text_color="#00b894")
        self.a2_deutch_label.place(relx=0.5, rely=0.08, anchor=tkinter.CENTER)
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(self.a2_deutsch_frame, 
                                         text="Enhanced with Cultural Context & Grammar Patterns",
                                         font=("Helvetica", 14),
                                         text_color="#74b9ff")
        self.subtitle_label.place(relx=0.5, rely=0.13, anchor=tkinter.CENTER)
        
        # Language selection section
        self.lang_frame = ctk.CTkFrame(self.a2_deutsch_frame, fg_color="#636e72", corner_radius=15,
                                     width=600, height=100)
        self.lang_frame.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
        
        ctk.CTkLabel(self.lang_frame, text="Language Settings", 
                    font=("Helvetica", 16, "bold")).place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
        
        ctk.CTkLabel(self.lang_frame, text="From:", font=("Helvetica", 12)).place(relx=0.15, rely=0.6)
        self.from_language_options = ctk.CTkOptionMenu(self.lang_frame,
                                                      values=["english", "deutsch", "french", "spanish"],
                                                      command=self.set_from_language,
                                                      width=120)
        self.from_language_options.place(relx=0.25, rely=0.6)
        
        ctk.CTkLabel(self.lang_frame, text="To:", font=("Helvetica", 12)).place(relx=0.55, rely=0.6)
        self.to_language_options = ctk.CTkOptionMenu(self.lang_frame,
                                                    values=["english", "deutsch", "french", "spanish"],
                                                    command=self.set_to_language,
                                                    width=120)
        self.to_language_options.place(relx=0.65, rely=0.6)
        
        # Advanced Features Buttons
        self.create_feature_buttons()
        
        # Back button with improved styling
        self.back_button = ctk.CTkButton(self.a2_deutsch_frame, text="← Back to Menu",
                                       command=self.go_back,
                                       width=140, height=35,
                                       font=("Helvetica", 12, "bold"),
                                       fg_color="#e17055", hover_color="#d63031")
        self.back_button.place(relx=0.05, rely=0.05)
    
    def create_feature_buttons(self):
        """Create buttons for advanced A2 features"""
        features = [
            ("🏠 Compound Words", self.start_compound_words, "#6c5ce7"),
            ("🎭 Cultural Context", self.start_cultural_context, "#fd79a8"),
            ("📝 Grammar Patterns", self.start_grammar_patterns, "#fdcb6e"),
            ("🎯 Modal Verbs Practice", self.start_modal_verbs, "#00b894"),
            ("🎮 Translation Game", self.start_translation_game, "#0984e3"),
            ("📊 Progress Review", self.show_progress, "#6c5ce7")
        ]
        
        # Create buttons in a grid
        for i, (text, command, color) in enumerate(features):
            row = i // 2
            col = i % 2
            
            button = ctk.CTkButton(self.a2_deutsch_frame, text=text,
                                 command=command,
                                 width=250, height=60,
                                 font=("Helvetica", 14, "bold"),
                                 fg_color=color,
                                 hover_color=self.darken_color(color))
            
            x_pos = 0.25 + (col * 0.5)
            y_pos = 0.4 + (row * 0.12)
            button.place(relx=x_pos, rely=y_pos, anchor=tkinter.CENTER)
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        # Simple darkening by reducing each RGB component
        return color  # Simplified for now
    
    def start_compound_words(self):
        """Start compound word construction exercise"""
        self.open_compound_words_window()
    
    def start_cultural_context(self):
        """Start cultural context learning"""
        self.open_cultural_context_window()
    
    def start_grammar_patterns(self):
        """Start grammar pattern practice"""
        self.open_grammar_patterns_window()
    
    def start_modal_verbs(self):
        """Start modal verbs exercise"""
        self.open_modal_verbs_window()
    
    def start_translation_game(self):
        """Start enhanced translation game"""
        try:
            self.master.open_frame("a2_deutsch_frame", 'translation_game_frame')
        except:
            print("Translation game frame not available")
    
    def show_progress(self):
        """Show progress dashboard"""
        try:
            self.master.open_frame("a2_deutsch_frame", 'progress_dashboard')
        except:
            print("Progress dashboard not available")
    
    def open_compound_words_window(self):
        """Open compound words practice window"""
        window = ctk.CTkToplevel(self)
        window.title("German Compound Words")
        window.geometry("600x500")
        window.configure(fg_color="#2d3436")
        
        # Title
        title = ctk.CTkLabel(window, text="🏠 Compound Word Construction",
                           font=("Helvetica", 20, "bold"),
                           text_color="#00b894")
        title.pack(pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(window, 
                                  text="Combine the German words to create compound words!",
                                  font=("Helvetica", 14),
                                  text_color="#74b9ff")
        instructions.pack(pady=10)
        
        # Current exercise frame
        self.compound_frame = ctk.CTkFrame(window, fg_color="#636e72", corner_radius=15)
        self.compound_frame.pack(pady=20, padx=20, fill="x")
        
        self.current_compound = None
        self.setup_compound_exercise()
    
    def setup_compound_exercise(self):
        """Setup a compound word exercise"""
        # Clear previous exercise
        for widget in self.compound_frame.winfo_children():
            widget.destroy()
        
        # Get random compound word
        compounds = self.features.get_compound_words()
        self.current_compound = random.choice(compounds)
        
        # Display parts
        parts_label = ctk.CTkLabel(self.compound_frame, 
                                 text=f"Combine: {' + '.join(self.current_compound['parts'])}",
                                 font=("Helvetica", 16, "bold"))
        parts_label.pack(pady=15)
        
        # Meaning hint
        meaning_label = ctk.CTkLabel(self.compound_frame,
                                   text=f"Meaning: {self.current_compound['meaning']}",
                                   font=("Helvetica", 12),
                                   text_color="#fdcb6e")
        meaning_label.pack(pady=5)
        
        # Answer entry
        self.compound_entry = ctk.CTkEntry(self.compound_frame, 
                                         placeholder_text="Enter compound word...",
                                         font=("Helvetica", 14),
                                         width=200)
        self.compound_entry.pack(pady=15)
        
        # Check button
        check_btn = ctk.CTkButton(self.compound_frame, text="Check Answer",
                                command=self.check_compound_answer,
                                fg_color="#00b894")
        check_btn.pack(pady=10)
        
        # Result label
        self.compound_result = ctk.CTkLabel(self.compound_frame, text="",
                                          font=("Helvetica", 14, "bold"))
        self.compound_result.pack(pady=10)
        
        # Next button
        next_btn = ctk.CTkButton(self.compound_frame, text="Next Exercise",
                               command=self.setup_compound_exercise,
                               fg_color="#74b9ff")
        next_btn.pack(pady=10)
    
    def check_compound_answer(self):
        """Check the compound word answer"""
        user_answer = self.compound_entry.get().strip()
        correct_answer = self.current_compound['answer']
        
        if user_answer.lower() == correct_answer.lower():
            self.compound_result.configure(text="✅ Correct! Well done!",
                                         text_color="#00b894")
        else:
            self.compound_result.configure(text=f"❌ Incorrect. The answer is: {correct_answer}",
                                         text_color="#e17055")
    
    def open_cultural_context_window(self):
        """Open cultural context learning window"""
        window = ctk.CTkToplevel(self)
        window.title("German Cultural Context")
        window.geometry("700x600")
        window.configure(fg_color="#2d3436")
        
        # Title
        title = ctk.CTkLabel(window, text="🎭 German Cultural Context",
                           font=("Helvetica", 20, "bold"),
                           text_color="#fd79a8")
        title.pack(pady=20)
        
        # Context selector
        contexts = self.features.get_cultural_contexts()
        context_names = [ctx["context"] for ctx in contexts]
        
        self.context_var = tkinter.StringVar(value=context_names[0])
        context_menu = ctk.CTkOptionMenu(window, values=context_names,
                                       variable=self.context_var,
                                       command=self.display_cultural_context)
        context_menu.pack(pady=20)
        
        # Content frame
        self.cultural_content = ctk.CTkScrollableFrame(window, width=650, height=400,
                                                     fg_color="#636e72")
        self.cultural_content.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Display initial context
        self.display_cultural_context(context_names[0])
    
    def display_cultural_context(self, selected_context):
        """Display selected cultural context"""
        # Clear previous content
        for widget in self.cultural_content.winfo_children():
            widget.destroy()
        
        # Find selected context
        contexts = self.features.get_cultural_contexts()
        context_data = next(ctx for ctx in contexts if ctx["context"] == selected_context)
        
        # Display context information
        context_title = ctk.CTkLabel(self.cultural_content, 
                                   text=f"📍 {context_data['context']}",
                                   font=("Helvetica", 18, "bold"),
                                   text_color="#fdcb6e")
        context_title.pack(pady=15, anchor="w")
        
        # Cultural note
        note_label = ctk.CTkLabel(self.cultural_content,
                                text=f"Cultural Context:\n{context_data['cultural_note']}",
                                font=("Helvetica", 12),
                                text_color="#74b9ff",
                                justify="left")
        note_label.pack(pady=10, anchor="w", fill="x")
        
        # Vocabulary section
        vocab_title = ctk.CTkLabel(self.cultural_content, text="📚 Key Vocabulary:",
                                 font=("Helvetica", 14, "bold"),
                                 text_color="#00b894")
        vocab_title.pack(pady=(20,10), anchor="w")
        
        vocab_text = ", ".join(context_data['vocabulary'])
        vocab_label = ctk.CTkLabel(self.cultural_content, text=vocab_text,
                                 font=("Helvetica", 12),
                                 text_color="white")
        vocab_label.pack(pady=5, anchor="w", fill="x")
        
        # Phrases section
        phrases_title = ctk.CTkLabel(self.cultural_content, text="💬 Common Phrases:",
                                   font=("Helvetica", 14, "bold"),
                                   text_color="#e17055")
        phrases_title.pack(pady=(20,10), anchor="w")
        
        for phrase in context_data['phrases']:
            phrase_label = ctk.CTkLabel(self.cultural_content, text=f"• {phrase}",
                                      font=("Helvetica", 12),
                                      text_color="white")
            phrase_label.pack(pady=2, anchor="w")
    
    def open_grammar_patterns_window(self):
        """Open grammar patterns practice window"""
        window = ctk.CTkToplevel(self)
        window.title("A2 Grammar Patterns")
        window.geometry("600x500")
        window.configure(fg_color="#2d3436")
        
        # Title
        title = ctk.CTkLabel(window, text="📝 A2 Grammar Patterns",
                           font=("Helvetica", 20, "bold"),
                           text_color="#fdcb6e")
        title.pack(pady=20)
        
        # Pattern type selector
        pattern_types = ["modal_verbs", "conjunctions"]
        self.pattern_var = tkinter.StringVar(value="modal_verbs")
        
        type_menu = ctk.CTkOptionMenu(window, values=pattern_types,
                                    variable=self.pattern_var,
                                    command=self.setup_grammar_exercise)
        type_menu.pack(pady=20)
        
        # Exercise frame
        self.grammar_exercise_frame = ctk.CTkFrame(window, fg_color="#636e72", corner_radius=15)
        self.grammar_exercise_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Setup initial exercise
        self.setup_grammar_exercise("modal_verbs")
    
    def setup_grammar_exercise(self, pattern_type):
        """Setup grammar pattern exercise"""
        # Clear previous exercise
        for widget in self.grammar_exercise_frame.winfo_children():
            widget.destroy()
        
        patterns = self.features.get_grammar_patterns()
        exercises = patterns["A2"][pattern_type]
        
        self.current_grammar = random.choice(exercises)
        
        # Display exercise
        exercise_label = ctk.CTkLabel(self.grammar_exercise_frame,
                                    text=self.current_grammar["sentence"],
                                    font=("Helvetica", 16, "bold"))
        exercise_label.pack(pady=20)
        
        # Options frame
        options_frame = ctk.CTkFrame(self.grammar_exercise_frame, fg_color="transparent")
        options_frame.pack(pady=15)
        
        self.grammar_var = tkinter.StringVar()
        for option in self.current_grammar["options"]:
            radio = ctk.CTkRadioButton(options_frame, text=option,
                                     variable=self.grammar_var, value=option)
            radio.pack(pady=5, anchor="w")
        
        # Check button
        check_btn = ctk.CTkButton(self.grammar_exercise_frame, text="Check Answer",
                                command=self.check_grammar_answer,
                                fg_color="#00b894")
        check_btn.pack(pady=20)
        
        # Result label
        self.grammar_result = ctk.CTkLabel(self.grammar_exercise_frame, text="",
                                         font=("Helvetica", 14, "bold"))
        self.grammar_result.pack(pady=10)
    
    def check_grammar_answer(self):
        """Check grammar pattern answer"""
        user_answer = self.grammar_var.get()
        correct_answer = self.current_grammar["answer"]
        
        if user_answer == correct_answer:
            self.grammar_result.configure(text="✅ Correct! Excellent grammar!",
                                        text_color="#00b894")
        else:
            self.grammar_result.configure(text=f"❌ Incorrect. The answer is: {correct_answer}",
                                        text_color="#e17055")
    
    def open_modal_verbs_window(self):
        """Open modal verbs specialized practice"""
        window = ctk.CTkToplevel(self)
        window.title("Modal Verbs Practice")
        window.geometry("600x400")
        window.configure(fg_color="#2d3436")
        
        # Title
        title = ctk.CTkLabel(window, text="🎯 German Modal Verbs",
                           font=("Helvetica", 20, "bold"),
                           text_color="#00b894")
        title.pack(pady=20)
        
        # Modal verbs explanation
        explanation = """
        German Modal Verbs (Modalverben):
        • können (can/to be able to)
        • müssen (must/have to)
        • wollen (to want to)
        • sollen (should/ought to)
        • dürfen (may/to be allowed to)
        • mögen/möchten (to like/would like to)
        """
        
        exp_label = ctk.CTkLabel(window, text=explanation,
                               font=("Helvetica", 12),
                               text_color="#74b9ff",
                               justify="left")
        exp_label.pack(pady=20, padx=20)
        
        # Practice button
        practice_btn = ctk.CTkButton(window, text="Start Modal Verb Practice",
                                   command=lambda: self.setup_grammar_exercise("modal_verbs"),
                                   fg_color="#00b894",
                                   width=200, height=40)
        practice_btn.pack(pady=30)
    
    def go_back(self):
        """Go back to main menu"""
        try:
            self.master.open_frame("a2_deutsch_frame", 'mainmenuframe')
        except Exception as e:
            print(f"Error going back to main menu: {e}")


class B1DeutschFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.features = AdvancedLearningFeatures()
        self.setup_b1_deutsch_frame()
    
    def setup_b1_deutsch_frame(self):
        self.master.change_geometry("800x700")
        
        # Main frame with enhanced design
        self.b1_deutsch_frame = ctk.CTkFrame(self, width=800, height=700,
                                           corner_radius=20, fg_color="#2c3e50")
        self.b1_deutsch_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title
        self.b1_title = ctk.CTkLabel(self.b1_deutsch_frame, text="B1 Deutsch - Upper Intermediate",
                                   font=("Helvetica", 26, "bold"),
                                   text_color="#e74c3c")
        self.b1_title.place(relx=0.5, rely=0.08, anchor=tkinter.CENTER)
        
        # Subtitle
        self.subtitle = ctk.CTkLabel(self.b1_deutsch_frame,
                                   text="Advanced Grammar & Real-World Applications",
                                   font=("Helvetica", 14),
                                   text_color="#f39c12")
        self.subtitle.place(relx=0.5, rely=0.13, anchor=tkinter.CENTER)
        
        # Feature buttons
        self.create_b1_features()
        
        # Back button
        self.back_button = ctk.CTkButton(self.b1_deutsch_frame, text="← Back to Menu",
                                       command=self.go_back,
                                       width=140, height=35,
                                       font=("Helvetica", 12, "bold"),
                                       fg_color="#c0392b", hover_color="#a93226")
        self.back_button.place(relx=0.05, rely=0.05)
    
    def create_b1_features(self):
        """Create B1 level feature buttons"""
        features = [
            ("🔄 Passive Voice", self.start_passive_voice, "#9b59b6"),
            ("🎭 Subjunctive Mood", self.start_subjunctive, "#e67e22"),
            ("💼 Business German", self.start_business_german, "#27ae60"),
            ("📰 News Comprehension", self.start_news_comprehension, "#2980b9"),
            ("🏛️ Cultural History", self.start_cultural_history, "#8e44ad"),
            ("🎯 Advanced Translation", self.start_advanced_translation, "#d35400")
        ]
        
        # Create buttons in a grid
        for i, (text, command, color) in enumerate(features):
            row = i // 2
            col = i % 2
            
            button = ctk.CTkButton(self.b1_deutsch_frame, text=text,
                                 command=command,
                                 width=250, height=60,
                                 font=("Helvetica", 14, "bold"),
                                 fg_color=color,
                                 hover_color=color)
            
            x_pos = 0.25 + (col * 0.5)
            y_pos = 0.3 + (row * 0.12)
            button.place(relx=x_pos, rely=y_pos, anchor=tkinter.CENTER)
    
    def start_passive_voice(self):
        """Start passive voice exercises"""
        # Implementation for passive voice practice
        pass
    
    def start_subjunctive(self):
        """Start subjunctive mood practice"""
        # Implementation for subjunctive practice
        pass
    
    def start_business_german(self):
        """Start business German module"""
        # Implementation for business German
        pass
    
    def start_news_comprehension(self):
        """Start news comprehension exercises"""
        # Implementation for news comprehension
        pass
    
    def start_cultural_history(self):
        """Start cultural history module"""
        # Implementation for cultural history
        pass
    
    def start_advanced_translation(self):
        """Start advanced translation exercises"""
        try:
            self.master.open_frame("b1_deutsch_frame", 'advanced_translation')
        except:
            print("Advanced translation not available")
    
    def go_back(self):
        """Go back to main menu"""
        try:
            self.master.open_frame("b1_deutsch_frame", 'mainmenuframe')
        except Exception as e:
            print(f"Error going back to main menu: {e}")


class B2DeutschFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.features = AdvancedLearningFeatures()
        self.setup_b2_deutsch_frame()
    
    def setup_b2_deutsch_frame(self):
        self.master.change_geometry("800x700")
        
        # Main frame with professional design
        self.b2_deutsch_frame = ctk.CTkFrame(self, width=800, height=700,
                                           corner_radius=20, fg_color="#1a252f")
        self.b2_deutsch_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title
        self.b2_title = ctk.CTkLabel(self.b2_deutsch_frame, text="B2 Deutsch - Advanced Level",
                                   font=("Helvetica", 26, "bold"),
                                   text_color="#3498db")
        self.b2_title.place(relx=0.5, rely=0.08, anchor=tkinter.CENTER)
        
        # Subtitle
        self.subtitle = ctk.CTkLabel(self.b2_deutsch_frame,
                                   text="Academic German & Professional Communication",
                                   font=("Helvetica", 14),
                                   text_color="#1abc9c")
        self.subtitle.place(relx=0.5, rely=0.13, anchor=tkinter.CENTER)
        
        # Feature buttons
        self.create_b2_features()
        
        # Back button
        self.back_button = ctk.CTkButton(self.b2_deutsch_frame, text="← Back to Menu",
                                       command=self.go_back,
                                       width=140, height=35,
                                       font=("Helvetica", 12, "bold"),
                                       fg_color="#2c3e50", hover_color="#34495e")
        self.back_button.place(relx=0.05, rely=0.05)
    
    def create_b2_features(self):
        """Create B2 level feature buttons"""
        features = [
            ("🗣️ German Idioms", self.start_idioms, "#e74c3c"),
            ("📚 Academic Writing", self.start_academic_writing, "#9b59b6"),
            ("⚖️ Advanced Prepositions", self.start_advanced_prepositions, "#f39c12"),
            ("🎓 Technical German", self.start_technical_german, "#27ae60"),
            ("💭 Argumentation Skills", self.start_argumentation, "#e67e22"),
            ("📖 Literature Analysis", self.start_literature, "#8e44ad")
        ]
        
        # Create buttons in a grid
        for i, (text, command, color) in enumerate(features):
            row = i // 2
            col = i % 2
            
            button = ctk.CTkButton(self.b2_deutsch_frame, text=text,
                                 command=command,
                                 width=250, height=60,
                                 font=("Helvetica", 14, "bold"),
                                 fg_color=color,
                                 hover_color=color)
            
            x_pos = 0.25 + (col * 0.5)
            y_pos = 0.3 + (row * 0.12)
            button.place(relx=x_pos, rely=y_pos, anchor=tkinter.CENTER)
    
    def start_idioms(self):
        """Start German idioms and expressions"""
        self.open_idioms_window()
    
    def open_idioms_window(self):
        """Open German idioms learning window"""
        window = ctk.CTkToplevel(self)
        window.title("German Idioms & Expressions")
        window.geometry("700x600")
        window.configure(fg_color="#1a252f")
        
        # Title
        title = ctk.CTkLabel(window, text="🗣️ German Idioms & Expressions",
                           font=("Helvetica", 20, "bold"),
                           text_color="#e74c3c")
        title.pack(pady=20)
        
        # Content frame
        self.idiom_content = ctk.CTkScrollableFrame(window, width=650, height=450,
                                                  fg_color="#2c3e50")
        self.idiom_content.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Display idioms
        self.display_idioms()
        
        # Practice button
        practice_btn = ctk.CTkButton(window, text="Practice Quiz",
                                   command=self.start_idiom_quiz,
                                   fg_color="#e74c3c",
                                   width=200, height=40)
        practice_btn.pack(pady=20)
    
    def display_idioms(self):
        """Display German idioms with explanations"""
        idioms = self.features.get_german_idioms()
        
        for idiom_data in idioms:
            # Idiom frame
            idiom_frame = ctk.CTkFrame(self.idiom_content, fg_color="#34495e", corner_radius=10)
            idiom_frame.pack(pady=10, padx=10, fill="x")
            
            # German idiom
            idiom_label = ctk.CTkLabel(idiom_frame, text=f"🎭 {idiom_data['idiom']}",
                                     font=("Helvetica", 16, "bold"),
                                     text_color="#f39c12")
            idiom_label.pack(pady=10, anchor="w", padx=15)
            
            # Literal translation
            literal_label = ctk.CTkLabel(idiom_frame, 
                                       text=f"Literal: {idiom_data['literal']}",
                                       font=("Helvetica", 12, "italic"),
                                       text_color="#95a5a6")
            literal_label.pack(pady=2, anchor="w", padx=15)
            
            # Meaning
            meaning_label = ctk.CTkLabel(idiom_frame,
                                       text=f"Meaning: {idiom_data['meaning']}",
                                       font=("Helvetica", 12, "bold"),
                                       text_color="#1abc9c")
            meaning_label.pack(pady=2, anchor="w", padx=15)
            
            # Usage
            usage_label = ctk.CTkLabel(idiom_frame,
                                     text=f"Usage: {idiom_data['usage']}",
                                     font=("Helvetica", 11),
                                     text_color="#ecf0f1")
            usage_label.pack(pady=(2,10), anchor="w", padx=15)
    
    def start_idiom_quiz(self):
        """Start idiom comprehension quiz"""
        # Implementation for idiom quiz
        pass
    
    def start_academic_writing(self):
        """Start academic writing module"""
        # Implementation for academic writing
        pass
    
    def start_advanced_prepositions(self):
        """Start advanced prepositions practice"""
        # Implementation for advanced prepositions
        pass
    
    def start_technical_german(self):
        """Start technical German vocabulary"""
        # Implementation for technical German
        pass
    
    def start_argumentation(self):
        """Start argumentation skills training"""
        # Implementation for argumentation skills
        pass
    
    def start_literature(self):
        """Start literature analysis module"""
        # Implementation for literature analysis
        pass
    
    def go_back(self):
        """Go back to main menu"""
        try:
            self.master.open_frame("b2_deutsch_frame", 'mainmenuframe')
        except Exception as e:
            print(f"Error going back to main menu: {e}")
