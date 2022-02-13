from typing import List
import random
import pandas as pd
from game import word_list


def letter_to_number(character):
    """
    Convert letter to its alphabetical order number
    """
    return ord(character.lower()) - 96


def number_to_letter(number):
    """
    Convert alphabetical order number to lower case letter
    """
    return chr(number + 96)


class NaiveBot:
    def __init__(self, complete_word_set):
        self.encoded_dictionary = []
        for word in complete_word_set:
            self.encoded_dictionary.append(self.encode_word(word))
        self.reset_dictionary()

    def reset_dictionary(self) -> None:
        self.filtered_dictionary = self.encoded_dictionary.copy()

    def process_feedback(self, guess_word: str, score: List[int]) -> None:
        encoded_word = self.encode_word(guess_word)
        filtered_matrix = pd.DataFrame(self.filtered_dictionary)
        # Filter out words with incorrect letters
        incorrect_letters = [char for idx, char in enumerate(encoded_word) if score[idx] == -1]
        filtered_matrix = filtered_matrix[~filtered_matrix.isin(incorrect_letters).any(axis=1)]
        # Filter words with known misplaced letters
        misplaced_letters = [(char, idx) for idx, char in enumerate(encoded_word) if score[idx] == 0]
        for misplaced in misplaced_letters:
            cols = list(filtered_matrix.columns)
            cols.remove(misplaced[1])
            filtered_matrix = filtered_matrix[(filtered_matrix[cols].isin([misplaced[0]]).any(axis=1))
                                              & (filtered_matrix[[misplaced[1]]] != misplaced[0]).any(axis=1)]
        # Filter for correctly placed letters
        correct_letters = [(char, idx) for idx, char in enumerate(encoded_word) if score[idx] == 1]
        for correct in correct_letters:
            filtered_matrix = filtered_matrix[(filtered_matrix[[correct[1]]] == correct[0]).any(axis=1)]

        self.filtered_dictionary = filtered_matrix.values.tolist()

    def guess(self) -> str:
        return self.decode_word(random.choice(self.filtered_dictionary))

    @staticmethod
    def encode_word(word) -> List[int]:
        encoded = []
        for char in word:
            encoded.append(letter_to_number(char) - 1)
        return encoded

    @staticmethod
    def decode_word(encoded_word) -> str:
        return ''.join([number_to_letter(char + 1) for char in encoded_word])

naive_bot = NaiveBot(word_list)