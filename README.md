# C Interpreter
When I was writing projects in c/c++, I missed pythons functionality of being able to check syntax and functionality in an interactive shell. It was very useful for testing little things while writing a larger program. I decided to would write my own to make my life a bit easier for future c/c++ projects. Hopefully this helps others as well.

# Usage
run python3 run.py to start the interactive shell. The help menu can be reached by typing h or help, and has all of the useful commands included. 

# Challenges
The biggest issue I encountered outside of scope was deciding how to setup multiline inputs. I wanted to automatically detect when part of a function had been entered, or part of a class had been entered, but that was too complicated compared to the benefits. I opted to have the user manually indicate when they are entering multiline segments. Additionally, setting up the pretty print functions was difficult because it was communicating between python and c/c++ using strings, which isn't the cleanest way to do it.

# Where to go from here
Ideally I would like to improve the multiline stuff. It would be nice to automatically detect if an input is the start of a function and continue getting input until the function is complete. Same with classes, structs, etc. Currently this is done manually, which isn't super nice. Additional features could be more pretty print functions for different types, a method to save and load an environment (code file), a better method for removing code that breaks things (ex: an option to view all lines of code, and delete specific ones), and viewing the output of macro substitution and adding macro commands.

# What I learned
Here is what I learned
	* How to run terminal commands with python using the subprocess module
	* Python logging using logging module
