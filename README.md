# ee5450-module1-hw0
This homework assignment should provide a quick primer for Python.
There are two files: `blackjack.py` and `test_blackjack.py`.
The first file contains the class and function definitions for the blackjack game.
The second file contains unit tests for the blackjack game.

To grade your submission, GitHub will automatically run the tests inside `test_blackjack.py`.
These unit tests test each **mandatory** class member function inside the `Blackjack` class.

You are free to write any helper functions inside or outside of the class as you need.

You will notice that some of the functions within the `Blackjack` class have names that start 
with a single underscore (as opposed to the double-underscore surround that indicates a function
is a built-in Python function).  One example is `_create_stack()`.  The single underscore
indicates that this function is meant to be an internal function that is not recommended to be 
called by someone else using a variable that is of the `Blackjack` object type.  

This particular example, `_create_stack()`, is defined this way because any code that wants to call 
our `Blackjack` game object will not really want to have to manually initialize the whole game.  
They'd probably prefer that we setup the game for them.

Another example is a helper function that is specifically just for data within your
`Blackjack` class's internal data members.  Others can call this helper function if they want,
but you indicate using the underscore that it's not recommended because it's an internal helper
function.

As you read through the code, fill in function definitions that are just `pass`. 
You can test whether your implementation of the function works by click the Play button 
(green triangle) next to the signature for `test_{function_name}` in `test_blackjack.py`.  
For example, if you want to test `_create_stack()`, then you click the Play button that appears
left of `def test__create_stack(self):` (line 9) in `test_blackjack.py`.  
When you have completed all of the class member functions, you can click the Play button on line 5
of `test_blackjack.py` to test everything.  When it all passes, you can right-click anywhere
inside `blackjack.py` and click "Run blackjack.py" to run the game.

Hope you enjoy the game!
