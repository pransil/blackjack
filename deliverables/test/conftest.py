"""
Pytest configuration and fixtures for Blackjack Game tests.
"""

import pytest
import sys
import os

# Add src directory to Python path for all tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def sample_cards():
    """Fixture providing sample cards for testing."""
    from game_engine import Card, Suit, Rank
    
    return {
        'ace_hearts': Card(Suit.HEARTS, Rank.ACE),
        'king_spades': Card(Suit.SPADES, Rank.KING),
        'five_diamonds': Card(Suit.DIAMONDS, Rank.FIVE),
        'eight_clubs': Card(Suit.CLUBS, Rank.EIGHT),
        'ten_hearts': Card(Suit.HEARTS, Rank.TEN),
    }

@pytest.fixture
def fresh_game():
    """Fixture providing a fresh BlackjackGame instance."""
    from game_engine import BlackjackGame
    return BlackjackGame()

@pytest.fixture
def started_game():
    """Fixture providing a BlackjackGame with a started game."""
    from game_engine import BlackjackGame
    game = BlackjackGame()
    game.start_new_game()
    return game