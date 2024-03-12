from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import router as key_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("DB cleared")
    await create_tables()
    print("DB created")
    yield
    print("Turning off")


app = FastAPI(lifespan=lifespan)
app.include_router(key_router)

origins = [
    "http://localhost:8000",  # Разрешить запросы с этого домена
    "http://127.0.0.1:8000",  # Также разрешить запросы с этого домена
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
