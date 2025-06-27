"""
Comprehensive test suite for Blackjack Game Engine
Tests core game logic, card handling, and game states.
"""

import pytest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game_engine import (
    Card, Suit, Rank, Hand, Deck, BlackjackGame, 
    GameState, GameResult
)


class TestCard:
    def test_card_creation(self):
        card = Card(Suit.HEARTS, Rank.ACE)
        assert card.suit == Suit.HEARTS
        assert card.rank == Rank.ACE
        assert card.value == 11
        assert str(card) == "A♥"

    def test_face_card_values(self):
        king = Card(Suit.SPADES, Rank.KING)
        queen = Card(Suit.DIAMONDS, Rank.QUEEN)
        jack = Card(Suit.CLUBS, Rank.JACK)
        
        assert king.value == 10
        assert queen.value == 10
        assert jack.value == 10

    def test_number_card_values(self):
        two = Card(Suit.HEARTS, Rank.TWO)
        five = Card(Suit.SPADES, Rank.FIVE)
        ten = Card(Suit.DIAMONDS, Rank.TEN)
        
        assert two.value == 2
        assert five.value == 5
        assert ten.value == 10


class TestHand:
    def test_empty_hand(self):
        hand = Hand([])
        assert hand.get_value() == 0
        assert not hand.is_bust()
        assert not hand.is_blackjack()

    def test_simple_hand_value(self):
        hand = Hand([
            Card(Suit.HEARTS, Rank.FIVE),
            Card(Suit.SPADES, Rank.SEVEN)
        ])
        assert hand.get_value() == 12

    def test_ace_handling_soft_hand(self):
        # Ace + 6 = 17 (soft)
        hand = Hand([
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.SPADES, Rank.SIX)
        ])
        assert hand.get_value() == 17

    def test_ace_handling_hard_hand(self):
        # Ace + 6 + 8 = 15 (ace becomes 1)
        hand = Hand([
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.SPADES, Rank.SIX),
            Card(Suit.DIAMONDS, Rank.EIGHT)
        ])
        assert hand.get_value() == 15

    def test_multiple_aces(self):
        # Ace + Ace + 9 = 21 (one ace = 11, other = 1)
        hand = Hand([
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.NINE)
        ])
        assert hand.get_value() == 21

    def test_blackjack_detection(self):
        # Ace + King = Blackjack
        hand = Hand([
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.SPADES, Rank.KING)
        ])
        assert hand.is_blackjack()
        assert hand.get_value() == 21

        # 21 with 3 cards is not blackjack
        hand_three_cards = Hand([
            Card(Suit.HEARTS, Rank.SEVEN),
            Card(Suit.SPADES, Rank.SEVEN),
            Card(Suit.DIAMONDS, Rank.SEVEN)
        ])
        assert not hand_three_cards.is_blackjack()
        assert hand_three_cards.get_value() == 21

    def test_bust_detection(self):
        hand = Hand([
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.DIAMONDS, Rank.FIVE)
        ])
        assert hand.is_bust()
        assert hand.get_value() == 25

    def test_can_split(self):
        # Two cards of same rank can be split
        hand = Hand([
            Card(Suit.HEARTS, Rank.EIGHT),
            Card(Suit.SPADES, Rank.EIGHT)
        ])
        assert hand.can_split()

        # Different ranks cannot be split
        hand_different = Hand([
            Card(Suit.HEARTS, Rank.EIGHT),
            Card(Suit.SPADES, Rank.NINE)
        ])
        assert not hand_different.can_split()

        # More than 2 cards cannot be split
        hand_three = Hand([
            Card(Suit.HEARTS, Rank.EIGHT),
            Card(Suit.SPADES, Rank.EIGHT),
            Card(Suit.DIAMONDS, Rank.TWO)
        ])
        assert not hand_three.can_split()


class TestDeck:
    def test_deck_creation(self):
        deck = Deck()
        assert len(deck.cards) == 52

    def test_deck_contains_all_cards(self):
        deck = Deck()
        
        # Check we have all suits and ranks
        suits_found = set()
        ranks_found = set()
        
        for card in deck.cards:
            suits_found.add(card.suit)
            ranks_found.add(card.rank)
        
        assert len(suits_found) == 4
        assert len(ranks_found) == 13

    def test_deck_deal_card(self):
        deck = Deck()
        initial_count = len(deck.cards)
        
        card = deck.deal_card()
        assert isinstance(card, Card)
        assert len(deck.cards) == initial_count - 1

    def test_deck_reset_when_empty(self):
        deck = Deck()
        
        # Deal all cards
        for _ in range(52):
            deck.deal_card()
        
        assert len(deck.cards) == 0
        
        # Next deal should reset deck
        card = deck.deal_card()
        assert isinstance(card, Card)
        assert len(deck.cards) == 51


