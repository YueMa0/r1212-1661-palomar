#!/usr/bin/env bash
# Run `lake comparator` on Challenge.lean and Solution.lean as Palomar does: with the tools that
# ship in the toolchain named by lean-toolchain, and with the toolchain's independent kernels
# (nanoda and con-ron) registered as external kernels. Palomar ignores `enable_nanoda` and sets
# the external kernels itself, so this script does the same in a temporary copy of the config.
# On Linux the build runs inside a bubblewrap sandbox; elsewhere pass --no-sandbox.
set -euo pipefail
cd "$(dirname "$0")/.."
extra=()
if [ "${1:-}" = "--no-sandbox" ]; then extra=(--inadvisably-no-sandbox); fi
prefix=$(lean --print-prefix)
for tool in lake leanexport leanchecker nanoda_bin con-ron; do
  [ -x "$prefix/bin/$tool" ] || { echo "error: the toolchain does not bundle $tool" >&2; exit 1; }
done
config=$(mktemp "${TMPDIR:-/tmp}/comparator.XXXXXX")
trap 'rm -f "$config"' EXIT
python3 - comparator.json "$config" "$prefix" <<'PY'
import json, pathlib, sys
src, dst, prefix = sys.argv[1:]
cfg = json.loads(pathlib.Path(src).read_text(encoding='utf-8'))
cfg.pop('enable_nanoda', None)
cfg['external_kernels'] = {'nanoda': [f'{prefix}/bin/nanoda_bin'], 'con-ron': [f'{prefix}/bin/con-ron']}
pathlib.Path(dst).write_text(json.dumps(cfg, indent=2) + '\n', encoding='utf-8')
PY
lake exe cache get
lake comparator --config "$config" ${extra[@]+"${extra[@]}"}
