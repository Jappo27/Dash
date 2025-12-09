from flask import Flask

app = Flask(__name__. static_folder="../client/dist", static_url_path="/")

@app.route("/", methods=['Get'])
def home():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run()