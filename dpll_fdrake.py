# code file
# fdrake

import csv

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

def dpll(clauses, assignment):
    """Recursive implementation of the Davis-Putnam-Logemann-Loveland Algorithm."""
    # base cases
    if not clauses:  # no clauses --> satisfied
        return True, assignment
    if any([not clause for clause in clauses]):  # any empty clause --> unsatisfied
        return False, assignment

    # unit propagation
    unit_clause = None
    for clause in clauses:
        # get the first clause with only one literal (unit clause)
        if len(clause) == 1:
            unit_clause = clause
    if unit_clause:
        # the variable in the unit clause must be assigned its truth value in the clause
        return dpll(assign_variable(clauses, unit_clause[0]), assignment + [unit_clause[0]])

    # get variable to assign 
    chosen_var = abs(clauses[0][0])
    
    # try chosen var as true
    satisfied, new_assignment = dpll(assign_variable(clauses, chosen_var), assignment + [chosen_var])
    if satisfied: # don't need to try chosen var as false since true works
        return True, new_assignment
    
    # else try chosen var as false
    satisfied, new_assignment = dpll(assign_variable(clauses, -chosen_var), assignment + [-chosen_var])
    return satisfied, new_assignment

def assign_variable(clauses, var):
    """Update wff based on new assignment of a variable."""
    updated_wff = []
    for clause in clauses:
        if var in clause:
            continue  # satisfied --> removed from wff
        new_clause = [x for x in clause if x != -var]  # propagation - remove negation of the assignment
        updated_wff.append(new_clause)
    return updated_wff

def main():
    file = "kSAT.cnf.csv" # test file
    cnfs = read_cnf_csv(file)

    num_correct = 0
    num_wrong = 0

    for cnf in cnfs:
        satisfiable, assignment = dpll(cnf['wff'], [])

        answer = cnf['metadata']['satisfiability']

        # check if right answer
        if answer == "S" and satisfiable == True:
            num_correct += 1
        elif answer == "U" and satisfiable == False:
            num_correct += 1
        else:
            num_wrong += 1

    print(f"{num_correct} correct, {num_wrong} wrong")

if __name__ == "__main__":
    main()
