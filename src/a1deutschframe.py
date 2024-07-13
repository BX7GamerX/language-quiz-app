import customtkinter as ctk
import tkinter
from functions import game_properties


class A1DeutschFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_a1_deutsch_frame()
    def set_from_language(self,language):
        game_properties.user_language = language
    def set_to_language(self,language):
        game_properties.second_language = language
    # main function
    def setup_a1_deutsch_frame(self):
        self.master.change_geometry("400x600")
        # frame label
        self.a1_deutsch_frame = ctk.CTkFrame(self, width=400, height=600)  # Frame n it's attributes
        self.a1_deutsch_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.a1_deutch_label = ctk.CTkLabel(self.a1_deutsch_frame, text="A1 Deutsch",
                                            anchor='center',
                                            font=("Old English Text", 20, "bold"))
        self.a1_deutch_label.place(relx=0.3, rely=0.05)
        self.from_language_options = ctk.CTkOptionMenu(self.a1_deutsch_frame,
                                                   values=["english", "deutsch", "french", "spanish"], anchor="center",
                                                   command=self.set_from_language)
        self.from_language_options.place(relx=0.3, rely=0.35)

        self.to_language_options = ctk.CTkOptionMenu(self.a1_deutsch_frame,
                                                   values=["english", "deutsch", "french", "spanish"], anchor="center",
                                                   command=self.set_to_language)
        self.to_language_options.place(relx=0.3, rely=0.55)

        # main menu label, go back
        self.back_main_menu = ctk.CTkLabel(self.a1_deutsch_frame, text='<--',
                                           font=("Old English Text", 20, "bold"))
        self.back_main_menu.place(relx=0.2, rely=0.02)
        self.back_main_menu.bind("<Button-1>", lambda event:
        self.master.open_frame("a1_deutsch_frame", 'mainmenuframe'))
        self.back_main_menu.bind("<Enter>", lambda event:
        self.back_main_menu.configure(cursor="hand2",
                                      text_color="green", text='Main Menu', font=("Old English Text", 10, "bold")))
        self.back_main_menu.bind("<Leave>", lambda event:
        self.back_main_menu.configure(cursor="arrow",
                                      text_color="white", text='<--', font=("Old English Text", 20, "bold")))
        # deutsch dictionary label n attributes
        self.dict_label = ctk.CTkLabel(self.a1_deutsch_frame,
                                       text="Deutsch Dictionary",
                                       font=('Century Gothic', 15))
        self.dict_label.place(relx=0.15, rely=0.25)
        self.dict_label.bind("<Button-1>", lambda event:
        self.master.open_frame('a1_deutsch_frame', 'translator_frame'))
        self.dict_label.bind("<Enter>", lambda event:
        self.dict_label.configure(cursor="hand2", text_color="green",
                                  fg_color='transparent'))  # mainmenu_colour.frame_light))
        self.dict_label.bind("<Leave>", lambda event:
        self.dict_label.configure(cursor="arrow", text_color="white", fg_color='transparent'))
        # translatio game label
        self.game_label = ctk.CTkLabel(self.a1_deutsch_frame, text="Translation Game",
                                       font=('Century Gothic', 15))
        self.game_label.place(relx=0.15, rely=0.65)
        self.game_label.bind("<Button-1>", lambda event:
        self.master.open_frame("a1_deutsch_frame", 'translation_game_frame'))
        self.game_label.bind("<Enter>", lambda event:
        self.game_label.configure(cursor="hand2", text_color="green", fg_color='transparent'))
        self.game_label.bind("<Leave>", lambda event:
        self.game_label.configure(cursor="arrow", text_color="white", fg_color='transparent'))


        self.revision_label = ctk.CTkLabel(self.a1_deutsch_frame, text="Vocabulary Revision",
                                           font=('Century Gothic', 15))
        self.revision_label.place(relx=0.15, rely=0.7)
        self.revision_label.bind("<Button-1>", lambda event:
        self.master.open_frame("a1_deutsch_frame", 'translation_game_frame'))
        self.revision_label.bind("<Enter>", lambda event:
        self.revision_label.configure(cursor="hand2", text_color="green", fg_color='transparent'))
        self.revision_label.bind("<Leave>", lambda event:
        self.revision_label.configure(cursor="arrow", text_color="white", fg_color='transparent'))