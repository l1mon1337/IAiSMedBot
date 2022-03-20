def validate_age(message):
    try:
        age = int(message)
    except (TypeError, ValueError):
        return False

    if age < 0 or age > 100:
        return False
    return True      
