# Developer Guide - Blackjack Game

## Code Architecture

### Game Engine (`src/game_engine.py`)

The core game logic is implemented using clean Python classes:

#### Key Classes

**Card**: Represents a playing card
```python
@dataclass
class Card:
    suit: Suit
    rank: Rank
    
    @property
    def value(self) -> int:
        return self.rank.card_value
```

**Hand**: Manages a collection of cards with blackjack scoring
```python
class Hand:
    def get_value(self) -> int:
        # Handles ace optimization automatically
    
    def is_blackjack(self) -> bool:
        # 21 with exactly 2 cards
    
    def can_split(self) -> bool:
        # Two cards of same rank
```

**BlackjackGame**: Main game controller
```python
class BlackjackGame:
    def start_new_game(self) -> dict:
        # Deals initial cards, checks for blackjack
    
    def hit(self) -> dict:
        # Adds card to player hand
    
    def stand(self) -> dict:
        # Ends player turn, triggers dealer play
```

#### State Management

Games progress through these states:
- `DEALING`: Initial card distribution
- `PLAYER_TURN`: Player making decisions
- `DEALER_TURN`: Dealer playing by rules
- `GAME_OVER`: Final result determined

### API Layer (`src/api.py`)

FastAPI provides RESTful endpoints:

```python
@app.post("/game/new")
async def new_game():
    # Creates new game session
    # Returns session_id and initial state

@app.post("/game/{session_id}/hit")
async def hit(session_id: str):
    # Executes hit action
    # Returns updated game state
```

#### Session Management
- Games stored in memory: `games: Dict[str, BlackjackGame]`
- UUID-based session identifiers
- Automatic cleanup on game end

### Frontend Architecture (`src/frontend/`)

React TypeScript application with Material-UI:

#### Component Hierarchy
```
App
├── GameTable
│   ├── PlayingCard (multiple)
│   └── Action buttons
└── GameStats
```

#### State Management
```typescript
const [gameState, setGameState] = useState<GameState | null>(null);
const [sessionId, setSessionId] = useState<string | null>(null);
const [stats, setStats] = useState({wins: 0, losses: 0, ...});
```

#### API Integration
```typescript
class ApiClient {
    async newGame(): Promise<NewGameResponse>
    async hit(sessionId: string): Promise<GameState>
    async stand(sessionId: string): Promise<GameState>
}
```

## Testing Strategy

### Test Coverage

**Game Engine Tests** (`test/test_game_engine.py`):
- Card value calculations
- Ace handling (soft/hard hands)
- Blackjack detection
- Bust conditions
- Game state transitions
- Edge cases

**API Tests** (`test/test_api.py`):
- Endpoint functionality
- Error handling
- Session management
- Game flow integration

### Running Tests

```bash
python deliverables/test/run_tests.py
```

Creates timestamped reports in `test/reports/`

## Development Workflow

### Adding New Features

1. **Update Game Engine**: Add logic to `game_engine.py`
2. **Add API Endpoint**: Create route in `api.py`
3. **Update Frontend**: Add UI components and API calls
4. **Write Tests**: Cover new functionality
5. **Update Documentation**: Document changes

### Code Quality Standards

- **Type Hints**: All Python functions use type annotations
- **Error Handling**: Comprehensive exception handling
- **Testing**: >95% test coverage maintained
- **Documentation**: Docstrings for all public methods

## Key Implementation Details

### Ace Handling
```python
def get_value(self) -> int:
    total = 0
    aces = 0
    
    for card in self.cards:
        if card.rank == Rank.ACE:
            aces += 1
            total += 11
        else:
            total += card.value
    
    # Convert aces from 11 to 1 if needed
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    
    return total
```

### Game State Serialization
```python
def get_game_state(self) -> dict:
    return {
        "player_hand": {
            "cards": [{"suit": card.suit.value, "rank": card.rank.display} 
                     for card in self.player_hand.cards],
            "value": self.player_hand.get_value(),
            "is_blackjack": self.player_hand.is_blackjack()
        },
        "dealer_hand": {
            "hidden_card": self.state == GameState.PLAYER_TURN
        },
        "available_actions": {
            "can_hit": self.state == GameState.PLAYER_TURN,
            "can_double_down": self.can_double_down
        }
    }
```

### Dealer Logic
```python
def _dealer_play(self) -> dict:
    # Dealer hits on 16, stands on 17
    while self.dealer_hand.get_value() < 17:
        self.dealer_hand.add_card(self.deck.deal_card())
    
    # Determine winner
    if self.dealer_hand.is_bust():
        self.result = GameResult.PLAYER_WIN
    # ... other win conditions
```

## Performance Considerations

- **Memory Usage**: Games stored in memory (consider Redis for production)
- **Deck Management**: Auto-reset when empty to prevent stalling
- **Frontend Optimization**: React state updates minimized
- **API Efficiency**: Single round-trip for most actions

## Security Notes

- **Input Validation**: All API inputs validated
- **Session Security**: UUID-based session IDs
- **No Persistence**: Game state not permanently stored
- **CORS**: Configured for development (localhost:3000)

## Deployment

### Production Considerations

1. **Database**: Replace in-memory storage with Redis/PostgreSQL
2. **Authentication**: Add user sessions if needed
3. **CORS**: Configure for production domains
4. **Monitoring**: Add logging and metrics
5. **Scaling**: Consider horizontal scaling for multiple instances

### Docker Deployment

Create `Dockerfile` for backend:
```dockerfile
FROM python:3.12-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Frontend builds to static files for CDN deployment.