from flask import Flask, g

DATABASE = 'database.db'


app = Flask(__name__)

@app.route('/')
def home():
    #home page 
    return "Chur g!"

if __name__ == "__main__":
    app.run(debug=True)