
import TP1
import networkx as nx
import matplotlib.pyplot as plt
import pydot

'''
Since this program is only meant to be used to find the answers to the questions, the code are not as structured
as the code in TP1.py. The code in TP1.py is more structured and easier to read. However, Comments are provided to better explain the code.

When executing, please bear this in mind.
'''

sequences = TP1.readFile(input("Enter the path of the file: "))
matrix = TP1.createMatrix(len(sequences), len(sequences))

print("Please wait while the program is calculating the distance matrix...")

for i in range(len(sequences)):
    for j in range(len(sequences)):
        if i != j:
            table, optimal = TP1.alignment_prefix_suffix(A=sequences[i], B=sequences[j], match=+4, missmatch=-4,
                                                         indel=-8, horizontal=False)
            matrix[i][j] = optimal.score
        else:
            matrix[i][j] = 0

print("The matrix is: ")
TP1.print_table(matrix)

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

