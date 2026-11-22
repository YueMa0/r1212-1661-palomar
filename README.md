# R(12,12) ≥ 1661: the Lean proof, prepared for Palomar

This repository contains a Lean 4 proof that the diagonal Ramsey number R(12,12) is at least 1661, in the form required by the [Palomar registry](https://palomar-registry.org) of Lean-verified mathematics.

```lean
theorem R1212.lower_bound_1661 :
    ∃ G : SimpleGraph (Fin 1660), G.CliqueFree 12 ∧ Gᶜ.CliqueFree 12
```

There is a simple graph on 1660 vertices such that neither the graph nor its complement contains a clique on 12 vertices. Colouring the edges of the graph red and the other edges of K₁₆₆₀ blue gives a red/blue colouring of K₁₆₆₀ with no monochromatic K₁₂, so R(12,12) ≥ 1661.

- **The paper.** The construction and the proof are described in *R(12,12) ≥ 1661 by extending the Mathon–Shearer coloring* by Yue Ma, [hexagon:2611.00248](https://hexagonmath.org/2611.00248).
- **The original repository.** [r1212-1661](https://github.com/YueMa0/r1212-1661) contains the colouring as a file, the computer checks (two independent exhaustive searches), and the original Lean proof in Lean 4.32.1. This repository is a port of its Lean proof to Lean 4.35.0 and Lean's module system, which Palomar requires; [UPSTREAM.md](UPSTREAM.md) lists every change.

## Files

| Path | Contents |
|---|---|
| Challenge.lean | the statement, using only Mathlib definitions; the proof is `sorry`, as Palomar requires |
| Solution.lean | the same statement, proved from the library |
| RamseyIncrement/ | the proof: the colouring, the finite checks, the clone projection, and the (11,11) property of M(797) |
| comparator.json | the declarations that Comparator compares, and the permitted axioms |
| formalization.yaml | Palomar's metadata: sources, automation, review status |
| scripts/ | the check of Palomar's source rules, and a script that runs Comparator as Palomar does |

## The proof

- **The colouring.** RamseyIncrement/R1661/Graph.lean defines it as the Mathon–Shearer (11,11)-colouring M(797) without 21 vertices, together with 85 core vertices, each of which copies one of the 21 deleted vertices or has a single colour towards the other vertices of M(797). The tables of the core are in RamseyIncrement/R1661/Data.lean.
- **The argument** is the clone projection with an antipodal rule (RamseyIncrement/R1661/Projection.lean). It uses that M(797) has no monochromatic K₁₁, that antipodal vertices of M(797) have opposite colours towards every other vertex, and finite checks on the core.
- **The (11,11) property of M(797)** is proved in Lean, not assumed: RamseyIncrement/R1212/ comes from [r1212-1642](https://github.com/YueMa0/r1212-1642).
- **Kernel computation.** The finite checks are evaluated by the Lean kernel with `decide +kernel`. There is no `native_decide`, and the only axioms are propext, Classical.choice and Quot.sound.

## Building

The build needs [elan](https://github.com/leanprover/elan), which installs the Lean version in lean-toolchain.

```bash
lake exe cache get
lake build
```

Nine modules need much memory: each of the eight modules RamseyIncrement/R1212/H01Branch*.lean and RamseyIncrement/R1661/Checks.lean needs 5–6 GB while it is compiled. They import each other in a chain, so Lake compiles them one at a time. On an Apple M4 Mac mini with 16 GB of memory, the whole build took about 14 minutes, and the Lean processes used at most 6.1 GB together.

To check the statement against the proof as Palomar does, with Comparator, Lean's kernel and the independent kernels that ship with the toolchain:

```bash
./scripts/verify_comparator.sh
```

On Linux this needs bubblewrap for Comparator's sandbox; on other systems, `./scripts/verify_comparator.sh --no-sandbox` runs it without the sandbox. The GitHub Actions workflow runs the build and Comparator on Linux.

## How this work was done

The colouring was found on 3 November 2026 by a local search designed and run by the AI system Claude (Anthropic, model Claude Opus 5.5), used through the coding agent Claude Code. Claude also wrote the Lean proof, first in r1212-1661 and then in this port, and ran its builds and checks. The research continues r1212-1642 and r1212-1658; r1212-1658 started from exploratory work by GPT-6 Astra (OpenAI). Yue Ma directed the project, approved each stage and decides how the result is published.

## Credits

- The (11,11)-colouring M(797) is due to Mathon (1987) and Shearer (1986).
- **Milos Tatarevic**: the definition of `ramseyNumber` and the basic lemmas in RamseyIncrement/Basic.lean, Cone.lean, RamseyNumber.lean, SpecialLift.lean and Transport.lean come from his [ramsey-increment-theorem](https://github.com/milostatarevic/ramsey-increment-theorem) (MIT licence), through r1212-1642.
- From r1212-1642 and r1212-1658: RamseyIncrement/R1212/ and the defect lemma RamseyIncrement/R1658/Defect.lean.
- **Author**: Yue Ma.

## License

MIT; see [LICENSE](LICENSE).
