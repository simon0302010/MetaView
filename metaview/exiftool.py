import subprocess
import json
import os

def get_metadata(file_path):
    result = subprocess.run(
        ["exiftool", "-j", file_path], capture_output=True, text=True
    )
    metadata = json.loads(result.stdout)
    return metadata[0] if metadata else {}

def write_metadata(file_path, new_data):
    if len(new_data) and os.path.exists(file_path):
        command = ["exiftool"]
        for key in new_data:
            command.append(f"-{key}={new_data[key]}")
        command.append(file_path)
        result = subprocess.run(
            command, capture_output=True, text=True
        )
        return result.stdout.strip()
    else:
        return "Nothing to write."
    
def delete_metadata(file_path, all=True):
    if os.path.exists(file_path) and all:
        command = ["exiftool", "-All=", file_path]
        result = subprocess.run(
            command, capture_output=True, text=True
        )
        return result.stdout.strip()
