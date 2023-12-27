import ast
import queue
import random
import subprocess
import sys
import threading
import time
from typing import List

sys.path.append("../mini_fuzzer/mutation.py")
sys.path.append("../mini_fuzzer/monitor.py")

from monitor import Monitor
from mutation import bitflip

lock: threading.Lock = threading.Lock()


class Fuzzer:
    target: str
    seeds: queue.Queue[List[str]]
    testing_seed: List[str]
    rand: random.SystemRandom

    def __init__(self, target: str, seeds: queue.Queue) -> None:
        self.target = target
        self.seeds = seeds
        self.rand = random.SystemRandom()

    def do_fuzzing(self) -> int:
        seed = self.seeds.get()
        self.testing_seed = seed
        seed.insert(0, self.target)
        command = " ".join(seed)
        child_process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        
        status = child_process.returncode
        return status
    
    def mutation(self, s:str)->str:
        mutators = [
            bitflip
        ]
        mutator = random.choice(mutators)
        return mutator(s)
    
    def generate_fuzz(self) -> None:
        mutated_seed = []
        for s in self.testing_seed:
            mutated_seed.append(self.mutation(s))
        self.seeds.put(mutated_seed)


    def dump(self, status: int) -> None:
        fuzz_and_status = str(status) + "," + " ".join(self.testing_seed) + "\n"
        f = open("dump.csv", "a")
        f.write(fuzz_and_status)
        f.close()


def display_run_time(stop_event, monitor) -> None:
    while not stop_event.is_set():
        monitor.display()
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
    thread = threading.Thread(target=display_run_time, args=(stop_event, monitor))
    thread.start()

    try:
        while not fuzzer.seeds.empty():
            lock.acquire()
            monitor.cycles_done += 1
            lock.release()
            status = fuzzer.do_fuzzing()
            if status > 0:
                lock.acquire()
                monitor.uniqu_crash += 1
                monitor.last_crash_time = time.time()
                lock.release()
                monitor.display()

                if True:  # for test
                   fuzzer.generate_fuzz()
                fuzzer.dump(status)
    except KeyboardInterrupt:
        print("\033[10B\n")
        stop_event.set()


if __name__ == "__main__":
    main()
