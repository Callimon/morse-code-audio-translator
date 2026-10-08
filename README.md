# Morse Code Audio Translator

A Python command-line program that translates a message into Morse code and
creates a playable WAV audio file. This portfolio project grew from a classroom
assignment and was reorganized into a small, documented, and tested application.

## What it demonstrates

- Python functions, dictionaries, loops, and string processing
- Input validation and command-line arguments
- File creation using Python's standard library
- Digital audio basics, including sample rates and sine waves
- Automated testing with `unittest`

## Run it

Python 3.9 or newer is recommended. No third-party packages are required.

```bash
python3 main.py "Hello world"
```

The program displays the translation and creates `morse_message.wav`.

To choose a filename:

```bash
python3 main.py "SOS" --output sos.wav
```

To translate without producing audio:

```bash
python3 main.py "Python 3" --no-audio
```

## Run the tests

```bash
python3 -m unittest -v
```

## Example

```text
$ python3 main.py "SOS"
Morse code: ... --- ...
Audio saved to: /path/to/morse_message.wav
```

## Possible future improvements

- Add punctuation support
- Decode Morse code back into text
- Add a graphical interface
- Let users adjust tone frequency and transmission speed
