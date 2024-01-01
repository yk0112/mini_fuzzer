import ast
import queue
import random
import subprocess
import sys
import threading
import time
from itertools import product

sys.path.append("../mini_fuzzer/mutation.py")
sys.path.append("../mini_fuzzer/monitor.py")
sys.path.append("../mini_fuzzer/coverage.py")
sys.path.append("../mini_fuzzer/config.py")

import coverage
import mutation
from config import SKIP_ARGS
from monitor import Monitor

lock: threading.Lock = threading.Lock()


class Fuzzer:
    target: str
    seeds: queue.Queue[list[str]]
    testing_seed: list[str]
    total_line: int
    executed_line: int
    before_executed_line : int
    isReady : bool
    rand: random.SystemRandom

    def __init__(self, target: str, seeds: queue.Queue) -> None:
        self.target = target
        self.seeds = seeds
        self.total_line = 0
        self.executed_line = 0
        self.before_executed_line = 0
        self.isReady = False
        self.rand = random.SystemRandom()
        
    def do_fuzzing(self) -> int:
        seed = self.seeds.get()
        self.testing_seed = seed[:]
        args = []
        for s in seed:
            arg = "'" + s + "'"
            args.append(arg)

        args.insert(0, self.target)
        command = " ".join(args)
        child_process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        
        if not self.isReady:
            coverage.prepare_get_coverage()
            self.total_line = coverage.get_total_line()
            self.isReady = True

        self.before_executed_line = self.executed_line
        self.executed_line = coverage.get_executed_line()
        
        status = child_process.returncode
        return status
    
    def mutation_fuzz(self) -> None:
        seed = self.testing_seed[:]
        
        mutators = [mutation.bitflip, mutation.byteflip, mutation.arithmetic_inc, 
                    mutation.arithmetic_dec, mutation.add_random_character, mutation.add_interesting_value,
                    mutation.delete_random_character]

        for mutator_combination in product(mutators, repeat=len(seed)):
            mutated = []
            index = 0
            for func, elem in zip(mutator_combination, seed):
                if index in SKIP_ARGS:
                    mutated.append(elem)
                else:
                    mutated.append(func(elem))
                index += 1
            self.seeds.put(mutated)

    
    def is_good_testcase(self) -> bool:
        if self.executed_line > self.before_executed_line:
            return True
        else:
            return False

    def dump(self, status: int) -> None:
        fuzz_and_status = str(status) + "," + " ".join(self.testing_seed) + "\n"
        f = open("dump.csv", "a")
        f.write(fuzz_and_status)
        f.close()


def display_run_time(stop_event, monitor) -> None:
    while not stop_event.is_set():
        lock.acquire()
        monitor.display()
        lock.release()
        time.sleep(1)


def main():
    target = sys.argv[1]
    seed_file = sys.argv[2]

    my_queue = queue.Queue()

    with open(seed_file, "r") as file:
        for line in file:
            list = ast.literal_eval(line.strip())
            my_queue.put(list)

    fuzzer = Fuzzer(target, my_queue)
    monitor = Monitor()

    stop_event = threading.Event()
    thread = threading.Thread(
        target=display_run_time, args=(stop_event, monitor), daemon=True
    )
    thread.start()

    try:
        while not fuzzer.seeds.empty():
            lock.acquire()
            monitor.change_cycles()
            lock.release()
            status = fuzzer.do_fuzzing()
            if status > 0:
                lock.acquire()
                monitor.change_crashes()
                lock.release()
                fuzzer.dump(status)
            
            if  True:    #fuzzer.is_good_testcase():
                lock.acquire()
                monitor.change_coverage(fuzzer.total_line, fuzzer.executed_line)
                lock.release()
                fuzzer.mutation_fuzz()
            
            lock.acquire()
            monitor.change_exec_speed()
            lock.release()
        print("\033[10B\n")
        stop_event.set()
    except KeyboardInterrupt:
        print("\033[10B\n")
        coverage.clear_coverage_files()
        stop_event.set()


if __name__ == "__main__":
    main()
