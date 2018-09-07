# -*- coding: utf-8 -*-
"""
Basic Framework for the Case Study
"""

def Processtime(Machine,Model):
    
def Changetime(Machine,Model):

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
            if self.Status ==0:
                Queue[self.Type,self.Last]+=1     
        return
            
T = 0
exChunker=[Machine({Type:"exC"}),Machine({Type:"exC"}),Machine({Type:"exC"}),Machine({Type:"exC"})]
inChunker=[Machine({Type:"inC"}),Machine({Type:"inC"}),Machine({Type:"inC"})]
Mill = [Machine({Type:"Mi"}),Machine({Type:"Mi"})]
Drill = [Machine({Type:"Dr"})]
NeedexC = [0,0,0,0,0,0]
NeedinC = [0,0,0,0,0,0]
NeedMi = [0,0,0,0,0,0]
NeedDr = [0,0,0,0,0,0]
Dict = {"B15":0, "C17":1, "D20":2, "D25":3, "E26":4, "F35":5, "N99":6}
while True:
    T+=0.5
    for exchunker in exChunker:
        if self.Status>0:
            exchunker.update()
        else:
            #List the status of Machine, status of the Models choose which to get
            Need = input()
            if Need != "":
            #if the need <=0: put an error message
            
    for ... in ...:
        
    for ... in ...:
        
    for ... in ...:
        
    #Output What happened Now.
    