from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings

# Import models để SQLAlchemy tạo bảng
from app.models import User, Room, Booking, Payment, Review

# Import routers
from app.routers import auth, rooms, bookings, chat, payments, reviews



# Tạo tất cả bảng trong DB
Base.metadata.create_all(bind=engine)

from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title=settings.app_name,
    description="API quản lý homestay với chatbot AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.app_name,
        version="1.0.0",
        description="API quản lý homestay với chatbot AI",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Cho phép Frontend gọi API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
app.include_router(auth.router,     prefix="/api/auth",     tags=["Auth"])
app.include_router(rooms.router,    prefix="/api/rooms",    tags=["Rooms"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(chat.router,     prefix="/api/chat",     tags=["Chatbot"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(reviews.router,  prefix="/api/reviews",  tags=["Reviews"])

@app.get("/")
def root():
    return {"message": "Homestay API đang chạy!", "docs": "/docs"}