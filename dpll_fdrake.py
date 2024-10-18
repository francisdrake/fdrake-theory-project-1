# code file
# fdrake

import csv
import time

recursive_call_count = 0

def read_cnf_csv(file):
    '''Read in the cnfs and their metadata from given csv file.'''
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
                if current_cnf["wff"]:  # if there's already data in the current cnf, append it and start a new one
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

    # sort cnfs first by number of clauses * number of vars
    cnfs.sort(key=lambda x: x['clauses'] * x['vars'])
    return cnfs

def find_pure_literals(clauses):
    '''Finding pure literals - only one polarity in the wff.'''
    count = {}
    
    # get all the literals
    for clause in clauses:
        for literal in clause:
            count[literal] = count.get(literal, 0) + 1
    
    # get pure literals with only one truth assignment
    pure_literals = []
    for literal in count:
        if -literal not in count:  # if no negation --> pure literal
            pure_literals.append(literal)
    
    return pure_literals

def find_unit_clause(clauses):
    '''Finding unit clauses - clause contains only one literal.'''
    unit_clause = None
    for clause in clauses:
        # get the first clause with only one literal (unit clause)
        if len(clause) == 1:
            unit_clause = clause
    return unit_clause

def dpll(clauses, assignment):
    '''Recursive implementation of the Davis-Putnam-Logemann-Loveland Algorithm.'''
    global recursive_call_count
    recursive_call_count += 1

    # base cases
    if not clauses:  # no clauses --> satisfied
        return True, assignment
    if any([not clause for clause in clauses]):  # any empty clause --> unsatisfied
        return False, assignment

    # unit propagation
    unit_clause = find_unit_clause(clauses)
    if unit_clause:
        # the variable in the unit clause must be assigned its truth value in the clause
        return dpll(assign_variable(clauses, unit_clause[0]), assignment + [unit_clause[0]])
    
    # pure literal elimination
    pure_literals = find_pure_literals(clauses)
    if pure_literals:
        for pure_literal in pure_literals:
            # assign pure literals
            return dpll(assign_variable(clauses, pure_literal), assignment + [pure_literal])

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
    '''Update wff based on new assignment of a variable.'''
    updated_wff = []
    for clause in clauses:
        if var in clause:
            continue  # satisfied --> removed from wff
        new_clause = [x for x in clause if x != -var]  # propagation - remove negation of the assignment
        updated_wff.append(new_clause)
    return updated_wff

def get_and_write_data(test_file, output_file_name, accuracy, verbose=False):
    global recursive_call_count
    output_file = open(output_file_name, mode='a', newline='', encoding='utf-8')
    cnfs = read_cnf_csv(test_file)

    num_correct = 0
    num_wrong = 0

    for cnf in cnfs:
        start = time.time()
        satisfiable, assignment = dpll(cnf['wff'], [])
        end = time.time()
        exec_time=int((end-start)*1e6)
        problem_number = cnf["metadata"]["problem_number"]
        num_variables=cnf["vars"]
        num_clauses=cnf["clauses"]
        answer = cnf['metadata']['satisfiability']
        problem_type = answer
    
        # formatting
        if satisfiable == True:
            problem_type = "S"
        else:
            problem_type = "U"

        # check if right answer
        if accuracy:
            if answer == "S" and satisfiable == True:
                num_correct += 1
            elif answer == "U" and satisfiable == False:
                num_correct += 1
            else:
                num_wrong += 1

        output_file.write(f"{problem_number},{exec_time},{num_variables},{num_clauses},{problem_type}\n")
        if verbose:
            output_file.write(f"assignment of variables: {assignment}\n")
            output_file.write(f"# of recursive calls: {recursive_call_count}\n")
            if accuracy:
                output_file.write(f"Accuracy: {num_correct} correct out of {num_correct+num_wrong} problems.\n")

    if accuracy:
        print(f"Accuracy: {num_correct} correct out of {num_correct+num_wrong} problems.")
    output_file.close()

def main():
    output_file_name = r"output_fdrake.csv"
    output_verbose = r"verbose_output_fdrake.txt"

    # test file for accuracy and timing
    with open(output_verbose, mode='a', newline='', encoding='utf-8') as output_file:
        output_file.write("problem_number,execution_time,variables,clauses,problem_type\n")
    get_and_write_data("data_kSAT.cnf_fdrake.csv", output_verbose, accuracy=True, verbose=True)

    # more test files for timing (don't have answers)
    files = ["data_kSAT.cnf_fdrake.csv", "data_2SAT.cnf_fdrake.csv", "data_kSATu.cnf_fdrake.csv"]
    with open(output_file_name, mode='a', newline='', encoding='utf-8') as output_file:
        output_file.write("problem_number,execution_time,variables,clauses,problem_type\n")
    for file in files:
        get_and_write_data(file, output_file_name, accuracy=False)

if __name__ == "__main__":
    main()