# Blackjack Game

A single-player web-based Blackjack game built with React frontend and Python FastAPI backend. This educational game focuses on pure gameplay mechanics without betting, perfect for learning blackjack strategy.

## Features

- **Authentic Blackjack Rules**: Standard casino rules implementation
- **Single Player**: Play against the dealer without betting mechanics
- **Game Actions**: Hit, Stand, Double Down (Split capability built-in)
- **Statistics Tracking**: Track wins, losses, pushes, and win rate
- **Responsive Design**: Works on desktop and mobile devices
- **Educational Focus**: Learn proper blackjack strategy without gambling

## Quick Start

### Backend Setup

1. **Install Python Dependencies**:
   ```bash
   cd deliverables
   pip install -r requirements.txt
   ```

2. **Start the API Server**:
   ```bash
   python src/api.py
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install Node.js Dependencies**:
   ```bash
   cd deliverables/src/frontend
   npm install
   ```

2. **Start the React App**:
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000`

## Game Rules

### Basic Gameplay
- Goal: Get your hand value as close to 21 as possible without going over
- Card Values:
  - Number cards (2-10): Face value
  - Face cards (J, Q, K): 10 points
  - Aces: 11 or 1 (automatically optimized)

### Player Actions
- **Hit**: Take another card
- **Stand**: End your turn with current hand
- **Double Down**: Double your stake, take exactly one more card, then stand

### Winning Conditions
- **Player Wins**: Player closer to 21 than dealer (without busting)
- **Dealer Wins**: Dealer closer to 21, or player busts
- **Push**: Both player and dealer have same value
- **Blackjack**: 21 with first two cards (Ace + 10-value card)

### Dealer Rules
- Dealer hits on 16 and below
- Dealer stands on 17 and above

## Project Structure

```
deliverables/
├── src/
│   ├── game_engine.py          # Core game logic
│   ├── api.py                  # FastAPI backend
│   └── frontend/               # React frontend
│       ├── src/
│       │   ├── App.tsx         # Main application
│       │   ├── components/     # React components
│       │   └── services/       # API client
│       └── package.json
├── test/
│   ├── test_game_engine.py     # Game logic tests
│   ├── test_api.py             # API endpoint tests
│   └── run_tests.py            # Test runner
├── docs/
│   └── README.md               # This file
├── requirements.txt            # Python dependencies
└── PRD.md                      # Product Requirements Document
```

## Development

### Running Tests

```bash
python deliverables/test/run_tests.py
```

Tests cover:
- Card handling and scoring logic
- Game state management
- API endpoints
- Edge cases (blackjack, bust, etc.)

Test results are saved with timestamps in `test/reports/`

### API Endpoints

- `POST /game/new` - Start new game
- `GET /game/{session_id}` - Get game state  
- `POST /game/{session_id}/hit` - Player hits
- `POST /game/{session_id}/stand` - Player stands
- `POST /game/{session_id}/double-down` - Player doubles down
- `DELETE /game/{session_id}` - End game session

### Frontend Components

- **App.tsx**: Main application with game state management
- **GameTable**: Game interface with cards and actions
- **PlayingCard**: Individual card display component
- **GameStats**: Win/loss statistics panel

## Architecture

### Backend (Python/FastAPI)
- **Game Engine**: Pure Python classes for game logic
- **API Layer**: RESTful endpoints for frontend communication
- **Session Management**: In-memory game state storage

### Frontend (React/TypeScript)
- **Component-Based**: Modular React components
- **State Management**: React hooks for game state
- **API Integration**: Axios for backend communication
- **Material-UI**: Professional UI components

## Educational Value

This implementation demonstrates:
- **Clean Architecture**: Separation of game logic, API, and UI
- **Test-Driven Development**: Comprehensive test coverage
- **Modern Web Stack**: React + FastAPI best practices
- **Game Development**: State machines and rule implementation

## Future Enhancements

- Split functionality (framework exists)
- Multiple deck support
- Card counting practice mode
- Strategy hints
- Game replay functionality