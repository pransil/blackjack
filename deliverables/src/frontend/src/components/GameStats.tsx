import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

interface GameStatsProps {
  stats: {
    wins: number;
    losses: number;
    pushes: number;
    hands: number;
  };
}

const GameStats: React.FC<GameStatsProps> = ({ stats }) => {
  const winRate = stats.hands > 0 ? ((stats.wins / stats.hands) * 100).toFixed(1) : '0.0';

  return (
    <Paper className="stats-card">
      <Typography variant="h6" gutterBottom>
        Game Statistics
      </Typography>
      
      <Box className="stat-item">
        <span>Hands Played:</span>
        <span className="stat-value">{stats.hands}</span>
      </Box>
      
      <Box className="stat-item">
        <span>Wins:</span>
        <span className="stat-value" style={{ color: '#28a745' }}>{stats.wins}</span>
      </Box>
      
      <Box className="stat-item">
        <span>Losses:</span>
        <span className="stat-value" style={{ color: '#dc3545' }}>{stats.losses}</span>
      </Box>
      
      <Box className="stat-item">
        <span>Pushes:</span>
        <span className="stat-value" style={{ color: '#6c757d' }}>{stats.pushes}</span>
      </Box>
      
      <Box className="stat-item">
        <span>Win Rate:</span>
        <span className="stat-value" style={{ color: '#007bff' }}>{winRate}%</span>
      </Box>
    </Paper>
  );
};

export default GameStats;