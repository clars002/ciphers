from typing import Set

from cipher import Cipher


def bruteforce_attack(ciphertext: str, cipher: Cipher, max_key: int):
    best_candidate = None
    best_score = -1

    with open("wordlist.txt", "r") as word_list:
        word_set = {line.strip() for line in word_list.readlines()}

    for i in range(max_key):
        plaintext = cipher.decrypt(ciphertext, i)
        score = _score_candidate(plaintext, word_set)

        if score > best_score:
            best_score = score
            best_candidate = plaintext
            print(
                f'Processed {i + 1}/{max_key} candidates thus far; best candidate:\n "{plaintext[:512]}..." \nWith score: {best_score}.'
            )

    return best_candidate


def _score_candidate(text: str, words: Set[str]) -> int:
    score = 0

    for l in range(2, 45):
        for left_border in range(len(text) - l):
            right_border = left_border + l

            substring = text[left_border:right_border].lower()

            if substring in words:
                score += len(substring) ** 2

    return score
