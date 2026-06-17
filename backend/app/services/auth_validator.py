from app.models.user import User


def validate_token(token, db):
    user = db.query(User).filter(
        User.auth_token == token
    ).first()

    return user