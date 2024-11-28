from typing import Set

from cipher import Cipher


def bruteforce_attack(ciphertext: str, cipher: Cipher, max_key: int):
    text_length = len(ciphertext)

    long_text = text_length > 1024

    if long_text:
        front_text = ciphertext[:1024]
        remaining_text = ciphertext[1024:]
        ciphertext = front_text

    best_candidate = None
    best_score = -1
    best_key = 0

    with open("wordlist.txt", "r") as word_list:
        word_set = {line.strip() for line in word_list.readlines()}

    for i in range(max_key):
        plaintext = cipher.decrypt(ciphertext, i)
        score = _score_candidate(plaintext, word_set)

        if score > best_score:
            best_score = score
            best_candidate = plaintext
            best_key = i

            _print_update(plaintext, text_length, i, max_key, best_score)
    
    if long_text:
        best_candidate += cipher.decrypt(remaining_text, best_key)

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


def _print_update(plaintext, text_length, i, max_key, best_score):
    text_preview = f"\"{plaintext[:512]}...\"" if text_length > 512 else f"\"{plaintext}\""
    print(
        f'Processed {i + 1}/{max_key} candidates thus far; best candidate:\n{text_preview}\nWith score: {best_score}.'
    )
    return