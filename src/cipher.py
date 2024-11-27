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
        offset = key

        if self.alphabetic:
            offset = key % 26

        for char in plaintext:
            if self.alphabetic and not char.isalpha():
                ciphertext += char
                continue

            initial_index = ord(char)
            shifted_index = initial_index + offset

            new_letter = chr(shifted_index)

            ciphertext += new_letter

        return ciphertext