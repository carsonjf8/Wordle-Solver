# Wordle Solver
This project is a command line program that assists the user in choosing optimal guesses when playing the game Wordle.
This is done by using Information Theory to choose words that would provide the most information when guessed.
It uses a list of possible answers to choose from that would be the most helpful.

This can be run by having wordle_solver.py and wordle_answers.txt in the same directory together.
Then run the command: ```python wordle_solver.py```
Follow the directions in the command line where it will provide information and prompt the user for what they guessed to update it's knowledge and provide optimal next guesses.

![Out for an example run](./example_run.png)
![Image of Wordle for the example run](./wordle_example_run.png)