from flask import Flask, render_template, jsonify, send_file, send_from_directory
import json
import os

# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Now you can use `script_dir` to construct the relative path to other files
file_path = os.path.join(script_dir, "model_log.json")

app = Flask(__name__)


# Load model log data from JSON file
def load_model_log():
    with open(file_path, "r") as f:
        model_log = json.load(f)
    return model_log


# Home page
@app.route("/")
def home():
    model_log = load_model_log()
    return render_template("index.html", model_log=model_log)


# Route to handle button click and reload model log data
@app.route("/reload_model_log", methods=["GET"])
def reload_model_log():
    model_log = load_model_log()
    return jsonify(model_log)


@app.route("/download/<path:filename>", methods=["GET"])
def download_file(file_name):
    # Get the directory where the Flask application is located
    app_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path relative to the Flask application's directory
    file_path = os.path.join(app_dir, file_name)

    try:
        # Send the file as an attachment
        return send_from_directory(app.config["DATA_FOLDER"], file_path)
    except FileNotFoundError:
        # If the file is not found, return a 404 error
        return "File not found", 404


if __name__ == "__main__":
    app.run(debug=True)
