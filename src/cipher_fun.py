import argparse
import os
import time
from pathlib import Path

import attacks as atk
import cipher
import utilities as util


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
        help="Path to the input file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to which results will be outputted.",
        default=None,
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
        output_directory = "ciphertext"
        mode_suffix = "_encrypted"
    elif mode == "decrypt":
        output_directory = "plaintext"
        mode_suffix = "_decrypted"
    elif mode == "crack":
        output_directory = "cracked"
        mode_suffix = "_cracked"

    if alphabetic:
        alpha_suffix = "_alpha"
    else:
        alpha_suffix = ""

    output_path = os.path.join(
        output_directory, f"{base_filename}{mode_suffix}{alpha_suffix}.txt"
    )

    return output_path


def print_summary(header: str, text_out: str, output_path: str, start_time: float):
    print(header)
    print(f"-----------------------------------------------------------------------")
    print(util.preview_text(text_out))
    print(f"\n")
    print(f"Wrote results to: {output_path}")
    print(f"Total runtime: {time.time() - start_time:.3f} seconds.")


def validate_input(args: argparse.Namespace) -> bool:
    if args.key == 0:
        if args.mode == "encrypt":
            print("In order to encrypt, please provide a key using the --key argument.")
            return False
        elif args.mode == "decrypt":
            print(
                "In order to decrypt, please provide a key using the --key argument. If you instead want to try to crack the ciphertext using brute force, use --mode crack."
            )
            return False

    if not os.path.isfile(args.input):
        print(
            f"Invalid input file: {args.input}\nPlease ensure the file path is valid and that the file exists."
        )
        return False

    if args.output:
        output_path = Path(args.output)
        if not output_path.parent.is_dir():
            print(f"Error: {output_path.parent} is not a directory.")

    return True


def main():
    start_time = time.time()
    args = process_args()

    if not validate_input(args):
        return

    my_cipher = cipher.CaesarCipher(args.alphabetic)

    if not args.output:
        output_path = generate_output_path(args.input, args.mode, args.alphabetic)
    else:
        output_path = args.output

    with open(args.input, "r") as input_file, open(output_path, "w") as output_file:
        text_in = input_file.read()

        if args.mode == "encrypt":
            print(f"Encrypting file at {args.input} with key {args.key}...")
            text_out = my_cipher.encrypt(text_in, args.key)
            summary_header = f"Encryption finished! Ciphertext:"

        elif args.mode == "decrypt":
            print(f"Decrypting file at {args.input} with key {args.key}...")
            text_out = my_cipher.decrypt(text_in, args.key)
            summary_header = f"Decryption finished! Plaintext:"

        elif args.mode == "crack":
            max_key = 26 if args.alphabetic else 128
            text_out, cracked_key = atk.bruteforce_attack(text_in, my_cipher, max_key)
            summary_header = f"Brute force crack finished! The key is most likely {cracked_key} with plaintext:"
            util.clear_screen()

        output_file.write(text_out)
        print_summary(summary_header, text_out, output_path, start_time)


if __name__ == "__main__":
    main()
