import os
import random
import time
import subprocess

class CCode:
    def __init__(self):
        #self.__filename_length = 10
        #str(random.randint(10**self.__filename_length, 10**(self.__filename_length+1)))

        # TODO Make this c or cpp?
        #self.filename = "c_interpreter_" + time.strftime("%m_%d_%H_%M_%S") + ".cpp"
        self.filename = "c_interpreter.cpp"
        self.__includes = ["#include <stdio.h>"]
        self.__functions = []
        self.__variables = []
        self.__commands = []
        self.__compiler = "g++" #"gcc", clang, clang++

        self.insertion_order = []
        self.__last_print = ""

    def compile(self):
        # Write to file, run file
        with open(self.filename, "w") as fp:
            for include in self.__includes:
                fp.write(include+"\n")
            for function in self.__functions:
                fp.write(function)
            fp.write("using namespace std;\n")
            fp.write("int main() {\n")
            for command in self.__commands:
                fp.write(command)
            fp.write(self.__last_print+"\n")
            fp.write("return 0;\n}")

        # Compile
        subprocess.run([self.__compiler, self.filename])

        # Run
        tmp=subprocess.call("./a.out")
        print()
        #print(f"tmp: {tmp}")

    def add_include(self, include):
        self.__includes.append(include)
        self.insertion_order.append("include")
        self.__last_print = ""

    def add_command(self, command):
        self.__commands.append(command)
        self.insertion_order.append("command")
        self.__last_print = ""

    def add_function(self, function):
        self.__functions.append(function)
        self.insertion_order.append("function")
        self.__last_print = ""

    def undo(self):
        if len(self.insertion_order) == 0:
            print("Nothing to undo")
        else:
            last_insertion = self.insertion_order.pop()
            if last_insertion == "include":
                self.__includes.pop()
            elif last_insertion == "function":
                self.__functions.pop()
            elif last_insertion == "command":
                self.__commands.pop()
        self.__last_print = ""


    def add_print(self, print_stmt):
        self.__last_print = print_stmt


    def print_file(self):
        print(f"Contents of {self.filename}")
        line_length = 20
        print("-"*line_length)
        os.system(f"cat {self.filename}")
        print("\n"+"-"*line_length)

def main():
    Runner = CCode()
    while True:
        inp = input(">>> ")
        if inp == "exit()":
            break
        elif inp in ["help", "h"]:
            #TODO add help menu
            print("help, h, exit(), print file, etc, can't redeclare variables")
        elif inp == "undo":
            Runner.undo()
        elif inp == "file":
            Runner.print_file()
        elif inp == "":
            pass
        #elif inp[-1] == ";":
        #    pass
        elif inp[:8] == "#include":
            Runner.add_include(inp)
        elif inp[:4] == "cout" or inp[:9] == "std::cout" or inp[:5] == "print" or inp[:9] == "std::print":
            #TODO remove using namespace from code?
            Runner.add_print(inp)
        else:
            Runner.add_command(inp)

        Runner.compile()

        #TODO make debugger only
        #Runner.print_file()
        #gcc -E file
        #cpp file


if __name__ == "__main__":
    main()
