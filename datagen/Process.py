import csv
import datetime
import json
import os
import socket
import sqlite3
from urllib.request import urlopen
import cpuinfo
import kagglehub
from Harness import Harness
import psutil
import time
import threading
from datetime import timezone, datetime
import json

#https://saturncloud.io/blog/how-to-get-current-cpu-gpu-and-ram-usage-of-a-particular-program-in-python/
#https://www.geeksforgeeks.org/python/multithreading-python-set-1/
#https://www.tutorialspoint.com/check-if-a-thread-has-started-in-python

class Process():

    def __init__(self, Model):
        BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "server")
        db_path = os.path.join(BASE_DIR, "mydata.db")
        self.connection = sqlite3.connect(db_path)

        self.cursor = self.connection.cursor()
        self.createProcessTable()
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(BASE_DIR, "model_prices.json")
        with open(json_path, "r") as f:
            self.modelData = json.load(f)

        #Metrics
        self.Model = Model
        self.getModelID()
        self.tokenCost = None
        self.Latency = None
        self.Cost = None
        self.cpuAvgPercent = None
        self.memoryAvgTotal = None

    def calcLatency(self):
        #Starts and ends a timer for the duration of response generation
        self.latency = self.Model.getReseponse().prompt_eval_duration / 1000000000
        
    def calcCloudCost(self):
        #Calc costs using input token + output token * token cost
        #github.com/AgentOps-AI/tokencost/blob/main/tokencost/model_prices.json
        
        prev = 0
        modelCharacteristics = []

        # Split self.Model by '-' or ':'
        for i, char in enumerate(self.Model.modelName):
            if char in ('-', ':'):
                modelCharacteristics.append(self.Model.modelName[prev:i])
                prev = i + 1

        # Add the last chunk
        modelCharacteristics.append(self.Model.modelName[prev:])

        # Match against modelData keys
        inputTokenCost = None
        outputTokenCost = None
        for model in self.modelData.keys():
            if all(char in model for char in modelCharacteristics):
                inputTokenCost = self.modelData[model].input_cost_per_token
                outputTokenCost = self.modelData[model].output_cost_per_token
                break
        
        if inputTokenCost == None or outputTokenCost == None:
            self.cost = 'NULL'
        else:
            self.cost = (self.Model.getReseponse().prompt_eval_count * inputTokenCost)+ (self.Model.getReseponse().eval_count * outputTokenCost)
    
    def calcHardwareCost(self):
        modelCpu , modelMemory, modelDisk = [], [], []
        #starts a timer to calc duration of use
        stime = time.time()
        #threads to allow for measuring cpu usage
        t1 = threading.Thread(target=self.Model.generateResponse, args=())
        t1.start()
        
        #while thread is active measure cpu%, ram total, disk%
        while t1.is_alive():
            cpu , memory, disk = self.sampleModel(modelCpu , modelMemory, modelDisk)
        t1.join()

        #Gets average over use
        self.cpuAvgPercent = sum(cpu)/len(cpu)
        self.memoryAvgTotal = sum(memory)/len(memory)
        self.diskAvgPercent = sum(disk)/len(disk) 

        self.getTDP()
        self.wattageUsed = self.watts * (self.cpuAvgPercent / 100)
        self.Cost = (self.wattageUsed / 1000) * ((self.Latency)/ 3600) * 0.2635

    def getTDP(self, download = "baraazaid/cpu-and-gpu-stats"):

        #Checks if file is present, downloads
        if os.path.isfile("tpu_cpus.csv") is False:
            try:
                #This data set is 3 years out of date
                path = kagglehub.dataset_download(download)
                print("Downloading File")            
            except:
                print("Download Failed")
        #Opens file and loads data into a csvdict
        csvfile = open(path, newline='')
        dataset = csv.DictReader(csvfile)
        #gets cpu brand name
        cpu = cpuinfo.get_cpu_info()['brand_raw']

        #compares device cpu to dataset getting wattage
        for row in dataset:
            if row["Name"] == cpu:
                self.watts = int(row["TDP"][:-1])
                csvfile.close()
                return self.watts
                    
        #laptops typically use 30-70w
        csvfile.close()
        self.watts = 70
        return self.watts

    def sampleModel(self, cpu=[], memory=[]):
        #This function samples the system during a model running
        cpu.append(self.calcCPU())
        memory.append(self.calcMemory())
        time.sleep(0.1)
        return cpu , memory
    
    def calcCPU(self):
        #Gets the percentage of CPU used
        return psutil.cpu_percent(interval=0.1)
    
    def calcMemory(self):
        #https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
        #Gets the total MB used 
        return psutil.Process().memory_info().rss / (1024 * 1024)
    
    def getModelID(self):
        data = (self.Model.model, )
        self.cursor.execute(f"""
            SELECT model_id FROM models WHERE model_name = ?;
        """, data)
        self.model_id = self.cursor.fetchone()[0]

    def createProcessTable(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS process (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER,                   
        latency INTEGER,
        cost INTEGER,
        cpuAvg INTEGER,
        memAvg INTEGER,
        time TIMESTAMP,
        FOREIGN KEY (model_id) REFERENCES models(model_id)

        );
        """)

        self.connection.commit()

    def insertProcessTable(self):
        data = (self.model_id, self.Latency, self.Cost, self.cpuAvgPercent, self.memoryAvgTotal, datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        self.cursor.execute(f"""
            INSERT INTO process (model_id, latency, cost, cpuAvg, memAvg, time) VALUES (?, ?, ?, ?, ?, ?);
        """, data)

        self.connection.commit()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def processALL(self):
        self.calcLatency()
        self.calcCloudCost()
        self.calcHardwareCost()

        self.insertProcessTable()

    def getModel(self):
        return self.Model
    
    def getLatency(self):
        return self.Latency
    
    def getCost(self):
        return self.Cost
    
    def getcpuAvgPercent(self):
        return self.cpuAvgPercent
    
    def getmemoryAvgTotal(self):
        return self.memoryAvgTotal
    
    def getwatts(self):
        return self.watts
    
    def getwattageUsed(self):
        return self.wattageUsed
