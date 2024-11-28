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
        "--key", type=int, default=0, help="Offset to shift for Caesar cipher."
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

    base_filename = os.path.splitext(os.path.basename(args.input))[0]
    output_directory = "ciphertext/" if args.mode == "encrypt" else "plaintext/"
    mode_suffix = "_encrypted" if args.mode == "encrypt" else "_decrypted"
    alpha_suffix = "_alpha" if args.alphabetic else ""
    output_path = f"{output_directory}{base_filename}{mode_suffix}{alpha_suffix}.txt"

    process_text = my_cipher.encrypt if args.mode == "encrypt" else my_cipher.decrypt
    with open(args.input, "r") as input_file, open(output_path, "w") as output_file:
        text_in = input_file.read()
        text_out = process_text(text_in, args.key)
        output_file.write(text_out)


if __name__ == "__main__":
    main()
