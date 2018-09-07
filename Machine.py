# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 19:52:20 2018

@author: lujq96
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