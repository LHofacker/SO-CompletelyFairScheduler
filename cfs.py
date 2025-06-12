import os
import ARN
from functools import total_ordering

@total_ordering
class Process:

    def __init__(self, creationTime, pid, totalTime, priority):

        self.creationTime = creationTime
        self.pid = pid
        self.totalTime = totalTime
        self.priority = priority

        self.remainingTime = totalTime
        self.timeFinished = 0
        self.executionTime = 0
        self.virtualRuntime = 0
        self.quantumUsed = 0

    def __lt__(self, otherProcess):

        if self.virtualRuntime == otherProcess.virtualRuntime:
            return self.pid < otherProcess.pid
        return self.virtualRuntime < otherProcess.virtualRuntime

    def __eq__(self, otherProcess):

        return self.pid == otherProcess.pid

class CompletelyFairScheduler:

    def __init__(self):
        
        self.quantum = 0
        self.basePriority = 1024
        self.currentTime = 0
        self.queue = ARN.RedBlackTree()
        self.currentProcess = None

        self.finishedProcessess = []
        self.readyList = []
        self.waitList = []

        

    def readFromFile(self):

        filePath = os.path.join(os.path.dirname(__file__), "entradaEscalonador.txt")

        with open(filePath, "r") as inputFile:

            firstLine = inputFile.readline().strip().split("|")
            self.quantum = int(firstLine[1])

            for line in inputFile:
                line = line.strip().split("|")

                aux = Process(int(line[0]), int(line[1]), int(line[2]), int(line[3]))
                self.loadProcesses(aux)
    
    def loadProcesses(self, process):

        self.waitList.append(process)

    def insertProcess(self, Process):

        self.queue.insert(Process)

    def Schedule(self):
        
        if self.queue.root == self.queue.TNULL:
            return None

        MinimunVrun = self.queue.minimum(self.queue.root)
        self.queue.delete_node(MinimunVrun.item)

        return MinimunVrun.item


    def Tick(self):

        #Verifica todos os processos na lista de espera. Caso o "momento atual" seja seu "momento de início",
        #Coloca o processo na lista dos "Prontos para execução" -> Árvore RN
        for process in list(self.waitList):
            if process.creationTime == self.currentTime:
                self.insertProcess(process)
                self.waitList.remove(process)

        #Se não há um processo ativo no momento, escalona um para execução.
        if not self.currentProcess:
            self.currentProcess = self.Schedule()

            if self.currentProcess:
                self.currentProcess.quantumUsed = 0

        #Se há um processo ativo, contabiliza seu tempo em CPU e tempo restante de operação.
        if self.currentProcess:


            if self.currentProcess:
                pass#self.currentProcessInfo(self.currentProcess)

            self.currentProcess.remainingTime -= 1
            self.currentProcess.executionTime += 1
            self.currentProcess.quantumUsed += 1

            self.currentProcess.virtualRuntime += 1 * (self.basePriority/self.currentProcess.priority)

            if self.currentProcess.remainingTime <= 0:

                self.currentProcess.executionTime += self.currentProcess.quantumUsed
                self.currentProcess.timeFinished = self.currentTime + 1
                self.finishedProcessess.append(self.currentProcess)
                self.currentProcess = None

            elif self.currentProcess.quantumUsed >= self.quantum:

                self.insertProcess(self.currentProcess)
                self.currentProcess = None

            #if self.queue.root != self.queue.root.TNULL:
            elif self.queue.root != self.queue.TNULL:
                min_node = self.queue.minimum(self.queue.root)
                if self.currentProcess.virtualRuntime > min_node.item.virtualRuntime:
                    self.insertProcess(self.currentProcess)
                    self.currentProcess = self.Schedule()


        if self.currentProcess:
            self.currentProcessInfo(self.currentProcess)
        self.currentTime += 1

    def currentProcessInfo(self, process):

        print((f"ID do Processo atual: {process.pid}, Tempo até terminar: {process.remainingTime}"
               f", Tempo utilizado: {process.quantumUsed}, Tempo: {self.currentTime}"
               f", Tempo de Execução: {process.executionTime}"))

    def finalStats(self):

        for process in sorted(self.finishedProcessess, key=lambda p: p.pid):

            print((f"PID: {process.pid}, "
                f"Momento de Criação: {process.creationTime}, "
                f"Fim de Execução: {process.timeFinished - process.creationTime}, "
                f"Tempo Pronto mas Parado: {process.timeFinished - process.creationTime - process.executionTime}"))
    

    def run(self):
        while (
            self.waitList or
            self.queue.root != self.queue.TNULL or
            self.currentProcess
        ):
        
            self.Tick()


def main():

    scheduler = CompletelyFairScheduler()
    scheduler.readFromFile()
    print("INICIANDO CFS!")
    scheduler.run()
    print("\n")
    print("######################################################################\n")
    scheduler.finalStats()
    print("CFS ENCERRADO!")

if __name__ == "__main__":
    main()
