class ApiError(Exception):
    def __init__(self, message, status_code=0):
        self.message = message
        self.status_code = status_code
super().__init__(self.message)

def api_error_to_text(ex: 'ApiError') -> str:
    return f"Error {ex.status_code}: {ex.message}" if ex.status_code else str(ex)
