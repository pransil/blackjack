import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Button, Alert } from '@mui/material';
import GameTable from './components/GameTable';
import GameStats from './components/GameStats';
import { GameState, ApiClient } from './services/apiClient';
import './App.css';

const App: React.FC = () => {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState({
    wins: 0,
    losses: 0,
    pushes: 0,
    hands: 0
  });

  const apiClient = new ApiClient();

  const startNewGame = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.newGame();
      setSessionId(response.session_id);
      setGameState(response.game_state);
      
      // Update stats
      if (gameState?.result) {
        updateStats(gameState.result);
      }
    } catch (err) {
      setError('Failed to start new game');
    } finally {
      setLoading(false);
    }
  };

  const updateStats = (result: string) => {
    setStats(prev => ({
      ...prev,
      hands: prev.hands + 1,
      wins: result === 'player_win' || result === 'player_blackjack' ? prev.wins + 1 : prev.wins,
      losses: result === 'dealer_win' ? prev.losses + 1 : prev.losses,
      pushes: result === 'push' ? prev.pushes + 1 : prev.pushes
    }));
  };

  const makeMove = async (action: 'hit' | 'stand' | 'double-down') => {
    if (!sessionId) return;
    
    setLoading(true);
    setError(null);
    try {
      let newState;
      switch (action) {
        case 'hit':
          newState = await apiClient.hit(sessionId);
          break;
        case 'stand':
          newState = await apiClient.stand(sessionId);
          break;
        case 'double-down':
          newState = await apiClient.doubleDown(sessionId);
          break;
      }
      setGameState(newState);
      
      // Update stats if game is over
      if (newState.state === 'game_over' && newState.result) {
        updateStats(newState.result);
      }
    } catch (err) {
      setError(`Failed to ${action}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    startNewGame();
  }, []);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom align="center">
        Blackjack
      </Typography>
      
      <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
        <Box sx={{ flex: 1, minWidth: '600px' }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          
          <GameTable 
            gameState={gameState}
            loading={loading}
            onAction={makeMove}
          />
          
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Button
              variant="contained"
              color="primary"
              onClick={startNewGame}
              disabled={loading}
              size="large"
            >
              New Game
            </Button>
          </Box>
        </Box>
        
        <Box sx={{ width: '300px' }}>
          <GameStats stats={stats} />
        </Box>
      </Box>
    </Container>
  );
};

export default App;