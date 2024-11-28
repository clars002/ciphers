class Cipher:
    def encrypt(plaintext: str):
        raise NotImplementedError

    def decrypt(ciphertext: str):
        raise NotImplementedError


class CaesarCipher(Cipher):
    def __init__(self, alphabetic: bool = False):
        self.alphabetic = alphabetic

    def encrypt(self, plaintext: str, key: int):
        ciphertext = ""

        for char in plaintext:
            if self.alphabetic:
                key %= 26

                if not char.isalpha():
                    ciphertext += char
                    continue

                is_upper = char.isupper()
                if is_upper:
                    char = char.lower()

                alpha_index = ord(char) - ord("a")

                shifted_alpha_index = (alpha_index + key) % 26

                new_letter = chr(shifted_alpha_index + ord("a"))

                if is_upper:
                    new_letter = new_letter.upper()

            else:
                key %= 128

                shifted_index = ord(char) + key
                new_letter = chr(shifted_index)

            ciphertext += new_letter

        return ciphertext

    def score_candidate(self, text: str):
        score = 0

        word_list = open("wordlist.txt", "r")
        words = [line.strip() for line in word_list.readlines()]
        word_set = set()

        for word in words:
            word_set.add(word)

        text_length = len(text)

        score = 0

        for l in range(2, 45):
            for left_border in range(text_length - l):
                right_border = left_border + l

                window_size = right_border - left_border

                substring = text[left_border:right_border]

                substring = substring.lower()

                substring_length = len(substring)

                if substring in word_set:
                    score += substring_length**2
                    # print(f"Wordlist hit: {substring}.")

        return score

    def decrypt(self, ciphertext: str, key: int = 0):
        offset = key

        if offset != 0:

            plaintext = ""

            if not self.alphabetic:

                for char in ciphertext:
                    initial_index = ord(char)
                    shifted_index = initial_index - offset

                    new_letter = chr(shifted_index)

                    plaintext += new_letter

            else:

                for char in ciphertext:

                    if not char.isalpha():
                        plaintext += char
                        continue

                    upper = False

                    if char.isupper():
                        upper = True
                        char = char.lower()

                    initial_index = ord(char) - ord("a")
                    shifted_index = (initial_index - offset) % 26

                    new_letter = chr(shifted_index + ord("a"))

                    if upper:
                        new_letter = new_letter.upper()

                    plaintext += new_letter

            return plaintext

        else:  # Try to brute force if an offset (key) is not supplied
            best_candidate = None
            best_score = -1

            if self.alphabetic:
                limit = 26
            else:
                limit = 128

            for i in range(limit):
                plaintext = ""

                for char in ciphertext:

                    if not self.alphabetic:
                        initial_index = ord(char)
                        shifted_index = initial_index - i

                        if shifted_index < 0:
                            shifted_index += 128

                        new_letter = chr(shifted_index)

                    else:
                        if not char.isalpha():
                            plaintext += char
                            continue

                        upper = False

                        if char.isupper():
                            upper = True
                            char = char.lower()

                        initial_index = ord(char) - ord("a")
                        shifted_index = (initial_index - i) % 26

                        new_letter = chr(shifted_index + ord("a"))

                        if upper:
                            new_letter = new_letter.upper()

                    plaintext += new_letter

                score = self.score_candidate(plaintext)

                if score > best_score:
                    best_score = score
                    best_candidate = plaintext

                    print(
                        f'Processed {i + 1}/{limit} candidates thus far; best candidate:\n "{plaintext[:512]}..." \nWith score: {best_score}.'
                    )

            return best_candidate

        return ciphertext
