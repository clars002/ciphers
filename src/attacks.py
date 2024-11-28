from typing import Set

import utilities as util
from cipher import Cipher


def bruteforce_attack(ciphertext: str, cipher: Cipher, max_key: int):
    long_text = len(ciphertext) > 1024

    if long_text:
        front_text = ciphertext[:1024]
        remaining_text = ciphertext[1024:]
        base_text = front_text
    else:
        base_text = ciphertext

    best_candidate = None
    best_score = -1
    best_key = 0

    with open("wordlist.txt", "r") as word_list:
        word_set = {line.strip() for line in word_list.readlines()}

    for i in range(max_key):
        plaintext = cipher.decrypt(base_text, i)
        score = _score_candidate(plaintext, word_set)

        if score > best_score:
            best_score = score
            best_candidate = plaintext
            best_key = i

            _print_update(plaintext, ciphertext, i, max_key, best_score)

    if long_text:
        best_candidate += cipher.decrypt(remaining_text, best_key)

    return best_candidate, best_key


def _score_candidate(text: str, words: Set[str]) -> int:
    score = 0

    for l in range(2, 45):
        for left_border in range(len(text) - l):
            right_border = left_border + l

            substring = text[left_border:right_border].lower()

            if substring in words:
                score += len(substring) ** 2

    return score


def _print_update(plaintext, ciphertext, i, max_key, best_score):
    util.clear_screen()
    plaintext_preview = util.preview_text(plaintext)
    ciphertext_preview = util.preview_text(ciphertext)
    print(f"Brute force attack in progress...\n")
    print(f"Ciphertext:")
    print(f"--------------------------------------------------------------")
    print(ciphertext_preview)
    print(f"\n")
    print(f"Best plaintext candidate so far:")
    print(f"--------------------------------------------------------------")
    print(plaintext_preview)
    return
