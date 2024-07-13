import threading
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
from assetlibmanager import lingleap_pic
from word_library import read_csv_files,random_word_gen
from functions import game_properties,write_to_csv
from app_variables import CSVPaths
word_lists = [(CSVPaths.NOUNS.value, 'nouns'),
              (CSVPaths.VERBS.value, 'verbs'),
              (CSVPaths.ADVERBS.value, 'adverbs'),
              (CSVPaths.ADJECTIVES.value, 'adjectives')]

def start_reading(app, word_lists, progress_bar, progress_var, status_label):
    def thread_function():
        read_csv_files(app, word_lists, progress_bar, progress_var)
        status_label.configure(text="Thread completed")

    threading.Thread(target=thread_function).start()

class UpdateAppFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_update_app_frame()

    def start_reading_button(self):
        self.start_update_label.configure(text='')
       # self.update_status_label.pack(pady=10)
        self.update_frame.configure( fg_color='#535454')
        self.logo_label.destroy()
        self.handle_loading_gif(self.update_frame, 'images/buildlib_gif_dark.gif')
        start_reading(self.update_frame, word_lists, self.progress_bar, self.progress_var, self.start_update_label)
        self.back_main_menu = ctk.CTkLabel(self.update_frame, text='<--',
                                           font=("Old English Text", 20, "bold"))
        self.back_main_menu.place(relx=0.1, rely=0.05)
        self.back_main_menu.bind("<Button-1>", lambda event:
        self.master.open_frame('update_app_frame', 'mainmenuframe'))
        self.back_main_menu.bind("<Enter>", lambda event:
        self.back_main_menu.configure(cursor="hand2",
                                      text_color="green", text='Main Menu', font=("Old English Text", 10, "bold")))
        self.back_main_menu.bind("<Leave>", lambda event:
        self.back_main_menu.configure(cursor="arrow",
                                      text_color="white", text='<--', font=("Old English Text", 20, "bold")))
        game_properties.is_library_built = True
        write_to_csv(CSVPaths.APP_PROPERTIES.value,game_properties.data)
        game_properties.default_answer = random_word_gen(game_properties.user_language, game_properties.word_type)

    def handle_loading_gif(self, frame, gif_path):
        try:
            self.gif = Image.open(gif_path)
            self.frames = []
            try:
                while True:
                    frame_image = self.gif.copy().convert("RGBA").resize((600, 600))
                    ctk_image = ctk.CTkImage(frame_image, size=(600, 600))
                    self.frames.append(ctk_image)
                    self.gif.seek(len(self.frames))
            except EOFError:
                pass

            if not self.frames:
                print("Error: No frames loaded from GIF.")
            else:
                self.gif_label = ctk.CTkLabel(frame)
                self.gif_label.pack(pady=10)
                self.delay = self.gif.info.get('duration', 100)

                self.update_gif(self.gif_label, self.frames, 0, self.delay)

        except FileNotFoundError:
            print(f"Error: GIF file not found - {gif_path}")

    def update_gif(self, label, frames, frame_index, delay):
        frame = frames[frame_index]
        frame_index = (frame_index + 1) % len(frames)
        label.configure(image=frame)
        label.image = frame
        label.after(delay, self.update_gif, label, frames, frame_index, delay)

    def setup_update_app_frame(self):
        self.master.change_geometry("800x1000")
        self.update_frame = ctk.CTkFrame(self, width=800, height=1000, fg_color='#292929')
        self.update_frame.pack(fill="both", expand=True)
        #self.update_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.progress_var = tk.StringVar()
        self.progress_var.set("0.00%")

        self.progress_bar = ttk.Progressbar(self.update_frame, orient='horizontal', mode='determinate', maximum=100)
        self.progress_bar.pack(pady=10)

        self.progress_label = ctk.CTkLabel(self.update_frame, textvariable=self.progress_var)
        self.progress_label.pack(pady=10)



        self.start_update_label = ctk.CTkLabel(self.update_frame, text="Thread not started")
        self.start_update_label.pack(pady=10)
        self.start_update_label.bind("<Button-1>", lambda event:
        self.start_reading_button())
        self.start_update_label.bind("<Enter>", lambda event:
        self.start_update_label.configure(cursor="hand2",
                                          text_color="green", text='start update'))
        self.start_update_label.bind("<Leave>", lambda event:
        self.start_update_label.configure(cursor="arrow",
                                          text_color="white", text='update not started'))
        self.logo_label = ctk.CTkLabel(self.update_frame, image=lingleap_pic, text="",
                                       font=ctk.CTkFont(size=20, weight="bold"), corner_radius=25)
        self.logo_label.place(relx=0.25, rely=0.2)


        #self.handle_loading_gif(self.update_frame, 'images/buildlib_gif_light.gif')

