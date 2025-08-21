import customtkinter as ctk
import tkinter
from functions import game_properties


class A2DeutschFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_a2_deutsch_frame()
    
    def set_from_language(self, language):
        game_properties.user_language = language
    
    def set_to_language(self, language):
        game_properties.second_language = language
    
    def setup_a2_deutsch_frame(self):
        self.master.change_geometry("400x600")
        
        # Main frame
        self.a2_deutsch_frame = ctk.CTkFrame(self, width=400, height=600)
        self.a2_deutsch_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title
        self.a2_deutch_label = ctk.CTkLabel(self.a2_deutsch_frame, text="A2 Deutsch",
                                           anchor='center',
                                           font=("Old English Text", 20, "bold"))
        self.a2_deutch_label.place(relx=0.3, rely=0.05)
        
        # Language selection
        self.from_language_options = ctk.CTkOptionMenu(self.a2_deutsch_frame,
                                                      values=["english", "deutsch", "french", "spanish"],
                                                      anchor="center",
                                                      command=self.set_from_language)
        self.from_language_options.place(relx=0.3, rely=0.35)
        
        self.to_language_options = ctk.CTkOptionMenu(self.a2_deutsch_frame,
                                                    values=["english", "deutsch", "french", "spanish"],
                                                    anchor="center",
                                                    command=self.set_to_language)
        self.to_language_options.place(relx=0.3, rely=0.55)
        
        # Back button
        self.back_main_menu = ctk.CTkLabel(self.a2_deutsch_frame, text='<--',
                                          font=("Old English Text", 20, "bold"))
        self.back_main_menu.place(relx=0.2, rely=0.02)
        self.back_main_menu.bind("<Button-1>", lambda event:
        self.master.open_frame("a2_deutsch_frame", 'mainmenuframe'))
        self.back_main_menu.bind("<Enter>", lambda event:
        self.back_main_menu.configure(cursor="hand2",
                                     text_color="green", text='Main Menu',
                                     font=("Old English Text", 10, "bold")))
        self.back_main_menu.bind("<Leave>", lambda event:
        self.back_main_menu.configure(cursor="arrow",
                                     text_color="white", text='<--',
                                     font=("Old English Text", 20, "bold")))
        
        # Dictionary
        self.dict_label = ctk.CTkLabel(self.a2_deutsch_frame,
                                      text="Deutsch Dictionary",
                                      font=('Century Gothic', 15))
        self.dict_label.place(relx=0.15, rely=0.25)
        self.dict_label.bind("<Button-1>", lambda event:
        self.master.open_frame('a2_deutsch_frame', 'translator_frame'))
        self.dict_label.bind("<Enter>", lambda event:
        self.dict_label.configure(cursor="hand2", text_color="green", fg_color='transparent'))
        self.dict_label.bind("<Leave>", lambda event:
        self.dict_label.configure(cursor="arrow", text_color="white", fg_color='transparent'))
        
        # Translation game
        self.game_label = ctk.CTkLabel(self.a2_deutsch_frame, text="Translation Game",
                                      font=('Century Gothic', 15))
        self.game_label.place(relx=0.15, rely=0.65)
        self.game_label.bind("<Button-1>", lambda event:
        self.master.open_frame("a2_deutsch_frame", 'translation_game_frame'))
        self.game_label.bind("<Enter>", lambda event:
        self.game_label.configure(cursor="hand2", text_color="green", fg_color='transparent'))
        self.game_label.bind("<Leave>", lambda event:
        self.game_label.configure(cursor="arrow", text_color="white", fg_color='transparent'))
        
        # Interactive mode - A2 specific
        self.interactive_label = ctk.CTkLabel(self.a2_deutsch_frame, text="Interactive Conversations",
                                             font=('Century Gothic', 15))
        self.interactive_label.place(relx=0.15, rely=0.75)
        self.interactive_label.bind("<Button-1>", lambda event:
        self.master.open_frame("a2_deutsch_frame", 'interactive_mode_frame'))
        self.interactive_label.bind("<Enter>", lambda event:
        self.interactive_label.configure(cursor="hand2", text_color="green", fg_color='transparent'))
        self.interactive_label.bind("<Leave>", lambda event:
        self.interactive_label.configure(cursor="arrow", text_color="white", fg_color='transparent'))


