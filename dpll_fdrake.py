# Algorithm DPLL
#     Input: A set of clauses Φ.
#     Output: A truth value indicating whether Φ is satisfiable.
# function DPLL(Φ)
#     // unit propagation:
#     while there is a unit clause {l} in Φ do
#         Φ ← unit-propagate(l, Φ);
#     // pure literal elimination:
#     while there is a literal l that occurs pure in Φ do
#         Φ ← pure-literal-assign(l, Φ);
#     // stopping conditions:
#     if Φ is empty then
#         return true;
#     if Φ contains an empty clause then
#         return false;
#     // DPLL procedure:
#     l ← choose-literal(Φ);
#     return DPLL(Φ ∧ {l}) or DPLL(Φ ∧ {¬l});

