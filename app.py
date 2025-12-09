from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['Get'])
def home():
    return "<h1>Header</h1>"

if __name__ == "__main__":
    app.run()