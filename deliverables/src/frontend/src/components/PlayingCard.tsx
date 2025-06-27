import React from 'react';
import { Box } from '@mui/material';
import { Card } from '../services/apiClient';

interface PlayingCardProps {
  card: Card;
  hidden?: boolean;
}

const PlayingCard: React.FC<PlayingCardProps> = ({ card, hidden = false }) => {
  const isRed = card.suit === '♥' || card.suit === '♦';
  
  if (hidden) {
    return (
      <Box className="playing-card hidden">
        <span>?</span>
        <span>?</span>
        <span>?</span>
      </Box>
    );
  }

  return (
    <Box className={`playing-card ${isRed ? 'red' : ''}`}>
      <span className="card-rank">{card.rank}</span>
      <span className="card-suit">{card.suit}</span>
      <span className="card-rank" style={{ transform: 'rotate(180deg)' }}>
        {card.rank}
      </span>
    </Box>
  );
};

export default PlayingCard;