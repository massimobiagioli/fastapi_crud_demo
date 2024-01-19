from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_crud_demo.db import get_session
from fastapi_crud_demo.models.user import User, UserCreate, UserLogin
from fastapi_crud_demo.use_cases import user

router = APIRouter(
    prefix="/api/user",
)


@router.post("/register", response_model=User, status_code=HTTPStatus.CREATED)
async def register(
    data: UserCreate, session: AsyncSession = Depends(get_session)
) -> User:
    return await user.register(session=session, data=data)


@router.post("/login", response_model=dict, status_code=HTTPStatus.OK)
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)) -> dict:
    login_result = await user.login(session=session, data=data)
    if login_result is None:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Login failed")

    if "error" in login_result:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Login failed")

    return login_result
