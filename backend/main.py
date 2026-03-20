import os
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load backend/.env when running locally (Gmail SMTP vars, etc.)
load_dotenv(Path(__file__).resolve().parent / ".env")

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://keepmesafe.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactRequest(BaseModel):
    name: str
    email: str
    message: str


def send_email(subject: str, body: str, recipient: str) -> None:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL", smtp_user or "")

    if not smtp_host or not smtp_user or not smtp_password or not from_email:
        raise RuntimeError(
            "SMTP config missing. Set SMTP_HOST, SMTP_USER, SMTP_PASSWORD, and FROM_EMAIL."
        )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = recipient

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, [recipient], msg.as_string())


@app.get("/")
def read_root():
    return {"message": "Welcome to KeepMeSafe API"}


@app.post("/contact")
def submit_contact_form(payload: ContactRequest):
    owner_email = os.getenv("CONTACT_RECEIVER_EMAIL", os.getenv("SMTP_USER", ""))
    if not owner_email:
        raise HTTPException(
            status_code=500,
            detail="CONTACT_RECEIVER_EMAIL is not configured on the backend.",
        )

    owner_subject = f"New Contact Form Message from {payload.name}"
    owner_body = (
        f"Name: {payload.name}\n"
        f"Email: {payload.email}\n\n"
        f"Message:\n{payload.message}\n"
    )

    auto_reply_subject = "Thanks for contacting KeepMeSafe"
    auto_reply_body = (
        f"Hi {payload.name},\n\n"
        "Thank you for contacting us. We received your message and will contact you shortly.\n\n"
        "Best regards,\nKeepMeSafe Team"
    )

    try:
        send_email(owner_subject, owner_body, owner_email)
        send_email(auto_reply_subject, auto_reply_body, str(payload.email))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Email send failed: {exc}") from exc

    return {
        "message": "Your message has been sent successfully. We will contact you shortly.",
        "sent_to": owner_email,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
