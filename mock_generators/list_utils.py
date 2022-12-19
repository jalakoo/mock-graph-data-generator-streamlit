import datetime

def clean_list(list: list[any]) -> list[any]:
    # Remove None values from a list
    result = [item for item in list if item is not None]

    # Convert datetime to string
    result = [item.isoformat() if isinstance(item, datetime.date) else item for item in result]

    return result