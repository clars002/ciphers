"""
The main file; contains primary driving logic.
"""

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
    """
    Generates a string representing the (default) file path to write results to.

    Args:
        input_path (str): See the --input flag in process_args; reflected in the filename.
        mode (str): See the --mode flag in process_args; reflected in the filename.
        alphabetic (bool): See the --alphabetic flag in process_args; reflected in the filename.

    Returns:
        str: A string representing the file path constructed from the arguments.
    """

    base_filename = os.path.splitext(os.path.basename(input_path))[0]

    output_directory = "output"

    if mode == "encrypt":
        output_subdir = "encrypted"
        mode_suffix = "_enc"
    elif mode == "decrypt":
        output_subdir = "decrypted"
        mode_suffix = "_dec"
    elif mode == "crack":
        output_subdir = "cracked"
        mode_suffix = "_crack"

    if alphabetic:
        alpha_suffix = "_alpha"
    else:
        alpha_suffix = ""

    output_path = os.path.join(
        output_directory, output_subdir, f"{base_filename}{mode_suffix}{alpha_suffix}.txt"
    )

    return output_path


def print_summary(header: str, text_out: str, output_path: str, start_time: float):
    """
    Prints a summary of the program's results.

    Args:
        header (str): The header, printed on the first line.
        text_out (str): The main text output, intended to display final ciphertext/plaintext.
        output_path (str): The file path to which results have (already) been written.
        start_time (float): The start time of the program, used to calculate runtime.
    """

    print(header)
    print(f"-----------------------------------------------------------------------")
    print(util.preview_text(text_out))
    print(f"\n")
    print(f"Wrote results to: {output_path}")
    print(f"Total runtime: {time.time() - start_time:.3f} seconds.")
    return


def validate_input(args: argparse.Namespace) -> bool:
    """
    Validates the arguments passed to the program.

    Args:
        args (argparse.Namespace): The arguments passed to the program.

    Returns:
        bool: True if the arguments are valid, else False
    """

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
    """
    The main driver; processes arguments, executes the chosen operation, and displays results.
    """

    start_time = time.time()
    args = process_args()

    if not validate_input(args):
        return

    my_cipher = cipher.CaesarCipher(args.alphabetic)

    if not args.output:  # Check if an output path was supplied; if not, use the default
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
