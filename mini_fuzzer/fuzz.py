import random
import string
import subprocess
import sys


class Fuzzer:
    def __init__(self, target):
        self.target = target
        self.base = string.ascii_letters + string.digits
        self.rand = random.SystemRandom()

    def generate_fuzz(self):
        fuzz_length = self.rand.randint(1, 64)
        fuzz = random.choices(self.base, k=fuzz_length)
        fuzz = "".join(fuzz)
        return fuzz

    def do_fuzzing(self, fuzz):
        command = " ".join([self.target, fuzz])
        sys.stdout.write(command + "\n")
        child_process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        status = child_process.returncode
        return status

    def dump(self, fuzz, status):
        fuzz_and_status = str(status) + "," + fuzz + "\n"
        f = open("dump.csv", "a")
        f.write(fuzz_and_status)
        f.close()


def main():
    target = sys.argv[1]
    fuzzer = Fuzzer(target)

    fuzz_count = 0
    crashs = 0
    while crashs < 5:
        fuzz = fuzzer.generate_fuzz()
        fuzz_count += 1
        status = fuzzer.do_fuzzing(fuzz)
        if status > 0:
            crashs += 1
            fuzzer.dump(fuzz, status)
        sys.stdout.write("\r fuzz: %d, crashs: %d" % (fuzz_count, crashs))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
