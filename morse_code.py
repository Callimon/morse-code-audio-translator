"""Translate text to Morse code and generate a playable WAV file."""

from __future__ import annotations

import math
import struct
import wave
from pathlib import Path


MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....",
    "7": "--...", "8": "---..", "9": "----.",
}


def encode(message: str) -> str:
    """Return a Morse-code representation of ``message``.

    Unsupported characters are ignored. Letters are separated by one space and
    words by `` / `` so the result remains easy to read.
    """
    words: list[str] = []
    for word in message.upper().split():
        encoded_letters = [MORSE_CODE[char] for char in word if char in MORSE_CODE]
        if encoded_letters:
            words.append(" ".join(encoded_letters))
    return " / ".join(words)


def _tone(frequency: float, seconds: float, sample_rate: int, volume: float) -> bytes:
    sample_count = int(seconds * sample_rate)
    amplitude = int(32767 * volume)
    return b"".join(
        struct.pack("<h", int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)))
        for i in range(sample_count)
    )


def _silence(seconds: float, sample_rate: int) -> bytes:
    return b"\x00\x00" * int(seconds * sample_rate)


def write_wav(
    morse: str,
    destination: str | Path,
    *,
    frequency: float = 700.0,
    words_per_minute: int = 18,
    sample_rate: int = 44_100,
    volume: float = 0.35,
) -> Path:
    """Write ``morse`` to a mono 16-bit WAV file and return its path."""
    if not morse:
        raise ValueError("Morse code cannot be empty")
    if words_per_minute <= 0:
        raise ValueError("Words per minute must be positive")
    if not 0 < volume <= 1:
        raise ValueError("Volume must be between 0 and 1")

    unit = 1.2 / words_per_minute
    dot = _tone(frequency, unit, sample_rate, volume)
    dash = _tone(frequency, unit * 3, sample_rate, volume)
    symbol_gap = _silence(unit, sample_rate)
    letter_gap = _silence(unit * 3, sample_rate)
    word_gap = _silence(unit * 7, sample_rate)

    audio = bytearray()
    tokens = morse.split(" ")
    for index, token in enumerate(tokens):
        if token == "/":
            audio.extend(word_gap)
            continue

        for symbol_index, symbol in enumerate(token):
            audio.extend(dot if symbol == "." else dash)
            if symbol_index < len(token) - 1:
                audio.extend(symbol_gap)

        if index < len(tokens) - 1 and tokens[index + 1] != "/":
            audio.extend(letter_gap)

    output_path = Path(destination)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio)
    return output_path
