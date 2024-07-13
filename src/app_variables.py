from enum import Enum
import os
import sys


# converts to relative path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class CSVPaths(Enum):
    APP_PROPERTIES = resource_path(r'wordlib/appproperties')
    NOUNS = resource_path(r'wordlib/nouns')
    VERBS = resource_path(r'wordlib/verbs')
    ADJECTIVES = resource_path(r'wordlib/adjectives')
    ADVERBS = resource_path(r'wordlib/adverbs')

wordlib_location = [
    (CSVPaths.NOUNS.value, "nouns"),
    (CSVPaths.ADJECTIVES.value, "adjectives"),
    (CSVPaths.ADVERBS.value, "adverbs"),
    (CSVPaths.VERBS.value, "verbs"),
]

class properties_set:
    def __init__(self, Apperance_mode, Default_theme):
        self.apperance_mode = Apperance_mode
        self.default_theme = Default_theme
        self.library_builed = False


class colour_used:
    def __init__(self, Cyan_colour, blue_colour, greenish):
        self.frame_light = Cyan_colour
        self.frame_dark = blue_colour
        self.frame_darker = greenish


mainmenu_colour = colour_used("#03404d", "#2a3342", "#424242")  # "#011636"#046073
Myapp = properties_set('Dark', 'dark-blue')

class GameProperties():
    def __init__(self, date, default_app_version, default_word_type,
                 default_score, default_trials_left, default_user_name,
                 default_library_status, default_language, default_appearance,
                 default_second_language):
        self.word_type = default_word_type
        self.score = default_score
        self.trials_left = default_trials_left
        self.user_name = default_user_name
        self.is_library_built = True if default_library_status == 1 else False
        self.user_language = default_language
        self.date = date
        self.app_version = default_app_version
        self.appearance = default_appearance
        self.second_language = default_second_language
        self.default_answer = "word library not found"
        self.data = [self.date,self.app_version,self.word_type,self.score,
                     self.trials_left,self.user_name,self.is_library_built,
                     self.user_language,self.appearance,self.second_language]
        self.default_answer_array =["first ", "second", "third", "fourth"]
