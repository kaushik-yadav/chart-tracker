def get_status(immunity_level):
    if immunity_level < 40:
        return "Low"
    elif immunity_level < 70:
        return "Moderate"
    else:
        return "Good"