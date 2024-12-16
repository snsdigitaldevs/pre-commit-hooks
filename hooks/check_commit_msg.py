import argparse
import re
from typing import Sequence


class Colors:
    LBLUE = "\033[00;34m"
    LRED = "\033[01;31m"
    RESTORE = "\033[0m"
    YELLOW = "\033[00;33m"


RESULT_SUCCESS = 0
RESULT_FAIL = 1

TICKET_PREFIX = ["TO", "ECS", "P20E", "CRS"]

SPECIAL_PREFIX = ["Merge branch", "Revert"]

DEFAULT_COMMIT_TYPE = [
    "build",
    "chore",
    "ci",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "revert",
    "style",
    "test",
]

def validate_commit_message(commit_message, supported_types):
    ticket_pattern = r"((({}))-\d+|N/A)".format("|".join(TICKET_PREFIX))
    type_pattern = r"({})".format("|".join(supported_types))
    regex = re.compile(rf"^{ticket_pattern} {type_pattern}: [\s\S]+$")
    special_prefix_regex = re.compile(r"^({})".format("|".join(SPECIAL_PREFIX)))
    return (special_prefix_regex.match(commit_message) is not None) or (regex.match(commit_message) is not None)

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check-commit-msg", description="Checks commit message for Conventional Commits formatting."
    )
    parser.add_argument("types", type=str, nargs="*", default=DEFAULT_COMMIT_TYPE, help="Optional list of types to support")
    parser.add_argument("input", type=str, help="A file containing a git commit message")

    args = parser.parse_args(argv)

    try:
        with open(args.input, encoding="utf-8") as f:
            commit_message = f.read()
    except UnicodeDecodeError:
        print(f"""{Colors.LRED}[Bad Commit message encoding] {Colors.LRED}""")
        return RESULT_FAIL

    if not validate_commit_message(commit_message, args.types):
        print(
            f"""
            {Colors.LRED}Invalid commit message. Please follow this template:{Colors.LRED}

            ticket type: message (TO-123 feat: message)

            Ticket: {", ".join(TICKET_PREFIX)}
            Type: {", ".join(args.types)}
            """
        )
        return RESULT_FAIL
    return RESULT_SUCCESS

if __name__ == "__main__":
    raise SystemExit(main())
