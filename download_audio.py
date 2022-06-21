#!/usr/bin/env python3

import os
from gtts import gTTS


def download(slow=False):
    """
    """

    for grade in range(1, 13):
        download_grade(grade, slow)


def download_grade(grade, slow=False):
    """
    """

    audio_dirname = './audio'
    if not os.path.exists(audio_dirname):
        os.makedirs(audio_dirname)

    fname = f"./word_lists/grade_{grade}.txt"
    if not os.path.exists(fname):
        raise ValueError

    grade_dirname = f"{audio_dirname}/grade_{grade}/{'slow' if slow else 'normal'}"
    if not os.path.exists(grade_dirname):
        os.makedirs(grade_dirname)

    with open(fname) as f:
        words = [word.strip() for word in f.readlines()]
        print(f"Downloading audio for grade {grade} ({len(words)} words)...")
        for word in words:
            word_audio_fname = f"{grade_dirname}/{word}.mp3"
            if not os.path.exists(word_audio_fname):
                gTTS(word, slow=slow).save(word_audio_fname)


def main():
    download(slow=False)
    download(slow=True)


if __name__ == "__main__":
    main()
