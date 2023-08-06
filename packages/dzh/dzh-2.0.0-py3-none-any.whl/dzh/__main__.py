import argparse
import sys
from dzh.CLI import run_cli
from dzh.GUI import run_gui


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", action="store_true")
    return parser.parse_args(argv)


def main():
    args = parse_arguments(sys.argv[1:])
    run_cli() if args.cli else run_gui()


if __name__ == '__main__':
    main()
