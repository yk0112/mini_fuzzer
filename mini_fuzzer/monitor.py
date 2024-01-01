import time
from datetime import timedelta

from colorama import Fore, Style


class Monitor:
    start_time: float
    last_crash_time: float
    cycles_done: int
    crashes: int
    coverage : float
    exec_speed: float

    def __init__(self) -> None:
        self.start_time = time.time()
        self.last_crash_time = time.time()
        self.cycles_done = 0
        self.crashes = 0
        self.coverage = 0
        self.exec_speed = 0
    
    def change_cycles(self) -> None:
        self.cycles_done += 1
        self.display()

    def change_crashes(self) -> None:
        self.crashes += 1
        self.last_crash_time = time.time()
        self.display()

    def change_coverage(self, total_line : int, executed_line : int) -> None:
        self.coverage = (executed_line / total_line) * 100
        self.display()
      
    def change_exec_speed(self) -> None:
        self.exec_speed = (time.time() - self.start_time) / self.cycles_done
        self.display()

        
    def display(self) -> None:
        width = 62

        table_topline = (
            "+"
            + "-" * 22
            + f" {Fore.GREEN}mini fuzz 2.21.1{Style.RESET_ALL} "
            + "-" * 22
            + "+"
        )

        print(table_topline)
        
        key_length = 16
        value_length = width - key_length - 3

        item1_title = "run time".rjust(key_length)
        formtatted_run_time = f"{translate_time_format(self.start_time)}".ljust(value_length)
        item1 = f"|{Fore.MAGENTA}{item1_title}{Style.RESET_ALL} : {formtatted_run_time}|\n"
        print(item1, end="", flush=True)

        item2_title = "last_crash_time".rjust(key_length)
        formatted_crash_time = f"{translate_time_format(self.last_crash_time)}".ljust(value_length)
        item2 = f"|{Fore.MAGENTA}{item2_title}{Style.RESET_ALL} : {formatted_crash_time}|\n"
        print(item2, end="", flush=True)

        item3_title = "cycles_done".rjust(key_length)
        formatted_cycles = f"{self.cycles_done}".ljust(value_length)
        item3 = f"|{Fore.MAGENTA}{item3_title}{Style.RESET_ALL} : {formatted_cycles}|\n"
        print(item3, end="", flush=True)

        item4_title = "crashs".rjust(key_length)
        formatted_crashs = f"{self.crashes}".ljust(value_length)
        item4 = f"|{Fore.MAGENTA}{item4_title}{Style.RESET_ALL} : {formatted_crashs}|\n"
        print(item4, end="", flush=True)

        item5_title = "line_coverage"
        formatted_coverage =  f"{self.coverage:.2f}%".ljust(value_length)
        item5 = f"|{Fore.MAGENTA}{item5_title.rjust(key_length)}{Style.RESET_ALL} : {formatted_coverage}|\n"
        print(item5, end="", flush=True)
        
        item6_title = "exec_speed"
        formatted_exec = f"{self.exec_speed:.2f} sec".ljust(value_length)
        item6 = f"|{Fore.MAGENTA}{item6_title.rjust(key_length)}{Style.RESET_ALL} : {formatted_exec}|\n"
        print(item6, end="", flush=True)
        
        line_up = 8
        table_bottomline = "+" + "-" * width + f"+\033[{line_up}A" + "+" 
        print(table_bottomline, flush=True)
   

def translate_time_format(base_time: float) -> str:
    delta = timedelta(seconds=time.time() - base_time)
    days, remainder = divmod(delta.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    formatted_time = f"{int(days)} days, {int(hours)} hrs, {int(minutes)} min, {int(seconds)} sec"
    return formatted_time
    

