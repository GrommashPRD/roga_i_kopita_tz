"""
Кастомные исключения для слоев работы с базой данных и usecase
"""


class DatabaseError(Exception):
    """Базовое исключение для ошибок работы с базой данных"""
    pass


class DatabaseConnectionError(DatabaseError):
    """Ошибка подключения к базе данных"""
    pass


class DatabaseQueryError(DatabaseError):
    """Ошибка выполнения запроса к базе данных"""
    pass


class UseCaseError(Exception):
    """Базовое исключение для ошибок usecase слоя"""
    pass


class NotFoundError(UseCaseError):
    """Исключение для случаев, когда сущность не найдена (404)"""
    pass


class UseCaseExecutionError(UseCaseError):
    """Исключение для ошибок выполнения usecase (500)"""
    pass

