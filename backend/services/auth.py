from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy User Database
fake_users_db = {
    "user@example.com": {"password": pwd_context.hash("securepassword")}
}

def authenticate_user(email: str, password: str):
    if email in fake_users_db and pwd_context.verify(password, fake_users_db[email]["password"]):
        return True
    return False

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": "secure_generated_token", "token_type": "bearer"}
