import time
from datetime import timedelta

from colorama import Fore, Style


class Monitor:
    start_time: float
    last_crash_time: float
    cycles_done: int
    uniqu_crash: int
    line_coverage: int
    exec_speed: float

    def __init__(self) -> None:
        self.start_time = time.time()
        self.last_crash_time = time.time()
        self.cycles_done: int = 0
        self.uniqu_crash: int = 0
        self.line_coverage: int = 0
        self.exec_speed: float = 0

    def translate_time_format(self, base_time: float) -> str:
        delta = timedelta(seconds=time.time() - base_time)
        days, remainder = divmod(delta.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        formatted_time = f"{int(days)} days, {int(hours)} hrs, {int(minutes)} min, {int(seconds)} sec"
        return formatted_time

    def display(self) -> None:
        table_topline = (
            "+"
            + "-" * 20
            + f" {Fore.GREEN}mini fuzz 2.21.1{Style.RESET_ALL} "
            + "-" * 20
            + "+"
        )

        print(table_topline)

        item1_title = "run time"
        run_time = self.translate_time_format(self.start_time)
        item1 = f"|{Fore.MAGENTA}{item1_title.rjust(20)}{Style.RESET_ALL} : {str(run_time).ljust(34)} |\n"
        print(item1, end="", flush=True)

        item2_title = "last_crash_time"
        last_crash_time2 = self.translate_time_format(self.last_crash_time)
        item2 = f"|{Fore.MAGENTA}{item2_title.rjust(20)}{Style.RESET_ALL} : {str(last_crash_time2).ljust(34)} |\n"
        print(item2, end="", flush=True)

        item3_title = "cycles_done"
        item3 = f"|{Fore.MAGENTA}{item3_title.rjust(20)}{Style.RESET_ALL} : {str(self.cycles_done).ljust(34)} | \n"
        print(item3, end="", flush=True)

        item4_title = "uniqu_crash"
        item4 = f"|{Fore.MAGENTA}{item4_title.rjust(20)}{Style.RESET_ALL} : {str(self.uniqu_crash).ljust(34)} | \n"
        print(item4, end="", flush=True)

        item5_title = "line_coverage"
        item5 = f"|{Fore.MAGENTA}{item5_title.rjust(20)}{Style.RESET_ALL} : {str(self.line_coverage).ljust(34)} | \n"
        print(item5, end="", flush=True)

        item6_title = "exec_speed"
        exec_speed2 = str(self.exec_speed) + " sec"
        item6 = f"|{Fore.MAGENTA}{item6_title.rjust(20)}{Style.RESET_ALL} : {exec_speed2.ljust(34)} | \n"
        print(item6, end="", flush=True)

        table_bottomline = "+" + "-" * 58 + "+\033[8A"
        print(table_bottomline, flush=True)
