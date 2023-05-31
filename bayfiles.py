import subprocess
import json
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.key_binding import KeyBindings


def upload_file(file_path):
    curl_command = ['curl', '-s' , '-F', f'file=@{file_path}', 'https://api.bayfiles.com/upload']
    response = subprocess.check_output(curl_command).decode('utf-8')
    data = json.loads(response)
    
    if data['status']:
        file_info = data['data']['file']
        full_url = file_info['url']['full']
        metadata = file_info['metadata']
        file_id = metadata['id']
        file_name = metadata['name']
        file_size = metadata['size']['readable']
        
        print(f"File ID: {file_id}")
        print(f"File Name: {file_name}")
        print(f"File Size: {file_size}")
        print(f"Full URL: {full_url}")
    else:
        print("Upload failed.")


def input_file_path():
    kb = KeyBindings()

    @kb.add('c-c')
    def _(event):
        event.app.exit()

    completer = PathCompleter(expanduser=True)

    file_path = prompt(
        'Enter the file path: ',
        completer=completer,
        key_bindings=kb
    )
    return file_path


# Example usage
file_path = input_file_path()
upload_file(file_path)