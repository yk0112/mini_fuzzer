import fnmatch
import os
import subprocess
import sys

sys.path.append("../mini_fuzzer/config.py")
from config import EX_DIRECTORY


def find_files(directory: str, pattern: str) -> list[str]:
    matches = []
    for curdir, dirs, files in os.walk(directory):
        for file in fnmatch.filter(files, pattern):
            matches.append(os.path.join(curdir, file))
    return matches


def prepare_get_coverage() -> None:
    gcda_files = find_files(EX_DIRECTORY, "*.gcda")

    if not gcda_files:
        print("no gcda file")
        sys.exit(1)

    for file in gcda_files:
        command = "gcov " + file
        result = subprocess.run(
            command, shell=True, cwd=EX_DIRECTORY, text=True, capture_output=True
        )
        if result.returncode != 0:
            print("can not excute gcov command\n")
            sys.exit(1)

    gcov_files = find_files(EX_DIRECTORY, "*.cpp.gcov")
    
    if not gcov_files:
        print("no gcov file")
        sys.exit(1)



def get_total_line() -> dict[str, int]:
    result = {}
    gcov_files = find_files(EX_DIRECTORY, "*.cpp.gcov")

    for gcov_file in gcov_files:
        with open(gcov_file, "r") as file:
            line_count = 0
            source_file = ""
            for line in file:
                parts = line.split(":")
                line_number = int(parts[1].strip())
                if line_number == 0:
                    if parts[2] == "Source":
                        source_file = parts[3].strip()
                else:
                    line_count += 1
            result[source_file] = line_count
    return result


def get_executed_line() -> dict[str, int]:
    result = {}
    gcov_files = find_files(EX_DIRECTORY, "*.cpp.gcov")
   
    for gcov_file in gcov_files:
        with open(gcov_file, "r") as file:
            executed_line = 0
            source_file = ""
            for line in file:
                parts = line.split(":")
                executed_count = parts[0].strip()
                line_number = int(parts[1].strip())
                if line_number == 0 and parts[2] == "Source":
                    source_file = parts[3].strip()
                if line_number > 0 and executed_count != "#####":
                    executed_line += 1
            result[source_file] = executed_line
    return result



def calculate_coverage(total_line : dict[str,int], 
                       executed_line : dict[str,int]) -> float:
    total = 0
    executed = 0

    for file in total_line.keys():
        total += total_line[file]
        executed += executed_line[file]
    if total == 0:
        return 12.0
    return (executed / total) * 100



def calculate_coverage_perFile(total_line : dict[str,int], 
                               executed_line : dict[str,int]) -> dict[str,float]:
    persent = {}

    for file in total_line.keys():
        persent[file] = (executed_line[file] / total_line[file]) * 100
    return persent 


# delete coverage info for next fuzzing
def clear_coverage_files() -> None:
    gcda_files = find_files(EX_DIRECTORY, "*.gcda")
    gcov_files = find_files(EX_DIRECTORY, "*.cpp.gcov")

    for file in gcda_files:
        os.remove(file)

    for file in gcov_files:
        os.remove(file)
