import json
import pandas as pd

def export_logfile():
    # Create an object to store the log data
    log_data = []

    # Retrieve the data from the log file
    with open('log_file.json', 'r') as log_file:
        for line in log_file:
            log_entry = json.loads(line)
            log_data.append(log_entry)

    # Export a CSV file containing the log data
    pd.DataFrame(log_data).to_csv('log_data.csv', index=False)

