#!/usr/bin/env python3
"""Titulky SubRip editor.

Command line program for editing .srt files. Display file informations, shift or
fit subtitles.

Note: We internally process binary data to work around the various text encodings / BOMs.
"""
import argparse
import datetime
import math
import os
import sys
from typing import Generator, Iterable, List, NamedTuple, Tuple
from argparse import Namespace


DIGITS = set(b'0123456789')
ARROW = b' --> '
__version__ = '1.0.2'


def parse_timestamp(text: str) -> float:
    """Parse normal timestamp.

    Example:
        >>> parse_timestamp('1:23:45.6789')
        5025.6789
    """
    parts = text.split(':')
    if len(parts) > 3:
        raise ValueError(f'Invalid time string {text!r}')

    timestamp = 0.
    sign = math.copysign(1, float(parts[0]))
    for i, part in enumerate(reversed(parts)):
        timestamp += abs(float(part)) * (60 ** i)

    return sign * timestamp


def parse_timestamp_srt(text: bytes) -> float:
    """Parse SubRip timestamp from bytes.

    Example:
        >>> parse_timestamp_srt(b'12:34:56,789')
        45296.789
    """
    text = text.decode().strip()
    dt = datetime.datetime.strptime(text, '%H:%M:%S,%f')
    return datetime.timedelta(
        hours=dt.hour,
        minutes=dt.minute,
        seconds=dt.second,
        microseconds=dt.microsecond,
    ).total_seconds()


def format_timestamp_srt(timestamp: float) -> bytes:
    """Format SubRip timestamp to bytes.

    Example:
        >>> format_timestamp_srt(45296.789)
        b'12:34:56,789'
    """
    hours, remainder = divmod(timestamp, 3600)
    minutes, seconds = divmod(remainder, 60)
    ret = b'%02d:%02d:%06.3f' % (int(hours), int(minutes), seconds)
    return ret.replace(b'.', b',')


class Subtitle(NamedTuple):

    """Single SubRip subtitle entry."""

    nr: int
    start: float
    end: float
    content: list


def parse_subtitle(lines: List[bytes]) -> Subtitle:
    """Parse single subtitle from bytes lines.

    Args:
        lines: Bytes lines to parse.

    Returns:
        Parsed Subtitle instance.

    Example:
        >>> lines = [b'42', b'01:23:45,500 --> 01:34:54,000', b'Hello,', b'world!', b'']
        ... parse_subtitle(lines)
        Subtitle(nr=42, start=5025.5, end=5694.0, content=[b'Hello,', b'world!', b''])
    """
    if len(lines) < 3 or ARROW not in lines[1]:
        raise ValueError('Can not parse Subtitle from invalid lines', lines)

    start, end = map(parse_timestamp_srt, lines[1].split(ARROW))
    return Subtitle(
        nr = int(lines[0]),
        start=start,
        end=end,
        content=lines[2:],
    )


def parse_subtitles(lines: List[bytes]) -> Generator[Subtitle, None, None]:
    """Parse all subtitles from bytes lines.

    Args:
        lines: Bytes lines to parse.

    Yields:
        All parsed subtitles.
    """
    lines = [ line.strip() for line in lines if line.strip() ]
    start = -1
    for end, line in enumerate(lines):
        if DIGITS.issuperset(line):
            if start != -1:
                yield parse_subtitle(lines[start:end])

            start = end

    if start != -1:
        yield parse_subtitle(lines[start:])


def format_subtitle(subtitle: Subtitle) -> List[bytes]:
    """Format subtitle to bytes lines.

    Args:
        subtitle: Subtitle to format.

    Returns:
        Bytes lines of text (caller can decide which newline character).
    """
    lines = [
        str(subtitle.nr).encode(),
        ARROW.join([
            format_timestamp_srt(subtitle.start),
            format_timestamp_srt(subtitle.end),
        ]),
    ]
    lines.extend(subtitle.content)
    lines.append(b'')  # Empty line SubRip subtitle termination
    return lines


def format_subtitles(subtitles: Iterable[Subtitle], newline: bytes = b'\n') -> bytes:
    """Format multiple subtitles to bytes.

    Args:
        subtitles: Subtitles to format.

    Kwargs:
        newline: Newline character to use.

    Returns:
        Formatted SubRip subtitles.
    """
    return newline.join(
        newline.join(format_subtitle(sub))
        for sub in subtitles
    )


def ceil(x, ndigits: int = 0) -> float:
    """Ceil up number at ndigits."""
    shift = 10 ** ndigits
    return math.ceil(x * shift) / shift


def floor(x, ndigits: int = 0) -> float:
    """Floor down number at ndigits."""
    shift = 10 ** ndigits
    return math.floor(x * shift) / shift


def tranform_subtitles(
    subtitles: Iterable[Subtitle],
    scale: float = 1.,
    offset: float = 0.,
) -> Generator[Subtitle, None, None]:
    """Transform start and end times of subtitles. f(t) = scale * t + offset.

    Args:
        subtitles: Subtitles to transform.

    Kwargs:
        scale: Scale factor.
        offset: Offset factor.

    Yields:
        Transformed subtitles.
    """
    for sub in subtitles:
        yield sub._replace(
            start=ceil(scale * sub.start + offset, ndigits=3),
            end=floor(scale * sub.end + offset, ndigits=3),
        )


