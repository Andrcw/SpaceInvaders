class GameStats():
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Start game in an inactive state.
        self.game_active = False
        
        # High score should never be reset.
        self.high_score = 0

        # to pause when ship explode
        self.game_pause = False

        # Open high score txt
        self.wr = open('high_score.txt', 'r+')
        self.current = int(self.wr.read())
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def update_txt(self):
        self.wr.seek(0)
        self.current = int(self.wr.read())
        if self.current < self.high_score:
            self.wr.seek(0)
            self.wr.truncate()
            self.wr.write(str(self.high_score))