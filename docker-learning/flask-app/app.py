from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    quote = "Stay hungry, stay foolish. – Steve Jobs"
    return render_template('index.html', quote=quote)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))