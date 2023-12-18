import random
import string
import subprocess
import sys


class Fuzzer:
    target: str
    base: str
    rand: random.SystemRandom

    def __init__(self, target: str) -> None:
        self.target = target
        self.base = string.ascii_letters + string.digits
        self.rand = random.SystemRandom()

    def generate_fuzz(self) -> str:
        fuzz_length = self.rand.randint(1, 64)
        fuzz = random.choices(self.base, k=fuzz_length)
        fuzz = "".join(fuzz)
        return fuzz

    def do_fuzzing(self, fuzz: str) -> int:
        command = " ".join([self.target, fuzz])
        child_process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        status = child_process.returncode
        return status

    def dump(self, fuzz: str, status: int):
        fuzz_and_status = str(status) + "," + fuzz + "\n"
        f = open("dump.csv", "a")
        f.write(fuzz_and_status)
        f.close()


def main():
    target = sys.argv[1]
    fuzzer = Fuzzer(target)

    fuzz_count = 0
    crashs = 0
    while fuzz_count < 100:
        fuzz = fuzzer.generate_fuzz()
        fuzz_count += 1
        status = fuzzer.do_fuzzing(fuzz)
        if status > 0:
            crashs += 1
            fuzzer.dump(fuzz, status)

        sys.stdout.write("\r fuzz: %d, crashs: %d" % (fuzz_count, crashs))
        sys.stdout.flush()
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
