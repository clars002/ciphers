from typing import Set


class Cipher:
    def encrypt(plaintext: str):
        raise NotImplementedError

    def decrypt(ciphertext: str):
        raise NotImplementedError


class CaesarCipher(Cipher):
    def __init__(self, alphabetic: bool = False):
        self.alphabetic = alphabetic
        self.shift_function = (
            CaesarCipher._shift_char_alpha if alphabetic else CaesarCipher._shift_char
        )

    def encrypt(self, plaintext: str, key: int):
        ciphertext = ""

        for char in plaintext:
            new_letter = self.shift_function(char, key)
            ciphertext += new_letter

        return ciphertext

    def decrypt(self, ciphertext: str, key: int = 0):

        if key != 0:
            return self._reverse_caesar(ciphertext, key)

        else:  # Try to brute force if an offset (key) is not supplied
            return self._bruteforce_caesar(ciphertext)

        return ciphertext

    def _reverse_caesar(self, ciphertext, key):
        plaintext = ""

        for char in ciphertext:
            new_letter = self.shift_function(char, -key)
            plaintext += new_letter

        return plaintext

    def _bruteforce_caesar(self, ciphertext):
        best_candidate = None
        best_score = -1

        with open("wordlist.txt", "r") as word_list:
            word_set = {line.strip() for line in word_list.readlines()}

        limit = 26 if self.alphabetic else 128

        for i in range(limit):
            plaintext = ""

            for char in ciphertext:
                new_letter = self.shift_function(char, -i)
                plaintext += new_letter

            score = CaesarCipher._score_candidate(plaintext, word_set)

            if score > best_score:
                best_score = score
                best_candidate = plaintext
                print(
                    f'Processed {i + 1}/{limit} candidates thus far; best candidate:\n "{plaintext[:512]}..." \nWith score: {best_score}.'
                )

        return best_candidate

    @staticmethod
    def _shift_char_alpha(char, key):
        if not char.isalpha():
            return char

        is_upper = char.isupper()
        char = char.lower() if is_upper else char

        initial_index = ord(char) - ord("a")
        shifted_index = (initial_index + key) % 26
        new_letter = chr(shifted_index + ord("a"))
        new_letter = new_letter.upper() if is_upper else new_letter
        return new_letter

    @staticmethod
    def _shift_char(char, key):
        initial_index = ord(char)
        shifted_index = (initial_index + key) % 128
        new_letter = chr(shifted_index)
        return new_letter

    @staticmethod
    def _score_candidate(text: str, words: Set[str]) -> int:
        score = 0

        for l in range(2, 45):
            for left_border in range(len(text) - l):
                right_border = left_border + l

                window_size = right_border - left_border

                substring = text[left_border:right_border].lower()

                substring_length = len(substring)

                if substring in words:
                    score += substring_length**2
                    # print(f"Wordlist hit: {substring}.")

        return score
