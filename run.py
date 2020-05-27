"""C runtime

This program attempts to implement a simple C runtime environment

The goal of this pogram was to have a quick way to test out code snippets to confirm functionality while in the middle of a larger project. This is a very naive approach. Using python, we generate and compile a code file, and that is how we test everything. There will definitely be edge cases that fail, and this is in no way a perfect runtime environment. 

This file can also be imported as a module, and contains the following useful class
    * CCode - a representation of a c code file
"""


import os
import subprocess
import logging

# Small Slant from http://www.patorjk.com/software/taag/
GLOBAL_INTRO = """
  _____  ___            __  _
 / ___/ / _ \__ _____  / /_(_)_ _  ___
/ /__  / , _/ // / _ \/ __/ /  ' \/ -_)
\___/ /_/|_|\_,_/_//_/\__/_/_/_/_/\__/
"""


class CCode:
    """
    A Class used to represent a C code file to be run

    Attributes are grouped by where they need to appear in the code file.
    Includes should appear at the top, code appears in the main function,
    functions appear outside of main, etc.

    Attributes
    ----------
    __filename : str
        name of the c or c++ file written to, compiled, and run
    __compiler : list
        list of compiler and flags. Example: ["g++", "-std=c++11"] or ["clang"]
    __includes : list
        list of include statements:
    __functions : list
        list of functions
    __commands : list
        list of code segments that appear inside the main function
    __namespaces : list
        list of namesapces changes. Example: ["using namespace std;"]
    __insertion_order : list
        order that different pieces of code were added to various attributes
        important for implementing undo function
    __last_print : str
        the last print statement that was added. Code will only ever contain
        at most one print statement to simulate a runtime

    Methods
    -------
    def compile()
        writes all of the necessary code to a file, compiles it, and runs it
    def add_include(include)
        Adds the include statement to the includes
    def add_command(self, command):
        Adds the command statement to the commands
    def add_function(self, function):
        Adds the function statement to the functions
    def add_namespace(self, namespace):
        Adds the namespace statement to the namespaces
    def undo(self):
        Undos the previous insertion, regardless of what the insertion was
    def add_print(self, print_stmt):
        Adds a print statement to our code. Only ever contains one print statement
    def add_code(self, code):
        Adds a code statemetns to the commands
    def set_compiler(self, compiler):
        Set the compiler
    def get_compiler(self):
        Get the current compiler
    def print_file(self):
        Print the contents of the code file
    """

    def __init__(self, filename = "c_interpeter.cpp", compiler = ["g++"]):
        """
        Parameters
        ----------
        filename : str
            The name of the file to write the c code to
        compiler : list
            List containing the compiler and any flags to use to compile the code
        """

        # Name of code file
        self.__filename = filename
        # Compiler to use on code file
        self.__compiler = compiler # -std=c++11" #"gcc", clang, clang++
        # Include statements, written to top of file
        self.__includes = ["#include <stdio.h>"]
        # Functions, written before main function
        self.__functions = []
        # Commands, written inside main function
        self.__commands = []
        # Namespaces, written after includes
        self.__namespaces = []
        # Order of inserted code segments to each attribute
        self.__insertion_order = []
        # The most revent print statement added
        self.__last_print = ""
        # Compile code file
        self.compile()

    def __str__(self):
        return (
            f"__filename: {self.__filename}\n"
            f"Compiler: {self.__compiler}\n"
            f"Includes: {self.__includes}\n"
            f"Functions: {self.__functions}\n"
            f"Code: {self.__commands}\n"
            f"Namespaces: {self.__namespaces}\n"
            f"Insertion Order: {self.__insertion_order}"
        )

    def compile(self):
        """Writes, compiles, and runs the C code file

        This method overwrites the contents of the file pointed to by __filename.
        Uses __includes, __functions, __commands, __namespaces, and __last_print,
        writing each to the appropriate section. 
        """

        # Write all of the code segments to file in appropriate order
        with open(self.__filename, "w") as fp:
            for include in self.__includes:
                fp.write(include+"\n")
            for namespace in self.__namespaces:
                fp.write(namespace+"\n")
            for function in self.__functions:
                fp.write(function+"\n")
            fp.write("int main() {\n")
            for command in self.__commands:
                fp.write(command+"\n")
            fp.write(self.__last_print+"\n")
            fp.write("return 0;\n}")

        # Compile using __compiler
        subprocess.run(self.__compiler + [self.__filename])

        # Run the compiled file, with output appearing in terminal
        tmp=subprocess.call("./a.out")
        print()

    def add_include(self, include: str):
        """Add an include statement to the code

        Parameters
        ----------
        include : str
            Include statment to be added to the code
        """

        self.__includes.append(include)
        self.__insertion_order.append("include")
        self.__last_print = ""

    def add_command(self, command: str):
        """Add a code statement to the code

        Parameters
        ----------
        command : str
            Code statment to be added to the code
        """

        self.__commands.append(command)
        self.__insertion_order.append("command")
        self.__last_print = ""

    def add_function(self, function: str):
        """Add a function statement to the code

        Parameters
        ----------
        function : str
            Function statment to be added to the code
        """

        self.__functions.append(function)
        self.__insertion_order.append("function")
        self.__last_print = ""

    def add_namespace(self, namespace: str):
        """Add a namespace statement to the code

        Parameters
        ----------
        namespace : str
            Namespace statment to be added to the code
        """
        self.__namespaces.append(namespace)
        self.__insertion_order.append("namespace")
        self.__last_print = ""

    def add_print(self, print_stmt: str):
        """Add a print statement to the code

        Parameters
        ----------
        print_stmt : str
            Print statment to be added to the code
        """

        self.__last_print = print_stmt

    def add_code(self, code: str, in_main=True):
        """Add an arbitrary piece of code

        This method accepts any code statement, and decides which attribute it
        should be added to. For example, is it an include, a namespace, a print, etc.

        Parameters
        ----------
        in_main : bool
            is the piece of code to be added inside the main functionk
        code : str
            Code statment to be added to the code
        """

        if code[:8] == "#include":
            self.add_include(code)
        elif code[:4] == "cout" or code[:9] == "std::cout" or code[:5] == "print":
            self.add_print(code)
        elif code[:5] == "using":
            self.add_namespace(code)
        elif in_main:
            self.add_command(code)
        else:
            self.add_function(code)

    def undo(self):
        """Undo the previous code insertion

        This method is vital for undoing insertions that break the code. It uses
        the __insertion_order list to track which attributes need to have code
        statements removed. If there is currently a __last_print statement, that
        means it was the last thing inserted.
        """

        if len(self.__insertion_order) == 0:
            # No insertions made
            print("Nothing to undo")
        if self.__last_print != "":
            # Print statement was last piece of added code
            self.__last_print = ""
        else:
            # Find which attribute had code added to it
            last_insertion = self.__insertion_order.pop()
            if last_insertion == "include":
                self.__includes.pop()
            elif last_insertion == "function":
                self.__functions.pop()
            elif last_insertion == "command":
                self.__commands.pop()
            elif last_insertion == "namespace":
                self.__namespaces.pop()

    def set_compiler(self, compiler: [str]):
        """Set the compiler for the c code

        Parameters
        ----------
        compiler : list
            Compiler and flags to be used for compilation
        """

        self.__compiler = compiler

    def get_compiler(self):
        """Get the curent compiler for the c code

        """

        return self.__compiler

    def print_file(self):
        """Print the current contents of the compilation file

        """

        print(f"Contents of {self.__filename}")
        line_length = 20
        print("-"*line_length)
        os.system(f"cat {self.__filename}")
        print("\n"+"-"*line_length)

