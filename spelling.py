#!/usr/bin/env python3

import csv, random, os
from enum import Enum
from playsound import playsound
from termcolor import colored


class ExtendedEnum(Enum):

    @classmethod
    def list(enum_class):
        return list(map(lambda e: e.value, enum_class))


class YesNo(ExtendedEnum):
    """"""

    YES = 'Y'
    NO = 'N'


class PracticeMode(ExtendedEnum):
    """"""

    TEXT = 'TEXT'
    LISTEN = 'LISTEN'


class QuitError(Exception):
    """Raised when the user quits the program."""

    pass


def start_program():
    """
    """

    print("╔═════════════════════════════════════════╗")
    print(
        f"║            {colored('SPELLING PRACTICE!', 'blue', attrs=['bold'])}           ║"
    )
    print(f"║ Input {colored('Q', 'red')} at any time to quit the program ║")
    print("╚═════════════════════════════════════════╝")
    print()

    practice_mode = get_input(
        f"Please select your practice mode ({colored('text', 'magenta')}, {colored('listen', 'magenta')}): "
    )
    while practice_mode not in PracticeMode.list():
        practice_mode = get_input(
            f"Invalid practice mode. Please select from ({colored('text', 'magenta')}, {colored('listen', 'magenta')}): "
        )
    practice_mode = PracticeMode(practice_mode)
    print()

    grade = get_input(
        f"Please select your grade level ({colored('1', 'magenta')}-{colored('12', 'magenta')}): "
    )
    while not (1 <= int(grade) <= 12):
        grade = get_input(
            f"Invalid grade level. Please select from ({colored('1', 'magenta')}-{colored('12', 'magenta')}): "
        )
    grade = int(grade)
    print()

    record_progress = get_input(
        f"Do you want to record your progress ({colored('Y', 'magenta')}/{colored('N', 'magenta')})? "
    )
    while record_progress not in YesNo.list():
        record_progress = get_input(
            f"Invalid input. Please select from ({colored('Y', 'magenta')}/{colored('N', 'magenta')}): "
        )
    record_progress = (YesNo(record_progress) == YesNo.YES)
    print()

    reset_progress = False
    if record_progress:
        reset_progress = get_input(
            f"Do you want to reset your progress from last time ({colored('Y', 'magenta')}/{colored('N', 'magenta')})? "
        )
        while reset_progress not in YesNo.list():
            reset_progress = get_input(
                f"Invalid input. Please select from ({colored('Y', 'magenta')}/{colored('N', 'magenta')}): "
            )
        reset_progress = (YesNo(reset_progress) == YesNo.YES)
        print()

    start_practice(practice_mode, grade, record_progress, reset_progress)


