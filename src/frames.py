#necessary frames import
from modern_main_menu import ModernMainMenuFrame as MainMenuFrame
from translatorframe import TranslatorFrame
from translationgameframe import TranslationGameFrame, GameOverFrame
from a1deutschframe import A1DeutschFrame
from modern_main_menu import ModernMainMenuFrame
from enhanced_proficiency_levels import (
    A2DeutschFrame,
    B1DeutschFrame,
    B2DeutschFrame
)
from modern_spaced_repetition import ModernSpacedRepetitionFrame
from modern_update_frame import ModernUpdateAppFrame as UpdateAppFrame
from modern_loading_frame import ModernLoadingFrame as LoadingFrame
from interactive_modes import InteractiveModeFrame, AdvancedTranslationFrame, PracticeScheduleFrame
from audio_manager import PronunciationPracticeFrame
from progress_dashboard import ProgressDashboardFrame


#from vocabularyrevisionframe import VocabularyRevisionFrame


frame_window = {"mainmenuframe":MainMenuFrame,"translation_game_frame":TranslationGameFrame,
                "game_over_frame":GameOverFrame,"translator_frame":TranslatorFrame,
                "a1_deutsch_frame":A1DeutschFrame,"a2_deutsch_frame":A2DeutschFrame,
                "b1_deutsch_frame":B1DeutschFrame,"b2_deutsch_frame":B2DeutschFrame,
                "update_app_frame":UpdateAppFrame, "loading_frame":LoadingFrame,
                "interactive_mode":InteractiveModeFrame,
                "advanced_translation":AdvancedTranslationFrame,
                "practice_schedule":PracticeScheduleFrame,
                "pronunciation_practice":PronunciationPracticeFrame,
                "progress_dashboard":ProgressDashboardFrame,
                "spaced_repetition_frame":ModernSpacedRepetitionFrame}


#function to transsion between frame, destroy previous n create new
def get_destination_frame(frame_name):
    return frame_window[frame_name]
