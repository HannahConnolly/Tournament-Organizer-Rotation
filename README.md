# TO-Roles

Small utility to generate a rotating schedule of TOs (technical owners) for the next ~2 months.

The script in this repository generates a weekly TO schedule that falls on Wednesdays. It can read TOs from a file or accept them via the command line, and it can print the schedule to the terminal or write it to `TO_Rotation.txt`.

## Files

- `Roles.py` — main script. Generates the rotation and handles CLI flags.
- `TO_List.txt` — optional file listing TO names (one per line). Lines starting with `---` are ignored.
- `TO_Rotation.txt` — output file produced when using the `-f`/`--file` flag.

## Requirements

- Python 3.8+

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/HannahConnolly/Tournament-Organizer-Rotation.git
   cd Tournament-Organizer-Rotation
   ```

2. Ensure you have Python 3.8 or higher installed.

3. No external dependencies are required—this project uses only the Python standard library.

## Usage

Run the script from the project root.

### Basic Usage

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

### Advanced Options

- **`--days NUM`** — Set the rotation period length (default: 60 days). Example:

  ```bash
  python3 Roles.py --days 90
  ```

- **`--start-date YYYY-MM-DD`** — Specify a custom start date (default: today). Example:

  ```bash
  python3 Roles.py --start-date 2026-02-01
  ```

- **Combine options**:
  ```bash
  python3 Roles.py --tos Alice Bob Carol --days 90 --start-date 2026-02-01 -f
  ```

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

- Generate a 90-day rotation starting from a specific date:

```bash
python3 Roles.py --tos Alice Bob Carol --days 90 --start-date 2026-03-01 -f
```

- View a 3-month rotation for planning:

```bash
python3 Roles.py --days 90
```

## Troubleshooting

**Error: `TO_List.txt not found`**

- Ensure `TO_List.txt` exists in the project root, or use the `--tos` flag to provide TOs directly.

**Error: `Invalid start date format`**

- Use the `YYYY-MM-DD` format for `--start-date`. Example: `2026-02-15`

**No output or blank schedule**

- Check that `TO_List.txt` is not empty or that you provided TOs via `--tos`.
- Ensure you have at least one TO in the list.

## Contributing

Contributions are welcome! Feel free to:

- Report bugs or request features via GitHub issues
- Submit pull requests for improvements
- Improve documentation and examples

## License

[MIT License](/LICENSE)
