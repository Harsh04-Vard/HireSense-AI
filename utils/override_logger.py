import json
import os


def save_override(data):

    log_path = "outputs/logs/override_log.json"

    existing_logs = []

    if os.path.exists(log_path):

        with open(log_path, "r") as file:

            try:
                existing_logs = json.load(file)
            except:
                existing_logs = []

    existing_logs.append(data)

    with open(log_path, "w") as file:

        json.dump(
            existing_logs,
            file,
            indent=4
        )