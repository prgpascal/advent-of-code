import glob
import time
from os import system

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import argparse

TIME_THRESHOLD = 1000
ROOT_DIR = "."

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("year", type=str, help="Selected year", nargs="?", default="**")
arg_parser.add_argument("day", type=str, help="Selected day", nargs="?", default="**")
arg_parser.add_argument("--year", type=str, help="Selected year", default="**")
arg_parser.add_argument("--day", type=str, help="Selected day", default="**")
arg_parser.add_argument("--w", action="store_true", help="Run in watch mode")
args = arg_parser.parse_args()
year = args.year
day = args.day
watch = args.w

input_files = [f for f in glob.glob(f"{ROOT_DIR}/*{year}*/*{day}*/*.py")]
input_files.sort()

current_time = lambda: round(time.time() * 1000)
run_times = [current_time()]


def run_files():
    if len(input_files) > 0:
        for file in input_files:
            print(f"Running {file}")
            system(f"python {file}")
            print()
    else:
        print("No files found")


def on_file_change(event):
    if current_time() - run_times[-1] > TIME_THRESHOLD:
        run_times.append(current_time())
        run_files()


if __name__ == "__main__":
    system("clear")
    print(args, "\n")
    run_files()
    if watch:
        patterns = ["*.py"]
        ignore_patterns = ["*run.py*"]
        ignore_directories = False
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(
            patterns, ignore_patterns, ignore_directories, case_sensitive
        )
        my_event_handler.on_modified = on_file_change

        my_observer = Observer()
        my_observer.schedule(my_event_handler, ROOT_DIR, recursive=True)
        my_observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
