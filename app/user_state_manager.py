# Simple user state manager
user_states = {}

def get_user_state(user_id):
    """Retrieve the state of a user by their ID (phone number)."""
    return user_states.get(user_id, {"step": "start", "person_image": None, "garment_image": None})

def update_user_state(user_id, key, value):
    """Update the user's state with a given key-value pair."""
    if user_id not in user_states:
        user_states[user_id] = {"step": "start", "person_image": None, "garment_image": None}
    user_states[user_id][key] = value

def reset_user_state(user_id):
    """Reset the state of the user."""
    if user_id in user_states:
        user_states[user_id] = {"step": "start", "person_image": None, "garment_image": None}
