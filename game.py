import config

import random
from tqdm import tqdm
from typing import Union, List
from rich import print

# Load words
word_list = []
with open('words.txt', mode='r') as word_file:
    for line in word_file:
        word_list.append(line.rstrip('\n'))


def score_guess(guess_word: str, correct_answer: str) -> List[int]:
    """
    Returns an array that scores each letter of the guessed word against the answer with:
    -1 = letter not in word
    0 = correct letter but incorrect placement
    1 = correct letter and placement

    :param guess_word: Word being guessed by user
    :param correct_answer: Correct answer
    :return: A score array e.g. [0, -1, -1, -1, 1]
    """
    score = []
    for idx, char in enumerate(guess_word):
        if correct_answer[idx] == char:
            score.append(1)
        elif char in correct_answer:
            score.append(0)
        else:
            score.append(-1)
    return score


def pretty_feedback(score: List[int], guess_word: str) -> None:
    """
    Prints feedback to the users guess with colours indicating whether the letter and placement was correct
    :param score: Score array (see score_guess) e.g. [0, 0, 0, 1, -1]
    :param guess_word: The guess word
    :return:
    """

    def _colour(char_score):
        if char_score == -1:
            return config.INCORRECT_COLOUR
        elif char_score == 0:
            return config.WRONG_PLACEMENT_COLOUR
        else:
            return config.CORRECT_COLOUR

    output = ''
    for i in range(len(score)):
        output += f'[bold {_colour(score[i])}]{guess_word[i]}[/bold {_colour(score[i])}] '
    print(output)


class Wordle:
    def __init__(self,
                 manual: bool,
                 verbose: bool,
                 bot=None,
                 rounds: int = 1):
        if not manual:
            assert bot is not None
            self.bot = bot

        self.manual = manual
        self.verbose = verbose

        self.wins = 0
        self.points_scored = 0

        for _ in range(rounds):
            score = self.round()
            if score > 0:
                self.wins += 1
            self.points_scored += score
            if not manual:
                self.bot.reset_dictionary()

    def round(self) -> int:
        """
        Play a round of Wordle
        :param manual: Set this to True if you want to play / debug
        :return: A score based on how long the player took to guess the word, or None if they failed over all attempts
        """
        word = random.choice(word_list)
        self.word = word
        for round in range(1, config.ATTEMPT_LIMIT + 1):
            # Guess word
            if self.manual:
                guess = input(f'\nPlease guess a word [attempt {round}/{config.ATTEMPT_LIMIT}]:\n')
                assert len(guess) == config.WORD_LENGTH
            else:
                guess = self.bot.guess()

            # Check guess
            round_score = score_guess(guess, word)
            if sum(round_score) == config.WORD_LENGTH:
                if self.manual:
                    print(f'Congratulations! You scored {round} with the word {word}')
                elif self.verbose:
                    print(f'Bot guessed {word} in {round} tries')
                return (config.ATTEMPT_LIMIT - round) + 1

            # Provide feedback
            pretty_feedback(round_score, guess)
            if not self.manual:
                self.bot.process_feedback(guess, round_score)

        if self.manual:
            print(f'Failed to guess word {word}')
        return 0
