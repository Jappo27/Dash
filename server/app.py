
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from SelectDatabase import select
import datetime

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "../client/dist"),
    static_url_path="/"
)
CORS(app)

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/models")
def models():
    try:
        modelname = request.args.get('model', 'gemma3:1b')  # fallback to default if not provided
        query = select(modelname)
        
        query.getModels()
        
        models = query.getAllValues()
        returnList = []
        for model in models:
            returnList.append({"name":model})

        query.close()
        return returnList
    except Exception as e:
        return jsonify({})
    
@app.route("/api/tables")
def tables():
    try:
        modelname = request.args.get('model', 'base')  # fallback to default if not provided
        query = select(modelname)
        query.getALLtables()
        tables = query.getAllValues()
        
        tables = tables[2:-1]

        returnList = []
        for table in tables:
            returnList.append({"name":table})
            
        query.close()

        return returnList
    except Exception as e:
        return jsonify({})

@app.route("/api/processData")
def processData():
    try:
        modelname = request.args.get('model', 'gemma3:1b')  # fallback to default if not provided
        dates = request.args.getlist('dates')
        query = select(modelname)

        query.getALLtables()
        query.getModelID()
        query.selectTable("process")

        Alltables = query.getAllValues()
        rows = [row[2:] for row in Alltables]
        pData = []
        for i in range(len(rows[0])):
            pData.append([])
        for row in rows:
            for i in range(len(row)):
                pData[i].append(row[i])

        query.close()
        
        if dates != ["null"]:
            sDate, eDate = dates[0].split(",")
            newPdata = []
            if sDate != "":
                naive_dt = datetime.datetime.strptime(sDate[:-31], "%a %b %d %Y %H:%M:%S")
                sDate = naive_dt.replace(tzinfo=datetime.timezone.utc)
                sDate = sDate.timestamp()
            if eDate != "":
                naive_dt = datetime.datetime.strptime(eDate[:-31], "%a %b %d %Y %H:%M:%S")
                eDate = naive_dt.replace(tzinfo=datetime.timezone.utc)
                eDate = eDate.timestamp()

            if sDate != "" and eDate == "":
                for index, date in enumerate(pData[-1]):
                    
                    naive_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                    date = naive_dt.replace(tzinfo=datetime.timezone.utc)
                    date = date.timestamp()
                    
                    if sDate <= date <= sDate + 86400:
                        t = []
                        for i in range(len(pData)):
                            t.append(pData[i][index])
                        newPdata.append(t)

                rows = [row for row in newPdata]
                pData = []
                for i in range(len(rows[0])):
                        pData.append([])
                for row in rows:
                    for i in range(len(row)):
                        pData[i].append(row[i])

                return pData
            
            elif sDate != "" and eDate != "":
                for index, date in enumerate(pData[-1]):
                    
                    naive_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                    date = naive_dt.replace(tzinfo=datetime.timezone.utc)
                    date = date.timestamp()
                    
                    if sDate <= date <= eDate:
                        t = []
                        for i in range(len(pData)):
                            t.append(pData[i][index])
                        newPdata.append(t)

                rows = [row for row in newPdata]
                pData = []
                for i in range(len(rows[0])):
                        pData.append([])
                for row in rows:
                    for i in range(len(row)):
                        pData[i].append(row[i])

                return pData
        return pData
    except Exception as e:
        return jsonify({})
    
@app.route("/api/data")
def data():
    try:
        modelname = request.args.get('model', 'gemma3:1b')  # fallback to default if not provided

        query = select(modelname)

        query.getModelID()
        query.getALLtables()
        Alltables = query.getAllValues()

        tables = []
        for table in Alltables:
            tables.append(table[0])

        returnJson = {}
        if "sqlite_sequence" in tables:
            tables.remove("sqlite_sequence")

        for table in tables:
            query.selectTable(table)
            returnJson[table] = query.getAllValues()[0]

        query.close()
        return returnJson


    except Exception as e:
        return jsonify({})
    
if __name__ == "__main__":
    app.run(debug=True)