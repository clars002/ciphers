class Cipher:
    def encrypt(plaintext: str) -> str:
        raise NotImplementedError

    def decrypt(ciphertext: str) -> str:
        raise NotImplementedError


class CaesarCipher(Cipher):
    def __init__(self, alphabetic: bool = False):
        self.alphabetic = alphabetic
        self.shift_function = (
            CaesarCipher._shift_char_alphabetic
            if alphabetic
            else CaesarCipher._shift_char
        )

    def encrypt(self, plaintext: str, key: int) -> str:
        ciphertext = ""

        for char in plaintext:
            new_letter = self.shift_function(char, key)
            ciphertext += new_letter

        return ciphertext

    def decrypt(self, ciphertext: str, key: int) -> str:
        return self.encrypt(ciphertext, -key)

    @staticmethod
    def _shift_char_alphabetic(char: str, key: int) -> str:
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
    def _shift_char(char: str, key: int) -> str:
        initial_index = ord(char)
        shifted_index = (initial_index + key) % 128
        new_letter = chr(shifted_index)
        return new_letter
