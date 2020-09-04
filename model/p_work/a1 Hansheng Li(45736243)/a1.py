"""
CSSE1001 Assignment 1
Semester 2, 2020
"""

from a1_support import *

# Fill these in with your details
__author__ = "Hansheng Li (45736243)"
__email__ = "hansheng.li1@uqconnect.edu.au"
__date__ = "2020.8.31"



def input_loop():
    """ ’s’	Start game
        ’h’	The game rules will be printed out and then the game will commence
        ’q’	Quit game

     """

    input_order = input(INPUT_ACTION)

    if input_order == 'h':
        print(HELP)
        start_game()
    elif input_order == 's':
        start_game()
    elif input_order == 'q':
        return
    else:
        print(INVALID)
        input_loop()


def start_game():
    """
    FIXED” (meaning the word will be exactly eight letters long

    “ARBITRARY” (meaning the word will be anywhere between six to eight letters long)

    The goal of the game is for the player to guess that word through a series of guesses of “subwords”.
    The player will have a different number of guesses

     """
    index = 0
    scores = []
    
    word_select = input("Do you want a 'FIXED' or 'ARBITRARY' length word?: ")
    if word_select == 'FIXED' or word_select == 'ARBITRARY':
        word = select_word_at_random(word_select)

        print("Now try and guess the word, step by step!!")
        display_guess_matrix(0, len(word), scores)
        
        while index < len(word) :
            a, b = GUESS_INDEX_TUPLE[len(word) - 6][index]
            
            if (index + 1) == len(word):
                guess_word = input("Now enter your final guess. i.e. guess the whole word: ")
                if guess_word == word:
                    print("You have guessed the word correctly. Congratulations.")
                else :
                    print("Your guess was wrong. The correct word was \"" + word + "\"")
                return
            else :
                guess_word = guess_input(index, b - a + 1, len(word))
            
            score = compute_value_for_guess(word, a, b, guess_word)
            scores.append(score)
            display_guess_matrix(index + 1, len(word), scores)
            index += 1
        
    else:
        start_game()


def guess_input(index, letter_length, word_length):
    """
    Given the wordselect is either “FIXED” or “ARBITRARY”
    this function will return a string randomly selected from WORDS FIXED.txt or WORDS ARBITRARY.txt respectively.
    """
    if (index + 1) == word_length:
        guess_word = input("Now enter your final guess. i.e. guess the whole word: ")
    else :
        guess_word = input("Now enter Guess " + str(index + 1) + ": ")
    
    if len(guess_word) != letter_length :
        return guess_input(index, letter_length, word_length)
    else :
        return guess_word

def select_word_at_random(word_select):
    """
    Given the wordselect is either “FIXED” or “ARBITRARY” this function will return a string randomly
    selected from WORDS FIXED.txt or WORDS ARBITRARY.txt respectively.
    """
    if word_select in ["FIXED", "ARBITRARY"]:
        words = load_words(word_select)
        index = random_index(words)
        guess_word = words[index]
        return guess_word
    

def display_guess_matrix(guess_no, word_length, scores):
    """
    This function prints the progress of the game.
    This includes all line strings for guesses up to guess no with their corresponding scores
    (a tuple containing all previous scores), and the line string for guess no (without a score)
     """
    i = 0
    str_init = ' ' * 7
    cutline = '-' * int((4 * (word_length + 1) + 5))
    for k in range(word_length):
        str_init += WALL_VERTICAL + " " + str(k + 1) + " "
    str_init += f'{WALL_VERTICAL}\n{cutline}'
    str_init += "\n"

    j = 0
    for i in range(1, len(scores) + 1):
        if len(scores) <= 0:
            number = 0
        else :
            number = scores[j]

        str_init += f"{create_guess_line(i, word_length)}   {number} Points\n{cutline}\n"
        
    j +=1
    i += 1
    str_init += f"{create_guess_line(i, word_length)}\n{cutline}"
    print(str_init)


def create_guess_line(guess_no, word_length):
    """
    This function returns the string representing the display corresponding to the guess number integer, guess no.

    """
    No = guess_no - 1
    if No >= word_length :
        No = word_length - 1
        
    a, b = GUESS_INDEX_TUPLE[word_length - 6][No]
    guess_line = f"Guess {guess_no}"+WALL_VERTICAL
    for i in range(1,word_length+1):
        guess_line += f"{WALL_VERTICAL}"
        if i-1 in list(range(a, b+1)):
            guess_line += " * "
        else:
            guess_line += f" {WALL_HORIZONTAL} "
    guess_line += f"{WALL_VERTICAL}"


    return guess_line


def compute_value_for_guess(word, start_index, end_index, guess):
    """
    Return the score, an integer, the player is awarded for a specific guess.
    The word is a string representing the word the player has to guess.
    The substring to be guessed is determined by the start index and end index.
    The substring is created by slicing the word from the start index up to and including the end index.
    The guess is a string representing the guess attempt the player has made.

    """

    x = word[start_index:end_index + 1]
    score = 0
    index = 0
    for i in guess:
        if i in VOWELS and x[index:index + 1] == guess[index:index + 1]:
            score += 14
        elif i in CONSONANTS and x[index:index + 1] == guess[index:index + 1]:
            score += 12
        elif i in x:
            score += 5
        else:
            score += 0
        index += 1
    return score


def main():
    """
    Handles top-level interaction with user.
    """
    print(WELCOME)
    input_loop()


if __name__ == "__main__":
    main()
    
