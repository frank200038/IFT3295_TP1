
import Partie1
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import pydot


'''
Author: Yan Zhuang, YuChen Hui
Since this program is only meant to be used to find the answers to the questions, the code are not as structured
as the code in Partie1.py. The code in Partie1.py is more structured and easier to read. However, Comments are provided to better explain the code.

When executing, please bear this in mind.
'''

sequences = Partie1.readFile(input("Enter the path of the file: "))


for i in range(len(sequences)):
    sequences[i] = sequences[i].strip()
matrix = Partie1.createMatrix(len(sequences), len(sequences))

print("Please wait while the program is calculating the distance matrix...")

for i in range(len(sequences)):
    for j in range(len(sequences)):
        if i != j:
            table, optimal = Partie1.alignment_prefix_suffix(A=sequences[i], B=sequences[j], match=+4, missmatch=-4,
                                                         indel=-8, horizontal=False)
            matrix[i][j] = optimal.score
        else:
            matrix[i][j] = 0

print("The matrix is: ")

Partie1.print_table(matrix)

# save as a pickle file
# with open('matrix_no_end_of_line.pickle', 'wb') as f:
#     pickle.dump(matrix, f)



# Load pickle file. Save Time.
# with open('matrix_no_end_of_line.pickle', 'rb') as f:
#     matrix = pickle.load(f)


# Select pairs that has a score equal or more than 80 from the matrix
# When there is an alignment between i and j twice, we only select the one with the highest score
pairs = []
pairs_with_score = []
for i in range(len(matrix)):
    for j in range(len(matrix)):
        if matrix[i][j] >= 80:
            if((j,i) in pairs):
                if matrix[i][j] > matrix[j][i]:
                    pairs.remove((j,i))
                    pairs.append((i,j))
                else:
                    continue
            pairs.append((i, j))


# Create oriented graph based on pairs, original
G = nx.DiGraph()
for pair in pairs:
    G.add_edge(pair[0], pair[1])

pos = nx.spring_layout(G, k = 0.5, iterations = 20)
nx.draw(G, pos, with_labels=True)
plt.show()

# Apply Transitive Reduction to the graph
G = nx.transitive_reduction(G)

pos = nx.spring_layout(G, k = 0.5, iterations = 20)
nx.draw(G, pos, with_labels=True)
plt.show()

# Convert the network graph to a dot graph, allow better visualization of the graph
graph = nx.drawing.nx_pydot.to_pydot(G)
graph.write_png('assembly.png')

# transfer the G to a dictionary
dict = nx.to_dict_of_lists(G)
#print(dict)
#{0: [9], 9: [17], 14: [18], 17: [19], 19: [14], 1: [13], 7: [2], 10: [7], 13: [10], 2: [4], 4: [0], 3: [8], 5: [16], 6: [5], 8: [6], 16: [], 18: [12], 11: [15], 15: [3], 12: [11]}

# find the start node
value_set = set()
for value in dict.values():
    if len(value) > 0:
        value_set.add(value[0])

start = 0
for i in range(20):
    if i not in value_set:
        start = i
        break

# Find the path from the start node to the end node
path = []
path.append(start)
while True:
    if dict[start] == []:
        break
    else:
        start = dict[start][0]
        path.append(start)
# print(path)
# [1, 13, 10, 7, 2, 4, 0, 9, 17, 19, 14, 18, 12, 11, 15, 3, 8, 6, 5, 16]

## Assemble the fragments

# 1. get the optimal nodes
optimal_nodes = []
for i in range(len(path)-1):
    table, node = Partie1.alignment_prefix_suffix(A=sequences[path[i]], B=sequences[path[i+1]], match=+4, missmatch=-4, indel=-8, horizontal=False)
    optimal_nodes.append(node)

# 2. slice each fragment
start_indexes =[(node.position[1]) for node in optimal_nodes]
# print(start_indexes)
# [281, 135, 292, 169, 280, 133, 225, 258, 277, 243, 174, 199, 247, 281, 276, 293, 283, 194, 174]

# assemble the fragments
assembled = sequences[path[0]]
for i in range(1, len(path)):
    assembled += sequences[path[i]][start_indexes[i-1]:]

print("the assembled sequence is: ", assembled)


