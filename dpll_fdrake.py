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


def dppl(set_of_clauses):
    Satisfiable = False

    return Satisfiable

def unit_propagate():
    pass

def pure_literal_assignment():
    pass

def check(Wff,Nvars,Nclauses,Assignment):
# Run thru all possibilities for assignments to wff
# Starting at a given Assignment (typically array of Nvars+1 0's)
# At each iteration the assignment is "incremented" to next possible
# At the 2^Nvars+1'st iteration, stop - tried all assignments
    Satisfiable=False
    while (Assignment[Nvars+1]==0):
        # Iterate thru clauses, quit if not satisfiable
        for i in range(0,Nclauses): #Check i'th clause
            Clause=Wff[i]
            Satisfiable=False
            for j in range(0,len(Clause)): # check each literal
                Literal=Clause[j]
                if Literal>0: Lit=1
                else: Lit=0
                VarValue=Assignment[abs(Literal)] # look up literal's value
                if Lit==VarValue:
                    Satisfiable=True
                    break
            if Satisfiable==False: break
        if Satisfiable==True: break # exit if found a satisfying assignment
        # Last try did not satisfy; generate next assignment)
        for i in range(1,Nvars+2):
            if Assignment[i]==0:
                Assignment[i]=1
                break
            else: Assignment[i]=0
    return Satisfiable