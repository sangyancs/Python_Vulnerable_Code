import os
import subprocess
from flask import Flask, request
app = Flask(__name__)

# curl -X GET "http://localhost:5000/tainted7/touch%20HELLO"


@app.route("/tainted7/<something>")
def test_sources_7(something):
    if something.isalnum():  # Allow only alphanumeric characters
        subprocess.run(["touch", f"/tmp/{something}"])
        return f"Created file: {something}"
    else:
        return "Invalid input", 400


if __name__ == "__main__":
	app.run(debug=True) 
