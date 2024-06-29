# import for the GUI
import customtkinter as ctk

# necessary frames for start up
from frames import get_destination_frame
from welcomeframes import WelcomeFrame
from mainmenuframes import MainMenuFrame
# import app properties
from assetlibmanager import Myapp, mainmenu_colour

# initial properties
ctk.set_default_color_theme(Myapp.default_theme)  # default color of different widgets
ctk.set_appearance_mode(Myapp.apperance_mode)  # default color scheme/ theme


# class for the main application
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('BX7 Gamer')
        self.geometry('600x462')
        self.frames = {}
        self.main_frame = WelcomeFrame(master=self)

        self.main_frame.pack(expand=True, fill="both")  # Expand to fill the main app window

    # Change the window geometry
    def change_geometry(self, new_geometry):
        self.geometry(new_geometry)

    # change title on the window
    def change_title(self, new_title):
        self.title(new_title)

    # function to change apperance of the app{Theme in this case}
    def change_apperance_mode(self):
        if Myapp.apperance_mode == 'Dark':
            ctk.set_appearance_mode('Light')
            Myapp.apperance_mode = 'Light'
        elif Myapp.apperance_mode == 'Light':
            ctk.set_appearance_mode('Dark')
            Myapp.apperance_mode = 'Dark'
        else:
            ctk.set_appearance_mode('System')

    # fucntion to transition through various app frames
    def open_frame(self, origin_frame, destination_frame):
        # if orign frame is welcome frame then detinati is predefined sois the 'destroy frame' mechanism
        if origin_frame == 'welcomeframe':
            self.main_frame.destroy()
            # Start logged in frame
            self.mainmenuframe = MainMenuFrame(self, fg_color=mainmenu_colour.frame_darker)
            self.frames["mainmenuframe"] = self.mainmenuframe
            self.mainmenuframe.pack(expand=True, fill="both")
        else:
            self.main_frame.destroy()
            self.frames[origin_frame].destroy()
            self.destinationframe = get_destination_frame(destination_frame)(self)
            self.frames[destination_frame] = self.destinationframe
            self.destinationframe.pack(expand=True, fill='both')
