from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, users, merchants, orders

app = FastAPI(title="Food Order System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建表
Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(merchants.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Food Order System API OK"}
