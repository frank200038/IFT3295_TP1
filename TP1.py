
class Cell():
    def __init__(self):
        self.score = 0
        self.provenance = []    # should be a list of an ordered pair (i,j)
        self.position = (0,0)   # should be an ordered pair (i,j)

    def set_score(self, score):
        self.score = score
    
    def add_provenance(self, i, j):
        self.provenance.append((i,j))

    def set_position(self, i, j):
        self.position = (i,j)

    def __str__(self) -> str:
        return "[score: {}, provenance: {}, position: {}]".format(self.score, self.provenance, self.position)


def createMatrix(numRow,numColumn):
    result = [None] * numRow
    for i in range(numRow):
        result[i] = []
        for j in range(numColumn):
            cell = Cell() 
            cell.set_position(i,j)
            result[i].append(cell)
    
    return result

def find_optimal_path(T, optimal_cell):
    result_paths = []

    # find all possible paths using backtracking

    def find_paths(cell, path):
        if len(path) == 0:
            path = [cell]

        if len(cell.provenance) == 0:
            result_paths.append(path)
            return result_paths

        for i,j in cell.provenance:
            path_copy = path.copy()
            path_copy.insert(0,T[i][j])
            find_paths(T[i][j], path_copy)
    
    find_paths(optimal_cell, [])
    return result_paths



def alignment_prefix_suffix(A,B,match,missmatch,indel,horizontal):             
    '''
    If not horizontal In the table of dynamic programming, A is the suquence of column and B is the sequence of row.
    If horizontal In the table of dynamic programming, A is the suquence of row and B is the sequence of column. 
    indel should be negative.
    example: A = "ATCG", B = "ATCG", match = +4, missmatch = -4, indel = -8, horizontal = false
    example2: A = "CCTTCT", B = "CTTTCAC", match = +1, missmatch = -1, indel = -1, horizontal = true
    '''

    if horizontal:
        t = A 
        A = B
        B = t

    lenA = len(A)
    lenB = len(B)


    #initialization: lenA rows ,lenB cols   
    #the suquence of column decide the number of rows
    #the suquence of row decide the number of cols

    T = createMatrix(lenA + 1, lenB + 1)
    #T[0][0] = Cell()  

    if horizontal:
        # if horizontal
        # fist row = 0
        # fist column = 0, indel ,2*indel... 
        for i in range(lenA+1):
            T[i][0].set_score(indel*i)
            if i != 0:
                # i = 0 -> T[0][0], no provenance 
                T[i][0].add_provenance(i-1,0)
        for j in range(lenB+1):
            pass
            # pass means T[0][j] = Cell() 


    else:
        # fist column = 0
        # fist row = 0, indel ,2*indel... 
        for i in range(lenA+1):
            pass
            # pass means T[i][0] = Cell() 
        for j in range(lenB+1):
            T[0][j].set_score(indel*j)
            if j != 0:
                # j = 0 -> T[0][0], no provenance 
                T[0][j].add_provenance(0,j-1)

    for i in range(1,lenA+1):
        for j in range(1,lenB+1):
            left = T[i][j-1].score
            diagonal = T[i-1][j-1].score
            up = T[i-1][j].score
            # 
            delta = match if (A[i-1] == B[j-1]) else missmatch 
            max_score = max(left + indel , up + indel, diagonal+delta) 
            T[i][j].set_score(max_score)
            # for tracing back
            if max_score == left + indel:
                T[i][j].add_provenance(i,j-1)
            if max_score == up + indel:
                T[i][j].add_provenance(i-1,j)
            if max_score == diagonal+delta:
                T[i][j].add_provenance(i-1,j-1)


    ## find the max score in the last row or last column
    if horizontal:
        # find the max score in the last column
        optimal_cell = T[0][lenB]

        for i in range(1,lenA+1):
            if T[i][lenB].score > optimal_cell.score:
                optimal_cell = T[i][lenB]
    

    else:
        #find the max score in the last row
        optimal_cell = T[lenA][0]
        
        for j in range(1,lenB+1):
            if T[lenA][j].score > optimal_cell.score:
                optimal_cell = T[lenA][j]
        



    return T, optimal_cell
            

def print_table(T):    # for review of provenance
    numRow = len(T)
    numColumn = len(T[0])
    for i in range(numRow):
        for j in range(numColumn):
            print(T[i][j],end = " ")
        print("")

def print_table_score(T):   # for review of score
    numRow = len(T)
    numColumn = len(T[0])
    for i in range(numRow):
        for j in range(numColumn):
            print(T[i][j].score,end = " ")
        print("")

def print_paths(paths):
    for path in paths:
        print("One of the optimal paths:")
        for cell in path:
            print(cell ,end = " ")
        print("")


# use example2
table = alignment_prefix_suffix(A = "CCTTCT", B = "CTTTCAC", match = +1, missmatch = -1, indel = -1, horizontal = True)  
# use example
# table = alignment_prefix_suffix(A = "ATCG", B = "ATCG", match = +4, missmatch = -4, indel = -8, horizontal = False)

print_table(table[0])
print_table_score(table[0])
paths = find_optimal_path(table[0],table[1])
print_paths(paths)