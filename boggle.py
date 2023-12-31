from random import choice
import string


class Boggle():

    def __init__(self):

        self.words = self.read_dict("words.txt")
        print(self.words[:100])  # Print the first 100 words from the dictionary to ensure functionality on the backend
    def read_dict(self, dict_path):
        """Read and return all words in dictionary."""

        dict_file = open(dict_path)
        words = [w.strip() for w in dict_file]
        dict_file.close()
        return words

    def make_board(self):
        """Make and return a random boggle board with a minimum of 3 vowels."""

        VOWELS = "AEIOU"
        CONSONANTS = "BCDFGHJKLMNPQRSTVWXYZ"
        
        board = []

        for y in range(5):
            row = [choice(string.ascii_uppercase) for i in range(5)]
            board.append(row)

        # Count the number of vowels on the board
        vowel_count = sum(1 for row in board for letter in row if letter in VOWELS)

        # Ensure there are at least 3 vowels on the board
        while vowel_count < 3:
            for row in board:
                for i in range(5):
                    if row[i] not in VOWELS and vowel_count < 3:
                        row[i] = choice(VOWELS)
                        vowel_count += 1
        
        # Ensure there are at most 5 vowels on the board
        while vowel_count > 5:
             for row in board:
                for i in range(5):
                    if row[i] in VOWELS and vowel_count > 5:
                        row[i] = choice(CONSONANTS)
                        vowel_count -= 1

        return board


    def check_valid_word(self, board, word):
        """Check if a word is a valid word in the dictionary and/or the boggle board"""

        # Check word existence against lowercase version since dictionary words are lowercase
        word_exists = word.lower() in self.words

        # Check board presence against uppercase version since board letters are uppercase
        valid_word = self.find(board, word.upper())

        if word_exists and valid_word:
            result = "ok"
        elif word_exists and not valid_word:
            result = "not-on-board"
        else:
            result = "not-word"

        return result


    def find_from(self, board, word, y, x, seen):
        """Can we find a word on board, starting at x, y?"""
        if x > 4 or y > 4:
            return

        if board[y][x] != word[0]:
            return False

        if (y, x) in seen:
            return False

        if len(word) == 1:
            return True

        seen = seen | {(y, x)}

        if y > 0:
            if self.find_from(board, word[1:], y - 1, x, seen):
                return True

        if y < 4:
            if self.find_from(board, word[1:], y + 1, x, seen):
                return True

        if x > 0:
            if self.find_from(board, word[1:], y, x - 1, seen):
                return True

        if x < 4:
            if self.find_from(board, word[1:], y, x + 1, seen):
                return True

        if y > 0 and x > 0:
            if self.find_from(board, word[1:], y - 1, x - 1, seen):
                return True

        if y < 4 and x < 4:
            if self.find_from(board, word[1:], y + 1, x + 1, seen):
                return True

        if x > 0 and y < 4:
            if self.find_from(board, word[1:], y + 1, x - 1, seen):
                return True

        if x < 4 and y > 0:
            if self.find_from(board, word[1:], y - 1, x + 1, seen):
                return True

        return False

    def find(self, board, word):
        """Can word be found in board?"""
        for y in range(0, 5):
            for x in range(0, 5):
                if self.find_from(board, word, y, x, seen=set()):
                    return True
        return False
