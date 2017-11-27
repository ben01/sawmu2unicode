#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
python sawmu2unicode.py input.txt output.txt

Reads input.txt, converts to unicode, and writes
out to output.txt

Any text not inside <en>...</en> is assumed to be
ascii text formatted with the Sawmu font.

'''

import sys, re

def text2Unicode(text):
    '''
    Takes a string of ascii text which is assumed
    to be Karen copy written with the Sawmu font,
    converts to Unicode, and returns. Also makes some
    typographical adjustments.

    returns string
    '''

    charMap = {
        'u': 'က',
        'c': 'ခ',
        '*': 'ဂ',
        'C': 'ဃ',
        'i': 'င',
        'p': 'စ',
        'q': 'ဆ',
        'Z': 'ဇ',
        #   '': 'ၡ',
        'n': 'ည', 'ñ': 'ည',
        'w': 'တ',
        'x': 'ထ',
        "'": 'ဒ',
        'e': 'န', 'E': 'န',
        'y': 'ပ',
        'z': 'ဖ',
        '[': 'ဟ',
        'r': 'မ',
        '<': 'ယ',
        '&': 'ရ', '½': 'ရ',
        'v': 'လ',
        #   '': 'ဝ',
        'o': 'သ',
        'b': 'ဘ',
        't': 'အ',
        '{': 'ဧ',

        'S': 'ှ', '§': 'ှ', 'V': 'ှ့', '|': 'ှု', 'â': 'ှူ',
        'a': ' ၠ',
        's': 'ျ', '@': 'ျ့',
        'M': 'ြ', 'B': 'ြ', 'N': 'ြ', 'j': 'ြ', 'ê': 'ြု', 'û': 'ြု',
        'G': 'ွ',

        'D': 'ီ',
        'd': 'ိ',
        'H': 'ံ',
        'J': 'ဲ',
        'h': '့',
        'Y': '့',
        'g': 'ါ',
        'U': 'ၢ',
        'l': 'ူ', 'L': 'ူ',
        'k': 'ု', 'K': 'ု',

        'f': '်',

        'O': 'ၣ်',
        'P': 'ာ်',
        ';': 'း',
        'I': 'ၢ်',
        ':': 'ၤ',

        '1': '၁',
        '2': '၂',
        '3': '၃',
        '4': '၄',
        '5': '၅',
        '6': '၆',
        '7': '၇',
        '8': '၈',
        '9': '၉',
        '0': '၀',

        '=': u'\u2018',
        '+': u'\u2019',
    }

    # Change numeric zero to alphabetic "wa" if followed by vowel, tone, etc.
    text = re.sub(r'0([S§V|âs@MBNjêûGaDdHJhYgUlLkKfOP;I:])', r'ဝ\1', text)

    # Reorder medial "ra" to follow it's consonant
    text = re.sub(r"([MBNjêû])([uc*CipqZnwx'eyz[r<&vobt{])", r'\2\1', text)

    # Replace "ra" + medial "gha" with "sha"
    text = re.sub(r'&S', 'ၡ', text)

    # Remove whitespace after left quote
    text = re.sub(r'=\s+', '=', text)

    # Add a space before left quote if not precedded by whitespace or another quote
    text = re.sub(r'(?<=[^\s=])=', ' =', text)

    # Remove whitespace before right quotes
    text = re.sub(r'\s+\+', '+', text)

    # Add a space after right quote if not followed by whitespace, EOL, or another right quote
    text = re.sub(r'\+(?=[^\s+])', '+ ', text)

    # Replace 2 consecutive single quotes with a double quote
    text = re.sub(r'={2}', '\u201C', text); text = re.sub(r'\+{2}', '\u201D', text)

    # Add a space after comma and period if not followed by white space, right quote, right parentheses, or end of line
    text = re.sub(r'([,.])(?=[^\s=+’”)])', r'\1 ', text)

    # Remove whitespace after left parentheses
    text = re.sub(r'\(\s+', '(', text)

    # Add a space before left parentheses if not preceded by whitespace
    text = re.sub(r'(?<=\S)\(', ' (', text)

    # Remove whitespace before right parentheses
    text = re.sub(r'\s+\)', ')', text)

    # Add a space after right parentheses if not followed by whitespace or EOL
    text = re.sub(r'\)(?=\S)', ') ', text)

    # Replace characters according to the charMap
    output = ''
    for char in text:
        try:
            output += charMap[char]
        except KeyError:
            output += char
    return output

# Read in the source file
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    inText = f.read()

# Iterate over blocks of karen and non-karen text, convert karen blocks to Unicode
output = ''
for textBlock in re.split(r'(<en>.*?<\/en>)', inText):
    if textBlock.startswith('<en>'):
        output += textBlock
    else:
        output += text2Unicode(textBlock)

# Insert zero width spaces between syllables (before a consonant if that consonant is preceded by a myanmar block char
# and not followed by the silencer character).
output = re.sub(r'(?<=[က-႟])(?=[ကခဂဃငစဆၡညတထဒနပဖဘမယရလဝသဟအဧ][^်])', '\u200B', output)

# Write out to file
with open(sys.argv[2], 'w', encoding='utf-8') as f:
    f.write(output)
