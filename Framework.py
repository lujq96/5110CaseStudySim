# -*- coding: utf-8 -*-
"""
Basic Simulation Framework for the Case Study
Author: Jianqiu Lu
"""
import numpy as np

Dict = {"B15":0, "C17":0, "D20":0, "D25":0, "E26":0, "F35":0, "N99":0}
Queue = dict()
Queue["inC"] = dict(Dict)
Queue["exC"] = dict(Dict)
Queue["Mi"] = dict(Dict)
Queue["Dr"] = dict(Dict)
Queue["Fin"] = dict(Dict)
#Queue[x] means how many of each models are now waiting for processing

def Processtime(Machine,Model):
    # This is a simple function that will return the time to process Model on Machine
    if Machine=="inC":
        if Model=="B15":
            return 6
        if Model=="C17":
            return 3
        if Model=="D20":
            return 4.5
        if Model=="D25":
            return 4.5
        if Model=="E26":
            return 6
    if Machine=="exC":
        if Model=="E26":
            return 9
        else:
            return 8
    if Machine=="Mi":
        if Model=="B15" or Model=="C17":
            return 4
        if Model[0]=="D":
            return 3
        return 4.5
    if Machine=="Dr":
        if Model=="B15" or Model=="C17":
            return 1.5
        if Model[0]=="D"or Model[0]=="E":
            return 2
        return 3
def Changetime(Machine,Model):
    # This is a simple function that will return the time to change to process Model on Machine
    if Machine=="exC" or Machine=="inC":
        return 1.5
    if Machine=="Mi":
        return 2
    return 3

class Machine():
    def __init__(self,Type,Name):
        self.Type = Type #{"exC","inC","Mi","Dr"}
        self.Last = None #The last object it processed
        self.Status = 0 #How many hours before it is free
        self.Name = Name
    def process(self,Model):
        if self.Last == Model:
            self.Status = Processtime(self.Type,Model)
        else:
            self.Status = Processtime(self.Type,Model)+Changetime(self.Type,Model)
        self.Last = Model
        Queue[self.Type][Model]-=1
        return
    def update(self):
        if self.Status >0:
            self.Status -= 0.5
            def Next(Type):
                if Type=="inC":
                    return "exC"
                elif Type=="exC":
                    return "Mi"
                elif Type=="Mi":
                    return "Dr"
                else:
                    return "Fin"
            if self.Status ==0:
                Queue[Next(self.Type)][self.Last]+=1     
        return
    def Print(self):
        print([self.Name,self.Type,self.Last,self.Status])
    def getStatus(self):
        return self.Status
    def getType(self):
        return self.Type
    def getName(self):
        return self.Name

def StatusPrint(T,Need,Machines,node):
    # Comments at where it is used.
    print()
    print("At {} of time {}".format(node,T))
    for key in Need.keys():
        print("{}: {}".format(key,Need[key]))
    for key in Machines.keys():
        for i in Machines[key]:
            i.Print()
    
def Validation(machine,Type,model):
    # COmments at where it is used.
    if Queue[machine.Type][model]<=0:
        return False
    cnt = 0
    for m in Type:
        if (m.Name!=machine.Name and m.Last==model):
            cnt += 1
    if cnt>=2:
        return False
    return True
    
#def ManualPolicy():
    # Maybe we should define the policy seperately?
    
T = 0 # T for Time
# Here are all the machines we have now
inChunker=[Machine(Type="inC",Name="Chunker1"),Machine(Type="inC",Name="Chunker2"),Machine(Type="inC",Name="Chunker3")]
exChunker=[Machine(Type="exC",Name="ChunkerA"),Machine(Type="exC",Name="ChunkerB"),Machine(Type="exC",Name="ChunkerC"),
           Machine(Type="exC",Name="ChunkerD")]
Mill = [Machine(Type="Mi",Name="Mill1"),Machine(Type="Mi",Name="Mill2")]
Drill = [Machine(Type="Dr",Name="Drill1")]
Machines = {"inC":inChunker,"exC":exChunker,"Mi":Mill,"Dr":Drill}
while True:
    if T%(24*7*2)==0:
        print("New week comes. Please add the demand!")
        Queue["inC"]["B15"]+=int(input("B15: "))
        Queue["inC"]["C17"]+=int(input("C17: "))
        Queue["inC"]["D20"]+=int(input("D20: "))
        Queue["inC"]["D25"]+=int(input("D25: "))
        Queue["inC"]["E26"]+=int(input("E26: "))
        Queue["Dr"]["F35"]+=int(input("F35: "))
        ... #Here comes other prediction of needs
    # Maybe we can have more machine? To add a machine, please put code here.
    T+=0.5
    # Update status of the machine
    for key in Machines.keys():
        for machine in Machines[key]:
            machine.update()
    """
    for inchunker in inChunker:
        inchunker.update()
    for exchunker in exChunker:
        exchunker.update()
    for mill in Mill:
        mill.update()
    for drill in Drill:
        drill.update()
    """
    StatusPrint(T,Queue,Machines,"start")
    for key in Machines.keys():
        # Check if new models can add to the machine
        for machine in Machines[key]: #internal Chunker first
            if machine.getStatus()==0 and set(Queue[machine.getType()].values())!=set([0]):
                Need = input("What to put into {}? Press Enter to add nothing:".format(machine.getName()))
                while Need!="":
                    if Validation(machine,MType,Need):
                        # Here is function to valid: if there is Need in need, put an error message. 
                        # And if there are two other machine working on this model, put another error message.
                        # Please someone comes to write the function!
                        machine.process(Need)
                        Need = ""
                    else:
                        Need = input("Invalid Input! Please try again. Press Enter add nothing:")
    StatusPrint(T,Queue,inChunker,exChunker,Mill,Drill,"end")
    #Output What happened Now.
    