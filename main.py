"""Command-line interface for the Morse Code Audio Translator."""

import argparse

from morse_code import encode, write_wav


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Translate a message to Morse code and save it as audio."
    )
    parser.add_argument("message", nargs="*", help="message to translate")
    parser.add_argument("-o", "--output", default="morse_message.wav")
    parser.add_argument("--no-audio", action="store_true", help="only display Morse code")
    args = parser.parse_args()

    message = " ".join(args.message).strip()
    if not message:
        message = input("Message to translate: ").strip()

    morse = encode(message)
    if not morse:
        raise SystemExit("The message did not contain any supported letters or numbers.")

    print(f"Morse code: {morse}")
    if not args.no_audio:
        output_path = write_wav(morse, args.output)
        print(f"Audio saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
