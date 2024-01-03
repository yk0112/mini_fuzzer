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
        print("\033[10B\n")
        print("no gcda file")
        sys.exit(1)

    for file in gcda_files:
        command = "gcov " + file
        result = subprocess.run(
            command, shell=True, cwd=EX_DIRECTORY, text=True, capture_output=True
        )
        if result.returncode != 0:
            print("\033[10B\n")
            print("can not excute gcov command\n")
            sys.exit(1)

    gcov_files = find_files(EX_DIRECTORY, "*.*.gcov")

    if not gcov_files:
        print("\033[10B\n")
        print("no gcov file")
        sys.exit(1)


def get_excutable_line() -> int:
    total_line = 0
    gcov_files = find_files(EX_DIRECTORY, "*.*.gcov")

    for gcov_file in gcov_files:
        with open(gcov_file, "r") as file:
            excutable_line = 0
            for line in file:
              parts = line.split(":")
              if len(parts) > 2:
                  executed_count = parts[0].strip()
                  if executed_count != "-":
                        excutable_line += 1
                
            total_line += excutable_line
    return total_line


def get_executed_line() -> int:
    total_line = 0
    gcov_files = find_files(EX_DIRECTORY, "*.*.gcov")

    for gcov_file in gcov_files:
        with open(gcov_file, "r") as file:
            executed_line = 0
            for line in file:
                parts = line.split(":")
                if len(parts) > 2:
                    executed_count = parts[0].strip()
                    if executed_count != "#####" and executed_count != "-":
                        executed_line += 1
            total_line += executed_line
    return total_line


# delete coverage info for next fuzzing
def clear_coverage_files() -> None:
    gcda_files = find_files(EX_DIRECTORY, "*.gcda")
    gcov_files = find_files(EX_DIRECTORY, "*.*.gcov")

    for file in gcda_files:
        os.remove(file)

    for file in gcov_files:
        os.remove(file)

