# Placeholder storage for users (use a DB in production)
users = {}


def register_user(mobile, password):
    if mobile in users:
        return {"success": False, "error": "User already exists"}

    # Store user info (hashed passwords are preferred)
    users[mobile] = {"password": password, "verified": False}

    # Save to DB

    return {"success": True}


def login_user(mobile, password):
    if mobile not in users or users[mobile]["password"] != password:
        return {"success": False, "error": "Invalid credentials"}

    # Generate JWT (you can use libraries like PyJWT)
    token = "dummy_jwt_token"

    return {"success": True, "token": token}
