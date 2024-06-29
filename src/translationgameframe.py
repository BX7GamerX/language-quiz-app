import customtkinter as ctk
from word_library import Random_word_gen, translate_one as translate
import tkinter
from functions import shuffle_cubic
import random


class GameConstants():
    def __init__(self, Word_type, Score, Trials_left):
        self.word_type = Word_type
        self.score = Score
        self.trials_left = Trials_left


game_properties = GameConstants('nouns', 0, 20)
game_properties.word_type = 'nouns'

one_answer = Random_word_gen(game_properties.word_type)
answer_array = ["one", "two", "three", "error"]


def setup_choices(answer):
    answer_array[0] = (translate(answer))
    answer_array[1] = (translate(Random_word_gen(game_properties.word_type)))
    answer_array[2] = (translate(Random_word_gen(game_properties.word_type)))
    answer_array[3] = (translate(Random_word_gen(game_properties.word_type)))
    shuffle_cubic(answer_array)


class TranslationGameFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_translation_game_frame(one_answer)

    def setup_translation_game_frame(self, answer_one):
        self.master.change_geometry("400x600")
        self.spielen_frame = ctk.CTkFrame(self, width=400, height=600)  # Frame n it's attributes
        self.spielen_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.multi_choice_frame = ctk.CTkFrame(self.spielen_frame, width=300, height=200)
        self.multi_choice_frame.place(relx=0.125, rely=0.4)
        self.randy_word = answer_one
        setup_choices(one_answer)
        self.section_B_function = ctk.CTkLabel(self.spielen_frame, text="Translation Game",
                                               anchor='center', font=("Old English Text", 20, "bold"))
        self.section_B_function.place(relx=0.3, rely=0.05)
        self.word_type_label = ctk.CTkLabel(self.spielen_frame, text="Word Type:", anchor="center")
        self.word_type_label.place(relx=0.4, rely=0.1)
        self.word_type_options = ctk.CTkOptionMenu(self.spielen_frame,
                                                   values=["nouns", "adjectives", "verbs", "adverbs"], anchor="center",
                                                   command=self.set_word_type)
        self.word_type_options.place(relx=0.35, rely=0.15)
        self.Enquiry_Label = ctk.CTkLabel(self.spielen_frame, text="What is the English Translation of :",
                                          anchor="center", font=("Arial", 13, "bold"))
        self.Enquiry_Label.place(relx=0.2, rely=0.25)
        self.word_entry_name = ctk.CTkLabel(self.spielen_frame, text=self.randy_word, anchor="center",
                                            font=("Arial", 13, "italic"))
        self.word_entry_name.place(relx=0.4, rely=0.325)

        self.choice_label = ctk.CTkLabel(self.multi_choice_frame, text='Choices:', font=("Arial", 18, "bold"))
        self.choice_label.place(relx=0.35, rely=0.05)

        self.answer_1_label = ctk.CTkLabel(self.multi_choice_frame, text=answer_array[0], font=("Arial", 15, "bold"))
        self.answer_1_label.place(relx=0.1, rely=0.25)
        self.answer_1_label.bind("<Button-1>", lambda event: self.trial_check(answer_array[0]))
        self.answer_1_label.bind("<Enter>",
                                 lambda event: self.answer_1_label.configure(cursor="hand2", text_color="green",
                                                                             fg_color='transparent'))
        self.answer_1_label.bind("<Leave>",
                                 lambda event: self.answer_1_label.configure(cursor="arrow", text_color="white",
                                                                             fg_color='transparent'))

        self.answer_2_label = ctk.CTkLabel(self.multi_choice_frame, text=answer_array[1], font=("Arial", 15, "bold"))
        self.answer_2_label.place(relx=0.575, rely=0.25)
        self.answer_2_label.bind("<Button-1>", lambda event: self.trial_check(answer_array[1]))
        self.answer_2_label.bind("<Enter>",
                                 lambda event: self.answer_2_label.configure(cursor="hand2", text_color="green",
                                                                             fg_color='transparent'))
        self.answer_2_label.bind("<Leave>",
                                 lambda event: self.answer_2_label.configure(cursor="arrow", text_color="white",
                                                                             fg_color='transparent'))

        self.answer_3_label = ctk.CTkLabel(self.multi_choice_frame, text=answer_array[2], font=("Arial", 15, "bold"))
        self.answer_3_label.place(relx=0.1, rely=0.5)
        self.answer_3_label.bind("<Button-1>", lambda event: self.trial_check(answer_array[2]))
        self.answer_3_label.bind("<Enter>",
                                 lambda event: self.answer_3_label.configure(cursor="hand2", text_color="green",
                                                                             fg_color='transparent'))
        self.answer_3_label.bind("<Leave>",
                                 lambda event: self.answer_3_label.configure(cursor="arrow", text_color="white",
                                                                             fg_color='transparent'))

        self.answer_4_label = ctk.CTkLabel(self.multi_choice_frame, text=answer_array[3], font=("Arial", 15, "bold"))
        self.answer_4_label.place(relx=0.575, rely=0.5)
        self.answer_4_label.bind("<Button-1>", lambda event: self.trial_check(answer_array[3]))
        self.answer_4_label.bind("<Enter>",
                                 lambda event: self.answer_4_label.configure(cursor="hand2", text_color="green",
                                                                             fg_color='transparent'))
        self.answer_4_label.bind("<Leave>",
                                 lambda event: self.answer_4_label.configure(cursor="arrow", text_color="white",
                                                                             fg_color='transparent'))

        self.confirm_entry_label = ctk.CTkLabel(self.multi_choice_frame, text="[Results will appear here]", anchor="w",
                                                font=("Arial", 13, "italic"))
        self.confirm_entry_label.place(relx=0.05, rely=0.75)

        self.score_label = ctk.CTkLabel(self.spielen_frame, text=f"Score :{game_properties.score}    ", anchor="w",
                                        font=("Arial", 17, "bold"))
        self.score_label.place(relx=0.375, rely=0.75)
        self.score_label.bind("<Enter>", lambda event: self.score_label.configure(text_color="green"))
        self.score_label.bind("<Leave>", lambda event: self.score_label.configure(text_color="white"))

        self.back_main_menu = ctk.CTkLabel(self.spielen_frame, text='<--',
                                           font=("Old English Text", 20, "bold"))
        self.back_main_menu.place(relx=0.1, rely=0.05)
        self.back_main_menu.bind("<Button-1>", lambda event:
        self.master.open_frame('translation_game_frame', 'mainmenuframe'))
        self.back_main_menu.bind("<Enter>", lambda event:
        self.back_main_menu.configure(cursor="hand2",
                                      text_color="green", text='Main Menu', font=("Old English Text", 10, "bold")))
        self.back_main_menu.bind("<Leave>", lambda event:
        self.back_main_menu.configure(cursor="arrow",
                                      text_color="white", text='<--', font=("Old English Text", 20, "bold")))

        self.trials_left_label = ctk.CTkLabel(self.spielen_frame, text=f" Trials Left :{game_properties.trials_left}",
                                              anchor="w", font=("Arial", 17, "bold"), text_color='white')
        self.trials_left_label.place(relx=0.32, rely=0.85)
        self.user_score = 0
        self.user_trials_left = 10

        self.positive_comments = ["Great Job lad", "Keep Going", "Bravo!", "One more", "Great Job", "Kudos",
                                  "Explemprary Job", "Tou can Stop", "Bravo!"]
        self.negative_comments = ["Really Lad", "That's also a trial", "N you still think u r smart",
                                  "Keep practising Lad", "We too did Start somewhere", "there is no wrong answer",
                                  "Neither I could answer that !", "U sure about that ?", "Really Bruh!"]

    def set_word_type(self, word_type):
        game_properties.word_type = word_type
        self.randy_word = Random_word_gen(game_properties.word_type)
        self.word_entry_name.configure(text=self.randy_word)

    def trial_check(self, answer_in):

        self.word_entry_name.configure(text=self.randy_word)

        translation = translate(self.randy_word)
        word_in = answer_in.lower()
        if game_properties.trials_left > 0:

            if game_properties.trials_left <= 5:
                self.trials_left_label.configure(text_color='red')

            else:
                self.trials_left_label.configure(text_color='white')
            if (word_in == translation):
                self.confirm_entry_label.configure(text=f"{self.positive_comments[random.randint(0, 8)]}! ")
                self.confirm_entry_label.place(relx=0.04, rely=0.75)
                self.randy_word = Random_word_gen(game_properties.word_type)
                self.word_entry_name.configure(text=self.randy_word)
                setup_choices(self.randy_word)
                self.answer_1_label.configure(text=answer_array[0])
                self.answer_2_label.configure(text=answer_array[1])
                self.answer_3_label.configure(text=answer_array[2])
                self.answer_4_label.configure(text=answer_array[3])
                self.score_label.configure(text=f"Score :{game_properties.score}  ")
                self.trials_left_label.configure(text=f" Trials Left :{game_properties.trials_left}")

                game_properties.score += 3
            elif (word_in != translation):

                self.confirm_entry_label.configure(
                    text=f"{self.negative_comments[random.randint(0, 8)]}! answer was :'{translation}'  ")
                self.confirm_entry_label.place(relx=0.05, rely=0.75)
                self.randy_word = Random_word_gen(game_properties.word_type)
                self.word_entry_name.configure(text=self.randy_word)
                setup_choices(self.randy_word)
                self.answer_1_label.configure(text=answer_array[0])
                self.answer_2_label.configure(text=answer_array[1])
                self.answer_3_label.configure(text=answer_array[2])
                self.answer_4_label.configure(text=answer_array[3])
                self.score_label.configure(text=f"Score :{game_properties.score}  ")
                self.trials_left_label.configure(text=f" Trials Left :{game_properties.trials_left}")

                game_properties.trials_left -= 1
        else:
            self.master.open_frame('translation_game_frame', 'game_over_frame')


class GameOverFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_game_over_frame()

    def setup_game_over_frame(self):
        self.master.change_geometry("400x600")
        self.over_spielen_frame = ctk.CTkFrame(self, width=400, height=600, corner_radius=20)  # Frame n it's attributes
        self.over_spielen_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.game_over_Label = ctk.CTkLabel(self.over_spielen_frame, text=" GAME OVER",
                                            font=("Old English Text", 35, "bold"), text_color='#0890ff')
        self.game_over_Label.place(relx=0.2, rely=0.25)
        self.score_label = ctk.CTkLabel(self.over_spielen_frame, text=f" Score:{game_properties.score}",
                                        font=("Old English Text", 30, "bold"), text_color='#00ff76')
        self.score_label.place(relx=0.3, rely=0.35)
        self.out_of_trials_label = ctk.CTkLabel(self.over_spielen_frame, text="Out of Trials", anchor="w",
                                                font=("Arial", 17, "bold"), text_color='white')
        self.out_of_trials_label.place(relx=0.32, rely=0.85)
        self.restart_button = ctk.CTkButton(self.over_spielen_frame, text="Restart", hover_color='green',
                                            command=self.restart_game)
        self.restart_button.place(relx=0.3, rely=0.45)
        self.main_menu_button = ctk.CTkButton(self.over_spielen_frame, text="Main menu", command=self.back_to_main_menu)
        self.main_menu_button.place(relx=0.3, rely=0.55)
        game_properties.score = 0
        game_properties.trials_left = 20

    def restart_game(self):
        self.master.open_frame("game_over_frame", 'translation_game_frame')

    def back_to_main_menu(self):
        self.master.open_frame("game_over_frame", 'mainmenuframe')




