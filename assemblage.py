
import Partie1
import networkx as nx
import matplotlib.pyplot as plt
import pickle


'''
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

