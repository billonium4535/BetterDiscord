def get_version():
    try:
        with open("./VERSION", 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "NONE"
