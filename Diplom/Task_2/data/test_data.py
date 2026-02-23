class UserData:
    VALID_PASSWORD = "password123"
    INVALID_PASSWORD = "wrong_password"
    VALID_NAME = "TestUser"
    
    @staticmethod
    def generate_email():
        import random
        import string
        return f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"


class ResponseMessages:
    USER_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INVALID_CREDENTIALS = "email or password are incorrect"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"


class ErrorCodes:
    FORBIDDEN = 403
    UNAUTHORIZED = 401
    BAD_REQUEST = 400
    NOT_FOUND = 404