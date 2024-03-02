class GameStats():
    """ Track statistics for Alien Invasion """

    def __init__(self, ai_settings) -> None:
        """ Initialize statistics """
        self.ai_settings = ai_settings
        self.reset_stats()
        # Start Alien Invasion in an active state
        self.game_active = False
        # High score should never be reset
        self.high_score = self.load_high_score()

    def reset_stats(self):
        """ Initialize statistics that can change during game """
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        ''' Get highscore from file '''
        with open("high_score.txt", "r") as file:
            high_score = file.readline()
            return int(high_score)

    def save_high_score(self, new_high_score):
        '''  Save high score in file'''
        with open("high_score.txt", "w") as file:
            file.write(str(new_high_score))