def is_admin(user):
    return user.role == "ADMIN"


def is_investigator(user):
    return user.role == "INVESTIGATOR"


def is_user(user):
    return user.role == "USER"