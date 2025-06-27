import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export interface Card {
  suit: string;
  rank: string;
}

export interface Hand {
  cards: Card[];
  value: number | string;
  is_bust: boolean;
  is_blackjack: boolean;
  hidden_card?: boolean;
}

export interface GameState {
  player_hand: Hand;
  dealer_hand: Hand;
  state: string;
  result: string | null;
  available_actions: {
    can_hit: boolean;
    can_stand: boolean;
    can_double_down: boolean;
    can_split: boolean;
  };
}

export interface NewGameResponse {
  session_id: string;
  game_state: GameState;
}

export class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async newGame(): Promise<NewGameResponse> {
    const response = await axios.post(`${this.baseURL}/game/new`);
    return response.data;
  }

  async getGameState(sessionId: string): Promise<GameState> {
    const response = await axios.get(`${this.baseURL}/game/${sessionId}`);
    return response.data;
  }

  async hit(sessionId: string): Promise<GameState> {
    const response = await axios.post(`${this.baseURL}/game/${sessionId}/hit`);
    return response.data;
  }

  async stand(sessionId: string): Promise<GameState> {
    const response = await axios.post(`${this.baseURL}/game/${sessionId}/stand`);
    return response.data;
  }

  async doubleDown(sessionId: string): Promise<GameState> {
    const response = await axios.post(`${this.baseURL}/game/${sessionId}/double-down`);
    return response.data;
  }

  async endGame(sessionId: string): Promise<void> {
    await axios.delete(`${this.baseURL}/game/${sessionId}`);
  }
}