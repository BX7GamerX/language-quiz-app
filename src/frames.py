#necessary frames import
from mainmenuframes import MainMenuFrame
from translatorframe import TranslatorFrame
from translationgameframe import TranslationGameFrame, GameOverFrame
from a1deutschframe import A1DeutschFrame
from updateapp import UpdateAppFrame


#from vocabularyrevisionframe import VocabularyRevisionFrame


frame_window = {"mainmenuframe":MainMenuFrame,"translation_game_frame":TranslationGameFrame,
                "game_over_frame":GameOverFrame,"translator_frame":TranslatorFrame,
                "a1_deutsch_frame":A1DeutschFrame,"update_app_frame":UpdateAppFrame}


#function to transsion between frame, destroy previous n create new
def get_destination_frame(frame_name):
    return frame_window[frame_name]
