# import pretty_errors
import random
import csv
import string
import threading
from app_variables import wordlib_location

from functions import merge_sort, binary_search


# Class representing a word node
class WordNode:
    def __init__(self, word, english_word=None, deutsch_word=None, french_word=None, spanish_word=None):
        self.data = word
        self.gender = "Not applicable"
        self.english_word = english_word
        self.deutsch_word = deutsch_word
        self.french_word = french_word
        self.spanish_word = spanish_word

        self.previous_node = None
        self.next_node = None

    def translate(self, language):
        if language == 'english':
            return self.english_word
        elif language == 'deutsch':
            return self.deutsch_word
        elif language == 'spanish':
            return self.spanish_word
        elif language == 'french':
            return self.french_word


# Class representing a doubly linked list of words
class WordList:
    def __init__(self):
        self.current_node = None
        self.head_node = None
        self.tail_node = None
        self.element_count = 0

    # Insert a new word node into the linked list
    def insert(self, new_node):
        if not self.head_node:
            self.head_node = new_node
            self.tail_node = new_node
        else:
            current_node = self.head_node
            while current_node:
                if new_node.data < current_node.data:
                    new_node.next_node = current_node
                    new_node.previous_node = current_node.previous_node

                    if current_node.previous_node:
                        current_node.previous_node.next_node = new_node
                    else:
                        self.head_node = new_node

                    current_node.previous_node = new_node
                    break
                elif not current_node.next_node:
                    current_node.next_node = new_node
                    new_node.previous_node = current_node
                    self.tail_node = new_node
                    break

                current_node = current_node.next_node

        self.element_count += 1

    def search(self, word_in):
        self.current_node = self.head_node
        while self.current_node.next_node:
            if word_in == self.current_node.data:
                return self.current_node
            self.current_node = self.current_node.next_node
        return None

    def delete(self, word_in):
        self.current_node = self.head_node

        while self.current_node.next_node:
            if word_in == self.current_node.data:
                self.connected_nodes = [self.current_node.english_word, self.current_node.deutsch_word,
                                        self.current_node.french_word, self.current_node.spanish_word]
                for elements in self.connected_nodes:
                    self.connectee_nodes = [self.elements.english_word, self.elements.deutsch_word,
                                            self.elements.french_word, self.elements.spanish_word]
                    for foreign in self.connectee_nodes:
                        if foreign.data == self.current_node.data:
                            foreign = None
                    elements = None
                if self.current_node.previous_node:
                    self.current_node.previous_node.next_node = None
                if self.current_node.next_node:
                    self.current_node.next_node.previous_node = None
                self.current_node.previous_node = None
                self.current_node.next_node = None
                self.current_node = None
                break
            self.current_node = self.current_node.next_node


# Generate an alphabet dictionary
def generate_alphabet_dict():
    alphabet_dict = {chr(ord('a') + i): WordList() for i in range(26)}
    alphabet_dict.update({'é': WordList(), 'œ': WordList()})

    return alphabet_dict


# Build a hash table for different word types
def build_hash():
    language_hash = {}
    article_hash = generate_alphabet_dict()
    noun_hash = generate_alphabet_dict()
    pronoun_hash = generate_alphabet_dict()
    adjective_hash = generate_alphabet_dict()
    verb_hash = generate_alphabet_dict()
    adverb_hash = generate_alphabet_dict()
    conjunction_hash = generate_alphabet_dict()
    preposition_hash = generate_alphabet_dict()
    all_words = []
    word_type = ["articles", "nouns", "pronouns", "adjectives", "verbs", "adverbs", "conjunctions", "prepositions",
                 'all']
    word_hash = [article_hash, noun_hash, pronoun_hash, adjective_hash, verb_hash, adverb_hash, conjunction_hash,
                 preposition_hash, all_words]
    for index in range(len(word_type)):
        language_hash.update({word_type[index]: word_hash[index]})

    return language_hash


