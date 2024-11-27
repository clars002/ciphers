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


def main():
    args = process_args()

    if args.mode == "encrypt":
        base_filename = os.path.splitext(os.path.basename(args.input))[0]

        output_name = base_filename + "_encrypted.txt"

        with open(args.input) as file:
            plaintext = file.read()
            ciphertext = ""

            for char in plaintext:
                initial_index = ord(char)
                shifted_index = initial_index + args.offset

                new_letter = chr(shifted_index)

                ciphertext += new_letter

        output_file = open(f"ciphertext/{output_name}", "w")

        output_file.write(ciphertext)

        output_file.close()


if __name__ == "__main__":
    main()
