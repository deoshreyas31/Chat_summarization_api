from fastapi import FastAPI, HTTPException
from app.database import database
from app.routes import chats  # ✅ Import the chats router
from fastapi import FastAPI
from app.routes.chats import router as chats_router
from fastapi import FastAPI
from app.routes import chats
import os
import nltk
from fastapi import FastAPI
from app.routes.websockets import router as websocket_router
from fastapi import FastAPI
from app.routes import websockets
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.websockets import router as websocket_router
nltk_data_path = r"C:\Users\Sensei\AppData\Roaming\nltk_data"
os.environ["NLTK_DATA"] = nltk_data_path
nltk.data.path.append(nltk_data_path)

nltk.download("punkt")

app = FastAPI(title="Chat Summarization API")
@app.get("/")
def home():
    return {"message": "Chat Summarization API is running!"}
# ✅ Root endpoint
@app.get("/")
async def root():
    return {"message": "Chat Summarization API is running!"}

@app.get("/test-db")
async def test_db():
    try:
        await database.client.admin.command("ping")  # ✅ Corrected
        return {"message": "MongoDB Connection Successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Register API routes
app.include_router(chats_router)
app.include_router(chats.router, prefix="/api")
app.include_router(chats.router, prefix="/api")
app.include_router(chats.router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔴 Change this to specific domains in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include WebSocket Router
app.include_router(websocket_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
