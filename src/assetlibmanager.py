from PIL import Image
import customtkinter as ctk
import os
import sys
from word_library import random_word_gen

# converts to relative path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



class image_class:
    def __init__(self, Location_dark, Location_light):
        self.location_dark = Location_dark
        self.location_light = Location_light


# handles the location of the images used

welcome_screen_logo = image_class(resource_path(r"images/logo.png"),
                                  resource_path(r"images/logo.png"))
learn_duetsch_logo = image_class(resource_path(r"images/Deutsch/A1/spielen.jpg"),
                                 resource_path(r"images/Deutsch/A1/spielen.jpg"))

lingoleap_logo = image_class(resource_path(r'images/lingoleap_logo_dark.png'),
                             resource_path(r'images/lingoleap_logo_light.png'))

lingleap_pic = ctk.CTkImage(dark_image=Image.open(lingoleap_logo.location_dark),
                            light_image=Image.open(lingoleap_logo.location_light),size=(400, 400))

welcome_screen_pic = ctk.CTkImage(dark_image=Image.open(welcome_screen_logo.location_light),
                                  light_image=Image.open(welcome_screen_logo.location_dark), size=(150, 150))
learn_deutsch_pic = ctk.CTkImage(dark_image=Image.open(learn_duetsch_logo.location_dark),
                                 light_image=Image.open(learn_duetsch_logo.location_light), size=(200, 100))













