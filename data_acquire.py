import random

# Dictionary of information to be measured
keys = ["elevator_id", "position", "door_status", "weight"]   # If you want to add more information,
                                                              # just add the name here
                                                              # and make the acquisition below

# If any value is empty, it returns a False signal
def verify_data(data):
    if any(value is None for value in data.values()):
        print("Incomplete data!")
        return False
    return True

# Function to perform measurements and assemble the dictionary
def generate_data(keys=keys, values=None):
    values = values or {  # Replace with actual calls to sensors or data sources
        "elevator_id": lambda: random.randint(1, 100),
        "position": lambda: random.randint(0, 10),
        "door_status": lambda: random.choice(["open", "closed"]),
        "weight": lambda: random.randint(0, 750),
    }

    data = {key: values.get(key, lambda: None)() for key in keys}
    if verify_data(data):
        return data, True
    return data, False
