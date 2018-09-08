# -*- coding: utf-8 -*-
"""
Basic Framework for the Case Study
"""
"""
Dict = {"B15":0, "C17":0, "D20":0, "D25":0, "E26":0, "F35":0, "N99":0}
Queue = dict()
Queue["exC"] = dict(Dict)
Queue["inC"] = dict(Dict)
Queue["Mi"] = dict(Dict)
Queue["Dr"] = dict(Dict)
Queue["Fin"] = dict(Dict)
#Queue[x] means how many of each models are now waiting for processing

def Processtime(Machine,Model):
    # This is a simple function that will return the time to process Model on Machine
def Changetime(Machine,Model):
    # This is a simple function that will return the time to change to process Model on Machine

class Machine(*args):
    def __init__(self):
        self.Type = args.Type #{"exC","inC","Mi","Dr"}
        self.Last = None #The last object it processed
        self.Status = 0 #How many hours before it is free
    def process(self,Model):
        if self.Last == Model:
            self.Status = Processtime(self.Type,Model)
        else:
            self.Status = Processtime(self.Type,Model)+Changetime(self.Type,Model)
        self.Last = Model
        Queue[self.Type, Model]-=1
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
                Queue[Next(self.Type),self.Last]+=1     
        return
"""
import Machine

def StatusPrint():
    # Comments at where it is used.
    
def Validation():
    # COmments at where it is used.
    
def ManualPolicy():
    # Maybe we should define the policy seperately?
    
T = 0 # T for Time
# Here are all the machines we have now
exChunker=[Machine({Type:"exC"}),Machine({Type:"exC"}),Machine({Type:"exC"}),Machine({Type:"exC"})]
inChunker=[Machine({Type:"inC"}),Machine({Type:"inC"}),Machine({Type:"inC"})]
Mill = [Machine({Type:"Mi"}),Machine({Type:"Mi"})]
Drill = [Machine({Type:"Dr"})]
while True:
    if T%(24*7*2)==0:
        print("New weeks come, please add needings!")
        Queue["inC"]["B15"]+=int(input("B15: "))
        ... #Here comes other prediction of needs
    # Maybe we can have more machine? To add a machine, please put code here.
    T+=0.5
    for ... in ...: #internal Chunker first
    # Update status of the machine
    for exchunker in exChunker:
        if self.Status>0:
            exchunker.update()
    # Check if new models can add to the machine
    for exchunker in exChunker:
        if self.Status==0:
            StatusPrint(args you like)
            # List the time, status of Machine, status of the Models choose which to get
            # Who would like to make it???
            Need = input()
            if Need != "":
                if Validation():
                # Here is function to valid: if there is Need in need, put an error message. 
                # And if there are two other machine working on this model, put another error message.
                # Please someone comes to write the function!
                    exchunker.process(Need)
    for ... in ...: #Mill here
        
    for ... in ...: #Drill here
        
    #Output What happened Now.
    