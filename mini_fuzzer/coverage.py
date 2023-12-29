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


def get_line_coverage() -> dict[str, list[str]]:
    coverage = {}
    gcda_files = find_files(EX_DIRECTORY, "*.gcda")

    if not gcda_files:
        print("no gcda files")
        return coverage

    for file in gcda_files:
        command = "gcov " + file
        result = subprocess.run(
            command, shell=True, cwd=EX_DIRECTORY, text=True, capture_output=True
        )
        if result.returncode != 0:
            print("can not excute gcov command\n")
            sys.exit(1)

    gcov_files = find_files(EX_DIRECTORY, "*.cpp.gcov")

    for gcov_file in gcov_files:
        with open(gcov_file, "r") as file:
            all_line = 0
            line_coverage: list[int] = []
            for line in file:
                parts = line.split(":")
                executed_count = parts[0].strip()
                line_number = int(parts[1].strip())

                if line_number > 0:
                    all_line += 1
                    if executed_count != "#####":
                        print(line_number)
                        line_coverage.append(line_number)
            coverage[gcov_file] = line_coverage
    return coverage


# delete coverage info for next fuzzing
def clear_coverage_files() -> None:
    gcda_files = find_files(EX_DIRECTORY, "*.gcda")
    gcov_files = find_files(EX_DIRECTORY, "*.cpp.gcov")

    for file in gcda_files:
        os.remove(file)

    for file in gcov_files:
        os.remove(file)
