import matplotlib.pyplot as plt
import csv

# initialization
x = []
y = []
problem_types = []

# read file
with open('output_fdrake.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        if row[2].isdigit() and row[3].isdigit(): # skips header
            x.append(int(row[2]) * int(row[3])) # problem size
            y.append(float(row[1]))  # time
            problem_types.append(row[4])  # U / S

# different colors for U / S
unique_problem_types = list(set(problem_types))
colors = ['red', 'blue']  # Add more colors if needed
color_map = {unique_problem_types[i]: colors[i % len(colors)] for i in range(len(unique_problem_types))}

# assign colors to problem type
point_colors = [color_map[problem] for problem in problem_types]

# plot
plt.scatter(x, y, color=point_colors, s=75, edgecolor='black')

# labels, title
plt.xticks(rotation=45, fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.xlabel('Problem Size (# variables * # clauses)', fontsize=14, fontweight='bold')
plt.ylabel('Time (microseconds)', fontsize=14, fontweight='bold')
plt.title('DPLL Algorithm Time Analysis', fontsize=18, fontweight='bold', color='darkblue')

# legend
for problem_type, color in color_map.items():
    plt.scatter([], [], color=color, label=f"Type: {problem_type}")

plt.legend(loc='upper left', fontsize=12)

# save / display
plt.tight_layout()
plt.savefig('plot_dpll_algorithm_analysis.png', dpi=300)
plt.show()
