"""
Blackjack Game Engine
Core game logic for single-player blackjack without betting.
"""

import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional


class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Rank(Enum):
    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (10, "J")
    QUEEN = (10, "Q")
    KING = (10, "K")
    ACE = (11, "A")

    def __init__(self, card_value: int, display: str):
        self.card_value = card_value
        self.display = display


@dataclass
class Card:
    suit: Suit
    rank: Rank
    
    def __str__(self) -> str:
        return f"{self.rank.display}{self.suit.value}"
    
    @property
    def value(self) -> int:
        return self.rank.card_value


class GameState(Enum):
    DEALING = "dealing"
    PLAYER_TURN = "player_turn"
    DEALER_TURN = "dealer_turn"
    GAME_OVER = "game_over"


class GameResult(Enum):
    PLAYER_WIN = "player_win"
    DEALER_WIN = "dealer_win"
    PUSH = "push"
    PLAYER_BLACKJACK = "player_blackjack"


@dataclass
class Hand:
    cards: List[Card]
    
    def __post_init__(self):
        if not self.cards:
            self.cards = []
    
    def add_card(self, card: Card) -> None:
        """Add a card to the hand."""
        self.cards.append(card)
    
    def get_value(self) -> int:
        """Calculate the best possible value of the hand."""
        total = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == Rank.ACE:
                aces += 1
                total += 11
            else:
                total += card.value
        
        # Adjust for aces
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        return total
    
    def is_bust(self) -> bool:
        """Check if hand is bust (over 21)."""
        return self.get_value() > 21
    
    def is_blackjack(self) -> bool:
        """Check if hand is blackjack (21 with 2 cards)."""
        return len(self.cards) == 2 and self.get_value() == 21
    
    def can_split(self) -> bool:
        """Check if hand can be split."""
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank
    
    def __str__(self) -> str:
        return " ".join(str(card) for card in self.cards)


class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()
    
    def reset(self) -> None:
        """Create a fresh deck and shuffle."""
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))
        self.shuffle()
    
    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)
    
    def deal_card(self) -> Card:
        """Deal one card from the deck."""
        if not self.cards:
            self.reset()
        return self.cards.pop()


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand([])
        self.dealer_hand = Hand([])
        self.state = GameState.DEALING
        self.result: Optional[GameResult] = None
        self.can_double_down = False
        self.can_split = False
    
    def start_new_game(self) -> dict:
        """Start a new game of blackjack."""
        self.deck = Deck()
        self.player_hand = Hand([])
        self.dealer_hand = Hand([])
        self.state = GameState.DEALING
        self.result = None
        
        # Deal initial cards
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        
        # Set available actions
        self.can_double_down = True
        self.can_split = self.player_hand.can_split()
        
        # Check for immediate blackjack
        if self.player_hand.is_blackjack():
            if self.dealer_hand.is_blackjack():
                self.result = GameResult.PUSH
            else:
                self.result = GameResult.PLAYER_BLACKJACK
            self.state = GameState.GAME_OVER
        else:
            self.state = GameState.PLAYER_TURN
        
        return self.get_game_state()
    
    def hit(self) -> dict:
        """Player hits (takes another card)."""
        if self.state != GameState.PLAYER_TURN:
            raise ValueError("Cannot hit at this time")
        
        self.player_hand.add_card(self.deck.deal_card())
        self.can_double_down = False
        self.can_split = False
        
        if self.player_hand.is_bust():
            self.result = GameResult.DEALER_WIN
            self.state = GameState.GAME_OVER
        
        return self.get_game_state()
    
    def stand(self) -> dict:
        """Player stands (ends their turn)."""
        if self.state != GameState.PLAYER_TURN:
            raise ValueError("Cannot stand at this time")
        
        self.state = GameState.DEALER_TURN
        return self._dealer_play()
    
    def double_down(self) -> dict:
        """Player doubles down (hit once then stand)."""
        if self.state != GameState.PLAYER_TURN or not self.can_double_down:
            raise ValueError("Cannot double down at this time")
        
        self.player_hand.add_card(self.deck.deal_card())
        self.can_double_down = False
        self.can_split = False
        
        if self.player_hand.is_bust():
            self.result = GameResult.DEALER_WIN
            self.state = GameState.GAME_OVER
        else:
            self.state = GameState.DEALER_TURN
            return self._dealer_play()
        
        return self.get_game_state()
    
    def _dealer_play(self) -> dict:
        """Execute dealer's turn according to blackjack rules."""
        self.state = GameState.DEALER_TURN
        
        # Dealer hits on 16 and below, stands on 17 and above
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
        
        # Determine winner
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        if self.dealer_hand.is_bust():
            self.result = GameResult.PLAYER_WIN
        elif player_value > dealer_value:
            self.result = GameResult.PLAYER_WIN
        elif dealer_value > player_value:
            self.result = GameResult.DEALER_WIN
        else:
            self.result = GameResult.PUSH
        
        self.state = GameState.GAME_OVER
        return self.get_game_state()
    
    def get_game_state(self) -> dict:
        """Get current game state for API/frontend."""
        return {
            "player_hand": {
                "cards": [{"suit": card.suit.value, "rank": card.rank.display} for card in self.player_hand.cards],
                "value": self.player_hand.get_value(),
                "is_bust": self.player_hand.is_bust(),
                "is_blackjack": self.player_hand.is_blackjack()
            },
            "dealer_hand": {
                "cards": [{"suit": card.suit.value, "rank": card.rank.display} for card in self.dealer_hand.cards],
                "value": self.dealer_hand.get_value() if self.state in [GameState.DEALER_TURN, GameState.GAME_OVER] else "hidden",
                "is_bust": self.dealer_hand.is_bust(),
                "is_blackjack": self.dealer_hand.is_blackjack(),
                "hidden_card": self.state == GameState.PLAYER_TURN
            },
            "state": self.state.value,
            "result": self.result.value if self.result else None,
            "available_actions": {
                "can_hit": self.state == GameState.PLAYER_TURN,
                "can_stand": self.state == GameState.PLAYER_TURN,
                "can_double_down": self.state == GameState.PLAYER_TURN and self.can_double_down,
                "can_split": self.state == GameState.PLAYER_TURN and self.can_split
            }
        }