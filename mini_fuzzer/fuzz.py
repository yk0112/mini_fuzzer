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

import mutation
from monitor import Monitor

lock: threading.Lock = threading.Lock()


class Fuzzer:
    target: str
    seeds: queue.Queue[list[str]]
    testing_seed: list[str]
    rand: random.SystemRandom

    def __init__(self, target: str, seeds: queue.Queue) -> None:
        self.target = target
        self.seeds = seeds
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
        status = child_process.returncode
        return status
    
    def mutation_fuzz(self) -> None:
        seed = self.testing_seed[:]
        mutators = [mutation.delete_random_character]
        
        for mutator_combination in product(mutators, repeat=len(seed)):
            result = [func(elem) for func, elem in zip(mutator_combination, seed)]
            self.seeds.put(result)
    

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
    
    with open(seed_file, 'r') as file:
        for line in file:
            list = ast.literal_eval(line.strip())
            my_queue.put(list)

    fuzzer = Fuzzer(target, my_queue)
    monitor = Monitor()
    
    stop_event = threading.Event()
    thread = threading.Thread(target=display_run_time, args=(stop_event, monitor), daemon=True)
    thread.start()

    try:
        while not fuzzer.seeds.empty():
            lock.acquire()
            monitor.cycles_done += 1
            monitor.display()
            lock.release()
            status = fuzzer.do_fuzzing()
            if status > 0:
                lock.acquire()
                monitor.uniqu_crash += 1
                monitor.last_crash_time = time.time()
                monitor.display()
                lock.release()
                fuzzer.dump(status)
            else:
                fuzzer.dump(0) # for test
            if True:  # for test
               fuzzer.mutation_fuzz()

        print("\033[10B\n")
        stop_event.set()
    except KeyboardInterrupt:
        print("\033[10B\n")
        stop_event.set()


if __name__ == "__main__":
    main()
