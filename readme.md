# AoC19

Advent of Code 2019 solutions https://adventofcode.com/2019

## Installation

```cmd
py -m venv p38
p38/scripts/activate
pip install -r requirements.txt
```

## Usage

```cmd
py dayxx.py
```

## Notes

* Utils - general purpose / multi-day utils including the IntCode Computer

## Key Lessons

* Day 19 - Used a monochrome bitmap image to store 10000x10000 booleans good for time, great for visualisation!
* Day 20 - breadth first search with 3 dimensions not much trickier than two - color image for nicer mapping
  ![image info](./images/day20p1.png)
