# This script accepts a list of TOs that will be in rotation for the next 2 months of Cycles

import argparse
from datetime import datetime, timedelta


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Manage TO rotation for the next 2 months of Cycles."
    )
    parser.add_argument(
        "--tos",
        nargs="+",
        required=False,
        help="List of TOs to be included in the rotation.",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store_true",
        help="Print to file instead of terminal.",
    )
    return parser.parse_args()


def parse_file():
    with open("TO_List.txt", "r") as file:
        tos = [
            line.strip() for line in file if line.strip() and not line.startswith("---")
        ]
    return tos


def generate_rotation(tos):
    rotation = []
    start_date = datetime.now()
    end_date = start_date + timedelta(days=60)

    # Find the first Wednesday
    current_date = start_date
    while current_date.weekday() != 2:  # 2 represents Wednesday (0 is Monday)
        current_date += timedelta(days=1)

    to_index = 0

    while current_date < end_date:
        rotation.append((current_date.strftime("%Y-%m-%d"), tos[to_index]))
        current_date += timedelta(days=7)  # Weekly rotation on Wednesdays
        to_index = (to_index + 1) % len(tos)

    return rotation


def print_to_file(tos):
    print("Printing to TO_Rotation.txt...\n")
    with open("TO_Rotation.txt", "w") as file:
        TO_two = tos[-1][1] if len(tos) > 1 else "N/A"

        for date, TO_one in tos:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%b %d")
            file.write(f"# {formatted_date}\n")
            file.write(f"TO 1: {TO_one}\n")
            file.write(f"TO 2: {TO_two}\n\n")
            TO_two = TO_one


def print_to_terminal(tos):
    print("Printing to terminal...\n")
    TO_two = tos[-1][1] if len(tos) > 1 else "N/A"

    for date, TO_one in tos:
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%b %d")
        print(f"# {formatted_date}")
        print(f"TO 1: {TO_one}")
        print(f"TO 2: {TO_two}\n")
        TO_two = TO_one


def main():
    args = parse_arguments()
    tos = args.tos

    if not tos:
        print("Parsing TOs from file...\n")
        tos = parse_file()
        if not tos:
            print("No TOs found in the file. Exiting.")
            return

    rotation = generate_rotation(tos)

    print_to_file(rotation) if args.file else print_to_terminal(rotation)

    print("Done.")


if __name__ == "__main__":
    main()
