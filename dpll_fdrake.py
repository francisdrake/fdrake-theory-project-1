# CODE FILE
# fdrake

import csv
from collections import defaultdict

def read_cnf_csv(file):
    """Read in the cnfs and their metadata from given csv file."""
    cnfs = []
    current_cnf = {
        "metadata": {},
        "vars": 0,
        "clauses": 0,
        "wff": []
    }

    with open(file, mode='r', encoding='utf-8-sig') as f:
        csv_reader = csv.reader(f)
        
        for line in csv_reader:
            # first line is metadata
            if line[0] == 'c':
                if current_cnf["wff"]:  # if there's already data in the current CNF, append it and start a new one
                    cnfs.append(current_cnf)
                    current_cnf = {
                        "metadata": {},
                        "vars": 0,
                        "clauses": 0,
                        "wff": []
                    }
                current_cnf['metadata'] = {
                    'problem_number': line[1],
                    'vars': line[2],
                    'satisfiability': line[3]
                }
            # cnf declaration
            elif line[0] == 'p' and line[1] == 'cnf':
                current_cnf['vars'] = int(line[2])
                current_cnf['clauses'] = int(line[3])
            # cnf clauses
            else:
                clause = [int(x) for x in line if x and x != '0']
                if clause:
                    current_cnf['wff'].append(clause)

        # add the last entry after the loop finishes
        if current_cnf["wff"]:
            cnfs.append(current_cnf)

    return cnfs

def unit_propagate(wff):
    """Locate and propagate clauses containing a single literal that must have a certain assignment."""
    assignments = {}
    unit_clauses = []
    updated_wff = []

    # determine which clauses are unit clauses
    for clause in wff:
        if len(clause) == 1:  # single literal clause
            unit_clauses.append(clause[0])
        elif len(clause) >= 2 and clause[0] == clause[1]:  # case for -9, -9
            unit_clauses.append(clause[0])

    # propagate any unit clauses
    for literal in unit_clauses:
        var = abs(literal)  # get the abs value
        if literal < 0:
            assignments[var] = False  # assign that var to false
        else:
            assignments[var] = True  # assign that var to true

    # update wff given this new var assignment
    for clause in wff:
        if all(literal in assignments and assignments[literal] == (literal < 0) for literal in clause):
            continue  # clause is satisfied - don't need to include in updated wff
        else:
            updated_clause = []
            for literal in clause:
                if abs(literal) in assignments:
                    # if the variable is already assigned, remove it
                    if (literal < 0) == assignments[abs(literal)]:
                        continue
                updated_clause.append(literal)
            updated_wff.append(updated_clause)

    return assignments, updated_wff
    

def pure_literals(formula, assignments): # only one assignment / polarity
    """Locate and remove literals with one assignment in the entire wff."""
    literal_count = defaultdict(int)
    updated_wff = []

    # count occurences of each literal
    for clause in formula:
        for literal in clause:
            literal_count[literal] += 1

    pure_literals = []

    # identify pure literals
    for literal, count in literal_count.items():
        # check if the opposite literal exists
        if -literal not in literal_count:
            # if not then it's a pure literal
            pure_literals.append(literal)

            # if the literal is not already assigned, add it to assignments
            if literal not in assignments and -literal not in assignments:
                assignments[literal] = True if literal > 0 else False

    # remove pure literals
    for clause in formula:
        # only keep clauses that do not contain pure literals
        if not any(literal in assignments for literal in clause):
            updated_wff.append(clause)

    return pure_literals, assignments, updated_wff

def choose_literal(wff):
    """Choose the first non-empty clause to assign next."""
    for clause in wff:
        if clause:  # first non-empty clause
            return clause[0]
    return None

def assign_literal(wff, literal):
    """Assign a truth value to a given literal."""
    updated_wff_with_assignment = []
    for clause in wff:
        # if the clause contains the literal --> it is satisfied
        if literal in clause:
            continue
        # if the clause contains the negation of the literal
        # remove negation so we can look at the other literal(s)
        new_clause = [x for x in clause if x != -literal]
        updated_wff_with_assignment.append(new_clause)
    return updated_wff_with_assignment

def dpll(clauses):
    """Recursive implementation of the Davis–Putnam–Logemann–Loveland Algorithm."""
    # unit propagation
    print(clauses)
    assignments, wff = unit_propagate(clauses)
    print("after unit propagation:", wff)

    # break conditions
    if not wff:
        return True
    if any(len(clause) == 0 for clause in wff):
        return False
    
    # pure literal elimination
    found_pure_literals, assignments, wff = pure_literals(wff, assignments)
    print("pure literals:", found_pure_literals)
    print("after pure literal elimination:", wff)

    # break conditions
    # (checking after literal elimination and unit propagation)
    if not wff:
        # all clauses satisfied and thus removed
        return True
    if any(len(clause) == 0 for clause in wff):
        # no satisfiable assignment for a particular clause
        return False
        
    # dpll recursive call
    literal = choose_literal(wff)
    return dpll(assign_literal(wff, literal)) or dpll(assign_literal(wff, -literal))


def main():
    cnfs = read_cnf_csv("2SAT.cnf.csv")
    #print(cnfs)
    for i, cnf in enumerate(cnfs):
        # print(cnf["metadata"])
        # print(cnf["wff"])
        # print()
        print(dpll(cnf["wff"]))
        if i == 5:
            break

if __name__ == "__main__":
    main()
