# Translate DNA to protein

import sys
import re

# RNA Codon Table
codon_table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
        'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
    }

def readFile(path):
    with open(path, "r") as f:
        lines = f.readlines()
        dna = "".join([line.strip() for line in lines[1:]])
        return dna

# Translate DNA to protein
def translate(dna):

    # Different reading frames
    frames = [dna[i:] for i in range(3)]

    # Remove extra bases
    frames = [frame[:len(frame) - len(frame) % 3] for frame in frames]

    proteins = []
    for frame in frames:
        proteins.append("".join([codon_table[frame[i:i+3]] for i in range(0, len(frame), 3)]))
    return proteins

# Find First Start Codon
def findStartCodon(protein):
    return protein.find("M")

# Find Protein sequence in translated protein sequences
def findProtein(proteins, protein):
    for i in range(len(proteins)):
        if protein in proteins[i]:
            return i, proteins[i].find(protein)
    return -1, -1

if __name__ == "__main__":
    dna = readFile(input("Enter the path to the file: "))
    print(dna)
    proteins = translate(dna)
    print(proteins)
    print(findStartCodon(translate(dna)[0]))
    print(findStartCodon(translate(dna)[1]))
    print(findStartCodon(translate(dna)[2]))
    with open(input("Enter File Path: "),"r") as file:
        lines = file.readlines()
        protein = "".join([line.strip() for line in lines[1:]])
        print(findProtein(proteins, protein))


