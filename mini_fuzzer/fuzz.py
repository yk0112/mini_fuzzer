import random
import string
import subprocess
import sys
import threading
import time

sys.path.append("../mini_fuzzer/monitor.py")
from monitor import display_status

### global variables ###
start_time: float = 0
last_crash_time: float = 0
cycles_done: int = 0
uniqu_crash: int = 0
line_coverage: int = 0
exec_speed: float = 0
lock: threading.Lock = threading.Lock()


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


def display_run_time(stop_event) -> None:
    if not stop_event.is_set():
        display_status(
            start_time,
            last_crash_time,
            cycles_done,
            uniqu_crash,
            line_coverage,
            exec_speed,
        )
        threading.Timer(1, display_run_time, [stop_event]).start()


def main():
    global start_time
    global last_crash_time
    global cycles_done
    global uniqu_crash
    global line_coverage
    global exec_speed

    target = sys.argv[1]
    fuzzer = Fuzzer(target)

    start_time = time.time()

    stop_event = threading.Event()
    display_run_time(stop_event)

    try:
        while True:
            fuzz = fuzzer.generate_fuzz()
            lock.acquire()
            cycles_done += 1
            lock.release()
            status = fuzzer.do_fuzzing(fuzz)
            if status > 0:
                lock.acquire()
                uniqu_crash += 1
                lock.release()

                display_status(
                    start_time,
                    last_crash_time,
                    cycles_done,
                    uniqu_crash,
                    line_coverage,
                    exec_speed,
                )

                fuzzer.dump(fuzz, status)
    except KeyboardInterrupt:
        print("\033[10B\n")
        stop_event.set()


if __name__ == "__main__":
    main()