def print_help():
    """Print the help menu for the program

    """

    help_string = '''Welcome to the help menu. Here are some useful commands
    exit: end the program
    file: view the contents of the compilation file
    func[tion]: begin entering a multiline function
    endfunc[tion]: stop entering a multiline function
    multi[line]: begin entering a multiline piece of code
    endmulti[line]: stop entering a multiline piece of code
    <enter>: repeat the previous command
    compiler: show the current compiler
    compiler <new compiler>: change the compiler. Can add flags'''
    #TODO add custom print functions for common c types
    print(help_string)

def interactive_runner():
    pass

def main():
    Runner = CCode()
    print(GLOBAL_INTRO)
    print("To get help, type h[elp]")
    while True:
        inp = input(">>> ")
        if inp == "exit":
            break
        elif inp in ["help", "h"]:
            print_help()
        elif inp == "restart":
            Runner = CCode()
        elif inp == "undo":
            Runner.undo()
        elif inp == "file":
            Runner.print_file()
            continue;
        elif inp[:8] == "compiler":
            if len(inp) == 8:
                print(f"compiler: {Runner.get_compiler()}")
            else:
                print(f"old compiler: {Runner.get_compiler()}")
                Runner.set_compiler(inp.split()[1:])
                print(f"new compiler: {Runner.get_compiler()}")
        elif inp in ["func", "function"]:
            function = ""
            print("function mode, end using endfunc[tion]")
            inp = input("> ")
            while inp not in ["endfunction", "endfunc"]:
                function += (inp + "\n")
                inp = input("> ")
            Runner.add_function(function)
        elif inp in ["multiline", "multi"]:
            print("multiline mode, end using endmutli[line]")
            command = ""
            inp = input("> ")
            while inp not in ["endmultiline", "endmulti"]:
                command += (inp + "\n")
                inp = input("> ")
            Runner.add_command(command)
        elif inp == "":
            pass
        else:
            Runner.add_code(inp)

        Runner.compile()

        #TODO make debugger only, add logging output
        #Runner.print_file()


if __name__ == "__main__":
    main()
