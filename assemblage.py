import TP1
import networkx as nx
import matplotlib.pyplot as plt

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
pairs = []
for i in range(len(matrix)):
    for j in range(len(matrix)):
        if matrix[i][j] >= 80:
            pairs.append((i, j))

print(pairs)

# Create oriented graph based on pairs
G = nx.DiGraph()
for pair in pairs:
    G.add_edge(pair[0], pair[1])
#
# # Draw the graph
nx.draw(G, with_labels=True)
plt.show()


# Transitive reduction
def transitive_reduction(G):
    for v in G:
        for w in G[v]:
            for x in G[v]:
                if x in G[w]:
                    G.remove_edge(w, x)
    return G

# Remove Double Egdes
def remove_double_edges(G):
    for v in G:
        for w in G[v]:
            if w in G[v]:
                G.remove_edge(v, w)
    return G

# Remove cycles


# G = remove_cycles(G)
G = remove_double_edges(G)
G = transitive_reduction(G)


# Draw the graph with space between nodes
pos = nx.spring_layout(G, k = 0.5, iterations = 20)
nx.draw(G, pos, with_labels=True)
plt.show()

