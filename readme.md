## Introduction
A simple Sudoku generator and solver. Something that takes this:

```
5   4 | 6 7 8 | 9 1 2
6 7   | 1 9 5 |   4 8
1 9 8 | 3 4 2 | 5 6
---------------------
8   9 | 7   1 | 4 2 3
4 2 6 | 8 5 3 | 7 9 1
7 1 3 | 9 2 4 | 8   6
---------------------
9 6 1 |   3 7 | 2 8 4
2 8 7 | 4 1 9 | 6 3 5
3 4 5 | 2 8 6 | 1 7 9
```

and turns it into this:

```
5 3 4 | 6 7 8 | 9 1 2
6 7 2 | 1 9 5 | 3 4 8
1 9 8 | 3 4 2 | 5 6 7
---------------------
8 5 9 | 7 6 1 | 4 2 3
4 2 6 | 8 5 3 | 7 9 1
7 1 3 | 9 2 4 | 8 5 6
---------------------
9 6 1 | 5 3 7 | 2 8 4
2 8 7 | 4 1 9 | 6 3 5
3 4 5 | 2 8 6 | 1 7 9
```

## Usage

You can try to generate puzzles by running

```
python generate_puzzle.py
```

or just run the unit tests:

```
python unit_tests.py
```

Written and tested on Python 3.7.