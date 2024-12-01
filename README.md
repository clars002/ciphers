# ciphers
CS 463 Course Project for ODU by Caelan Larsen

## Overview
This is a python program designed to encrypt, decrypt, and crack ASCII-encoded text files.

Currently, it supports the Caesar cipher. Encryption and decryption can be performed either with respect to the alphabet or the set of printable ASCII characters. An implementation of a brute-force attack on the Caesar cipher, using a dictionary of valid english words, is included for the cracking functionality.

I have tried to adhere to good object-oriented design principles (especially modularity, abstraction, high cohesion, low coupling, liskov substitution, open/closed principle), as well as attempting to keep the code generally as clean and concise as I could manage.
The result should be fairly open to expansion in the future, particularly for adding more ciphers and attacks.
Originally, I had intended to implement at least one more cipher, but time constraints have made this unfeasible for now. Perhaps I will revisit it in the future.

## Usage
Ensure you have a recent version of python installed.

The main driving code resides in the src/cipher_fun.py file.
An example command to execute the program (assuming you are in the root directory of the project) would be:  
>`python src/cipher_fun.py --input sample_text/plaintext/hobbit_intro.txt --key 8`

Running this will encrypt the file at sample_text/plaintext/hobbit_intro.txt with a key (i.e. shift offset) of 8, and output the result to output/hobbit_intro_enc.txt.
Technically, only the --input argument is strictly necessary to run the program, although the --key argument is necessary to encrypt or decrypt (only cracking doesn't require a key).

In total, there are six (6) arguments the user can supply:  
`--input` - Select the input text file (expected to be ASCII-encoded) to be encrypted, decrypted, or cracked; required  
`--output` - Specify where to output the results. Must be a valid file path. By default, output goes to the output/ directory, with filename suffixes indicating the operation performed.  
`--mode` - Select the mode of operation from: "encrypt", "decrypt", and "crack"; defaults to "encrypt"  
`--cipher` - Choose the encryption/decryption cipher (currently only supports Caesar); defaults to "caesar".  
`--key` - The key to use for encryption/decryption (i.e. the shift offset for Caesar); required for encryption/decryption.  
`--alphabetic` - Enable shifting characters with respect to the 26-character alphabet instead of the 128-character ASCII set. Off by default.  
  
You can also run the program with the `--help` flag to get a summary of the arguments/options.

### More Example Execution Commands
`python src/cipher_fun.py --mode encrypt --key 16 --input sample_text/plaintext/brothers_karamazov_excerpt.txt` - Encrypts the file at sample_text/plaintext/brothers_karamazov_excerpt.txt with a key of 16, with respect to the ASCII character set.  
`python src/cipher_fun.py --mode encrypt --key 20 --input sample_text/plaintext/lewis_quote.txt --alphabetic` - Encrypts the file at sample_text/plaintext/lewis_quote.txt with a key of 20, with respect to the 26-character English alphabet.
`python src/cipher_fun.py --mode decrypt --key 32 --input sample_text/ciphertext/okarin-32.txt` - Decrypts the file at sample_text/plaintext/lewis_quote.txt with respect to ASCII using the key 32.  
`python src/cipher_fun.py --mode decrypt --key 24 --input sample_text/ciphertext/alphabetic/roads-24a.txt --alphabetic` - Decrypts the file at sample_text/ciphertext/alphabetic/roads-24a.txt with respect to the 26-character English alphabet using the key 24.  
`python src/cipher_fun.py --mode crack --input sample_text/ciphertext/sofya-72.txt` - Employs a brute force attack (with respect to ASCII) to crack the ciphertext at sample_text/ciphertext/sofya-72.txt.  
`python src/cipher_fun.py --mode crack --input sample_text/ciphertext/alphabetic/courage-16a.txt --alphabetic` - Employs a brute force attack (with respect to the 26-character English alphabet) to crack the ciphertext at sample_text/ciphertext/alphabetic/courage-16a.txt.

### File Structure
Several sample plaintexts and ciphertexts are provided in the sample_text/plaintext/ and sample_text/ciphertext/ directories, respectively.
The ciphertext directory contains another alphabetic/ subdirectory, containing ciphertexts encrypted in alphabetic mode (the base ciphertext/ directory contains texts encrypted with respect to ASCII).

All sample ciphertexts' filenames have been marked with the keys used to encrypt them.
  
If an output path is not supplied by the user via the --output argument, all output will go to the output/ directory.
Some sample output is provided in the output/sample subdirectory, with suffixes indicating which operations were performed on each respective source file.

### Sidenotes
Be mindful of the --alphabetic option. It is essential to decrypt and/or crack files in the same mode they were encrypted in.
Attempting to decrypt or crack a file that was encrypted with the --alphabetic option enabled without again enabling it will result in incorrect output. Similarly, attempting to decrypt or crack a file that was encrypted without the --alphabetic option with that option enabled will result in incorrect output.
Consistency is key.

Occasionally, the brute force crack will select a somewhat garbled candidate over the genuine original plaintext. This is a quirk inherent to the scoring system I've implemented that arises only with certain text input. I spent substantial time and effort trying to iron this out, but in the end I couldn't think of anything that didn't involve moving to an entirely different and much more complicated scoring system, which I unfortunately don't have time for. However, the issue is relatively minor, since the resulting output is still quite readable and reflects the target plaintext closely.

## Discussion
As alluded to in the overview, I had originally intended to implement more ciphers and attack methods, but ultimately had to narrow the scope for this submission.
I tried to keep the code open to expansion in the future for the purposes of adding more ciphers and attacks later.
One example of this is my use of the factory design pattern. From main, the code calls cipher.CipherFactory.create_cipher(); this function, in turn, takes a string indicating which cipher is to be used and returns an appropriate object of type Cipher (the abstract base class on which CaesarCipher is built).
Furthermore, the brute force attack implementation I wrote attempts to be cipher-agnostic; it can operate on any Cipher object. Of course, for complex ciphers, it will inevitably become infeasible as an attack method.  
  
This brute force attack implementation proved an interesting challenge. Initially, I had trouble keeping it performant, especially for longer ciphertexts. One simple but effective optimization I employed is to only process the first 1024 characters of the text when scoring candidate keys. Once the best key is thus found, it is subsequently applied to the full text.
I am sure a more sophisticated implementation is possible, but I feel satisfied with the simplicity and performance of my current version.

I hope my effort on this project is evident in the simplicity of the code. It took a lot of effort to make it so short and sweet!

Thank you for your time and interest :)

## Credits
Wordlist used for brute force decryption taken from: https://websites.umich.edu/~jlawler/wordlist  
Crime and Punishment txt file from: https://www.gutenberg.org/ebooks/2554
