#!/usr/bin/env python3
"""Check Palomar's source rules: every .lean file outside .git and .lake starts with the
`module` header (comments may precede it) and has at most 10,000 lines; Challenge.lean has at
most 1,000 lines and 100 KiB; no .lean file is a symbolic link."""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
failures = []
for path in sorted(root.rglob('*.lean')):
    rel = path.relative_to(root)
    if rel.parts[0] in ('.git', '.lake'):
        continue
    if path.is_symlink():
        failures.append(f'{rel}: symbolic link')
        continue
    data = path.read_bytes()
    lines = data.count(b'\n') + (1 if data and not data.endswith(b'\n') else 0)
    if lines > 10000:
        failures.append(f'{rel}: {lines} lines (limit 10,000)')
    if rel.name == 'lakefile.lean':
        continue
    text = re.sub(r'/-.*?-/', '', data.decode('utf-8'), flags=re.S)
    code = [l for l in text.splitlines() if l.strip() and not l.strip().startswith('--')]
    if not code or code[0].strip() != 'module':
        failures.append(f'{rel}: does not start with the `module` header')
challenge = root / 'Challenge.lean'
size = challenge.stat().st_size
nlines = challenge.read_bytes().count(b'\n')
if nlines > 1000 or size > 100 * 1024:
    failures.append(f'Challenge.lean: {nlines} lines, {size} bytes (limits 1,000 lines, 100 KiB)')
for f in failures:
    print('FAIL', f)
print('CHECK:', 'FAIL' if failures else 'PASS')
sys.exit(1 if failures else 0)
