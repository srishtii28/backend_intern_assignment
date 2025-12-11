from fastapi import APIRouter, HTTPException
from app.schemas.user import LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/admin")

@router.post("/login")
async def login(data: LoginRequest):
    token = await AuthService.login(data.email, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token}
