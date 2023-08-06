import os
from argparse import ArgumentParser
from contextlib import contextmanager
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen


@contextmanager
def working_directory(path):
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def run(cmd):
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    for line in p.stdout:
        print(line.decode().replace("\n", ""))


def download_huggingface_co(url, path=None):
    path = Path.cwd() if path is None else path
    with working_directory(path):
        run(cmd="git lfs install")
        print(f"Save data into {Path.cwd()}")
        run(cmd=f"git clone {url}")


def main():
    parser = ArgumentParser(
        "Download model from https://huggingface.co",
    )
    parser.add_argument(
        "--url",
        default=None,
        help="Download url from https://huggingface.co.",
    )
    parser.add_argument(
        "--path",
        default=None,
        help="Save path.",
    )

    args = parser.parse_args()

    download_huggingface_co(args.url, args.path)


if __name__ == "__main__":
    main()
