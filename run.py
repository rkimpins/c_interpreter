import os
import subprocess
import logging

class CCode:
    def __init__(self):
        #self.filename = "c_interpreter_" + time.strftime("%m_%d_%H_%M_%S") + ".cpp"
        self.filename = "c_interpreter.cpp"
        self.__includes = ["#include <stdio.h>"]
        self.__functions = []
        self.__variables = []
        self.__commands = []
        self.__compiler = "g++"# -std=c++11" #"gcc", clang, clang++

        self.__namespaces = []

        self.insertion_order = []
        self.__last_print = ""
        self.compile()

    def compile(self):
        # Write to file, run file
        with open(self.filename, "w") as fp:
            for include in self.__includes:
                fp.write(include+"\n")
            for namespace in self.__namespaces:
                fp.write(namespace+"\n")
            for function in self.__functions:
                fp.write(function)
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
    def add_namespace(self, namespace):
        self.__namespaces.append(namespace)
        self.insertion_order.append("namespace")
        self.__last_print = ""

    def undo(self):
        if len(self.insertion_order) == 0:
            print("Nothing to undo")
        if self.__last_print != "":
            self.__last_print = ""
        else:
            last_insertion = self.insertion_order.pop()
            if last_insertion == "include":
                self.__includes.pop()
            elif last_insertion == "function":
                self.__functions.pop()
            elif last_insertion == "command":
                self.__commands.pop()
            elif last_insertion == "namespace":
                self.__namespaces.pop()


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
            continue;
        elif inp == "function":
            function = ""
            inp = input(">")
            while inp != "endfunction":
                function += (inp + "\n")
                inp = input(">")
            Runner.add_function(function)
        elif inp == "":
            pass
        elif inp[:8] == "#include":
            Runner.add_include(inp)
        elif inp[:4] == "cout" or inp[:9] == "std::cout" or inp[:5] == "print":
            Runner.add_print(inp)
        elif inp[:5] == "using":
            Runner.add_namespace(inp)
        else:
            Runner.add_command(inp)

        Runner.compile()

        #TODO make debugger only
        #Runner.print_file()
        #gcc -E file
        #cpp file
        #TODO add function functionality


if __name__ == "__main__":
    main()
