from werkzeug.security import generate_password_hash


def check_password(user, password):
    if user.hashed_password != generate_password_hash(password):
        return False, "wrong password"
    return True, "success"


def check_leader_token(leader, token):
    if leader.hashed_secret_token != generate_password_hash(token):
        return False, "wrong token"
    return True, "success"
