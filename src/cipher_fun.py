import argparse
import os

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
        "--key", type=int, default=8, help="Offset to shift for Caesar cipher."
    )
    parser.add_argument(
        "--alphabetic",
        action="store_true",
        help="Enables shifting with respect to the 26-character alphabet instead of 128-character ASCII set.",
    )

    return parser.parse_args()


def main():
    args = process_args()

    my_cipher = cipher.CaesarCipher(args.alphabetic)

    input_path = args.input
    base_filename = os.path.splitext(os.path.basename(input_path))[0]

    if args.mode == "encrypt":
        output_name = base_filename + "_encrypted.txt"

        with open(args.input) as file:
            plaintext = file.read()

            ciphertext = my_cipher.encrypt(plaintext, args.key)

        output_file = open(f"ciphertext/{output_name}", "w")

        output_file.write(ciphertext)

        output_file.close()

    elif args.mode == "decrypt":
        output_name = base_filename + "_decrypted.txt"

        with open(args.input) as file:
            ciphertext = file.read()

            plaintext = my_cipher.decrypt(ciphertext, args.key)

        output_file = open(f"plaintext/{output_name}", "w")

        output_file.write(plaintext)

        output_file.close()


if __name__ == "__main__":
    main()
