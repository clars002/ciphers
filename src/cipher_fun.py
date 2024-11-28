import argparse
import os

import attacks as atk
import cipher


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
        "--key", type=int, default=0, help="Offset to shift for Caesar cipher."
    )
    parser.add_argument(
        "--alphabetic",
        action="store_true",
        help="Enables shifting with respect to the 26-character alphabet instead of 128-character ASCII set.",
    )

    return parser.parse_args()


def generate_output_path(input_path: str, mode: str, alphabetic: bool):
    base_filename = os.path.splitext(os.path.basename(input_path))[0]

    if mode == "encrypt":
        output_directory = "ciphertext/"
        mode_suffix = "_encrypted"
    elif mode == "decrypt":
        output_directory = "plaintext/"
        mode_suffix = "_decrypted"
    elif mode == "crack":
        output_directory = "cracked/"
        mode_suffix = "_cracked"

    if alphabetic:
        alpha_suffix = "_alpha"
    else:
        alpha_suffix = ""

    output_path = f"{output_directory}{base_filename}{mode_suffix}{alpha_suffix}.txt"

    return output_path


def main():
    args = process_args()
    my_cipher = cipher.CaesarCipher(args.alphabetic)

    output_path = generate_output_path(args.input, args.mode, args.alphabetic)

    with open(args.input, "r") as input_file, open(output_path, "w") as output_file:
        text_in = input_file.read()

        if args.mode == "encrypt":
            text_out = my_cipher.encrypt(text_in, args.key)
        elif args.mode == "decrypt":
            text_out = my_cipher.decrypt(text_in, args.key)
        elif args.mode == "crack":
            max_key = 26 if args.alphabetic else 128
            text_out = atk.bruteforce_attack(text_in, my_cipher, max_key)

        output_file.write(text_out)


if __name__ == "__main__":
    main()
