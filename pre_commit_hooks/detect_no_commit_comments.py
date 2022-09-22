from __future__ import annotations

import argparse
from typing import NamedTuple
from typing import Sequence
import re

NO_COMMIT_PATTERNS = (
    r"<<NOCOMMIT>>",
)

class BadFile(NamedTuple):
    filename: str
    pattern: str

def check_file_for_no_commit_pattern(filenames: Sequence[str])-> list[BadFile]:
    """Check if files contain patterns indicating debug code that shouldn't be
    committed.

    Return a list of all files containing no commit strings
    """
    bad_files = []

    for filename in filenames:
        for pattern in NO_COMMIT_PATTERNS:
            if re.findall(pattern, open(filename, 'r').read()):
                bad_files.append(BadFile(filename, pattern))
    return bad_files

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='Filenames to run')
    args = parser.parse_args(argv)

    bad_filenames = check_file_for_no_commit_pattern(args.filenames)
    if bad_filenames:
        for bad_file in bad_filenames:
            print(f'NOCOMMIT pattern found in {bad_file.filename}: {bad_file.pattern!r}')
        return 1
    else:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())