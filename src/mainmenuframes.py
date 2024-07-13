import customtkinter as ctk
import tkinter
from assetlibmanager import  learn_deutsch_pic
from app_variables import mainmenu_colour

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
        self.Learn_Deutch_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)  # relx=0.5, rely=0.5, anchor=tkinter.CENTER)
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
                                                                              "a1_deutsch_frame"))  # open_a1_deutsch_frame('mainmenuframe'))
        self.A1_label.bind("<Enter>", lambda event: self.A1_label.configure(cursor="hand2", text_color="green",
                                                                            fg_color='transparent'))  # mainmenu_colour.frame_light))
        self.A1_label.bind("<Leave>", lambda event: self.A1_label.configure(cursor="arrow", text_color="white",
                                                                            fg_color='transparent'))  # mainmenu_colour.frame_dark))

        self.A2_label = ctk.CTkLabel(self.Learn_Deutch_frame, text="A2 - Deutsch",
                                     font=('Century Gothic', 15))
        self.A2_label.place(relx=0.35, rely=0.55)
        self.A2_label.bind("<Button-1>", lambda event: self.master.open_forgot_password_frame())
        self.A2_label.bind("<Enter>", lambda event: self.A2_label.configure(cursor="hand2", text_color="green",
                                                                            fg_color='transparent'))  # mainmenu_colour.frame_light))
        self.A2_label.bind("<Leave>", lambda event: self.A2_label.configure(cursor="arrow", text_color="white",
                                                                            fg_color='transparent'))  # mainmenu_colour.frame_dark))

        self.B1_label = ctk.CTkLabel(self.Learn_Deutch_frame, text="B1 - Deutsch",
                                     font=('Century Gothic', 15))
        self.B1_label.place(relx=0.35, rely=0.65)
        self.B1_label.bind("<Button-1>", lambda event: self.master.open_forgot_password_frame())
        self.B1_label.bind("<Enter>", lambda event: self.B1_label.configure(cursor="hand2", text_color="green",
                                                                            fg_color='transparent'))  # mainmenu_colour.frame_light))
        self.B1_label.bind("<Leave>", lambda event: self.B1_label.configure(cursor="arrow", text_color="white",
                                                                            fg_color='transparent'))  # mainmenu_colour.frame_dark))

        self.B2_label = ctk.CTkLabel(self.Learn_Deutch_frame, text="B2 - Deutsch",
                                     font=('Century Gothic', 15))
        self.B2_label.place(relx=0.35, rely=0.75)
        self.B2_label.bind("<Button-1>", lambda event: self.master.open_forgot_password_frame())
        self.B2_label.bind("<Enter>", lambda event: self.B2_label.configure(cursor="hand2", text_color="green",
                                                                            fg_color='transparent'))  # mainmenu_colour.frame_light))
        self.B2_label.bind("<Leave>", lambda event: self.B2_label.configure(cursor="arrow", text_color="white",
                                                                            fg_color='transparent'))  # mainmenu_colour.frame_dark))

        self.Cant_decide_label = ctk.CTkLabel(self.Learn_Deutch_frame, text="Can't Decide?",
                                              font=('Century Gothic', 10))
        self.Cant_decide_label.place(relx=0.38, rely=0.85)
        self.Cant_decide_label.bind("<Button-1>",
                                    lambda event: self.master.open_frame("mainmenuframe", 'update_app_frame'))
        self.Cant_decide_label.bind("<Enter>",
                                    lambda event: self.Cant_decide_label.configure(cursor="hand2", text_color="blue",
                                                                                   fg_color='transparent'))  # mainmenu_colour.frame_light))
        self.Cant_decide_label.bind("<Leave>",
                                    lambda event: self.Cant_decide_label.configure(cursor="arrow", text_color="white",
                                                                                   fg_color='transparent'))  # mainmenu_colour.frame_dark))


pass
