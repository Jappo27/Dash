import os
import sqlite3

class select():
    
    def __init__(self, model_name):
        BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server")
        db_path = os.path.join(BASE_DIR, "mydata.db")
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.model_name = model_name
        self.model_id = None

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

    def createTopicTable(self, topic):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {topic} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER,
        correct INTEGER,
        incorrect INTEGER,
        unaswered INTEGER,
        time TIMESTAMP,
        FOREIGN KEY (model_id) REFERENCES models(model_id)

        );
        """)
        
    def close(self):
        self.connection.commit()
        self.connection.close()
        
