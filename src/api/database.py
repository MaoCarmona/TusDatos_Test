import json

def load_json_db():
    try:
        with open('process_db.json', 'r') as f:
            data = json.load(f)
            # Check if the data is a list
            if not isinstance(data, list):
                print("The JSON file does not contain a list of processes.")
                return []
            
    except FileNotFoundError:
        print("File 'process_db.json' not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return []

    return data
