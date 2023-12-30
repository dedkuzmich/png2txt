# Target platform: Windows 10 x64
# Requirements:     $ pip install -r requirements.txt

import sys
import os
import argparse
import glob
import subprocess
import pyperclip
import logging, verboselogs
import shutil
from colorama import Fore


verbose = False
os.environ["COLUMNS"] = "200"
base_dir = os.path.dirname(sys.executable)
output_dir = os.path.join(base_dir, "..\\output")
filename = os.path.basename(__file__).split(".")[0]
log = verboselogs.VerboseLogger(filename)


class ColorStreamHandler(logging.StreamHandler):
    def emit(self, record):
        msg = record.getMessage()
        color = Fore.RESET
        if record.levelno == logging.VERBOSE:
            if not verbose:  # If verbose mode is off, then messages will be ignored
                msg = None
        elif record.levelno == logging.NOTICE:
            color = Fore.LIGHTBLUE_EX
        elif record.levelno == logging.SUCCESS:
            color = Fore.GREEN
        elif record.levelno == logging.WARNING:
            color = Fore.YELLOW
        elif record.levelno == logging.ERROR:
            color = Fore.RED

            if verbose:  # If verbose mode is on, then callstack is printed
                (file_path, line_number, function_name, _) = log.findCaller()
                msg = "\n\nTraceback (most recent call last):\n" + \
                      f"  File {file_path}, line {line_number}, in {function_name}\n" + \
                      f"     raise log.error({msg})\n" + \
                      f"Exception: {msg}"
            else:
                msg = f"\n\n{msg}"

            print(color + msg + Fore.RESET)
            sys.exit(2023)

        if msg:
            if "\r" in msg:  # If line will be updated
                print(color + msg + Fore.RESET, end = "")
            else:
                print(color + msg + Fore.RESET)


def parse_cli_args():
    parser = argparse.ArgumentParser(description = "png2txt extracts a text from PNG file via Tesseract.")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Verbose mode.")
    parser.add_argument("-d", "--dir", type = str, default = "", help = "Path to directory that contains image file.")
    parser.add_argument("-f", "--file", type = str, default = "", help = "Name of PNG image which contains the text.")
    parser.add_argument("-l", "--language", type = str, default = "ukr+eng", help = "Language(s) which are represented in PNG.")
    args = parser.parse_args()
    return args


def get_dir(dir):
    """Gets full path to directory"""

    work_dir = dir
    if not work_dir:
        sharex_dir = "C:\\Users\\lol19\\Pictures\\ShareX"
        dirs = glob.glob(f"{sharex_dir}\\*\\")

        # Delete png2txt dir from search results
        png2txt_dir = f"{sharex_dir}\\png2txt\\"
        dirs = [d for d in dirs if d != png2txt_dir]

        if not dirs:
            log.error(f"Directory {sharex_dir} doesn't contain any directories!")
        work_dir = max(dirs, key = os.path.getmtime)  # The latest modified dir

    if not os.path.isdir(work_dir):  # Check
        log.error(f"Directory {work_dir} doesn't exist!")

    return work_dir


def get_png(work_dir, file):
    """Gets full path to PNG file"""

    png = f"{work_dir}\\{file}"
    if file:
        if ".png" not in file:
            log.error(f"File must be PNG!")
    else:  # Get the last PNG in dir
        images = glob.glob(f"{work_dir}\\*.png")
        if not images:
            log.error(f"Directory {work_dir} doesn't contain any PNG file!")
        png = max(images, key = os.path.getctime)  # The latest created file

    if not os.path.isfile(png):  # Check
        log.error(f"PNG file {png} doesn't exist!")

    return png


def extract_text(png, language):
    """Uses tesseract to extract the text from PNG file"""

    output_base = "extracted"
    subprocess.run(["tesseract.exe", png, output_base, "-l", language])

    txt = f"{output_dir}\\{output_base}.txt"
    shutil.move(f"{output_base}.txt", txt)
    if not os.path.isfile(txt):
        log.error(f"TXT file {txt} hasn't been created!")
    log.verbose(f"Extracted text has been written to {txt}")

    text = ""
    with open(txt, "r", encoding = "utf-8") as fin:
        text = fin.read()
    if not text:
        log.error(f"TXT file {txt} is empty")

    return text


def work(dir, file, language):
    log.verbose(f"Provided directory: {dir}")
    log.verbose(f"Provided PNG file: {file}")
    log.verbose(f"Provided language: {language}")

    work_dir = get_dir(dir)
    png = get_png(work_dir, file)
    log.info(f"Full path to PNG: {png}")

    text = extract_text(png, language)
    log.success(f"[+] Extracted text ({language}):")
    log.info(text)
    pyperclip.copy(text)


def main():
    global verbose
    args = parse_cli_args()
    verbose = args.verbose
    dir = args.dir
    file = args.file
    language = args.language

    # Create output directory
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass
    except Exception as e:
        log.error(f"Output directory {output_dir} cannot be created. Error: {e}")

    # Save all the log to log file
    file_handler = logging.FileHandler(f"{output_dir}\\{filename}.log", mode = "w", encoding = "utf-8")
    file_handler.setLevel(logging.NOTICE)

    stream_handler = ColorStreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)

    # Format: time, severity level, number of line, message
    logging.basicConfig(handlers = [file_handler, stream_handler],
                        format = "%(asctime)s\t%(levelname)s\t\tline: %(lineno)d\t\t%(message)s",
                        datefmt = "%H:%M:%S",
                        level = logging.DEBUG)

    work(dir, file, language)
    sys.exit(0)


if __name__ == "__main__":
    # Simulation of CLI arguments. For debug only
    # dir = "C:\\Users\\lol19\\Pictures\\Screenshots"
    # file = "WINWORD_FnT0p6PW9m.png"
    # language = "ukr+eng"

    # sys.argv = ["png2txt.py"]
    # sys.argv = ["png2txt.py", "-v"]
    # sys.argv = ["png2txt.py", "-v", "-d", dir]
    # sys.argv = ["png2txt.py", "-v", "-f", file]
    # sys.argv = ["png2txt.py", "-v", "-d", dir, "-f", file]
    # sys.argv = ["png2txt.py", "-v", "-d", dir, "-f", file, "-l", language]
    # sys.argv = ["png2txt.py", "-h"]

    # python png2txt.py
    # python png2txt.py -v -d "" -f "" -l ""

    main()
