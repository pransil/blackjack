# Blackjack Game - built using my repo at claude-code-automation-framework

The real point here is not the BlackJack game but that it was built in less than 1 hour by my claude-code-automation-framework without me typing a single line of code. It figured out where to find the rule, how to use React, etc. I just answered questions. Check out the repo if you are interested.

A single-player web-based Blackjack game built with React frontend and Python FastAPI backend. This educational game focuses on pure gameplay mechanics without betting, perfect for learning blackjack strategy.

## 🎯 Features

- **Authentic Blackjack Rules**: Standard casino rules implementation
- **Single Player**: Play against the dealer without betting mechanics
- **Game Actions**: Hit, Stand, Double Down (Split capability built-in)
- **Statistics Tracking**: Track wins, losses, pushes, and win rate
- **Responsive Design**: Works on desktop and mobile devices
- **Educational Focus**: Learn proper blackjack strategy without gambling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+

### 1. Backend Setup

```bash
cd deliverables
pip install -r requirements.txt
python src/api.py
```

The API will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd deliverables/src/frontend
npm install
npm start
```

The game will be available at `http://localhost:3000`

## 🎮 How to Play

1. **Open** http://localhost:3000 in your browser
2. **Start** a new game (automatic on first load)
3. **Make decisions**:
   - **Hit**: Take another card
   - **Stand**: End your turn
   - **Double Down**: Double stake, take one card, then stand
4. **Learn** from your statistics and improve your strategy!

## 🏗️ Project Structure

```
deliverables/
├── src/
│   ├── game_engine.py          # Core blackjack game logic
│   ├── api.py                  # FastAPI backend server
│   └── frontend/               # React TypeScript frontend
│       ├── src/
│       │   ├── App.tsx         # Main application
│       │   ├── components/     # UI components
│       │   └── services/       # API client
│       └── package.json
├── test/
│   ├── test_game_engine.py     # Game logic tests
│   ├── test_api.py             # API endpoint tests
│   └── run_tests.py            # Test runner with timestamps
├── docs/
│   ├── README.md               # Detailed documentation
│   └── DEVELOPER_GUIDE.md      # Technical architecture guide
├── requirements.txt            # Python dependencies
└── PRD.md                      # Product Requirements Document
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python deliverables/test/run_tests.py
```

- **38 tests** covering game logic and API endpoints
- **>95% code coverage**
- **Timestamped reports** in `test/reports/`

## 🎲 Game Rules

### Card Values
- **Number cards (2-10)**: Face value
- **Face cards (J, Q, K)**: 10 points
- **Aces**: 11 or 1 (automatically optimized)

### Winning Conditions
- **Player Wins**: Closer to 21 than dealer without busting
- **Dealer Wins**: Dealer closer to 21, or player busts
- **Push**: Both have same value
- **Blackjack**: 21 with first two cards (Ace + 10-value)

### Dealer Rules
- Hits on 16 and below
- Stands on 17 and above

## 🛠️ Technology Stack

### Backend
- **Python 3.12** with FastAPI
- **Game Engine**: Pure Python classes
- **API**: RESTful endpoints
- **Testing**: pytest with comprehensive coverage

### Frontend
- **React 18** with TypeScript
- **Material-UI** for components
- **Axios** for API communication
- **Local Storage** for statistics

## 📚 Documentation

- **[User Guide](deliverables/docs/README.md)**: Complete setup and usage
- **[Developer Guide](deliverables/docs/DEVELOPER_GUIDE.md)**: Architecture and code details
- **[PRD](deliverables/PRD.md)**: Product requirements and specifications

## 🎯 Educational Value

This implementation demonstrates:
- **Clean Architecture**: Separation of concerns
- **Test-Driven Development**: Comprehensive test suite
- **Modern Web Stack**: React + FastAPI best practices
- **Game Development**: State machines and rule implementation

## 🤝 Contributing

This project was built using the Claude Code Automation Framework, demonstrating systematic development practices and professional code quality standards.

## 📄 License

Educational project - feel free to use and modify for learning purposes.

---

**Ready to play?** Start both servers and visit http://localhost:3000 to begin your blackjack journey!
