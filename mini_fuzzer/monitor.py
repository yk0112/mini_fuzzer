import sys
import time
from datetime import timedelta

from colorama import Fore, Style


class Monitor:
    start_time: float  # fuzzing開始時刻
    last_crash_time: float  # 最後にcrashを検出した時間
    cycles_done: int  # サイクル時間
    uniqu_crash: int  # 発見したcrash数
    line_coverage: int  # テストした行の割合
    exec_speed: float  # 1ステージの平均実行時間

    def __init__(self):
        self.start_time = time.time()
        self.last_crash_time = 0
        self.cycles_done = 0
        self.uniqu_crash = 0
        self.line_coverage = 0
        self.exec_speed = 0

    def update_last_crash_time(self, new_time: float):
        self.last_crash_time = new_time
        self.display()

    def update_cycles_done(self):
        self.cycles_done += 1
        self.display()

    def update_uniqu_crash(self):
        self.uniqu_crash += 1
        self.display()

    def update_line_coverage(self):
        self.line_coverage += 1
        self.display()

    def update_exec_speed(self, new_speed: int):
        self.exec_speed = new_speed
        self.display()

    def display(self):
        display_status(
            self.start_time,
            self.last_crash_time,
            self.cycles_done,
            self.uniqu_crash,
            self.line_coverage,
            self.exec_speed,
        )


def translate_time_format(base_time: float) -> str:
    delta = timedelta(seconds=time.time() - base_time)
    days, remainder = divmod(delta.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    formatted_time = (
        f"{int(days)} days, {int(hours)} hrs, {int(minutes)} min, {int(seconds)} sec"
    )
    return formatted_time


def display_status(
    start_time: float,
    last_crash_time: float,
    cycles_done: int,
    uniqu_crash: int,
    line_coverage: int,
    exec_speed: float,
) -> None:
    table_topline = (
        "+"
        + "-" * 20
        + f" {Fore.GREEN}mini fuzz 2.21.1{Style.RESET_ALL} "
        + "-" * 20
        + "+"
    )

    print(table_topline)

    item1_title = "run time"
    run_time = translate_time_format(start_time)
    item1_format = f"|{Fore.MAGENTA}{item1_title.rjust(20)}{Style.RESET_ALL} : {str(run_time).ljust(34)} |\n"
    print(item1_format, end="")

    item2_title = "last_crash_time"
    last_crash_time2 = translate_time_format(last_crash_time)
    item2_format = f"|{Fore.MAGENTA}{item2_title.rjust(20)}{Style.RESET_ALL} : {str(last_crash_time2).ljust(34)} |\n"
    print(item2_format, end="")

    item3_title = "cycles_done"
    item3_format = f"|{Fore.MAGENTA}{item3_title.rjust(20)}{Style.RESET_ALL} : {str(cycles_done).ljust(34)} | \n"
    print(item3_format, end="")

    item4_title = "uniqu_crash"
    item4_format = f"|{Fore.MAGENTA}{item4_title.rjust(20)}{Style.RESET_ALL} : {str(uniqu_crash).ljust(34)} | \n"
    print(item4_format, end="")

    item5_title = "line_coverage"
    item5_format = f"|{Fore.MAGENTA}{item5_title.rjust(20)}{Style.RESET_ALL} : {str(line_coverage).ljust(34)} | \n"
    print(item5_format, end="")

    item6_title = "exec_speed"
    exec_speed2 = str(exec_speed) + " sec"
    item6_format = f"|{Fore.MAGENTA}{item6_title.rjust(20)}{Style.RESET_ALL} : {exec_speed2.ljust(34)} | \n"
    print(item6_format, end="")

    table_bottomline = "+" + "-" * 58 + "+\033[8A"
    print(table_bottomline)


def display_run_time(
    stop_event,
    start_time,
    last_crash_time,
    cycles_done,
    uniqu_crash,
    line_coverage,
    exec_speed,
) -> None:
    start_time.value = time.time()
    try:
        while not stop_event.is_set():
            display_status(
                start_time.value,
                last_crash_time.value,
                cycles_done.value,
                uniqu_crash.value,
                line_coverage.value,
                exec_speed.value,
            )
            time.sleep(1)
    except KeyboardInterrupt:
        print("\033[10B\n" + "stop fuzzing")


if __name__ == "__main__":
    monitor = Monitor()
    monitor.display()