class B1DeutschFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_b1_deutsch_frame()
    
    def set_from_language(self, language):
        game_properties.user_language = language
    
    def set_to_language(self, language):
        game_properties.second_language = language
    
    def setup_b1_deutsch_frame(self):
        self.master.change_geometry("400x600")
        
        # Main frame
        self.b1_deutsch_frame = ctk.CTkFrame(self, width=400, height=600)
        self.b1_deutsch_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title
        self.b1_deutch_label = ctk.CTkLabel(self.b1_deutsch_frame, text="B1 Deutsch",
                                           anchor='center',
                                           font=("Old English Text", 20, "bold"))
        self.b1_deutch_label.place(relx=0.3, rely=0.05)
        
        # Language selection
        self.from_language_options = ctk.CTkOptionMenu(self.b1_deutsch_frame,
                                                      values=["english", "deutsch", "french", "spanish"],
                                                      anchor="center",
                                                      command=self.set_from_language)
        self.from_language_options.place(relx=0.3, rely=0.35)
        
        self.to_language_options = ctk.CTkOptionMenu(self.b1_deutsch_frame,
                                                    values=["english", "deutsch", "french", "spanish"],
                                                    anchor="center",
                                                    command=self.set_to_language)
        self.to_language_options.place(relx=0.3, rely=0.55)
        
        # Back button
        self.back_main_menu = ctk.CTkLabel(self.b1_deutsch_frame, text='<--',
                                          font=("Old English Text", 20, "bold"))
        self.back_main_menu.place(relx=0.2, rely=0.02)
        self.back_main_menu.bind("<Button-1>", lambda event:
        self.master.open_frame("b1_deutsch_frame", 'mainmenuframe'))
        self.back_main_menu.bind("<Enter>", lambda event:
        self.back_main_menu.configure(cursor="hand2",
                                     text_color="green", text='Main Menu',
                                     font=("Old English Text", 10, "bold")))
        self.back_main_menu.bind("<Leave>", lambda event:
        self.back_main_menu.configure(cursor="arrow",
                                     text_color="white", text='<--',
                                     font=("Old English Text", 20, "bold")))
        
        # Advanced features for B1 level
        self.advanced_game_label = ctk.CTkLabel(self.b1_deutsch_frame, text="Advanced Translation",
                                               font=('Century Gothic', 15))
        self.advanced_game_label.place(relx=0.15, rely=0.65)
        self.advanced_game_label.bind("<Button-1>", lambda event:
        self.master.open_frame("b1_deutsch_frame", 'advanced_translation_frame'))
        self.advanced_game_label.bind("<Enter>", lambda event:
        self.advanced_game_label.configure(cursor="hand2", text_color="green", fg_color='transparent'))
        self.advanced_game_label.bind("<Leave>", lambda event:
        self.advanced_game_label.configure(cursor="arrow", text_color="white", fg_color='transparent'))
        
        # Grammar exercises
        self.grammar_label = ctk.CTkLabel(self.b1_deutsch_frame, text="Grammar Exercises",
                                         font=('Century Gothic', 15))
        self.grammar_label.place(relx=0.15, rely=0.75)
        self.grammar_label.bind("<Button-1>", lambda event:
        self.master.open_frame("b1_deutsch_frame", 'grammar_exercise_frame'))
        self.grammar_label.bind("<Enter>", lambda event:
        self.grammar_label.configure(cursor="hand2", text_color="green", fg_color='transparent'))
        self.grammar_label.bind("<Leave>", lambda event:
        self.grammar_label.configure(cursor="arrow", text_color="white", fg_color='transparent'))


class B2DeutschFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_b2_deutsch_frame()
    
    def set_from_language(self, language):
        game_properties.user_language = language
    
    def set_to_language(self, language):
        game_properties.second_language = language
    
    def setup_b2_deutsch_frame(self):
        self.master.change_geometry("400x600")
        
        # Main frame
        self.b2_deutsch_frame = ctk.CTkFrame(self, width=400, height=600)
        self.b2_deutsch_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        # Title
        self.b2_deutch_label = ctk.CTkLabel(self.b2_deutsch_frame, text="B2 Deutsch",
                                           anchor='center',
                                           font=("Old English Text", 20, "bold"))
        self.b2_deutch_label.place(relx=0.3, rely=0.05)
        
        # Language selection
        self.from_language_options = ctk.CTkOptionMenu(self.b2_deutsch_frame,
                                                      values=["english", "deutsch", "french", "spanish"],
                                                      anchor="center",
                                                      command=self.set_from_language)
        self.from_language_options.place(relx=0.3, rely=0.35)
        
        self.to_language_options = ctk.CTkOptionMenu(self.b2_deutsch_frame,
                                                    values=["english", "deutsch", "french", "spanish"],
                                                    anchor="center",
                                                    command=self.set_to_language)
        self.to_language_options.place(relx=0.3, rely=0.55)
        
        # Back button
        self.back_main_menu = ctk.CTkLabel(self.b2_deutsch_frame, text='<--',
                                          font=("Old English Text", 20, "bold"))
        self.back_main_menu.place(relx=0.2, rely=0.02)
        self.back_main_menu.bind("<Button-1>", lambda event:
        self.master.open_frame("b2_deutsch_frame", 'mainmenuframe'))
        self.back_main_menu.bind("<Enter>", lambda event:
        self.back_main_menu.configure(cursor="hand2",
                                     text_color="green", text='Main Menu',
                                     font=("Old English Text", 10, "bold")))
        self.back_main_menu.bind("<Leave>", lambda event:
        self.back_main_menu.configure(cursor="arrow",
                                     text_color="white", text='<--',
                                     font=("Old English Text", 20, "bold")))
        
        # Advanced features for B2 level
        self.expert_game_label = ctk.CTkLabel(self.b2_deutsch_frame, text="Expert Translation",
                                             font=('Century Gothic', 15))
        self.expert_game_label.place(relx=0.15, rely=0.65)
        self.expert_game_label.bind("<Button-1>", lambda event:
        self.master.open_frame("b2_deutsch_frame", 'expert_translation_frame'))
        self.expert_game_label.bind("<Enter>", lambda event:
        self.expert_game_label.configure(cursor="hand2", text_color="green", fg_color='transparent'))
        self.expert_game_label.bind("<Leave>", lambda event:
        self.expert_game_label.configure(cursor="arrow", text_color="white", fg_color='transparent'))
        
        # Text comprehension
        self.comprehension_label = ctk.CTkLabel(self.b2_deutsch_frame, text="Text Comprehension",
                                               font=('Century Gothic', 15))
        self.comprehension_label.place(relx=0.15, rely=0.75)
        self.comprehension_label.bind("<Button-1>", lambda event:
        self.master.open_frame("b2_deutsch_frame", 'comprehension_frame'))
        self.comprehension_label.bind("<Enter>", lambda event:
        self.comprehension_label.configure(cursor="hand2", text_color="green", fg_color='transparent'))
        self.comprehension_label.bind("<Leave>", lambda event:
        self.comprehension_label.configure(cursor="arrow", text_color="white", fg_color='transparent'))
