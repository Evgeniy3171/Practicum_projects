class Urls:
    BASE_URL = "https://stellarburgers.education-services.ru"
    API_URL = f"{BASE_URL}/api"
    
    # Auth endpoints
    REGISTER = f"{API_URL}/auth/register"
    LOGIN = f"{API_URL}/auth/login"
    USER = f"{API_URL}/auth/user"
    
    # Order endpoints
    ORDERS = f"{API_URL}/orders"
    
    # Ingredients endpoint
    INGREDIENTS = f"{API_URL}/ingredients"