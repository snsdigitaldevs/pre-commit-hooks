import argparse
import re
import sys
from typing import Sequence, List


class Colors:
    LBLUE = "\033[00;34m"
    LRED = "\033[01;31m"
    RESTORE = "\033[0m"
    YELLOW = "\033[00;33m"


RESULT_SUCCESS = 0
RESULT_FAIL = 1

SPECIAL_PREFIX = ["Merge branch", "Revert"]

DEFAULT_TICKET_PREFIX = ["TO", "P20E"]

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

def validate_commit_message(commit_message: str, supported_types: List[str], ticket_prefixes: List[str]):
    ticket_pattern = r"((({}))-\d+|N/A)".format("|".join(ticket_prefixes))
    type_pattern = r"({})".format("|".join(supported_types))
    regex = re.compile(rf"^{ticket_pattern} {type_pattern}: [\s\S]+$")
    special_prefix_regex = re.compile(r"^({})".format("|".join(SPECIAL_PREFIX)))
    return (special_prefix_regex.match(commit_message) is not None) or (regex.match(commit_message) is not None)

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check-commit-msg", description="Checks commit message for Conventional Commits formatting."
    )
    
    # read git commit message
    actual_argv = argv if argv is not None else sys.argv[1:]
    if not actual_argv:
        print(f"{Colors.LRED}Error: No arguments received.{Colors.RESTORE}")
        return RESULT_FAIL
    commit_file_path = actual_argv[-1]
    try:
        with open(commit_file_path, encoding="utf-8") as f:
            commit_message = f.read()
    except UnicodeDecodeError:
        print(f"""{Colors.LRED}[Bad Commit message encoding] {Colors.LRED}""")
        return RESULT_FAIL
    
    # read config.yaml args
    args_to_parse = actual_argv[:-1]
    parser.add_argument(
        "--commit-type", 
        dest="types", 
        type=str, 
        nargs="+", 
        default=DEFAULT_COMMIT_TYPE, 
        help="Optional list of types to support"
    )
    parser.add_argument(
        "--ticket-prefix", 
        dest="prefixes", 
        type=str, 
        nargs="+", 
        default=DEFAULT_TICKET_PREFIX, 
        help="Optional list of ticket prefixes to support"
    )

    args = parser.parse_args(args_to_parse)
    if not validate_commit_message(commit_message, args.types, args.prefixes):
        print(
            f"""
            {Colors.LRED}Invalid commit message. Please follow this template:{Colors.LRED}

            ticket type: message (TO-123 feat: message)

            Ticket: {", ".join(args.prefixes)}
            Type: {", ".join(args.types)}
            """
        )
        return RESULT_FAIL
    return RESULT_SUCCESS

if __name__ == "__main__":
    raise SystemExit(main())