def start_practice(practice_mode: PracticeMode, grade: int,
                   record_progress: bool, reset_progress: bool):
    """
    """

    print("┌─────────────────────────────────────────┐")
    print(
        f"│           {colored('Starting practice...', 'blue', attrs=['bold'])}          │"
    )
    print(
        f"│ • Practice mode: {colored(practice_mode.value, 'magenta')}{' '*(23-len(practice_mode.value))}│"
    )
    print(
        f"│ • Grade level: {colored(grade, 'magenta')}{' '*(25-len(str(grade)))}│"
    )
    print(
        f"│ • Record progress? {colored(('Y' if record_progress else 'N'), 'magenta')}                    │"
    )
    print(
        f"│ • Reset progress? {colored(('Y' if reset_progress else 'N'), 'magenta')}                     │"
    )
    print("└─────────────────────────────────────────┘")
    print()

    fname, word_scores = get_and_read_word_file(grade, record_progress,
                                                reset_progress)
    word_list = list(word_scores.keys())

    try:
        while True:
            max_score = max(word_scores.values())
            normalized_scores = [
                max_score - score + 1 for score in word_scores.values()
            ]
            word = random.choices(word_list, weights=normalized_scores)[0]

            if practice_mode == PracticeMode.TEXT:
                result = get_input(
                    f"Can you spell {colored(word, 'blue', attrs=['bold'])} correctly ({colored('Y', 'magenta')}/{colored('N', 'magenta')})? "
                )
                while result not in YesNo.list():
                    result = get_input(
                        f"Invalid input. Can you spell {colored(word, 'blue', attrs=['bold'])} correctly ({colored('Y', 'magenta')}/{colored('N', 'magenta')})? "
                    )
                word_scores[word] += (1 if YesNo(result) == YesNo.YES else -1)

            elif practice_mode == PracticeMode.LISTEN:
                word_audio_fname = f"./audio/grade_{grade}/normal/{word}.mp3"
                if not os.path.exists(word_audio_fname):
                    print(f"Audio file {word_audio_fname} is not downloaded.")
                    raise QuitError
                playsound(word_audio_fname)
                result = get_input(
                    f"Can you spell this word correctly (input {colored('R', 'magenta')} to replay the audio)? "
                )
                while result == 'R':
                    word_audio_fname = f"./audio/grade_{grade}/slow/{word}.mp3"
                    if not os.path.exists(word_audio_fname):
                        print(
                            f"Audio file {word_audio_fname} is not downloaded."
                        )
                        raise QuitError
                    playsound(word_audio_fname)
                    result = get_input(
                        f"Can you spell this word correctly (input {colored('R', 'magenta')} to replay the audio)? "
                    )
                if result == word.upper():
                    print(
                        f"Correct! The word was {colored(word, 'green', attrs=['bold'])}."
                    )
                    word_scores[word] += 1
                else:
                    print(
                        f"{colored(result.lower(), 'magenta', attrs=['bold'])} is incorrect. The word was {colored(word, 'blue', attrs=['bold'])}."
                    )
                    word_scores[word] -= 1
                print()

            else:
                raise ValueError
    except QuitError:
        print()
        if record_progress:
            save_progress(fname, word_scores)
        else:
            print("┌─────────────────────────────────────────┐")
            print(
                f"│            {colored('Quitting program.', 'blue', attrs=['bold'])}            │"
            )
            print("└─────────────────────────────────────────┘")


def get_and_read_word_file(grade: int, record_progress: bool,
                           reset_progress: bool) -> tuple[str, dict[str, int]]:
    """
    """

    original_fname = f"./word_lists/grade_{grade}.txt"
    if not os.path.exists(original_fname):
        raise ValueError

    fname = ""
    word_scores = {}

    if record_progress:
        fname = f"./in_progress_word_lists/grade_{grade}.csv"
        if not os.path.exists(fname) or reset_progress:
            with open(original_fname) as f:
                word_scores = {word.strip(): 0 for word in f.readlines()}
        else:
            with open(fname) as f:
                reader = csv.reader(f)
                word_scores = {row[0].strip(): int(row[1]) for row in reader}
    else:
        fname = original_fname
        with open(fname) as f:
            word_scores = {word.strip(): 0 for word in f.readlines()}

    return fname, word_scores


def save_progress(fname: str, word_scores: dict[str, int]):
    """
    """

    with open(fname, mode='w') as f:
        writer = csv.writer(f)
        for word, score in word_scores.items():
            writer.writerow([word, score])

    print("┌─────────────────────────────────────────┐")
    print(
        f"│      {colored('Your progress has been saved.', 'blue', attrs=['bold'])}      │"
    )
    print(
        f"│            {colored('Quitting program.', 'blue', attrs=['bold'])}            │"
    )
    print("└─────────────────────────────────────────┘")


def get_input(prompt: str = "") -> str:
    """
    Gets sanitized user input with the provided prompt. Throws QuitError when "Q" is entered.

    Args:
        prompt: Prompt for input.
    Returns:
        User input, stripped and in uppercase.
    """

    val = input(prompt).strip().upper()
    if val == "Q":
        raise QuitError
    return val


def main():
    try:
        start_program()
    except QuitError:
        print("Quitting program.")


if __name__ == "__main__":
    main()
