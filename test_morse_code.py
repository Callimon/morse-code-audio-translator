import tempfile
import unittest
import wave
from pathlib import Path

from morse_code import encode, write_wav


class EncodeTests(unittest.TestCase):
    def test_letters_and_words(self) -> None:
        self.assertEqual(encode("SOS help"), "... --- ... / .... . .-.. .--.")

    def test_numbers(self) -> None:
        self.assertEqual(encode("R2D2"), ".-. ..--- -.. ..---")

    def test_unsupported_characters_are_ignored(self) -> None:
        self.assertEqual(encode("Hi!"), ".... ..")


class AudioTests(unittest.TestCase):
    def test_wav_is_created(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = write_wav("... --- ...", Path(directory) / "sos.wav")
            self.assertTrue(output.exists())
            with wave.open(str(output), "rb") as wav_file:
                self.assertEqual(wav_file.getnchannels(), 1)
                self.assertEqual(wav_file.getsampwidth(), 2)
                self.assertGreater(wav_file.getnframes(), 0)

    def test_empty_morse_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            write_wav("", "unused.wav")


if __name__ == "__main__":
    unittest.main()
