import argparse
import os


def process_args():
    """
    Parses arguments from the CLI.

    Returns:
        A Namespace object where attributes correspond to the
        defined/provided args.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        type=str,
        default="plaintext/sample.txt",
        help="Path to the input file.",
    )
    parser.add_argument(
        "--mode", type=str, default="encrypt", help="Whether to encrypt or decrypt."
    )
    parser.add_argument(
        "--encryption_cipher",
        type=str,
        default="Caesar",
        help="Which cypher to use for encryption (unused in decryption mode).",
    )
    parser.add_argument(
        "--offset", type=int, default=8, help="Offset to shift for Caesar cipher."
    )

    return parser.parse_args()


def encrypt_caesar(plaintext: str, offset: int):
    ciphertext = ""

    for char in plaintext:
        initial_index = ord(char)
        shifted_index = initial_index + offset

        new_letter = chr(shifted_index)

        ciphertext += new_letter

    return ciphertext


def score_candidate(text: str):
    score = 0

    word_list = open("wordlist.txt", "r")
    words = [line.strip() for line in word_list.readlines()]
    word_set = set()

    for word in words:
        word_set.add(word)

    text_length = len(text)

    score = 0

    for l in range(2, 45):
        for left_border in range(text_length):
            right_border = left_border + l

            window_size = right_border - left_border

            substring = text[left_border:right_border]
            substring_length = len(substring)

            if substring in word_set:
                score += substring_length**2
                # print(f"Wordlist hit: {substring}.")

    return score


def decrypt_caesar(ciphertext: str, offset: int = 0):
    if offset != 0:

        plaintext = ""

        for char in ciphertext:
            initial_index = ord(char)
            shifted_index = initial_index - offset

            new_letter = chr(shifted_index)

            plaintext += new_letter

        return plaintext

    else:  # Try to brute force if an offset (key) is not supplied
        best_candidate = None
        best_score = -1

        for i in range(128):
            plaintext = ""

            for char in ciphertext:
                initial_index = ord(char)
                shifted_index = initial_index - i

                if shifted_index < 0:
                    shifted_index += 128

                new_letter = chr(shifted_index)

                plaintext += new_letter

            score = score_candidate(plaintext)

            if i == 12:
                print(plaintext)

            if score > best_score:
                best_score = score
                best_candidate = plaintext

                print(
                    f"Current best candidate: {best_candidate} with score {best_score}"
                )

        return best_candidate

    return ciphertext


def main():
    args = process_args()

    input_path = args.input
    base_filename = os.path.splitext(os.path.basename(input_path))[0]

    if args.mode == "encrypt":
        output_name = base_filename + "_encrypted.txt"

        with open(args.input) as file:
            plaintext = file.read()

            ciphertext = encrypt_caesar(plaintext, args.offset)

        output_file = open(f"ciphertext/{output_name}", "w")

        output_file.write(ciphertext)

        output_file.close()

    elif args.mode == "decrypt":
        output_name = base_filename + "_decrypted.txt"

        with open(args.input) as file:
            ciphertext = file.read()

            plaintext = decrypt_caesar(ciphertext, args.offset)

        output_file = open(f"plaintext/{output_name}", "w")

        output_file.write(plaintext)

        output_file.close()


if __name__ == "__main__":
    main()
