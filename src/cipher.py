from abc import ABC, abstractmethod
from typing import Callable

"""
File containing Cipher abstract base class and CaesarCipher instantiation of it.
"""


class Cipher(ABC):
    """
    Abstract base class; defines the interface of a Cipher object.
    """

    @abstractmethod
    def encrypt(plaintext: str) -> str:
        pass

    @abstractmethod
    def decrypt(ciphertext: str) -> str:
        pass


class CaesarCipher(Cipher):
    """
    Cipher child class for the Caesar Cipher.

    Attributes:
        alphabetic (bool):
            Whether to perform encryption and decryption with
            respect to the alphabet instead of the ASCII character
            set. Defaults to False.
        shift_function (Callable[[str, int], str]):
            Function used for shifting each individual character.
            Dynamically/automatically assigned based on the
            alphabetic attribute.
    """

    shift_function: Callable[[str, int], str]

    def __init__(self, alphabetic: bool = False):
        """
        Constructor for CaesarCipher.

        Args:
            alphabetic (bool, optional):
                Whether to perform encryption and decryption with
                respect to the alphabet instead of the ASCII character
                set. Defaults to False.
        """
        self.alphabetic = alphabetic
        self.shift_function = (
            CaesarCipher._shift_char_alphabetic
            if alphabetic
            else CaesarCipher._shift_char
        )

    def encrypt(self, plaintext: str, key: int) -> str:
        """
        Applies the Caesar cipher to plaintext to encrypt it.

        Args:
            plaintext (str): Text to be encrypted.
            key (int): Encryption key (i.e. the shift offset).

        Returns:
            str: The encrypted text (i.e. the ciphertext).
        """
        return "".join(self.shift_function(char, key) for char in plaintext)

    def decrypt(self, ciphertext: str, key: int) -> str:
        """
        Applies the Caesar cipher in reverse to decrypt ciphertext.

        Args:
            ciphertext (str): Encrypted text (i.e. ciphertext).
            key (int): The same key (offset) used to encrypt the text.

        Returns:
            str: The decrypted plaintext.
        """
        return self.encrypt(ciphertext, -key)

    @staticmethod
    def _shift_char_alphabetic(char: str, key: int) -> str:
        """
        Shifts the supplied character, with respect to the alphabet,
        the number of indices specified by the supplied key.

        Args:
            char (str): The character to be shifted.
            key (int): The offset/number of alphabetic spaces to shift.

        Returns:
            str: The resultant character after shifting.
        """
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
        """
        Shifts the supplied character, with respect to the ASCII
        character set, the number of indices specified by the supplied
        key.

        Args:
            char (str): The character to be shifted.
            key (int): The offset/number of ASCII spaces to shift.

        Returns:
            str: The resultant character after shifting.
        """
        initial_index = ord(char)
        shifted_index = (initial_index + key) % 128
        new_letter = chr(shifted_index)
        return new_letter
