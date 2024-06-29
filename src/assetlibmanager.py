from PIL import Image
import customtkinter as ctk
import os
import sys


# converts to relative path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
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

welcome_screen_pic = ctk.CTkImage(dark_image=Image.open(welcome_screen_logo.location_light),
                                  light_image=Image.open(welcome_screen_logo.location_dark), size=(150, 150))
learn_deutsch_pic = ctk.CTkImage(dark_image=Image.open(learn_duetsch_logo.location_dark),
                                 light_image=Image.open(learn_duetsch_logo.location_light), size=(200, 100))


class properties_set:
    def __init__(self, Apperance_mode, Default_theme):
        self.apperance_mode = Apperance_mode
        self.default_theme = Default_theme


class colour_used:
    def __init__(self, Cyan_colour, blue_colour, greenish):
        self.frame_light = Cyan_colour
        self.frame_dark = blue_colour
        self.frame_darker = greenish


mainmenu_colour = colour_used("#03404d", "#2a3342", "#424242")  # "#011636"#046073
Myapp = properties_set('Dark', 'dark-blue')
