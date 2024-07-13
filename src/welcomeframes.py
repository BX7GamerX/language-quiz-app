import customtkinter as ctk

import tkinter  # for center orientation
from functions import confirm_passcode, toggle_password , game_properties  # functions module import
from assetlibmanager import welcome_screen_pic


user_logo = welcome_screen_pic

# external file handling for the passcode and the version
app_version = 0.1

passcode = "him"



class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_welcome_frame()

        # main function to setup up the frame and its widgets

    def setup_welcome_frame(self):

        self.master.change_geometry("400x475")
        # the Welcome frame
        self.welcome_frame = ctk.CTkFrame(self, width=320, height=380)  # Frame n it's attributes
        self.welcome_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)  # frame position relative to the window

        # The frame label/Name
        self.welcome_label = ctk.CTkLabel(self.welcome_frame, text="Welcome",
                                          font=('Century Gothic', 25))
        self.welcome_label.place(relx=0.3, rely=0.05)
        self.welcome_label.bind("<Enter>", lambda event:
        self.welcome_label.configure(cursor="hand2", text_color="green"))
        self.welcome_label.bind("<Leave>", lambda event:
        self.welcome_label.configure(cursor="arrow", text_color="#92c3c9"))
        self.welcome_label.bind("<Button-1>", lambda event:
        self.master.change_apperance_mode())

        # Logo label impimentation
        self.logo_label = ctk.CTkLabel(self.welcome_frame, image=user_logo, text="",
                                       font=ctk.CTkFont(size=20, weight="bold"), corner_radius=25)
        self.logo_label.place(relx=0.2, rely=0.15)  # position
        # password
        self.show_password_var = ctk.BooleanVar()  # bool to check wheither or not the show passcode was pressed
        self.pass_code_entry = ctk.CTkEntry(master=self.welcome_frame, width=220,
                                            placeholder_text="Password", show="*")
        self.pass_code_entry.place(relx=0.17, rely=0.55)
        self.pass_code_entry.focus()


        self.show_password = ctk.CTkCheckBox(master=self.welcome_frame,
                                             text="Show Password", font=('Century Gothic', 12),
                                             command=lambda: toggle_password(self.pass_code_entry,
                                                                             self.show_password_var),
                                             variable=self.show_password_var)
        self.show_password.place(x=85, y=245)
        # forgot label n its attributes
        self.forgot_label = ctk.CTkLabel(master=self.welcome_frame,
                                         text="Forgot password/New?",
                                         font=('Century Gothic', 10))
        self.forgot_label.place(x=90, y=280)
        self.forgot_label.bind("<Enter>", lambda event:
        self.forgot_label.configure(cursor="hand2", text_color="green"))
        self.forgot_label.bind("<Leave>", lambda event:
        self.forgot_label.configure(cursor="arrow", text_color="white"))
        # error label and its attributes
        self.error_label = ctk.CTkLabel(master=self.welcome_frame, text="Please update app"
                                        if not game_properties.is_library_built else game_properties.user_name,
                                        font=('Century Gothic', 10), text_color="#ff0004")
        self.error_label.place(x=105, y=350)
        self.error_label.bind("<Enter>", lambda event:
        self.error_label.configure(cursor="hand2", text_color="green"))
        self.error_label.bind("<Leave>", lambda event:
        self.error_label.configure(cursor="arrow", text_color="#92c3c9"))
        self.error_label.bind("<Button-1>", lambda event:
        self.master.open_frame("welcomeframe", 'update_app_frame'))
        # login button an its attributes
        self.login_button = ctk.CTkButton(master=self.welcome_frame,
                                          width=100, text="Login",
                                          corner_radius=6, fg_color="#3498db", text_color="#ffffff",
                                          hover_color="green", command=self.check_passcode)
        self.login_button.place(x=100, y=325)
        # appversion label and it attributes
        self.app_version_label = ctk.CTkLabel(self.welcome_frame,
                                              text=app_version,
                                              font=('Century Gothic', 10))
        self.app_version_label.bind("<Enter>", lambda event:
        self.app_version_label.configure(cursor="hand2", text_color="blue"))
        self.app_version_label.bind("<Leave>", lambda event:
        self.app_version_label.configure(cursor="arrow", text_color="white"))
        self.app_version_label.place(x=250, y=335)

    def check_passcode(self):
        if self.pass_code_entry.get() != "":
            if confirm_passcode(self.pass_code_entry.get(), passcode):
                self.master.open_frame("welcomeframe", 'mainmenuframe')
            else:
                self.error_label.configure(text="Invalid Password")
        else:
            self.error_label.configure(text="Invalid Entry")