class TestBlackjackGame:
    def test_game_initialization(self):
        game = BlackjackGame()
        assert game.state == GameState.DEALING
        assert game.result is None

    def test_start_new_game(self):
        game = BlackjackGame()
        state = game.start_new_game()
        
        # Check initial dealing
        assert len(game.player_hand.cards) == 2
        assert len(game.dealer_hand.cards) == 2
        
        # Check game state
        assert game.state in [GameState.PLAYER_TURN, GameState.GAME_OVER]
        
        # Check state dictionary structure
        assert "player_hand" in state
        assert "dealer_hand" in state
        assert "state" in state
        assert "available_actions" in state

    def test_player_hit(self):
        game = BlackjackGame()
        game.start_new_game()
        
        if game.state == GameState.PLAYER_TURN:
            initial_cards = len(game.player_hand.cards)
            game.hit()
            assert len(game.player_hand.cards) == initial_cards + 1

    def test_player_stand(self):
        game = BlackjackGame()
        game.start_new_game()
        
        if game.state == GameState.PLAYER_TURN:
            game.stand()
            assert game.state == GameState.GAME_OVER
            assert game.result is not None

    def test_double_down(self):
        game = BlackjackGame()
        game.start_new_game()
        
        if game.state == GameState.PLAYER_TURN and game.can_double_down:
            initial_cards = len(game.player_hand.cards)
            game.double_down()
            
            # Should add exactly one card and end turn
            assert len(game.player_hand.cards) == initial_cards + 1
            assert game.state in [GameState.DEALER_TURN, GameState.GAME_OVER]

    def test_player_bust_ends_game(self):
        game = BlackjackGame()
        
        # Force a bust scenario
        game.player_hand = Hand([
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN)
        ])
        game.state = GameState.PLAYER_TURN
        
        # Add a card that will cause bust
        game.player_hand.add_card(Card(Suit.DIAMONDS, Rank.FIVE))
        
        # Simulate hit that causes bust
        if game.player_hand.is_bust():
            game.result = GameResult.DEALER_WIN
            game.state = GameState.GAME_OVER
        
        assert game.result == GameResult.DEALER_WIN
        assert game.state == GameState.GAME_OVER

    def test_blackjack_scenarios(self):
        game = BlackjackGame()
        
        # Player blackjack, dealer no blackjack
        game.player_hand = Hand([
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.SPADES, Rank.KING)
        ])
        game.dealer_hand = Hand([
            Card(Suit.HEARTS, Rank.NINE),
            Card(Suit.SPADES, Rank.EIGHT)
        ])
        
        assert game.player_hand.is_blackjack()
        assert not game.dealer_hand.is_blackjack()

    def test_game_state_serialization(self):
        game = BlackjackGame()
        state = game.start_new_game()
        
        # Verify all required fields are present
        required_fields = [
            "player_hand", "dealer_hand", "state", 
            "result", "available_actions"
        ]
        
        for field in required_fields:
            assert field in state
        
        # Check hand structure
        assert "cards" in state["player_hand"]
        assert "value" in state["player_hand"]
        assert "cards" in state["dealer_hand"]

    def test_dealer_play_logic(self):
        game = BlackjackGame()
        
        # Set up scenario where dealer must hit
        game.dealer_hand = Hand([
            Card(Suit.HEARTS, Rank.SEVEN),
            Card(Suit.SPADES, Rank.NINE)  # Total: 16
        ])
        game.player_hand = Hand([
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.SPADES, Rank.NINE)  # Total: 19
        ])
        game.state = GameState.DEALER_TURN
        
        # Dealer should hit on 16
        initial_value = game.dealer_hand.get_value()
        assert initial_value == 16
        
        # Simulate dealer play
        game._dealer_play()
        
        # Dealer should have hit and game should be over
        assert game.state == GameState.GAME_OVER
        assert game.result is not None

    def test_invalid_actions(self):
        game = BlackjackGame()
        game.start_new_game()
        
        # Try to hit when it's not player's turn
        game.state = GameState.DEALER_TURN
        
        with pytest.raises(ValueError):
            game.hit()
        
        with pytest.raises(ValueError):
            game.stand()
        
        with pytest.raises(ValueError):
            game.double_down()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])