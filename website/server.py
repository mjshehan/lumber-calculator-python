from flask import Flask, render_template, request 

app = Flask(__name__)

@app.route('/') 
@app.route('/index')

def index():
    return "Hellow Worlds"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
