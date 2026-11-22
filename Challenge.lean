module

public import Mathlib.Combinatorics.SimpleGraph.Clique

public section

/-!
# R(12,12) ≥ 1661

The diagonal Ramsey number `R(12,12)` is the least `n` such that every red/blue colouring of the
edges of the complete graph `K_n` contains a red `K_12` or a blue `K_12`.

Given a simple graph `G` on a vertex set, colour an edge red if it is an edge of `G` and blue
otherwise. A red `K_12` is then a clique on 12 vertices of `G`, and a blue `K_12` is a clique on
12 vertices of the complement `Gᶜ`. So a simple graph on 1660 vertices such that neither it nor
its complement contains a 12-clique is exactly a red/blue colouring of `K_1660` with no
monochromatic `K_12`. Its existence says that `R(12,12) > 1660`, that is, `R(12,12) ≥ 1661`.
-/

/-- **`R(12,12) ≥ 1661`.** There is a simple graph on 1660 vertices such that neither the graph
nor its complement contains a clique on 12 vertices. -/
theorem R1212.lower_bound_1661 :
    ∃ G : SimpleGraph (Fin 1660), G.CliqueFree 12 ∧ Gᶜ.CliqueFree 12 := by
  sorry
