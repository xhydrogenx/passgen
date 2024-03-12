from typing import Annotated
from fastapi import APIRouter, Depends, Request, Query
from repository import KeyRepository
from schemas import SKeyAdd, SKey
from fastapi.templating import Jinja2Templates
import os
import string
import random
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

TEMPLATES_DIR = os.path.join('front')
templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter(
    prefix="/keys",
    tags=["Пароли"]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("")
async def add_key(
        key: Annotated[SKeyAdd, Depends()],
):
    key_id = await KeyRepository.add_one(key)
    return {"ok": True, "key_id": key_id}


@router.get("")
async def get_keys() -> list[SKey]:
    keys = await KeyRepository.find_all()
    return keys


@router.get("/home")
def get_home_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/generate-password")
async def generate_password(
        length: int = Query(..., ge=8, description="Length of the password"),
        use_special_chars: bool = Query(False, description="Use special characters"),
        use_uppercase: bool = Query(False, description="Use uppercase letters"),
        language: str = Query("en", description="Language for the password")
):
    if length < 8:
        return {"error": "Password length must be at least 8 characters"}

    characters = string.ascii_letters + string.digits
    if use_special_chars:
        characters += string.punctuation
    if use_uppercase:
        characters = characters.upper()

    password = ''.join(random.choices(characters, k=length))
    hashed_password = pwd_context.hash(password)
    return {"password": password, "hashed_password": hashed_password}

