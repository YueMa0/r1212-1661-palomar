module

public import RamseyIncrement

public section

/-!
# Proof of `R1212.lower_bound_1661`

`RamseyIncrement.R1661.r1212_hasRamseyColoring` (`RamseyIncrement/R1661/Main.lean`) gives a graph
on `Fin 1660` that is `IsRamseyFree` for `(12,12)`: neither the graph nor its complement contains
a 12-clique. The graph is the Mathon–Shearer colouring `M(797)` without 21 vertices, together with
85 core vertices; the proof is the clone projection with the antipodal rule, described in the
paper hexagon:2611.00248 and in `RamseyIncrement/R1661/Projection.lean`.
-/

theorem R1212.lower_bound_1661 :
    ∃ G : SimpleGraph (Fin 1660), G.CliqueFree 12 ∧ Gᶜ.CliqueFree 12 := by
  obtain ⟨G, hred, hblue⟩ := RamseyIncrement.R1661.r1212_hasRamseyColoring
  exact ⟨G, hred, hblue⟩
