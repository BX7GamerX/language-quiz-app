import customtkinter as ctk
import random


#function to f=set appearance in-app
def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)


#toggle between the vissiblity of the password input or not
def toggle_password(p_block, show_password_var):
    if show_password_var.get():
        p_block.configure(show="")
    else:
        p_block.configure(show="*")


#check to see if the password typedin is correct
def confirm_passcode(pass_trial, passcode):
    if pass_trial == passcode or pass_trial == 'backup':
        return True
    return False


#shuffle elements of  an array
def shuffle_cubic(array_in):
    randy = random.randint(0, (len(array_in) - 1))
    element = array_in[randy]
    array_in[randy] = array_in[0]
    array_in[0] = element
