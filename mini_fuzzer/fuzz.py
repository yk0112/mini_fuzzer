import multiprocessing
import random
import string
import subprocess
import sys
from multiprocessing import Process, Value

sys.path.append("../mini_fuzzer/monitor.py")
from monitor import Monitor, display_run_time


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
    monitor = Monitor()
    fuzzer = Fuzzer(target)

    start_time = Value("f", monitor.start_time)
    last_crash_time = Value("f", monitor.last_crash_time)
    cycles_done = Value("i", monitor.cycles_done)
    uniqu_crash = Value("i", monitor.uniqu_crash)
    line_coverage = Value("i", monitor.line_coverage)
    exec_speed = Value("f", monitor.exec_speed)

    stop_event = multiprocessing.Event()

    process = Process(
        target=display_run_time,
        args=(
            stop_event,
            start_time,
            last_crash_time,
            cycles_done,
            uniqu_crash,
            line_coverage,
            exec_speed,
        ),
    )
    process.start()

    try:
        while monitor.cycles_done < 100:
            fuzz = fuzzer.generate_fuzz()
            monitor.cycles_done += 1
            status = fuzzer.do_fuzzing(fuzz)
            if status > 0:
                monitor.uniqu_crash += 1
                fuzzer.dump(fuzz, status)
        #    sys.stdout.write(
        #        "\r fuzz: %d, crashs: %d" % (monitor.cycles_done, monitor.uniqu_crash)
        #    )
        #    sys.stdout.flush()
        #  sys.stdout.write("\n")
    except KeyboardInterrupt:
        stop_event.set()
        process.join()


if __name__ == "__main__":
    main()
