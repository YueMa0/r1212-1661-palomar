#!/usr/bin/env python3
"""Compare the Lean files here with lean/ of an r1212-1661 checkout (commit
8709d47691c192c639a2f17bba5d0ef069b3edd8).

Before comparing, the changes made for the module system are undone: the `module` line, the
`public` in `public import`, the `@[expose] public section` line, the blank lines added with
them, and the build-order imports marked with BUILD_ORDER_MARK. Every file should then be
identical to the original, except the proof changes listed in UPSTREAM.md, which are printed as
a diff.

usage: compare_with_r1212_1661.py /path/to/r1212-1661
"""
import difflib
import pathlib
import sys

BUILD_ORDER_MARK = '-- Imported only so that Lake compiles the memory-heavy modules one at a time.'


def undo_port(text):
    lines = text.split('\n')
    out = []
    skip_next_import = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == 'module':
            i += 2 if i + 1 < len(lines) and lines[i + 1] == '' else 1
            continue
        if line == '' and i + 1 < len(lines) and lines[i + 1] == '@[expose] public section':
            i += 2
            continue
        if line == BUILD_ORDER_MARK:
            skip_next_import = True
            i += 1
            continue
        if skip_next_import and line.startswith('public import '):
            skip_next_import = False
            i += 1
            continue
        if line.startswith('public import '):
            line = line[len('public '):]
        out.append(line)
        i += 1
    return '\n'.join(out)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    here = pathlib.Path(__file__).resolve().parent.parent
    original = pathlib.Path(sys.argv[1]) / 'lean'
    files = sorted(p.relative_to(here) for p in here.joinpath('RamseyIncrement').rglob('*.lean'))
    files.append(pathlib.Path('RamseyIncrement.lean'))
    same, changed = 0, []
    for rel in files:
        ported = undo_port((here / rel).read_text(encoding='utf-8'))
        orig = (original / rel).read_text(encoding='utf-8')
        if ported == orig:
            same += 1
        else:
            changed.append(rel)
            sys.stdout.writelines(difflib.unified_diff(
                orig.splitlines(keepends=True), ported.splitlines(keepends=True),
                f'r1212-1661/lean/{rel}', f'{rel} (port, module-system changes undone)'))
    print(f'{same} of {len(files)} files identical to r1212-1661 after undoing the module-system '
          f'changes; changed: {", ".join(map(str, changed)) or "none"}')


main()
