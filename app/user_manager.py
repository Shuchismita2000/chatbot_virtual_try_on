from database import User, get_session
from datetime import datetime

def get_or_create_user(phone_number):
    """Retrieve a user by phone number or create a new one if not found."""
    session = get_session()
    user = session.query(User).filter_by(phone_number=phone_number).first()
    if not user:
        user = User(phone_number=phone_number)
        session.add(user)
        session.commit()
    session.close()
    return user

def update_user(user, **kwargs):
    """Update user attributes and save changes."""
    session = get_session()
    for key, value in kwargs.items():
        setattr(user, key, value)
    user.last_updated = datetime.utcnow()
    session.commit()
    session.close()

def reset_user(user):
    """Reset user state."""
    update_user(user, current_step="start", person_image_url=None, garment_image_url=None)
