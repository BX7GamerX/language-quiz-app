import customtkinter as ctk
import random
import csv
from datetime import date


from app_variables import CSVPaths, GameProperties


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
    random.shuffle(array_in)


# Merge function for merge sort algorithm
def merge(array, start, mid, end):
    n1 = mid - start + 1  # Size of the first sub-array
    n2 = end - mid  # Size of the second sub-array

    left_array = [0] * n1
    right_array = [0] * n2

    for i in range(n1):
        left_array[i] = array[start + i]
    for j in range(n2):
        right_array[j] = array[mid + 1 + j]

    i, j, k = 0, 0, start
    while i < n1 and j < n2:
        if left_array[i].data <= right_array[j].data:
            array[k] = left_array[i]
            i += 1
        else:
            array[k] = right_array[j]
            j += 1
        k += 1

    while i < n1:
        array[k] = left_array[i]
        i += 1
        k += 1

    while j < n2:
        array[k] = right_array[j]
        j += 1
        k += 1


# Merge sort function
def merge_sort(array, start, end):
    if start < end:
        mid = start + (end - start) // 2
        merge_sort(array, start, mid)
        merge_sort(array, mid + 1, end)
        merge(array, start, mid, end)


def binary_search(word_in, word_lib):
    # Base case: if the list is empty, return None
    if not word_lib:
        return None

    mid = len(word_lib) // 2

    # Base case: if the word is found, return it
    if word_lib[mid].data == word_in.lower():
        return word_lib[mid]
    # If the word is greater, search in the right half
    elif word_lib[mid].data < word_in.lower():
        return binary_search(word_in, word_lib[mid + 1:])
    # If the word is smaller, search in the left half
    else:
        return binary_search(word_in, word_lib[:mid])


def read_app_properties():
    # Read existing data from the CSV file
    today = date.today()
    default_heading =['date','app_version','word_type','score','trials_left','username','library_status','language','appearance','second_language']
    default_app_properties = [today, '0.4', 'nouns', '0', '20', 'lingo leaper', '1', 'english', 'Dark', 'deutsch']
    existing_data = []
    with open(CSVPaths.APP_PROPERTIES.value, 'r',
              newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            existing_data.append(row)
    are_the_values_default = False

    # Check and update values
    for i, row in enumerate(existing_data):
        for j, value in enumerate(row):
            if value.lower() == 'na':
                existing_data[i][j] = default_app_properties[j]  # Replace with defaults
                are_the_values_default = True

    if are_the_values_default :
        with open(CSVPaths.APP_PROPERTIES.value, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write each list as a row in the CSV file
            writer.writerow(default_heading)
            writer.writerow(default_app_properties)

    # Get the latest entry (if available)
    latest_entry = existing_data[-1] if existing_data else default_app_properties

    return latest_entry
def read_properties():
    app_property_data = read_app_properties()
    game_property = GameProperties(app_property_data[0], app_property_data[1],
                                   app_property_data[2], int(app_property_data[3]),
                                   int(app_property_data[4]), app_property_data[5],
                                   app_property_data[6], app_property_data[7],
                                   app_property_data[8], app_property_data[9])
    return game_property


game_properties = read_properties()

def write_to_csv(file_path, new_row):
    with open(file_path, 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(new_row)
    row1 = str(0)
    row2 = '0.4'
    with open(r'wordlib/libstatus', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

        # Override the first two rows with the given arguments
    if len(data) >= 2:
        data[0] = row1
        data[1] = row2
    elif len(data) == 1:
        data[0] = row1
        data.append(row2)
    else:
        data.append(row1)
        data.append(row2)
    with open(r'wordlib/libstatus', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)






