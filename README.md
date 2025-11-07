# TO-Roles

Small utility to generate a rotating schedule of TOs (technical owners) for the next ~2 months.

The script in this repository generates a weekly TO schedule that falls on Wednesdays. It can read TOs from a file or accept them via the command line, and it can print the schedule to the terminal or write it to `TO_Rotation.txt`.

## Files

- `Roles.py` — main script. Generates the rotation and handles CLI flags.
- `TO_List.txt` — optional file listing TO names (one per line). Lines starting with `---` are ignored.
- `TO_Rotation.txt` — output file produced when using the `-f`/`--file` flag.

## Requirements

- Python 3.8+

## Usage

Run the script from the project root.

- Print rotation to the terminal (default):

```bash
python3 Roles.py
```

- Provide TOs directly on the command line:

```bash
python3 Roles.py --tos Alice Bob Carol
```

- Write rotation to `TO_Rotation.txt` instead of printing:

```bash
python3 Roles.py -f
# or
python3 Roles.py --file
```

If you don't pass `--tos`, the script will read `TO_List.txt` from the project root.

## `TO_List.txt` format

Put one TO name per line. Empty lines and lines that start with `---` are ignored. Example:

```
Alice
Bob
Carol
---
# comments or separators
Dave
```

## Rotation rules

- The rotation starts from the next Wednesday (the script finds the next Wednesday from the current date).
- The script generates weekly assignments (every 7 days) for the next ~60 days (two months).
- The printed/written schedule shows `TO 1` as the primary assigned TO for that week and `TO 2` is a rolling previous TO (useful for backup/hand-off context).

## Examples

- Generate and print schedule using `TO_List.txt`:

```bash
python3 Roles.py
```

- Generate schedule from inline list and save to file:

```bash
python3 Roles.py --tos Alice Bob Carol -f
```

## License

[MIT License](/LICENSE)
