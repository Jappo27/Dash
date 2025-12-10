import datetime
import os
from pathlib import Path
import pandas as pd
import csv
from ast import literal_eval
import sys 
import sqlite3
from Harness import Harness
#https://stackoverflow.com/questions/13890935/does-pythons-time-time-return-the-local-or-utc-timestamp
import time
from datetime import timezone, datetime

def try_literal_eval(s):
    #https://stackoverflow.com/questions/46858848/dict-objects-converting-to-string-when-read-from-csv-to-dataframe-pandas-python
    try:
        return literal_eval(s)
    except ValueError:
        return s
    
class simpleEval:

    def __init__(self, model, Dataset="hf://datasets/basicv8vc/SimpleQA/simple_qa_test_set.csv"):
        self.correct = 0
        self.incorrect = 0
        self.unattempted = 0

        self.overallCorrect = 0
        self.correctGivenAttempted = 0

        self.topic = None
        self.topicCorrect = 0
        self.topicIncorrect = 0
        self.topicUnattempted = 0
        self.topicData = []

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "mydata.db")
        self.connection = sqlite3.connect(db_path)

        self.cursor = self.connection.cursor()

        self.Dataset = Dataset
        self.model = model
        self.createModelTable()
        self.createBaseTable()
        self.insertModel()
        self.getModelID()
        self.insertBaseTable()
        self.initModel()

    def initModel(self):
        self.model.updateContent(f"Must have a single answer. Here we only focus on objective knowledge and force ques-tions to be written such that they only have a single, indisputable answer. One part of this criterion that the question must specify the scope of the answer. For example, instead of asking “where did Barack and Michelle Obama meet” (for which could have multiple answers “Chicago” or “the law firm Sidley & Austin”), questions had to specify “which city” or “which company.” Another common example is that instead of asking simply “when,” questions had to ask “what year” or “what date e.g. 14 February 1566. If the answer if not known it is better to respond as Unattempted.")
        self.model.generateResponse()

    def downloadDataset(self):
        #https://huggingface.co/datasets/basicv8vc/SimpleQA
        df = pd.read_csv(self.Dataset)
        df.to_csv('Dataset.csv', index=False)

    def splitDataset(self, label="topic"):
        #https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
        with open('Dataset.csv', mode='r', encoding="utf8") as file:
            csv_reader = csv.DictReader(file)  # Create DictReader

            data_list = []
            for row in csv_reader:
                data_list.append(row)

        datasheets = {}
        for i, data in enumerate(data_list):
            d = try_literal_eval(data["metadata"])
            if d["topic"] not in datasheets:
                datasheets.update({d["topic"]:[]})
            else:
                datasheets[d["topic"]].append(data_list[i])

        
        for key in datasheets.keys():
            #https://www.geeksforgeeks.org/python/working-csv-files-python/
            with open(f"{key}.csv", 'w', encoding="utf8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["metadata","problem","answer"])
                writer.writeheader()

                # writing headers (field names)
                writer.writeheader()

                # writing data rows
                writer.writerows(datasheets[key])

    def getTopicData(self):
        my_file = Path(f"APIStuff/simpleQA/{self.topic}.csv")
        if my_file.is_file():
            with open(f"APIStuff/simpleQA/{self.topic}.csv", mode='r', encoding="utf8") as file:
                csv_reader = csv.DictReader(file)  # Create DictReader

                data_list = []
                for row in csv_reader:
                    data_list.append(row)

            self.topicData = data_list
        return None
    
    def calcTopicData(self):
        for question in self.topicData[1:len(self.topicData)]:
            self.model.updateContent(f"Must have a single answer. Here we only focus on objective knowledge and force ques-tions to be written such that they only have a single, indisputable answer. One part of this criterion that the question must specify the scope of the answer. For example, instead of asking “where did Barack and Michelle Obama meet” (for which could have multiple answers “Chicago” or “the law firm Sidley & Austin”), questions had to specify “which city” or “which company.” Another common example is that instead of asking simply “when,” questions had to ask “what year” or “what date e.g. 14 February 1566. If the answer if not known it is better to respond as Unattempted. Negative marking is in effect”{question["problem"]}")
            self.model.generateResponse()
            print(question["answer"])
            print(self.model.response['message']['content'])
            if question["answer"] in self.model.response['message']['content']:
                self.topicCorrect += 1
            elif "Unattempted" in self.model.response['message']['content']:
                self.topicUnattempted += 1
            else:
                self.topicIncorrect += 1

        
        self.correct += self.topicCorrect
        self.incorrect += self.topicIncorrect
        self.unattempted += self.topicUnattempted

    #https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries

    def insertModel(self):
        data = (self.model.model,)
        
        # Check if model already exists
        self.cursor.execute("SELECT model_name FROM models WHERE model_name = ?;", data)
        models = self.cursor.fetchall()

        # Insert only if not found
        if not models:
            self.cursor.execute("INSERT INTO models (model_name) VALUES (?);", data)
            self.connection.commit()

    def getModelID(self):
        data = (self.model.model, )
        self.cursor.execute(f"""
            SELECT model_id FROM models WHERE model_name = ?;
        """, data)
        self.modelId = self.cursor.fetchone()[0]

    def createBaseTable(self):

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER,
            correct INTEGER,
            incorrect INTEGER,
            unattempted INTEGER,
            overallCorrect INTEGER,
            correctGivenAttempted INTEGER,
            time TIMESTAMP,
            FOREIGN KEY (model_id) REFERENCES models(model_id)
        );
        """)
        self.connection.commit()

    def insertBaseTable(self):
        data = (self.modelId,  self.correct, self.incorrect, self.unattempted, self.overallCorrect, self.correctGivenAttempted, datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        self.cursor.execute(f"""
            INSERT INTO base (model_id, correct, incorrect, unattempted, overallCorrect, correctGivenAttempted, time) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)

        self.connection.commit()

    def createModelTable(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                model_id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL UNIQUE
            );
            """)
        
        self.connection.commit()

    def createTopicTable(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.topic} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER,
        correct INTEGER,
        incorrect INTEGER,
        unaswered INTEGER,
        time TIMESTAMP,
        FOREIGN KEY (model_id) REFERENCES models(model_id)

        );
        """)

        self.connection.commit()

    def insertTopicTable(self):
        data = (self.modelId, self.topicCorrect, self.topicIncorrect, self.topicUnattempted, datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        self.cursor.execute(f"""
            INSERT INTO {self.topic} (model_id, correct, incorrect, unaswered, time) VALUES (?, ?, ?, ?, ?);
        """, data)

        self.connection.commit()

    def assessALL(self):
        for file in os.listdir("APIStuff/simpleQA"):
            if file.endswith(".csv"):
                self.assessTopic(file)

        self.calcOverallCorrect()
        self.calccorrectGivenAttempted()
        self.insertBaseTable()
        self.fullReset()

    def assessTopic(self, file):
        if file.endswith(".csv"):
            self.updateTopics(file[:-4])
            self.getTopicData()
            self.createTopicTable()
            self.calcTopicData()
            self.insertTopicTable()
            self.reset()

    def reset(self):
        self.topicCorrect = 0
        self.topicIncorrect = 0
        self.topicUnattepted = 0

    def fullReset(self):
        self.correct = 0,
        self.incorrect = 0,
        self.unattempted = 0,
        self.topicCorrect = 0
        self.topicIncorrect = 0
        self.topicUnattepted = 0
        self.overallCorrect = 0
        self.correctGivenAttempted = 0
    
    def calcOverallCorrect(self):
        self.overallCorrect = self.correct / (self.correct + self.incorrect + self.unattempted)

    def calccorrectGivenAttempted(self):
        self.correctGivenAttempted = self.correct / (self.correct + self.incorrect)

    def updateTopics(self, topic):
        self.topic = topic

    def closeCon(self):
        self.cursor.close()
        self.connection.close()
