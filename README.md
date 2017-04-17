# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

This submission only implements naked twins (triples and quadruples are not implemented).

Constraint propagation in general allows us to apply lower level (smaller unit) constraints to other connected parts of the puzzle. 
 
Naked Twins strategy provides one additional constraint: if we have 2 (3+, it'll work the same for higher level groups) boxes with 2(3+) available digits for them, and we have more unsolved boxes in the same unit(s), we can remove the twin digits from all other boxes where these digits are also available, because for the twin boxes, no other digits are available, and that means that these two(three+) boxes will definitely have one of the two(three+) twin digits, but not some other digit. 

This concept will wor for pair, triples and more of values. For a single value, the technique is absutely the same as elimination technique. 

For twins, the easiest way to implement this is this: 
1. Find all pairs of equal digit-possibilities of two digits in same units. 
2. For every pair, go through every unit they both are in, and for every other unsolved box in that unit, we can exclude these two digits from the list of possibilities. 

So, for example, if we have a unit where two boxes have available digits `2, 3`, and the third box has `2, 3, 5` available, than we can solve the third box to `5`, because 2 and 3 will be in the first two (twin) boxes.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

Diagonal sudoku problem is different from the classic sudoku problem in a way that both diagonals form additional unit in which every digit from 1 to 9 should only be presented once.

This additional constraint to solve against.

Constraint propagation is basically using constraints in local problem (each box, each unit) to form additional constraints in bigger space (another unit), which makes search much easier (less available possibilities), and in some cases gives us enough constraints to solve the problem (i.e. only one digit available).

Using diagonal units gives us an additional constraint together with classic unit constraints (rows, cols, 3x3 squares), which applies to using most Sudoku strategies (elimination, only available square, only available digit, naked twins).

Cons: the diagonal sudoku problem imposes additional constraints on the field => some classic sudoku problems become unsolvable.


### Additional strategies implemented

1. Only Square strategy is also implemented and used in `solution.py`. See the details on [SudokuDragon](https://www.sudokudragon.com/tutorialonlysquare.htm).
2. `solution_test_from_file.py` contains additional code that loads sudokus from `easy50.txt` and `top95.txt` and tries to solve them. They're classic sudoku problems and most of them are unsolvable with diagonal approach. To test them, you'd need to comment out `diagonal_units` and run `solution_test_from_file.py`.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

