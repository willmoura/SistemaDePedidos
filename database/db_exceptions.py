class DatabaseError(Exception):
    def __init__(self, message="Ocorreu um erro no banco de dados", error_code=None):
        super().__init__(message)
        self.error_code = error_code