
# mini fuzzer
mini fuzzer is a mutation-based fuzzing tool aimed at command line tools. By measuring the line coverage of the target program, effective test cases can be generated.
mini fuzz currently supports software written in C/C++ language.

# Features
- Automatically generate input to target program
- Use multiple mutation strategies
- Use measured line coverage for test case generation
- Display fuzzing progress in real time
- Generate a report summarizing detected crashes
<img width="1036" alt="スクリーンショット 2024-01-05 23 50 24" src="https://github.com/yk0112/mini_fuzzer/assets/130746469/f9e1b403-0379-43c6-b441-140a0580bdfe">

# Installation
```
$ git clone https://github.com/yk0112/mini_fuzzer.git
```

# Usage

## compile your program 
First, compile your C or C++ program using GCC. At this time, add the `-fprofile-arcs` and `-ftest-coverage` options to the compilation command.
```
$ gcc -fprofile-arcs -ftest-coverage example.c -o example
```

## config file settings
Before start fuzzing, you need to edit config.py for settings.
First, specify the path where the gcov file will be generated in GCOV_DIRECTORY. Basically, the path to the directory where the executable file is located is preferable.

```python
GCOV_DIRECTORY = 'your path'
```
Next, you can configure some behaviors of the fuzzer.

```python
# setting the target program timeout
TIMEOUT = 5

# list of arguments that will not be mutated
SKIP_ARGS = []

# for arithmetic inc or dec in mutation
INCREMENT_VALUE = 30
DECREMENT_VALUE = 30
```
## Preparing the seed file
Sets the seeds in text file. mini fuzzer generates diverse test cases by mutating seeds.
Describe the seeds as a list of string types corresponding to each command line argument of the target program.
```
["-O", "arg1", "arg2", "arg3"]
["-l", "arg4", "arg5"]
...
```
## Start fuzzing
Start fuzzing by running the command below. Info about detected crashes is stored in dump.csv.
```
$ python fuzz.py <Path to the executable file to be tested>　 <path to seed file>
```

# Dependencies
- Python 3.9 or greater
- Linux OS
- gcov (gcov is a code coverage analysis tool provided as part of GCC)
- Colorama (Python library)

# License
mini fuzzer is licensed under the [MIT license](https://github.com/yk0112/mini_fuzzer/blob/main/LICENSE).
