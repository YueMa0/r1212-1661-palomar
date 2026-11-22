# Where the files come from

## The Lean files

RamseyIncrement.lean and the 25 files in RamseyIncrement/ come from lean/ of [r1212-1661](https://github.com/YueMa0/r1212-1661) at commit 8709d47691c192c639a2f17bba5d0ef069b3edd8, which uses Lean 4.32.1 and Mathlib 520045ab. They were ported to Lean 4.35.0 and Mathlib v4.35.0 with the following changes, and no others.

**The module system** (every file). Palomar requires every Lean file to be a module:

- `module` is added before the imports;
- each `import` becomes `public import`;
- `@[expose] public section` is added after the imports, so that every declaration is public and every definition keeps its body visible to importing modules. The `decide +kernel` checks unfold definitions from other modules, so they need these bodies.

**Build order.** RamseyIncrement/R1212/H01Branch1.lean to H01Branch7.lean each import the previous branch module, and RamseyIncrement/R1661/Checks.lean imports H01Branch7. These imports are marked with the comment `-- Imported only so that Lake compiles the memory-heavy modules one at a time.` They add no mathematical dependency. Each of these nine modules needs 5–6 GB of memory to compile, and without the chain Lake compiles several of them at once, which exceeds 16 GB.

**One proof line.** In RamseyIncrement/R1212/Search.lean, the base case of `colourUnion_spec` was `by simp [colourUnion]`. With the newer Mathlib, `simp` leaves the goal `a ≤ a` with the two sides equal up to instances, so `; exact le_rfl` is added.

From r1212-1661 these files are not included: lean/AxiomAudit1661.lean and lean/Export1661.lean (Comparator now checks the axioms and the statement), lean/gen/, lean/tools/ and lean/audit/, and the colouring file and computer checks outside lean/.

To check these changes:

```bash
git clone https://github.com/YueMa0/r1212-1661 /tmp/r1212-1661
git -C /tmp/r1212-1661 checkout 8709d47691c192c639a2f17bba5d0ef069b3edd8
python3 scripts/compare_with_r1212_1661.py /tmp/r1212-1661
```

The script undoes the module-system changes and the build-order imports, compares every file with the original, and prints the remaining differences: only the line in Search.lean.

## Earlier origins

The files come, through r1212-1661, from these repositories (see the UPSTREAM.md of r1212-1661 and of r1212-1642):

- RamseyIncrement/Basic.lean, Cone.lean, RamseyNumber.lean, SpecialLift.lean and Transport.lean: Milos Tatarevic's [ramsey-increment-theorem](https://github.com/milostatarevic/ramsey-increment-theorem), commit 36c15eca0c601be7b7f33e30ee6890f395d2e1ea, under its MIT licence; the copyright notice is in LICENSE;
- RamseyIncrement/R1212/: [r1212-1642](https://github.com/YueMa0/r1212-1642) v1.0.0;
- RamseyIncrement/R1658/Defect.lean: [r1212-1658](https://github.com/YueMa0/r1212-1658);
- RamseyIncrement/R1661/ and RamseyIncrement.lean: new in r1212-1661.

## New in this repository

Challenge.lean, Solution.lean, comparator.json, formalization.yaml, lakefile.toml (in place of lakefile.lean), lean-toolchain, lake-manifest.json, scripts/, .github/workflows/ci.yml and README.md.
