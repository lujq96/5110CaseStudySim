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
WaitTime = dict()
WaitTime["inC"] = dict(Dict)
WaitTime["exC"] = dict(Dict)
WaitTime["Mi"] = dict(Dict)
WaitTime["Dr"] = dict(Dict)
WaitTime["Fin"] = dict(Dict)
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
    def __init__(self,Type,Name,Last=None):
        self.Type = Type #{"exC","inC","Mi","Dr"}
        self.Last = Last #The last object it processed
        self.Status = 0 #How many hours before it is free
        self.Name = Name
        self.WTime = 0
        self.LastChange = -1
    def process(self,T,Model):
        if self.Last == Model:
            self.Status = Processtime(self.Type,Model)
            Queue[self.Type][Model]-=1
            self.Last = Model
        else:
            print("Changing tooling kits... Please add model later.")
            self.change(T,Model)
            #self.Status = Processtime(self.Type,Model)+Changetime(self.Type,Model)
        return
    def change(self,T,Model):
        if self.Last == Model:
            return
        if self.LastChange<0:
            self.Last=Model
            self.process(T,Model)
            self.LastChange=T
        else:
            self.Status -= Changetime(self.Type,Model)
            self.Last = Model
            self.LastChange=T
    def update(self):
        if self.Status >0:
            self.Status -= 0.5
            self.WTime += 0.5
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
        if self.Status <0:
            self.Status += 0.5
        return
    def Print(self):
        print([self.Name,self.Type,self.Last,self.Status,self.WTime])
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

def PeopleVal(Macs):
    n = 3
    cnt = 0
    for key in Macs.keys():
        for value in Macs[key]:
            if value.getStatus()<0:
                cnt += 1
    if cnt>=n:
        input("Warning: All worker is working! We need more worker to change the model!")
        return False
    return True
    
def Policy1(mac,Macs):
    mac = 1
    
def DefaultPolicy(T,mac,Macs):
    if mac.getName()=="Chunker1":
        if Queue["inC"]["C17"]>0:
            mac.process(T,"C17")
    elif mac.getName()=="ChunkerA" or mac.getName()=="ChunkerB":
        if Queue["exC"]["C17"]>0:
            mac.process(T,"C17")
    elif mac.getName()=="Mill1":
        if Queue["Mi"]["C17"]>0:
            mac.process(T,"C17")
    elif mac.getName()=="Chunker2":
        if Queue["inC"]["E26"]>0:
            mac.process(T,"E26")
    elif mac.getName()=="Chunker3":
        if Queue["inC"]["B15"]>0:
            mac.process(T,"B15")
        elif Queue["inC"]["D20"]>0:
            mac.process(T,"D20")
        elif Queue["inC"]["D25"]>0:
            mac.process(T,"D25")
    elif mac.getName()=="ChunkerC":
        if Queue["exC"]["E26"]>0:
            mac.process(T,"E26")
        elif ((Macs["inC"][2].Last=="E26" and Macs["inC"][2].getStatus()==0) or Macs["inC"][2].Last!="E26") and Queue["exC"]["D20"]>0:
            mac.process(T,"D20")
    elif mac.getName()=="ChunkerD":
        if Queue["exC"]["B15"]>0:
            mac.process(T,"B15")
        elif ((Macs["inC"][2].Last=="B15" and Macs["inC"][2].getStatus()==0) or Macs["inC"][2].Last!="B15") and Queue["exC"]["D25"]>0:
            mac.process(T,"D25")
    elif mac.getName()=="Mill2":
        if Queue["Mi"]["B15"]>0:
            mac.process(T,"B15")
            return True
        if Macs["exC"][3].Last=="B15" and Macs["exC"][3].getStatus()>0:
            return True
        if Queue["Mi"]["E26"]>0:
            mac.process(T,"E26")
            return True
        if Macs["exC"][2].Last=="E26" and Macs["exC"][2].getStatus()>0:
            return True
        if Queue["Mi"]["D25"]>0:
            mac.process(T,"D25")
            return True
        if Macs["exC"][2].Last=="D25" and Macs["exC"][2].getStatus()>0:
            return True
        if Queue["Mi"]["D20"]>0:
            mac.process(T,"D20")
            return True
    else:
        if Queue["Dr"]["F35"]>0:
            mac.process(T,"F35")
            return True
        if Queue["Dr"]["C17"]>0:
            mac.process(T,"C17")
            return True
        if Macs["Mi"][0].Last=="C17" and Macs["Mi"][0].getStatus()>0:
            return True
        if Queue["Dr"]["E26"]>0:
            mac.process(T,"E26")
            return True
        if Macs["Mi"][1].Last=="E26" and Macs["Mi"][1].getStatus()>0:
            return True
        if Queue["Dr"]["B15"]>0:
            mac.process(T,"B15")
            return True
        if Macs["Mi"][1].Last=="B15" and Macs["Mi"][1].getStatus()>0:
            return True
        if Queue["Dr"]["D25"]>0:
            mac.process(T,"D25")
            return True
        if Macs["Mi"][1].Last=="D25" and Macs["Mi"][1].getStatus()>0:
            return True
        if Queue["Dr"]["D20"]>0:
            mac.process(T,"D20")
            return True
    return True
    
