class GameState:
    def __init__(self, players):
        self.players = players
        self.dealer_index = 0
        self.bet_holder = None  # Tracks last raiser
        self.stage = "pre-flop"
        self.stages = ["pre-flop", "flop", "turn", "river"]
        self.active_players = [p for p in players]

    def reset_for_stage(self, stage):
        self.stage = stage
        self.bet_holder = None
        print(f"\n=== Starting {stage.upper()} ===")
        self.debug_active_players()

    def debug_active_players(self):
        active = [p.name for p in self.active_players if not p.folded]
        print(f"Active Players: {active}")