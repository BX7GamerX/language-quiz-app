#necessary frames import
from mainmenuframes import MainMenuFrame
from translatorframe import TranslatorFrame
from translationgameframe import TranslationGameFrame, GameOverFrame
from a1deutschframe import A1DeutschFrame


#from vocabularyrevisionframe import VocabularyRevisionFrame


frame_list = ["mainmenuframe",
              "translation_game_frame", "game_over_frame",
               "translator_frame","a1_deutsch_frame" ]
frame_window = [MainMenuFrame,
                TranslationGameFrame, GameOverFrame,
                TranslatorFrame,A1DeutschFrame]


#function to transsion between frame, destroy previous n create new
def get_destination_frame(frame_name):
    if frame_name in frame_list:
        return frame_window[frame_list.index(frame_name)]
    return 0
