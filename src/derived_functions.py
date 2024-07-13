from word_library import random_word_gen, translate_two
from functions import shuffle_cubic, game_properties


def setup_choices(question_word, from_language, to_language):
    if game_properties.is_library_built:

        game_properties.default_answer_array[0] = (
            translate_two(question_word, from_language, to_language, game_properties.word_type))
        for _ in range(3):
            game_properties.default_answer_array[_+1] = random_word_gen(to_language, game_properties.word_type)

        shuffle_cubic(game_properties.default_answer_array)
    else:
        shuffle_cubic(game_properties.default_answer_array)
        print(f'is lib build {game_properties.is_library_built}')
