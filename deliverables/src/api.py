"""
FastAPI backend for Blackjack Game
RESTful API endpoints for game operations.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uuid
from game_engine import BlackjackGame

app = FastAPI(title="Blackjack Game API", version="1.0.0")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory game session storage
games: Dict[str, BlackjackGame] = {}


class GameResponse(BaseModel):
    session_id: str
    game_state: Dict[str, Any]


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Blackjack Game API is running"}


@app.post("/game/new", response_model=GameResponse)
async def new_game():
    """Start a new blackjack game."""
    session_id = str(uuid.uuid4())
    game = BlackjackGame()
    game_state = game.start_new_game()
    games[session_id] = game
    
    return GameResponse(session_id=session_id, game_state=game_state)


@app.get("/game/{session_id}", response_model=Dict[str, Any])
async def get_game_state(session_id: str):
    """Get current game state."""
    if session_id not in games:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    game = games[session_id]
    return game.get_game_state()


@app.post("/game/{session_id}/hit", response_model=Dict[str, Any])
async def hit(session_id: str):
    """Player hits (takes another card)."""
    if session_id not in games:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    game = games[session_id]
    try:
        return game.hit()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/game/{session_id}/stand", response_model=Dict[str, Any])
async def stand(session_id: str):
    """Player stands (ends their turn)."""
    if session_id not in games:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    game = games[session_id]
    try:
        return game.stand()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/game/{session_id}/double-down", response_model=Dict[str, Any])
async def double_down(session_id: str):
    """Player doubles down (hit once then stand)."""
    if session_id not in games:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    game = games[session_id]
    try:
        return game.double_down()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/game/{session_id}")
async def end_game(session_id: str):
    """End game and clean up session."""
    if session_id not in games:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    del games[session_id]
    return {"message": "Game session ended"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)