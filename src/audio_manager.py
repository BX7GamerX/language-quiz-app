import os
import sys
import threading
import tempfile
from typing import Optional
import customtkinter as ctk
import tkinter.messagebox as messagebox

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


class AudioManager:
    def __init__(self):
        self.tts_engine = None
        self.temp_files = []
        self.available_engines = []
        
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.available_engines.append("pyttsx3")
                self.configure_tts_engine()
            except Exception as e:
                print(f"Error initializing TTS engine: {e}")
                self.tts_engine = None
        
        if PYGAME_AVAILABLE:
            self.available_engines.append("pygame")
        
        if GTTS_AVAILABLE:
            self.available_engines.append("gtts")
    
    def configure_tts_engine(self):
        """Configure the TTS engine settings"""
        if self.tts_engine:
            try:
                # Set properties
                voices = self.tts_engine.getProperty('voices')
                
                # Try to find German voice, fallback to English
                german_voice = None
                english_voice = None
                
                for voice in voices:
                    if 'german' in voice.name.lower() or 'de' in voice.id.lower():
                        german_voice = voice.id
                        break
                    elif 'english' in voice.name.lower() or 'en' in voice.id.lower():
                        english_voice = voice.id
                
                # Set voice preference
                if german_voice:
                    self.tts_engine.setProperty('voice', german_voice)
                elif english_voice:
                    self.tts_engine.setProperty('voice', english_voice)
                
                # Set speech rate and volume
                self.tts_engine.setProperty('rate', 150)  # Speed of speech
                self.tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
                
            except Exception as e:
                print(f"Error configuring TTS engine: {e}")
    
    def speak_text_offline(self, text: str, language: str = 'en') -> bool:
        """Use offline TTS to speak text"""
        if not self.tts_engine:
            return False
        
        try:
            # Run TTS in a separate thread to avoid blocking UI
            def speak_thread():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            thread = threading.Thread(target=speak_thread, daemon=True)
            thread.start()
            return True
            
        except Exception as e:
            print(f"Error in offline TTS: {e}")
            return False
    
    def speak_text_online(self, text: str, language: str = 'de') -> bool:
        """Use online TTS (gTTS) to speak text"""
        if not GTTS_AVAILABLE or not PYGAME_AVAILABLE:
            return False
        
        try:
            def speak_thread():
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                self.temp_files.append(temp_file.name)
                temp_file.close()
                
                # Generate speech
                tts = gTTS(text=text, lang=language, slow=False)
                tts.save(temp_file.name)
                
                # Play audio
                pygame.mixer.music.load(temp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                # Clean up
                os.unlink(temp_file.name)
                if temp_file.name in self.temp_files:
                    self.temp_files.remove(temp_file.name)
            
            thread = threading.Thread(target=speak_thread, daemon=True)
            thread.start()
            return True
            
        except Exception as e:
            print(f"Error in online TTS: {e}")
            return False
    
    def speak_text(self, text: str, language: str = 'de', prefer_online: bool = True) -> bool:
        """Speak text using available TTS method"""
        if not text.strip():
            return False
        
        # Try online TTS first if preferred and available
        if prefer_online and GTTS_AVAILABLE:
            if self.speak_text_online(text, language):
                return True
        
        # Fallback to offline TTS
        if TTS_AVAILABLE:
            return self.speak_text_offline(text, language)
        
        return False
    
    def is_audio_available(self) -> bool:
        """Check if any audio functionality is available"""
        return TTS_AVAILABLE or (GTTS_AVAILABLE and PYGAME_AVAILABLE)
    
    def get_available_features(self) -> list:
        """Get list of available audio features"""
        features = []
        if TTS_AVAILABLE:
            features.append("Offline TTS (pyttsx3)")
        if GTTS_AVAILABLE and PYGAME_AVAILABLE:
            features.append("Online TTS (Google)")
        return features
    
    def cleanup(self):
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                print(f"Error cleaning up temp file {temp_file}: {e}")
        self.temp_files.clear()
    
    def __del__(self):
        """Cleanup on destruction"""
        self.cleanup()


class PronunciationPracticeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.audio_manager = AudioManager()
        self.current_word = ""
        self.current_language = "de"
        self.setup_pronunciation_frame()
    
    def setup_pronunciation_frame(self):
        self.master.change_geometry("600x700")
        
        # Main frame
        self.pronunciation_frame = ctk.CTkFrame(self, width=600, height=700)
        self.pronunciation_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title
        self.title_label = ctk.CTkLabel(self.pronunciation_frame, text="Pronunciation Practice",
                                       font=("Old English Text", 20, "bold"))
        self.title_label.place(relx=0.25, rely=0.05)
        
        # Back button
        self.back_button = ctk.CTkLabel(self.pronunciation_frame, text='<--',
                                       font=("Old English Text", 20, "bold"))
        self.back_button.place(relx=0.05, rely=0.05)
        self.back_button.bind("<Button-1>", lambda event:
        self.master.open_frame("pronunciation_frame", 'mainmenuframe'))
        self.back_button.bind("<Enter>", lambda event:
        self.back_button.configure(cursor="hand2", text_color="green"))
        self.back_button.bind("<Leave>", lambda event:
        self.back_button.configure(cursor="arrow", text_color="white"))
        
        # Audio availability check
        if not self.audio_manager.is_audio_available():
            warning_frame = ctk.CTkFrame(self.pronunciation_frame)
            warning_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.15)
            
            warning_label = ctk.CTkLabel(warning_frame, 
                                        text="⚠️ Audio features not available\n"
                                             "Install: pip install pyttsx3 pygame gtts\n"
                                             "for full pronunciation support",
                                        font=("Arial", 12), text_color="orange")
            warning_label.pack(pady=20)
        
        # Word display area
        word_frame = ctk.CTkFrame(self.pronunciation_frame)
        word_frame.place(relx=0.1, rely=0.32 if self.audio_manager.is_audio_available() else 0.32, 
                        relwidth=0.8, relheight=0.25)
        
        word_label = ctk.CTkLabel(word_frame, text="Current Word:", font=("Arial", 16, "bold"))
        word_label.pack(pady=10)
        
        self.word_display = ctk.CTkLabel(word_frame, text="Click 'New Word' to start",
                                        font=("Arial", 24, "bold"), text_color="lightblue")
        self.word_display.pack(pady=10)
        
        self.translation_display = ctk.CTkLabel(word_frame, text="",
                                               font=("Arial", 14), text_color="lightgray")
        self.translation_display.pack(pady=5)
        
        # Control buttons
        control_frame = ctk.CTkFrame(self.pronunciation_frame)
        control_frame.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.15)
        
        button_row1 = ctk.CTkFrame(control_frame)
        button_row1.pack(pady=10)
        
        self.new_word_btn = ctk.CTkButton(button_row1, text="New Word", 
                                         command=self.load_new_word, width=120)
        self.new_word_btn.pack(side="left", padx=5)
        
        self.play_btn = ctk.CTkButton(button_row1, text="🔊 Play", 
                                     command=self.play_pronunciation, width=120,
                                     state="disabled" if not self.audio_manager.is_audio_available() else "normal")
        self.play_btn.pack(side="left", padx=5)
        
        self.slow_btn = ctk.CTkButton(button_row1, text="🐌 Play Slow", 
                                     command=self.play_slow, width=120,
                                     state="disabled" if not self.audio_manager.is_audio_available() else "normal")
        self.slow_btn.pack(side="left", padx=5)
        
        button_row2 = ctk.CTkFrame(control_frame)
        button_row2.pack(pady=5)
        
        # Language selection
        lang_label = ctk.CTkLabel(button_row2, text="Language:")
        lang_label.pack(side="left", padx=5)
        
        self.language_var = ctk.StringVar(value="German")
        self.language_menu = ctk.CTkOptionMenu(button_row2, variable=self.language_var,
                                              values=["German", "English", "French", "Spanish"],
                                              command=self.change_language, width=100)
        self.language_menu.pack(side="left", padx=5)
        
        # Practice mode selection
        mode_label = ctk.CTkLabel(button_row2, text="Mode:")
        mode_label.pack(side="left", padx=5)
        
        self.mode_var = ctk.StringVar(value="Random")
        self.mode_menu = ctk.CTkOptionMenu(button_row2, variable=self.mode_var,
                                          values=["Random", "Nouns", "Verbs", "Adjectives", "Adverbs"],
                                          command=self.change_mode, width=100)
        self.mode_menu.pack(side="left", padx=5)
        
        # Phonetic guide (if available)
        phonetic_frame = ctk.CTkFrame(self.pronunciation_frame)
        phonetic_frame.place(relx=0.1, rely=0.78, relwidth=0.8, relheight=0.15)
        
        phonetic_label = ctk.CTkLabel(phonetic_frame, text="Pronunciation Guide:",
                                     font=("Arial", 14, "bold"))
        phonetic_label.pack(pady=5)
        
        self.phonetic_display = ctk.CTkTextbox(phonetic_frame, height=60, font=("Courier", 11))
        self.phonetic_display.pack(pady=5, padx=10, fill="x")
        
        # Load first word
        self.load_new_word()
    
    def load_new_word(self):
        """Load a new word for pronunciation practice"""
        try:
            from word_library import random_word_gen, translate_two
            from functions import game_properties
            
            # Determine word type from mode
            if self.mode_var.get() == "Random":
                word_types = ["nouns", "verbs", "adjectives", "adverbs"]
                word_type = random.choice(word_types)
            else:
                word_type = self.mode_var.get().lower()
            
            # Get random word
            if self.current_language == "de":
                self.current_word = random_word_gen("deutsch", word_type)
                translation = translate_two(self.current_word, "deutsch", "english", word_type)
            else:
                # For other languages, use German as base and translate
                german_word = random_word_gen("deutsch", word_type)
                self.current_word = translate_two(german_word, "deutsch", self.current_language, word_type)
                translation = translate_two(german_word, "deutsch", "english", word_type)
            
            if self.current_word and self.current_word != "word library not found":
                self.word_display.configure(text=self.current_word.title())
                if translation:
                    self.translation_display.configure(text=f"({translation})")
                else:
                    self.translation_display.configure(text="")
                
                # Update phonetic guide
                self.update_phonetic_guide()
            else:
                self.word_display.configure(text="No words available")
                self.translation_display.configure(text="Please build vocabulary library first")
                
        except Exception as e:
            print(f"Error loading new word: {e}")
            self.word_display.configure(text="Error loading word")
            self.translation_display.configure(text="")
    
    def play_pronunciation(self):
        """Play the pronunciation of the current word"""
        if self.current_word and self.audio_manager.is_audio_available():
            success = self.audio_manager.speak_text(self.current_word, self.current_language)
            if not success:
                messagebox.showwarning("Audio Error", "Could not play pronunciation")
    
    def play_slow(self):
        """Play the pronunciation slowly"""
        if self.current_word and self.audio_manager.is_audio_available():
            # For slow speech, we can modify the text or use different settings
            # This is a simple implementation - could be enhanced
            success = self.audio_manager.speak_text(self.current_word, self.current_language)
            if not success:
                messagebox.showwarning("Audio Error", "Could not play slow pronunciation")
    
    def change_language(self, selection):
        """Change the pronunciation language"""
        lang_mapping = {
            "German": "de",
            "English": "en",
            "French": "fr",
            "Spanish": "es"
        }
        self.current_language = lang_mapping.get(selection, "de")
        self.load_new_word()  # Reload word in new language
    
    def change_mode(self, selection):
        """Change the practice mode"""
        self.load_new_word()  # Reload word with new mode
    
    def update_phonetic_guide(self):
        """Update the phonetic pronunciation guide"""
        if not self.current_word:
            return
        
        # Simple phonetic guide - this could be enhanced with actual IPA transcription
        phonetic_guides = {
            "de": {
                "ä": "like 'a' in 'cat'",
                "ö": "like 'u' in 'hurt' (with rounded lips)",
                "ü": "like 'ee' in 'see' (with rounded lips)",
                "ß": "sharp 's' sound",
                "ch": "like 'h' in 'huge' (after i, e) or like Scottish 'loch' (after a, o, u)",
                "sch": "like 'sh' in 'ship'",
                "sp": "'shp' sound at beginning of words",
                "st": "'sht' sound at beginning of words"
            }
        }
        
        guide_text = f"Word: {self.current_word}\n"
        
        if self.current_language in phonetic_guides:
            word_lower = self.current_word.lower()
            relevant_sounds = []
            
            for sound, description in phonetic_guides[self.current_language].items():
                if sound in word_lower:
                    relevant_sounds.append(f"'{sound}': {description}")
            
            if relevant_sounds:
                guide_text += "Pronunciation tips:\n" + "\n".join(relevant_sounds)
            else:
                guide_text += "Standard pronunciation - listen and repeat!"
        else:
            guide_text += f"Language: {self.language_var.get()}\nListen carefully and try to repeat."
        
        self.phonetic_display.delete("0.0", "end")
        self.phonetic_display.insert("0.0", guide_text)


# Global audio manager instance
audio_manager = AudioManager()


def install_audio_requirements():
    """Helper function to install required audio packages"""
    try:
        import subprocess
        import sys
        
        packages = ["pyttsx3", "pygame", "gtts"]
        
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("Audio packages installed successfully!")
        return True
        
    except Exception as e:
        print(f"Error installing audio packages: {e}")
        return False


if __name__ == "__main__":
    # Test the audio functionality
    audio_test = AudioManager()
    
    print("Available audio features:", audio_test.get_available_features())
    
    if audio_test.is_audio_available():
        # Test German pronunciation
        audio_test.speak_text("Hallo, wie geht es Ihnen?", "de")
    else:
        print("No audio features available. Run install_audio_requirements() to install packages.")
