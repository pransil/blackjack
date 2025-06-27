"""
Test suite for Blackjack API endpoints
Tests FastAPI routes and game integration.
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api import app

client = TestClient(app)


class TestAPIEndpoints:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Blackjack Game API is running"}

    def test_new_game_endpoint(self):
        response = client.post("/game/new")
        assert response.status_code == 200
        
        data = response.json()
        assert "session_id" in data
        assert "game_state" in data
        
        # Verify game state structure
        game_state = data["game_state"]
        assert "player_hand" in game_state
        assert "dealer_hand" in game_state
        assert "state" in game_state
        assert "available_actions" in game_state
        
        # Check initial dealing
        assert len(game_state["player_hand"]["cards"]) == 2
        assert len(game_state["dealer_hand"]["cards"]) == 2

    def test_get_game_state(self):
        # First create a game
        response = client.post("/game/new")
        session_id = response.json()["session_id"]
        
        # Then get its state
        response = client.get(f"/game/{session_id}")
        assert response.status_code == 200
        
        game_state = response.json()
        assert "player_hand" in game_state
        assert "dealer_hand" in game_state

    def test_get_nonexistent_game(self):
        response = client.get("/game/nonexistent-id")
        assert response.status_code == 404
        assert "Game session not found" in response.json()["detail"]

    def test_player_hit(self):
        # Create new game
        response = client.post("/game/new")
        session_id = response.json()["session_id"]
        initial_state = response.json()["game_state"]
        
        # Skip if game is already over (blackjack scenario)
        if initial_state["state"] == "game_over":
            return
        
        initial_cards = len(initial_state["player_hand"]["cards"])
        
        # Player hits
        response = client.post(f"/game/{session_id}/hit")
        assert response.status_code == 200
        
        new_state = response.json()
        assert len(new_state["player_hand"]["cards"]) == initial_cards + 1

    def test_player_stand(self):
        # Create new game
        response = client.post("/game/new")
        session_id = response.json()["session_id"]
        initial_state = response.json()["game_state"]
        
        # Skip if game is already over
        if initial_state["state"] == "game_over":
            return
        
        # Player stands
        response = client.post(f"/game/{session_id}/stand")
        assert response.status_code == 200
        
        final_state = response.json()
        assert final_state["state"] == "game_over"
        assert final_state["result"] is not None

    def test_double_down(self):
        # Create new game
        response = client.post("/game/new")
        session_id = response.json()["session_id"]
        initial_state = response.json()["game_state"]
        
        # Skip if game is already over or double down not available
        if (initial_state["state"] == "game_over" or 
            not initial_state["available_actions"]["can_double_down"]):
            return
        
        initial_cards = len(initial_state["player_hand"]["cards"])
        
        # Player doubles down
        response = client.post(f"/game/{session_id}/double-down")
        assert response.status_code == 200
        
        final_state = response.json()
        # Should add exactly one card
        assert len(final_state["player_hand"]["cards"]) == initial_cards + 1
        # Game should progress to dealer turn or end
        assert final_state["state"] in ["dealer_turn", "game_over"]

    def test_invalid_actions_on_nonexistent_game(self):
        fake_id = "fake-session-id"
        
        response = client.post(f"/game/{fake_id}/hit")
        assert response.status_code == 404
        
        response = client.post(f"/game/{fake_id}/stand")
        assert response.status_code == 404
        
        response = client.post(f"/game/{fake_id}/double-down")
        assert response.status_code == 404

    def test_end_game(self):
        # Create new game
        response = client.post("/game/new")
        session_id = response.json()["session_id"]
        
        # End the game
        response = client.delete(f"/game/{session_id}")
        assert response.status_code == 200
        assert "Game session ended" in response.json()["message"]
        
        # Verify game is gone
        response = client.get(f"/game/{session_id}")
        assert response.status_code == 404

    def test_multiple_games(self):
        # Create multiple games
        game1_response = client.post("/game/new")
        game2_response = client.post("/game/new")
        
        session1 = game1_response.json()["session_id"]
        session2 = game2_response.json()["session_id"]
        
        assert session1 != session2
        
        # Both games should be accessible
        response1 = client.get(f"/game/{session1}")
        response2 = client.get(f"/game/{session2}")
        
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_game_flow_complete(self):
        """Test a complete game flow from start to finish."""
        # Start new game
        response = client.post("/game/new")
        assert response.status_code == 200
        
        session_id = response.json()["session_id"]
        game_state = response.json()["game_state"]
        
        # If not already over (blackjack), play the game
        if game_state["state"] == "player_turn":
            # Player stands to complete the game quickly
            response = client.post(f"/game/{session_id}/stand")
            assert response.status_code == 200
            
            final_state = response.json()
            assert final_state["state"] == "game_over"
            assert final_state["result"] in [
                "player_win", "dealer_win", "push", "player_blackjack"
            ]
        
        # Clean up
        client.delete(f"/game/{session_id}")

    def test_dealer_hidden_card(self):
        """Test that dealer's second card is hidden during player turn."""
        response = client.post("/game/new")
        game_state = response.json()["game_state"]
        
        if game_state["state"] == "player_turn":
            # Dealer should have hidden card
            assert game_state["dealer_hand"]["hidden_card"] is True
            # Dealer value should be hidden or show partial
            assert game_state["dealer_hand"]["value"] == "hidden"

    def test_available_actions(self):
        """Test that available actions are correctly reported."""
        response = client.post("/game/new")
        game_state = response.json()["game_state"]
        
        actions = game_state["available_actions"]
        
        if game_state["state"] == "player_turn":
            assert actions["can_hit"] is True
            assert actions["can_stand"] is True
            # Double down should be available on first turn
            assert actions["can_double_down"] is True
        elif game_state["state"] == "game_over":
            assert actions["can_hit"] is False
            assert actions["can_stand"] is False
            assert actions["can_double_down"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])