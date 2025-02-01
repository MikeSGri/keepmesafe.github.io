from fastapi import APIRouter, HTTPException, Form
import secrets

router = APIRouter()

# CSRF Token
CSRF_TOKEN = secrets.token_urlsafe(32)

@router.post("/submit")
async def submit_form(name: str = Form(...), email: str = Form(...), csrf_token: str = Form(...)):
    if csrf_token != CSRF_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    
    return {"message": "Form submitted securely"}
