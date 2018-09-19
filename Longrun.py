# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 22:02:08 2018

@author: lujq9
"""

import numpy as np
import pandas as pd
import copy
import DemandAnalysis

Oneweek = 8*10
Dict = {"B15":0, "C17":0, "D20":0, "D25":0, "E26":0, "F35":0, "N99":0}
Queue = dict()
CBL = dict(Dict)
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

def reset(Macs):
    WaitTime = dict()
    WaitTime["inC"] = dict(Dict)
    WaitTime["exC"] = dict(Dict)
    WaitTime["Mi"] = dict(Dict)
    WaitTime["Dr"] = dict(Dict)
    WaitTime["Fin"] = dict(Dict)
    #for key in Macs.keys():
    #    for val in Macs[key]:
    return WaitTime

def Processtime(Machine,Model):
    # This is a simple function that will return the time to process Model on Machine
    if Machine=="inC":
        if Model=="B15":
            return 6
        if Model=="C17":
            return 3
        if Model=="D20" or Model=="N99":
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
        if Model[0]=="D" or Model[0]=="N":
            return 3
        return 4.5
    if Machine=="Dr":
        if Model=="B15" or Model=="C17":
            return 1.5
        if Model[0]=="D"or Model[0]=="E" or Model[0]=="N":
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
        self.Processed=dict(Dict)
    def process(self,T,Model):
        if self.Last == Model:
            self.Status = Processtime(self.Type,Model)
            Queue[self.Type][Model]-=1
            self.Processed[Model]+=1
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
                if Next(self.Type)=="Fin":
                    CBL[self.Last]-=1
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


def LongTermPolicy(T,mac,Macs):
    if mac.getName()=="Chunker1":
        if Queue["inC"]["N99"]>0:
            mac.process(T,"N99")
        elif mac.Last!=None and Queue["inC"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["inC"]["C17"]>0:
            mac.process(T,"C17")
        elif Queue["inC"]["E26"]>0:
            mac.process(T,"E26")
    elif mac.getName()=="Chunker2":
        if (mac.Last=="D20" or mac.Last=="D25") and Queue["inC"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["inC"]["D20"]>0:
            mac.process(T,"D20")
        elif Queue["inC"]["D25"]>0:
            mac.process(T,"D25")
        elif Queue["inC"]["B15"]>0:
            mac.process(T,"B15")
    elif mac.getName()=="Chunker3":
        if mac.Last!=None and Queue["inC"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["inC"]["B15"]>0:
            mac.process(T,"B15")
        elif Queue["inC"]["E26"]>0:
            mac.process(T,"E26")
    elif mac.getName()=="ChunkerA":
        if mac.Last!=None and Queue["exC"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["exC"]["C17"]>0:
            mac.process(T,"C17")
        elif Queue["exC"]["E26"]>0 and Validation(mac,Macs["exC"],"E26"):
            mac.process(T,"E26")
        elif Queue["exC"]["D20"]>0 and Validation(mac,Macs["exC"],"D20"):
            mac.process(T,"D20")
        elif Queue["exC"]["D25"]>0 and Validation(mac,Macs["exC"],"D25"):
            mac.process(T,"D25")
    elif mac.getName()=="ChunkerB":
        if mac.Last!=None and Queue["exC"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["exC"]["C17"]>0:
            mac.process(T,"C17")
        elif Queue["exC"]["E26"]>0 and Validation(mac,Macs["exC"],"E26"):
            mac.process(T,"E26")
        elif Queue["exC"]["D20"]>0 and Validation(mac,Macs["exC"],"D20"):
            mac.process(T,"D20")
        elif Queue["exC"]["D25"]>0 and Validation(mac,Macs["exC"],"D25"):
            mac.process(T,"D25")
    elif mac.getName()=="ChunkerC":
        if mac.Last!=None and Queue["exC"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["exC"]["D25"]>0 and Validation(mac,Macs["exC"],"D25"):
            mac.process(T,"D25")
        elif Queue["exC"]["D20"]>0 and Validation(mac,Macs["exC"],"D20"):
            mac.process(T,"D20")
        elif Queue["exC"]["B15"]>0 and Validation(mac,Macs["exC"],"B15"):
            mac.process(T,"B15")
    elif mac.getName()=="ChunkerD":
        if mac.Last!=None and Queue["exC"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["exC"]["B15"]>0 and Validation(mac,Macs["exC"],"B15"):
            mac.process(T,"B15")
        elif Queue["exC"]["E26"]>0 and Validation(mac,Macs["exC"],"E26"):
            mac.process(T,"E26")
    elif mac.getName()=="ChunkerE":
        if Queue["exC"]["N99"]>0:
            mac.process(T,"N99")
        elif Macs["inC"][0].Last=="N99" and Macs["inC"][0].Status>0:
            return True
        elif mac.Last!=None and Queue["exC"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["exC"]["B15"]>0 and Validation(mac,Macs["exC"],"B15"):
            mac.process(T,"B15")
        elif Queue["exC"]["D20"]>0 and Validation(mac,Macs["exC"],"D20"):
            mac.process(T,"D20")
    elif mac.getName()=="Mill1":
        if mac.Last!=None and Queue["Mi"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["Mi"]["C17"]>0:
            mac.process(T,"C17")
        elif Queue["Mi"]["D20"]>0:
            mac.process(T,"D20")
        elif Queue["Mi"]["D25"]>0:
            mac.process(T,"D25")
    elif mac.getName()=="Mill2":
        if Queue["Mi"]["N99"]>=max(1,min(3,2/3*CBL["N99"])):
            mac.process(T,"N99")
        elif mac.Last=="N99" and ((Macs["exC"][2].Last=="N99" and Macs["exC"][2].Status>0) or (Macs["exC"][4].Last=="N99" and Macs["exC"][4].Status>0)):
            return True
        elif mac.Last!=None and Queue["Mi"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["Mi"]["B15"]>0:
            mac.process(T,"B15")
        elif Queue["Mi"]["E26"]>0:
            mac.process(T,"E26")
        elif Queue["Mi"]["D25"]>3:
            mac.process(T,"D25")
    elif mac.getName()=="Drill1":
        if mac.Last!=None and Queue["Dr"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif Queue["Dr"]["F35"]>0:
            mac.process(T,"F35")
        elif Queue["Dr"]["C17"]>0:
            mac.process(T,"C17")
        elif Macs["Mi"][0].Last=="C17" and Macs["Mi"][0].Status>0 and sum(Queue["Dr"].values())<5:
            return True
        elif Queue["Dr"]["B15"]>3:
            mac.process(T,"B15")
        elif Macs["Mi"][1].Last=="B15" and Macs["Mi"][1].Status>0 and sum(Queue["Dr"].values())<5:
            return True
        elif Queue["Dr"]["D20"]>3:
            mac.process(T,"D20")
        elif Macs["Mi"][0].Last=="D20" and Macs["Mi"][0].Status>0 and sum(Queue["Dr"].values())<5:
            return True
        elif Queue["Dr"]["E26"]>3:
            mac.process(T,"E26")
        elif Queue["Dr"]["D25"]>5:
            mac.process(T,"D25")
        elif Queue["Dr"]["B15"]>0:
            mac.process(T,"B15")
        elif Queue["Dr"]["D20"]>0:
            mac.process(T,"D20")
        elif Queue["Dr"]["E26"]>0:
            mac.process(T,"E26")
        elif Queue["Dr"]["D25"]>0:
            mac.process(T,"D25")
    elif mac.getName()=="Drill2":
        if Queue["Dr"]["N99"]>=max(1,min(4,2/3*CBL["N99"])):
            mac.process(T,"N99")
        elif mac.Last!=None and Queue["Dr"][mac.Last]>0:
            mac.process(T,mac.Last)
        elif mac.Last=="N99" and Macs["Mi"][1].Last=="N99" and Macs["Mi"][1].Status>0:
            return True
        elif Queue["Dr"]["D25"]>0:
            mac.process(T,"D25")
        elif Queue["Dr"]["E26"]>3:
            mac.process(T,"E26")
        elif Macs["Mi"][1].Last=="E26" and Macs["Mi"][1].Status>0 and sum(Queue["Dr"].values())<5:
            return True
        elif Queue["Dr"]["D20"]>3:
            mac.process(T,"D20")
        elif Macs["Mi"][0].Last=="D20" and Macs["Mi"][0].Status>0 and sum(Queue["Dr"].values())<5:
            return True
        elif Queue["Dr"]["B15"]>3:
            mac.process(T,"B15")
        elif Macs["Mi"][1].Last=="B15" and Macs["Mi"][1].Status>0 and sum(Queue["Dr"].values())<5:
            return True
        elif Queue["Dr"]["D25"]>0:
            mac.process(T,"D25")
        elif Queue["Dr"]["E26"]>0:
            mac.process(T,"E26")
        elif Queue["Dr"]["D20"]>0:
            mac.process(T,"D20")
        elif Queue["Dr"]["B15"]>0:
            mac.process(T,"B15")
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
           Machine(Type="exC",Name="ChunkerD"),Machine(Type="exC",Name="ChunkerE")]
Mill = [Machine(Type="Mi",Name="Mill1"),Machine(Type="Mi",Name="Mill2")]
Drill = [Machine(Type="Dr",Name="Drill1"),Machine(Type="Dr",Name="Drill2")]
Machines = {"inC":inChunker,"exC":exChunker,"Mi":Mill,"Dr":Drill}
flag = True
flag1 = True
worker =[0,0,0,0,0,0,0,0,0,0,0]
FBL = []
Need = np.array([0,0,0,0,0,0,0])
NeedByWeek = []
f=open("result.txt","w")
Last=copy.copy(Queue["Fin"])
#def demand_gen(t=1):
#    return [8,14,3,4,4,2]
while flag :#and flag1 and T<=Oneweek*17:
    #if T==Oneweek*2:
    #    Machines["Dr"].append(Machine(Type="Dr",Name="Drill2"))
    if T%(Oneweek)==0:
        f.write(str([(Queue["Fin"][k]-Last[k]) for k in Queue["Fin"].keys()])+"\n")
        Last = copy.copy(Queue["Fin"])
        WaitTime = reset(Machines)
        print("\nWorking worker number: {}".format(worker))
        print("Current BackLog: {}".format(CBL))
        if T!=0:
            FBL.append([CBL["B15"]+Need[0],CBL["C17"]+Need[1],CBL["D20"]+Need[2],CBL["D25"]+Need[3],CBL["E26"]+Need[4],CBL["F35"]+Need[5]])
        worker = [0,0,0,0,0,0,0,0,0,0,0]
        print("\n Table of models processed by each machine:")
        for key in Machines.keys():
                for machine in Machines[key]:
                    print("{}: {}".format(machine.getName(),machine.Processed))
        flag1 = True
        Q = input("Press any key to continue.Q TO EXIT")
        if Q=="Q":
            break
        #if T==0:
        #    Queue["inC"]={"B15":A[0], "C17":A[1], "D20":A[2], "D25":A[3], "E26":A[4], "F35":0, "N99":0}
        #    Queue["Dr"]["F35"]=A[5]
        #    CBL={"B15":A[1], "C17":A[2], "D20":A[3], "D25":A[4], "E26":A[5], "F35":A[6], "N99":0}
        if T==0:
            Need = np.array(DemandAnalysis.demand_gen(t=14))+np.array(DemandAnalysis.demand_gen(t=15))#+np.array(DemandAnalysis.demand_gen(t=16))
        print(Need)
        #Add = input("It is Week {} now. Add cumulative demand?(Y/N) ".format(T//Oneweek+1))
        if int(T//Oneweek+1)%2==1:
            Add = "Y"
        else:
            Add = "N"
        if Add=="Y":
            #Pressure Test
            #Need = [int(1.5*x) for x in Need]
            Queue["inC"]["B15"]+=Need[0];CBL["B15"]+=Need[0]
            Queue["inC"]["C17"]+=Need[1];CBL["C17"]+=Need[1]
            Queue["inC"]["D20"]+=Need[2];CBL["D20"]+=Need[2]
            Queue["inC"]["D25"]+=Need[3];CBL["D25"]+=Need[3]
            Queue["inC"]["E26"]+=Need[4];CBL["E26"]+=Need[4]
            Queue["Dr"]["F35"]+=Need[5];CBL["F35"]+=Need[5]
            Need = None
        #else:
        #    Queue["inC"]["N99"]+=Need[6];CBL["N99"]+=Need[6]
        #    Need[6]=0
        NeedByWeek.append(np.array(DemandAnalysis.demand_gen(t=int(T//Oneweek+16))))
        if Need is None:
            Need = NeedByWeek[-1]
        else:
            Need = Need+NeedByWeek[-1]
        #Here comes other prediction of needs
    # Maybe we can have more machine? To add a machine, please put code here.
    # Update status of the machine
    for key in Machines.keys():
        for machine in Machines[key]:
            machine.update()
    StatusPrint(T,Queue,Machines,"start")
    cnt = 0
    cntworker = 0
    for key in Machines.keys():
        # Check if new models can add to the machine
        for machine in Machines[key]: #internal Chunker first
            if machine.getStatus()==0 and set(Queue[machine.getType()].values())!=set([0]):
                #Policy1(T,machine,Machines)
                #flag = ManualPolicy(T,machine,Machines)
                #flag = DefaultPolicy(T,machine,Machines)
                #flag = NewPolicy1(T,machine,Machines)
                flag = LongTermPolicy(T,machine,Machines)
                #flag = BackLogPolicy(T,machine,Machines)
            if machine.getStatus()==0:
                cnt+=1
            if machine.getStatus()<0:
                cntworker+=1
    worker[cntworker]+=1
    if cnt==12:
        if flag1:
            print("\n Table of models processed by each machine:")
            for key in Machines.keys():
                for machine in Machines[key]:
                    print("{}: {}".format(machine.getName(),machine.Processed))
            flag1 = False
            input("Finished!")
    StatusPrint(T,Queue,Machines,"end")
    T+=0.5
    #Output What happened Now.
    print("Wait Time for each model at each place is:")
    for key in WaitTime.keys():
        for val in WaitTime[key].keys():
            WaitTime[key][val]+=Queue[key][val]*0.5
        print("{}: {}".format(key,WaitTime[key]))
f.close()
pd.DataFrame(NeedByWeek).to_csv("Demand1.csv")
pd.DataFrame(FBL).to_csv("BackLogLongRun1.csv")