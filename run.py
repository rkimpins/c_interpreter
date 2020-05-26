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
        self.compiler = "g++" #"gcc", clang, clang++

    def compile(self):
        # Write to file, run file
        with open(self.filename, "w") as fp:
            for include in self.__includes:
                fp.write(include+"\n")
            for function in self.__functions:
                fp.write(function)
            fp.write("using namespace std;\n")
            fp.write('int main() {\nprintf("success\\n");\nreturn 0;\n}') #need double \\ for prints
        # Compile
        subprocess.call([self.compiler, self.filename])
        # Run
        tmp=subprocess.call("./a.out")

    def print_file(self):
        print(f"Contents of {self.filename}")
        print("-"*10)
        os.system(f"cat {self.filename}")
        print("\n"+"-"*10)

def main():
    Runner = CCode()
    while True:
        inp = input(">>>")




        Runner.compile()
        #TODO make debugger only
        Runner.print_file()


if __name__ == "__main__":
    main()
