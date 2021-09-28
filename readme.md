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

Day | Part | Notes
--- | ---- | -----
8  | 2 | ![printout](./images/day8p2.png)
19 |   | Used a monochrome bitmap image to store 10000x10000 booleans good for time, great for visualisation!
20 |   | breadth first search with 3 dimensions not much trickier than two - color image for nicer mapping, gif for 3d!
20 | 1 | ![Final BFS state](./images/day20p1.png)
20 | 2 | ![Animated final BFS state of all visited layers](./images/day20p2.gif)
22 | 1 | Slicing a list was easy enough :) Added a solution using part 2 method which needed deconstructing as part1 wants to find a value not return an indexes content
22 | 2 | Brute force results in MemoryError.  I gave up, this was way above my maths capabilities so I stole a [solution](https://github.com/metalim/metalim.adventofcode.2019.python/blob/master/22_cards_shuffle.ipynb). The concept of turning the whole script into a single linear time function was interesting.
24 | 1 | ![Final game of life state](./images/day24p1.png)
24 | 2 | Copying arrays of images then iterating over each pixel takes a long time, if I was restarting this now, I would just keep a ``set`` of bugs as 3-tuple (layer,x,y) and copy the single set instead of the stack of images.  Making the NEIGHbour lookup table was a lot simpler and shorter than trying to define the many rules individually. Finally, I could gif the pile of map images, but there's nothing interesting to see...
