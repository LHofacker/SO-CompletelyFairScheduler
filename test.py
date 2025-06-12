import os

filePath = os.path.join(os.path.dirname(__file__), "entradaEscalonador.txt")

with open(filePath, "r") as inputFile:

    firstLine = inputFile.readline().strip().split("|")
    print(firstLine)
    for line in inputFile:
        line = line.strip().split("|")
        print(line)