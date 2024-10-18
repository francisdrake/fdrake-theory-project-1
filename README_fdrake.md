Readme_fdrake
Version 1 8/22/24

Team name: fdrake

Names of all team members: Francis Drake

Link to github repository: https://github.com/francisdrake/fdrake-theory-project-1.git  

Which project options were attempted:
an implementation of the DPLL algorithm for SAT solving

Approximately total time spent on project: ~ 8 hours

The language you used, and a list of libraries you invoked.
Language: Python
Libraries: csv (to read in the testing data), time (to time the tests), and matplotlib (to plot my results)

How would a TA run your program (did you provide a script to run a test case?)
Run python3 dpll_fdrake.py to test around 700 cases, 400 of which have been verified for accuracy.

A brief description of the key data structures you used, and how the program functioned.
I used a variety of data structures for this project. First and foremost, I used a dictionary to store both the metadata and the actual clauses for the test cases that were in cnf form. Each test case read in was stored in a dictionary. Each test’s wff was stored in a list of lists. Each clause in the wff was a list of literals. Additionally, I utilized lists to keep track of the assignment of variables as well as to store pure literals. In terms of the functionality of my implementation of the Davis–Putnam–Logemann–Loveland algorithm, I utilized recursive backtracking with a few modifications. The recursion mimicked a depth-first traversal of a binary tree. Before assigning values to the variables, I looked for any unit clauses (clauses with one literal whose value I then assigned) or pure literals (single truth value assigned throughout). After simplifying the wff through assigning variables the values they had to have, I then tried to assign the next variable a value. If that assignment made the wff unsatisfiable, the algorithm would backtrack and try the other value. Otherwise, more recursive calls would be made making further assignments. A satisfied clause would be removed, and unsatisfied clauses would be empty, indicating that the wff was unsatisfiable.

A discussion as to what test cases you added and why you decided to add them (what did they tell you about the correctness of your code). Where did the data come from? (course website, handcrafted, a data generator, other)
I used the test cases provided by Prof. Kogge, namely his kSAT.cnf.csv, 2SAT.cnf.csv, and kSATu.cnf.csv files. One of these files (kSAT.cnf.csv) had 400 test cases with the correct answer, which I used to check the accuracy of my code. I added the other files so that I could have a lot of different problems of various sizes that I could use to plot the timing based on their sizes and have enough data to visualize the trends.

An analysis of the results, such as if timings were called for, which plots showed what? What was the approximate complexity of your program?
I plotted the results in a scatter plot, with the x-axis representing the problem size (# of variables multiplied by the # of clauses) and the y-axis representing the time in microseconds it took to solve. I noticed first that the unsatisfiable problems (denoted by the color red) took much longer than the satisfiable ones (denoted by the color blue), which is due to the fact that the backtracking algorithm had to look through all possible assignments to make sure none satisfied the formula. When a satisfiable solution was reached, the program was able to move on and not have to try every possible value. Additionally, the worst case performance was O(2^n), which was when the formula was unsatisfiable. Thus, the graph grew exponentially with the size of the problem. The average space complexity for the DPLL is O(n), but I used more space storing all of the test cases in dictionaries.

A description of how you managed the code development and testing.
I created a new git repository for this project and made a copy of it in my local environment. I tested in my local branch with a variety of files and outputs, which I filtered through before pushing any changes to main. As substantial changes were made, I added and committed them and eventually pushed them to main.

Did you do any extra programs, or attempted any extra test cases
I created a verbose output file detailing the assignments of variables (even if unsatisfiable) and number of recursive calls made. 
