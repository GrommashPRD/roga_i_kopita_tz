from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from app.api.routers import api_router

app = FastAPI(
    title="Luna Test API",
    description="API сервер с аутентификацией по статическому API ключу",
    version="1.0.0",
    default_response_class=JSONResponse,
)


# Глобальный обработчик HTTP исключений для обеспечения JSON ответов
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await request_validation_exception_handler(request, exc)


# Подключаем API роуты
app.include_router(api_router)


@app.get("/ping")
async def ping():
    """
    Эндпоинт для проверки работоспособности сервера
    Не требует API ключа
    """
    return {"status": "ok", "message": "pong"}
