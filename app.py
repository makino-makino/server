import base64
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form["data"]
    
    data = base64.b64decode(data)
    print(data)

    return 'ok'

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000)
