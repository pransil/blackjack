import React from 'react';
import { Box, Typography, Button, CircularProgress } from '@mui/material';
import { GameState } from '../services/apiClient';
import PlayingCard from './PlayingCard';

interface GameTableProps {
  gameState: GameState | null;
  loading: boolean;
  onAction: (action: 'hit' | 'stand' | 'double-down') => void;
}

const GameTable: React.FC<GameTableProps> = ({ gameState, loading, onAction }) => {
  if (!gameState) {
    return (
      <Box className="game-table">
        <Typography variant="h4">Loading game...</Typography>
      </Box>
    );
  }

  const getResultMessage = (result: string | null) => {
    switch (result) {
      case 'player_win':
        return '🎉 You Win!';
      case 'player_blackjack':
        return '🃏 Blackjack! You Win!';
      case 'dealer_win':
        return '😞 Dealer Wins';
      case 'push':
        return '🤝 Push (Tie)';
      default:
        return '';
    }
  };

  return (
    <Box className="game-table">
      {/* Dealer Section */}
      <Box className="hand-section">
        <Typography variant="h5" gutterBottom>
          Dealer
        </Typography>
        <Box className="cards-container">
          {gameState.dealer_hand.cards.map((card, index) => (
            <PlayingCard
              key={index}
              card={card}
              hidden={index === 1 && gameState.dealer_hand.hidden_card}
            />
          ))}
        </Box>
        <Typography variant="h6" className="hand-value">
          {gameState.dealer_hand.hidden_card 
            ? `Value: ${gameState.dealer_hand.cards[0].rank === 'A' ? '11' : 
                (gameState.dealer_hand.cards[0].rank === 'K' || 
                 gameState.dealer_hand.cards[0].rank === 'Q' || 
                 gameState.dealer_hand.cards[0].rank === 'J') ? '10' : 
                 gameState.dealer_hand.cards[0].rank} + ?`
            : `Value: ${gameState.dealer_hand.value}`
          }
          {gameState.dealer_hand.is_blackjack && !gameState.dealer_hand.hidden_card && ' (Blackjack!)'}
          {gameState.dealer_hand.is_bust && ' (Bust!)'}
        </Typography>
      </Box>

      {/* Game Result */}
      {gameState.result && (
        <Box className="game-result">
          <Typography variant="h4">
            {getResultMessage(gameState.result)}
          </Typography>
        </Box>
      )}

      {/* Player Section */}
      <Box className="hand-section">
        <Typography variant="h5" gutterBottom>
          Your Hand
        </Typography>
        <Box className="cards-container">
          {gameState.player_hand.cards.map((card, index) => (
            <PlayingCard key={index} card={card} />
          ))}
        </Box>
        <Typography variant="h6" className="hand-value">
          Value: {gameState.player_hand.value}
          {gameState.player_hand.is_blackjack && ' (Blackjack!)'}
          {gameState.player_hand.is_bust && ' (Bust!)'}
        </Typography>
      </Box>

      {/* Action Buttons */}
      {gameState.state === 'player_turn' && (
        <Box className="actions-container">
          <Button
            variant="contained"
            color="primary"
            onClick={() => onAction('hit')}
            disabled={loading || !gameState.available_actions.can_hit}
            startIcon={loading ? <CircularProgress size={20} /> : null}
          >
            Hit
          </Button>
          <Button
            variant="contained"
            color="secondary"
            onClick={() => onAction('stand')}
            disabled={loading || !gameState.available_actions.can_stand}
          >
            Stand
          </Button>
          {gameState.available_actions.can_double_down && (
            <Button
              variant="outlined"
              onClick={() => onAction('double-down')}
              disabled={loading}
            >
              Double Down
            </Button>
          )}
        </Box>
      )}

      {/* Game Status */}
      {gameState.state === 'dealer_turn' && (
        <Typography variant="h6">
          Dealer is playing...
        </Typography>
      )}
    </Box>
  );
};

export default GameTable;