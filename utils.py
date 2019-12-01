""" Advent of Code 2019
"""

from pathlib import Path

###########################

def run(part1, part2):
    """."""
    #print(
    #f"""Output from {PATH} using {DATA}""")
    print(
    f"""
    Part 1
    {part1()}
    """)
    print(
    f"""
    Part 2
    {part2()}
    """)

###########################

def get_input(day, converter=None):
    """."""
    input_file = Path('input') / (str(day) + ".txt")
    with open(input_file) as f:
        text = list(map(str.strip, f.readlines()))
    print(f'INPUT_TEXT={text}'[:75] + '...]')
    if converter:
        return list(map(converter, text))
    return text

def sscanf(text, regex):
    _ = re.compile(regex)
    return _.match(text).groups()

