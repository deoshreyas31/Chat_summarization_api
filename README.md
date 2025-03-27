# Chat Summarization API

## 📌 Project Overview
The **Chat Summarization API** is a FastAPI-based system that ingests chat messages, stores them in MongoDB, and generates AI-powered summaries and insights using an LLM (Large Language Model). The API supports real-time chat ingestion, retrieval, summarization, and sentiment analysis. WebSockets enable live summarization, and Docker simplifies deployment.

## ⚙️ Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** MongoDB
- **LLM Integration:** OpenAI API
- **Real-time:** WebSockets
- **Containerization:** Docker & Docker Compose
- **Deployment:** Cloud (AWS/GCP/Render)

---
## 🚀 How to Run the Project

### 1️⃣ Prerequisites
Ensure you have the following installed:
- Python (>=3.10)
- Docker & Docker Compose
- MongoDB (if running locally)
- OpenAI API Key

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/ChatSummarizationAPI.git
cd ChatSummarizationAPI
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file in the root directory and add:
```ini
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=mongodb://mongo:27017/chatdb
```

### 4️⃣ Install Dependencies (For Local Development)
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
pip install -r requirements.txt
```

### 5️⃣ Start MongoDB (If Running Locally)
```bash
mongod --dbpath ./data/db
```

### 6️⃣ Run the FastAPI Server Locally
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
API will be available at: **http://localhost:8000/docs**

---
## 🐳 Running with Docker
### 1️⃣ Build and Start the Containers
```bash
docker-compose up --build -d
```

### 2️⃣ Verify Running Containers
```bash
docker ps
```
You should see containers running for `chat-api` (FastAPI) and `chat-db` (MongoDB).

### 3️⃣ Stop Containers
```bash
docker-compose down
```

---
## 📡 API Endpoints
### 1️⃣ Store Chat Messages
**POST /chats**  
_Store new chat messages in the database._
#### Request:
```json
{
  "user_id": "12345",
  "conversation_id": "abc123",
  "messages": [
    { "timestamp": "2025-03-28T12:00:00Z", "text": "Hello!" },
    { "timestamp": "2025-03-28T12:01:00Z", "text": "How are you?" }
  ]
}
```
#### Response:
```json
{ "message": "Chat stored successfully" }
```

### 2️⃣ Retrieve Chat History
**GET /chats/{conversation_id}**  
_Get all messages in a conversation._
#### Response:
```json
{
  "conversation_id": "abc123",
  "messages": [
    { "timestamp": "2025-03-28T12:00:00Z", "text": "Hello!" }
  ]
}
```

### 3️⃣ Summarize Chat
**POST /chats/summarize**  
_Generate an AI-powered summary for a conversation._
#### Request:
```json
{ "conversation_id": "abc123" }
```
#### Response:
```json
{ "summary": "User greeted and asked about well-being." }
```

### 4️⃣ Real-time Summarization via WebSocket
**WS /ws/chat**  
_Stream live summaries as messages are received._
#### Example:
```python
import websockets
import asyncio

async def test_ws():
    async with websockets.connect("ws://localhost:8000/ws/chat") as ws:
        await ws.send("{\"conversation_id\": \"abc123\"}")
        summary = await ws.recv()
        print(summary)

asyncio.run(test_ws())
```

---
## 🛠️ Troubleshooting & Logs

### Check Logs
```bash
docker logs chat-api -f
```

### Common Issues
#### 1️⃣ Docker Errors: `Error: Cannot connect to MongoDB`
- Ensure MongoDB container is running (`docker ps`)
- Try restarting: `docker-compose down && docker-compose up --build -d`

#### 2️⃣ API Not Responding
- Check if FastAPI is running (`docker ps` or `uvicorn` logs)
- Restart server: `docker restart chat-api`

#### 3️⃣ LLM Summarization Fails
- Ensure your OpenAI API key is correct
- Check OpenAI API limits

---


🚀 **Happy Coding!**