# Initialize hashmaps for different languages
languages_array = ["english", "deutsch", "spanish", "french"]
english_hashmap = build_hash()
deutsch_hashmap = build_hash()
spanish_hashmap = build_hash()
french_hashmap = build_hash()
languages_hash_array = [english_hashmap, deutsch_hashmap, spanish_hashmap, french_hashmap]
language_hashmap = {languages_array[i]: languages_hash_array[i] for i in range(len(languages_array))}


# Check if a word exists in a CSV file
def check_name_exists(name, csv_filename):
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if name in row:
                return True
    return False


all_words_nodes_list = []


# Read CSV files and update the progress bar
def read_csv_files(app, word_properties, progress_bar, progress_var):
    def worker(file_path, word_types, lock_thread):
        nonlocal completed_threads
        nonlocal total_lines_read
        total_lines = sum(1 for _ in open(file_path))
        lines_read = 0

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    english_node = WordNode((row["English"]).lower())
                    deutsch_node = WordNode((row["German"]).lower())
                    spanish_node = WordNode((row["Spanish"]).lower())
                    french_node = WordNode((row["French"]).lower())

                    nodes_create = [english_node, deutsch_node, spanish_node, french_node]

                    for node in nodes_create:
                        node.english_word = english_node
                        node.deutsch_word = deutsch_node
                        node.french_word = french_node
                        node.spanish_word = spanish_node
                        all_words_nodes_list.append(node)

                    if check_name_exists("Pronoun", file_path):
                        deutsch_node.gender = row["Pronoun"]

                    for _ in range(4):
                        language_hashmap[languages_array[_]]['all'].append(nodes_create[_])
                        language_hashmap[languages_array[_]][word_types][nodes_create[_].data[0].lower()].insert(
                            nodes_create[_])
                    lines_read += 1

                    with lock_thread:
                        total_lines_read += 1
                        progress = total_lines_read / total_lines_sum
                        app.after(0, update_progress, progress_bar, progress_var, progress)
                except KeyError as e:
                    print(f"KeyError: {e} in file {file_path}")
            for languages in languages_array:
                merge_sort(language_hashmap[languages]['all'], 0, len(language_hashmap[languages]['all']) - 1)
            merge_sort(all_words_nodes_list, 0, len(all_words_nodes_list) - 1)
            print(f"Done for {file_path}")

        with lock_thread:
            completed_threads += 1
            progress = completed_threads / total_threads
            app.after(0, update_progress, progress_bar, progress_var, progress)

    threads = []
    total_threads = len(word_properties)
    completed_threads = 0
    total_lines_read = 0

    total_lines_sum = sum(sum(1 for _ in open(file_path)) for file_path, _ in word_properties)

    lock = threading.Lock()

    for file_path, word_type in word_properties:
        thread = threading.Thread(target=worker, args=(file_path, word_type, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    app.library_built = True


# Start reading CSV files in a separate thread
def start_reading(app, progress_bar, progress_var):
    threading.Thread(target=read_csv_files, args=(app, wordlib_location, progress_bar, progress_var)).start()


# Update the progress bar
def update_progress(progress_bar, progress_var, progress):
    progress_var.set(f"{progress * 100:.2f}%")
    progress_bar["value"] = progress * 100


def translate_one(word_in, to_language):
    result_node = binary_search(word_in, all_words_nodes_list)
    return result_node.translate(to_language).data


def translate_two(word_in, from_language, to_language, wordtype):
    temp_result_node = language_hashmap[from_language][wordtype][word_in[0].lower()].head_node
    if temp_result_node:
        while temp_result_node.next_node:
            if temp_result_node.data == word_in:
                return temp_result_node.translate(to_language).data
            temp_result_node = temp_result_node.next_node
    return None


def random_word_gen(language, word_type):
    temp_word_node = language_hashmap[language][word_type][random.choice(string.ascii_lowercase)].head_node
    if temp_word_node:
        while temp_word_node.next_node:
            if bool(random.randint(0, 1)) and temp_word_node:
                return temp_word_node.data
                temp_word_node = temp_word_node.next_node
    else:
        while not temp_word_node:
            random_char = random.choice(string.ascii_lowercase)
            temp_word_node = language_hashmap[language][word_type][random_char].head_node

    return temp_word_node.data
