from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from collections import defaultdict

router = APIRouter()

# Store active WebSocket connections
active_connections = defaultdict(set)

@router.websocket("/ws/{conversation_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str, user_id: str):
    """
    WebSocket API for receiving chat messages and returning real-time summaries.
    """
    await websocket.accept()  # ✅ Explicitly Accept the Connection

    # Add the WebSocket to the active connections list
    active_connections[conversation_id].add(websocket)

    try:
        messages = []  # Store messages for summarization
        while True:
            message = await websocket.receive_text()
            messages.append(message)

            # Generate a summary (Dummy function for now)
            summary = f"Summary of {len(messages)} messages."

            # ✅ Send the summary to all connected clients
            for connection in list(active_connections[conversation_id]):
                if connection.client_state == WebSocketState.CONNECTED:
                    await connection.send_text(summary)

    except WebSocketDisconnect:
        active_connections[conversation_id].remove(websocket)