def ManualPolicy(T,mac,Macs):
    key = mac.getType()
    Need = input("What to put into {}? Press Enter to add nothing:".format(mac.getName()))
    if Need == "Q":
        return False
    if Need == "":
        Need2 = input("Wanna change the model using on {}? Input the model name or Press Enter to skip:".format(mac.getName()))
        if Need2 != "":
            while Need2 not in Dict.keys():
                Need2 = input("Invalid Input! Please try again: ")
            if PeopleVal(Macs):
                mac.change(T,Need2)
    while Need!="":
        if Need not in Dict.keys():
            Need = input("Invalid Input! Please try again. Press Enter add nothing:")
        elif Validation(mac,Macs[key],Need):
            # Here is function to valid: if there is Need in need, put an error message. 
            # And if there are two other machine working on this model, put another error message.
            # Please someone comes to write the function!
            if mac.Last!=Need:
                if PeopleVal(Macs):
                    mac.change(T,Need)
            else:
                mac.process(T,Need)
            Need = ""
        else:
            Need = input("Invalid Input! Please try again. Press Enter to add nothing:")
    return True

T = 0 # T for Time
# Here are all the machines we have now
inChunker=[Machine(Type="inC",Name="Chunker1"),Machine(Type="inC",Name="Chunker2"),Machine(Type="inC",Name="Chunker3")]
exChunker=[Machine(Type="exC",Name="ChunkerA"),Machine(Type="exC",Name="ChunkerB"),Machine(Type="exC",Name="ChunkerC"),
           Machine(Type="exC",Name="ChunkerD")]
Mill = [Machine(Type="Mi",Name="Mill1"),Machine(Type="Mi",Name="Mill2")]
Drill = [Machine(Type="Dr",Name="Drill1")]
Machines = {"inC":inChunker,"exC":exChunker,"Mi":Mill,"Dr":Drill}
flag = True
while flag:
    if T%(8*2*7)==0:
        input("Press any key to continue.")
        print("New week comes. Please add the demand!")
        Queue["inC"]["B15"]+=int(input("B15: "))
        Queue["inC"]["C17"]+=int(input("C17: "))
        Queue["inC"]["D20"]+=int(input("D20: "))
        Queue["inC"]["D25"]+=int(input("D25: "))
        Queue["inC"]["E26"]+=int(input("E26: "))
        Queue["Dr"]["F35"]+=int(input("F35: "))
        ... #Here comes other prediction of needs
    # Maybe we can have more machine? To add a machine, please put code here.
    # Update status of the machine
    for key in Machines.keys():
        for machine in Machines[key]:
            machine.update()
    StatusPrint(T,Queue,Machines,"start")
    cnt = 0
    for key in Machines.keys():
        # Check if new models can add to the machine
        for machine in Machines[key]: #internal Chunker first
            if machine.getStatus()==0 and set(Queue[machine.getType()].values())!=set([0]):
                #Policy1(T,machine,Machines)
                #flag = ManualPolicy(T,machine,Machines)
                flag = DefaultPolicy(T,machine,Machines)
            if machine.getStatus()==0:
                cnt+=1
    if cnt==10:
        input("Finished!")
    StatusPrint(T,Queue,Machines,"end")
    T+=0.5
    #Output What happened Now.
    print("Wait Time for each model at each place is:")
    for key in WaitTime.keys():
        for val in WaitTime[key].keys():
            WaitTime[key][val]+=Queue[key][val]*0.5
        print("{}: {}".format(key,WaitTime[key]))