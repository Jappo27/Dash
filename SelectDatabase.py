import os
import sqlite3

class select():
    
    def __init__(self, model_name):
        self.connection = sqlite3.connect(os.path.abspath('C:/Users/jappo/OneDrive/Desktop/AI-DashBoard/mydata.db'))
        self.cursor = self.connection.cursor()
        self.model_name = model_name
        self.model_id = None
        
    def getModelID(self):
        data = (self.model_name, )
        self.cursor.execute(f"""
            SELECT model_id FROM models WHERE model_name = ?;
        """, data)
        self.model_id = self.cursor.fetchone()[0]

    def getModels(self):
        self.cursor.execute(f"""
            SELECT model_name FROM models;
        """)

    def selectTable(self, table):
        data = (self.model_id, )
        if self.model_id:
            self.cursor.execute(f"""
                SELECT * FROM {table} WHERE model_id = ?;
            """, data)
        
    def getALLtables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
    def getAllValues(self):
        return self.cursor.fetchall()
    
    def getNValues(self, n):
        return self.cursor.fetchone()[n]
        
    def close(self):
        self.connection.commit()
        self.connection.close()
        
