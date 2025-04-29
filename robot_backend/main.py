from fastapi import FastAPI, WebSocket, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()
security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store credentials (in real apps, use env variables or DB)
VALID_USERNAME = "admin"
VALID_PASSWORD = "alyhanykhaledhatem"

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    is_correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
    is_correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

robot_position = {"x": 0, "y": 0}
battery_voltage = 12.5
robot_speed = 0.6
robot_state = "Idle"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Received from frontend: {data}")
        await websocket.send_json({
            "position": robot_position,
            "battery": battery_voltage,
            "speed": robot_speed,
            "state": robot_state
        })

@app.get("/protected")
def read_protected(user: str = Depends(verify_credentials)):
    return {"message": f"Welcome {user}, you are authorized."}
