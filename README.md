# SnakeGome1
machine learns to play snake game ft. nicholas arana

Uses a conda virtual enviornment, pytorch, pygame, and numpy

We create a simple snake game using pygame and use this as the base for the AI.

The AI is created using pytorch machine learning framework with an Adam optimizer.

The program works by feeding the neural network 14 inputs all in the form of booleans: the direction its traveling in, the direction of the food is in realtion to its head, and the direction of its body and walls in relation to its head. 

We reward the snake if it eats the food and if it is moving in the direction of the food(equation).

We punish the snake if it runs into eihter itself or the wall and if it moves around aimlessly wihthout dying or eating.

By inputting all these factors into a complicated linear algebra equation we recieve a matrice of 3 values. Whichever of the 3 values is the greatest, we select as the output and the snake will make that decision. It has 3 decsions to go with these values of straight, right, and left.

The snake ends up performing pretty well with its average score increasing as the number of games increases. The longer we run the program, the better the snake gets.
