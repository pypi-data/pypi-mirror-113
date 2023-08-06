# Titulky

Tiny Python SubRip editor. Display infos, shift and re-fit timestamps. 

## Installation

Use the package manager pip to install titulky.

```bash
pip3 install titulky
```

## Usage

Display informations for some `.srt` file.

```bash
python3 titulky.py test.srt
```

Shift subtitles by some amount.

```bash
python3 titulky.py test.srt shift "12.34"
```

Refit subtitles to some interval.

```bash
python3 titulky.py test.srt shift "1:23.456" "2:34:56"
```

By default titulky writes to stdout. You can write the output to a file with

```bash
python3 titulky.py test.srt shift 5.0 --outfile out.srt
```
