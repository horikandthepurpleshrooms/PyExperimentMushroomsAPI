def validate_mushroom_data(data):
    name = data.get('name', '')
    description = data.get('description', '')

    if not name:
        return False, {'error': 'Name is required'}

    if not (1 <= len(name) <= 100):
        return False, {'error': 'Name must be between 1 and 100 characters'}

    if description and len(description) > 250:
        return False, {'error': 'Description must be no longer than 250 characters'}

    return True, None
