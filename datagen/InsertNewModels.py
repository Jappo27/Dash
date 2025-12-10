from Harness import Harness
from SimpleQA import simpleEval
from Process import Process

def insertModel(modelName):
    model = Harness(modelName)

    evalData = simpleEval(model)  #Must be run first if database not initiated
    evalData.assessALL()

    procData = Process(model)
    procData.processALL()

try:
    model = input("Input Full Model Name")
    insertModel(model)
except:
    print("Error Encounterd")