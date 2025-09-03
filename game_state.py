

class GameState:
    def __init__(self, players):
        self.players = players
        self.dealer_index = 0
        self.bet_holder = None  # Tracks last raiser
        self.stage = "pre-flop"
        self.stages = ["pre-flop", "flop", "turn", "river"]
        self.active_players = [p for p in players]
        self.pot = 0
        self.current_bet = 0
        self.min_raise = 20
        self.big_blind = 20
        self.small_blind = 10
        self.action_history = []  # List of (player, action, amount, stage)
        self.community_cards = []
        self.eliminated_players = []
        # Moderately advanced
        self.last_action = None  # (player, action, amount)
        self.num_raises_this_round = 0
        self.num_players = len(players)
        self.betting_order = []  # List of player names in order for this round
        self.player_bet = {}  # {player_name: amount bet this round}
        self.opponent_stacks = {}  # {player_name: chips}
        self.player_position = {}  # {player_name: position index}

    @property
    def pot_value(self):
        return self.pot

    @property
    def player_stacks(self):
        return {p.name: p.chips for p in self.players}

    @property
    def active_player_stacks(self):
        return {p.name: p.chips for p in self.players if not getattr(p, 'folded', False)}

    @property
    def to_call(self):
        # Returns a dict of how much each player needs to call
        return {p.name: max(0, self.current_bet - getattr(p, 'current_bet', 0)) for p in self.players if not getattr(p, 'folded', False)}

    @property
    def player_positions(self):
        # Returns a dict of player positions relative to dealer
        n = len(self.players)
        return {p.name: (i - self.dealer_index) % n for i, p in enumerate(self.players)}

    def update_betting_order(self, order):
        self.betting_order = order

    def update_player_bet(self, player_name, amount):
        self.player_bet[player_name] = amount

    def update_opponent_stacks(self):
        self.opponent_stacks = {p.name: p.chips for p in self.players if not getattr(p, 'folded', False)}

    def update_player_position(self):
        self.player_position = self.player_positions


    def reset_for_stage(self, stage):
        self.stage = stage
        self.bet_holder = None
        print(f"\n=== Starting {stage.upper()} ===")
        self.debug_active_players()

    def debug_active_players(self):
        active = [p.name for p in self.active_players if not getattr(p, 'folded', False)]
        print(f"Active Players: {active}")