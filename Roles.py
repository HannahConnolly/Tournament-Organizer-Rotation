# This script accepts a list of TOs that will be in rotation for the next 2 months of Cycles

import argparse
import csv
import sys
from datetime import datetime, timedelta
from typing import List, Tuple


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for TO rotation schedule generation."""
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
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Export rotation to CSV file (TO_Rotation.csv).",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=60,
        help="Number of days for the rotation schedule (default: 60).",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="Start date for the rotation (YYYY-MM-DD format). Default is today.",
    )
    return parser.parse_args()


def parse_file() -> List[str]:
    """Read TO names from TO_List.txt file.

    Returns:
        List[str]: List of TO names, with empty lines and lines starting with '---' filtered out.

    Raises:
        FileNotFoundError: If TO_List.txt does not exist.
    """
    try:
        with open("TO_List.txt", "r") as file:
            tos = [
                line.strip()
                for line in file
                if line.strip() and not line.startswith("---")
            ]
        return tos
    except FileNotFoundError:
        print("Error: TO_List.txt not found. Please create the file or use --tos flag.")
        sys.exit(1)


def generate_rotation(
    tos: List[str], num_days: int = 60, start_date: datetime | None = None
) -> List[Tuple[str, str]]:
    """Generate a weekly TO rotation schedule on Wednesdays.

    Args:
        tos (List[str]): List of TO names to rotate.
        num_days (int): Number of days for the rotation (default: 60).
        start_date (datetime | None): Start date for the rotation. Default is today.

    Returns:
        List[Tuple[str, str]]: List of (date, TO_name) tuples for each Wednesday in the rotation period.

    Raises:
        ValueError: If the tos list is empty or contains empty strings.
    """
    if not tos:
        raise ValueError("TO list cannot be empty.")

    tos = [to.strip() for to in tos]
    if any(not to for to in tos):
        raise ValueError("TO names cannot be empty strings.")

    rotation = []
    if start_date is None:
        start_date = datetime.now()
    end_date = start_date + timedelta(days=num_days)

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


def print_to_file(tos: List[Tuple[str, str]]) -> None:
    """Write the TO rotation schedule to TO_Rotation.txt.

    Args:
        tos (List[Tuple[str, str]]): List of (date, TO_name) tuples from generate_rotation().
    """
    print("Printing to TO_Rotation.txt...\n")
    with open("TO_Rotation.txt", "w") as file:
        TO_two = tos[-1][1] if len(tos) > 1 else "N/A"

        for date, TO_one in tos:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%b %d")
            file.write(f"# {formatted_date}\n")
            file.write(f"TO 1: {TO_one}\n")
            file.write(f"TO 2: {TO_two}\n\n")
            TO_two = TO_one


def print_to_terminal(tos: List[Tuple[str, str]]) -> None:
    """Print the TO rotation schedule to the terminal.

    Args:
        tos (List[Tuple[str, str]]): List of (date, TO_name) tuples from generate_rotation().
    """
    print("Printing to terminal...\n")
    TO_two = tos[-1][1] if len(tos) > 1 else "N/A"

    for date, TO_one in tos:
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%b %d")
        print(f"# {formatted_date}")
        print(f"TO 1: {TO_one}")
        print(f"TO 2: {TO_two}\n")
        TO_two = TO_one


def export_to_csv(tos: List[Tuple[str, str]]) -> None:
    """Export the TO rotation schedule to a CSV file.

    Args:
        tos (List[Tuple[str, str]]): List of (date, TO_name) tuples from generate_rotation().
    """
    print("Exporting to TO_Rotation.csv...\n")
    with open("TO_Rotation.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "TO 1", "TO 2"])

        TO_two = tos[-1][1] if len(tos) > 1 else "N/A"

        for date, TO_one in tos:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%b %d")
            writer.writerow([formatted_date, TO_one, TO_two])
            TO_two = TO_one


def main() -> None:
    """Main entry point for the TO rotation schedule generator."""
    args = parse_arguments()
    tos = args.tos

    if not tos:
        print("Parsing TOs from file...\n")
        tos = parse_file()
        if not tos:
            print("No TOs found in the file. Exiting.")
            return

    start_date = None
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid start date format. Please use YYYY-MM-DD format.")
            sys.exit(1)

    try:
        rotation = generate_rotation(tos, num_days=args.days, start_date=start_date)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.csv:
        export_to_csv(rotation)
    elif args.file:
        print_to_file(rotation)
    else:
        print_to_terminal(rotation)

    print("Done.")


if __name__ == "__main__":
    main()
