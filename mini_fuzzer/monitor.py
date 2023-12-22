import time
from datetime import timedelta

from colorama import Fore, Style


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
    print(item1_format, end="", flush=True)

    item2_title = "last_crash_time"
    last_crash_time2 = translate_time_format(last_crash_time)
    item2_format = f"|{Fore.MAGENTA}{item2_title.rjust(20)}{Style.RESET_ALL} : {str(last_crash_time2).ljust(34)} |\n"
    print(item2_format, end="", flush=True)

    item3_title = "cycles_done"
    item3_format = f"|{Fore.MAGENTA}{item3_title.rjust(20)}{Style.RESET_ALL} : {str(cycles_done).ljust(34)} | \n"
    print(item3_format, end="", flush=True)

    item4_title = "uniqu_crash"
    item4_format = f"|{Fore.MAGENTA}{item4_title.rjust(20)}{Style.RESET_ALL} : {str(uniqu_crash).ljust(34)} | \n"
    print(item4_format, end="", flush=True)

    item5_title = "line_coverage"
    item5_format = f"|{Fore.MAGENTA}{item5_title.rjust(20)}{Style.RESET_ALL} : {str(line_coverage).ljust(34)} | \n"
    print(item5_format, end="", flush=True)

    item6_title = "exec_speed"
    exec_speed2 = str(exec_speed) + " sec"
    item6_format = f"|{Fore.MAGENTA}{item6_title.rjust(20)}{Style.RESET_ALL} : {exec_speed2.ljust(34)} | \n"
    print(item6_format, end="", flush=True)

    table_bottomline = "+" + "-" * 58 + "+\033[8A"
    print(table_bottomline, flush=True)