def cli() -> Namespace:
    """Parse command line interface."""
    parser = argparse.ArgumentParser(prog='Titulky', description='SubRip editor')
    parser.add_argument('infile', help='input file')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.set_defaults(mode='info')

    subparsers = parser.add_subparsers()

    infoParser = subparsers.add_parser('info', help='show subtitle file infos')
    infoParser.set_defaults(mode='info')

    shiftParser = subparsers.add_parser('shift', help='shift all subtitles by some amount')
    shiftParser.add_argument('amount', help='time shift amount')
    shiftParser.add_argument('-o', '--outfile', default=sys.stdout, help='output file. stdout by default.')
    shiftParser.set_defaults(mode='shift')

    fitParser = subparsers.add_parser('fit', help='fit subtitles to start / end time')
    fitParser.add_argument('first', help='start time of first subtitle')
    fitParser.add_argument('last', help='start time of last subtitle')
    fitParser.add_argument('-o', '--outfile', default=sys.stdout, help='output file. stdout by default')
    fitParser.set_defaults(mode='fit')

    return parser.parse_args()


def analyze_srt_data(srtData: bytes) -> Tuple[bytes, bytes]:
    """Analyze raw binary SubRip data for BOM prefix and newline style.

    Args:
        srtData: Bytes to an

    Returns:
        BOM and newline bytes.

    Note: This only works for SubRip files since we are looking for digit
    character of the first subtitle in the data stream..
    """
    bom = b''
    maxBom = 4
    for char in srtData[:maxBom]:
        if char in DIGITS:
            break

        bom += bytes([char])

    for newline in [b'\r\n', b'\n', b'\r']:
        if newline in srtData:
            return bom, newline

    ValueError('Could not determine newline style!')


def yes_or_no(question: str) -> bool:
    """Yes or no question for the user.

    Args:
        question: Question to ask the user.

    Returns:
        Yes or no.

    Raises:
        RuntimeError: If not possible to parse answer from user.
    """
    answer = input(question + ' [y/n]')
    key = answer.lower()
    valid = {
        'y': True, 'ye': True, 'yes': True, 'n': False, 'no': False, '1': True,
        '0': False,
    }
    if key in valid:
        return valid[key]

    answer = input(f'I do not understand {answer!r}. Please answer with [{",".join(valid)}]')
    key = answer.lower()
    if key in valid:
        return valid[key]

    raise RuntimeError(f'Sorry but I still cannot understand you. What did you mean with {answer!r}?')


def main():
    args = cli()
    with open(args.infile, 'rb') as f:
        raw = f.read()

    bom, newline = analyze_srt_data(raw)
    data = raw.lstrip(bom)
    lines = data.split(newline)
    subtitles = list(parse_subtitles(lines))
    if not subtitles:
        print(f'No subtitles in {args.infile!r}')
        sys.exit(1)

    first = min(sub.start for sub in subtitles)
    last = max(sub.start for sub in subtitles)
    if args.mode == 'info':
        print(f'Found {len(subtitles)} subtitles in {args.infile!r}')
        print(f'{len(raw)} bytes')
        if bom:
            print(f'BOM: {bom}')
        else:
            print(f'BOM: {bom} (no BOM)')

        print(f'newline: {newline}')
        print('Subtitles:\n')
        print(format_subtitles(subtitles[:3]).decode())
        print('...\n')
        print(format_subtitles(subtitles[-3:]).decode())
        sys.exit(0)

    if args.mode == 'shift':
        amount = parse_timestamp(args.amount)
        if first + amount < 0:
            raise ValueError(f'amount {amount} would lead to negative start time')

        print(f'Shifting subtitles by {amount} seconds')
        newSubtitles = tranform_subtitles(subtitles, scale=1., offset=amount)

    elif args.mode == 'fit':
        if (last - first) == 0:
            raise RuntimeError('Subtitles are not spread out enough for re-scaling')

        firstDesired = parse_timestamp(args.first)
        lastDesired = parse_timestamp(args.last)
        print(f'Re-fitting subtitles to [{args.first}, {args.last}]')
        scale = (lastDesired - firstDesired) / (last - first)
        offset = firstDesired - scale * first
        newSubtitles = tranform_subtitles(subtitles, scale, offset)

    out = bom + format_subtitles(newSubtitles, newline)

    if args.outfile is sys.stdout:
        sys.stdout.buffer.write(out)
        sys.stdout.flush()
    else:
        if os.path.exists(args.outfile):
            question = f'File {args.outfile} does already exists! Do you want to overwrite it?'
            if not yes_or_no(question):
                sys.exit(0)

        with open(args.outfile, 'wb') as f:
            f.write(out)

        print(f'Wrote to {args.outfile!r}')


if __name__ == '__main__':
    main()
